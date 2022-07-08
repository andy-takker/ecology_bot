from aiogram import Dispatcher

from handlers.organization.management import choose_organization, \
    organization_menu, get_invite_link_choose_municipal, \
    get_invite_link_to_group_from_municipal, get_invite_link_navigate_municipal
from handlers.organization.registration import add_new_organization, \
    set_activity, navigate_and_update_activities, save_districts, \
    navigate_and_update_districts, save_name
from keyboards.inline.callback_data import action_callback_start, \
    action_callback_organization_register, action_callback_organization_menu
from states.management import OrganizationManagement
from states.registration import OrganizationRegistration


def register_organization(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        add_new_organization,
        action_callback_start.filter(name='add_organization'), state='*')
    dp.register_callback_query_handler(
        set_activity,
        action_callback_organization_register.filter(action='choose_activity',
                                                     name='next'),
        state=OrganizationRegistration.choosing_activities,
    )
    dp.register_callback_query_handler(
        navigate_and_update_activities,
        action_callback_organization_register.filter(action='choose_activity'),
        state=OrganizationRegistration.choosing_activities,
    )
    dp.register_callback_query_handler(
        save_districts,
        action_callback_organization_register.filter(action='choose_district',
                                                     name='next'),
        state=OrganizationRegistration.choosing_districts,
    )
    dp.register_callback_query_handler(
        navigate_and_update_districts,
        action_callback_organization_register.filter(action='choose_district'),
        state=OrganizationRegistration.choosing_districts,
    )
    dp.register_message_handler(save_name,
                                state=OrganizationRegistration.enter_name)
    dp.register_callback_query_handler(
        choose_organization,
        action_callback_start.filter(name='choose_organization'),
        state='*',
    )
    dp.register_callback_query_handler(
        organization_menu,
        action_callback_organization_menu.filter(action='choose_organization'),
        state=OrganizationManagement.menu)
    dp.register_callback_query_handler(
        get_invite_link_choose_municipal,
        action_callback_organization_menu.filter(name='enter_chat',action='enter'),
        state=OrganizationManagement.menu,
    )
    dp.register_callback_query_handler(
        get_invite_link_navigate_municipal,
        action_callback_organization_menu.filter(action='choose_municipal',name='page'),
        state=OrganizationManagement.choose_municipal,
    )
    dp.register_callback_query_handler(
        get_invite_link_to_group_from_municipal,
        action_callback_organization_menu.filter(action='choose_municipal'),
        state=OrganizationManagement.choose_municipal,
    )