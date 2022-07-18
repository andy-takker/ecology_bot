from aiogram import Dispatcher

from filters.several import SeveralCallbackDataFilter
from handlers.commands import user_start
from handlers.organization.create_event import choose_district_for_event, \
    choose_municipal_for_event, choose_type_for_event, \
    choose_eco_activity_for_event, set_name_for_event, \
    set_description_for_event, confirm_for_event, \
    choose_volunteer_type_for_event, set_volunteer_description_for_event, \
    confirm_volunteer_for_event
from handlers.organization.management import choose_organization, \
    organization_menu, get_invite_link_choose_municipal, \
    get_invite_link_to_group_from_municipal, get_invite_link_navigate_municipal
from handlers.organization.registration import choose_activities, \
    save_activities, navigate_and_update_activities, save_districts, \
    navigate_and_update_districts, save_name
from keyboards.inline.callback_data import cb_start, \
    cb_organization_register, cb_organization_menu, cb_create_event
from states.create_event import CreateEvent
from states.management import OrganizationManagement
from states.registration import OrganizationRegistration


def register_organization(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        choose_activities,
        cb_start.filter(name='add_organization'), state='*')
    dp.register_callback_query_handler(
        save_activities,
        cb_organization_register.filter(action='choose_activity',
                                        name='next'),

        state=OrganizationRegistration.choosing_activities,
    )
    dp.register_callback_query_handler(
        navigate_and_update_activities,
        SeveralCallbackDataFilter([
            cb_organization_register.filter(
                action='choose_activity', name='page'),
            cb_organization_register.filter(
                action='choose_activity', name='objects')
        ]),
        state=OrganizationRegistration.choosing_activities,
    )
    dp.register_callback_query_handler(
        user_start,
        cb_organization_register.filter(action='choose_activity',
                                        name='back', value='back'),
        state=OrganizationRegistration.choosing_activities,
    )
    dp.register_callback_query_handler(
        save_districts,
        cb_organization_register.filter(action='choose_district',
                                        name='next'),
        state=OrganizationRegistration.choosing_districts,
    )
    dp.register_callback_query_handler(
        navigate_and_update_districts,
        SeveralCallbackDataFilter([
            cb_organization_register.filter(
                action='choose_district', name='page'),
            cb_organization_register.filter(
                action='choose_district', name='objects'),
        ]),
        state=OrganizationRegistration.choosing_districts,
    )
    dp.register_callback_query_handler(
        choose_activities,
        cb_organization_register.filter(action='choose_district',
                                        name='back', value='back'),
        state=OrganizationRegistration.choosing_districts,

    )
    dp.register_callback_query_handler(
        navigate_and_update_districts,
        cb_organization_register.filter(action='input_name', name='back',value='back'),
        state=OrganizationRegistration.enter_name,
    )
    dp.register_message_handler(save_name,
                                state=OrganizationRegistration.enter_name)
    dp.register_callback_query_handler(
        choose_organization,
        cb_start.filter(name='choose_organization'),
        state='*',
    )
    dp.register_callback_query_handler(
        organization_menu,
        cb_organization_menu.filter(action='choose_organization',
                                    name='objects'),
        state='*')
    dp.register_callback_query_handler(
        organization_menu,
        cb_organization_menu.filter(action='choose_municipal',
                                    name='back', value='back'),
        state=OrganizationManagement.choose_municipal,
    )
    dp.register_callback_query_handler(
        get_invite_link_choose_municipal,
        cb_organization_menu.filter(name='enter_chat',
                                    action='enter'),
        state=OrganizationManagement.menu,
    )
    dp.register_callback_query_handler(
        get_invite_link_navigate_municipal,
        cb_organization_menu.filter(action='choose_municipal',
                                    name='page'),
        state=OrganizationManagement.choose_municipal,
    )
    dp.register_callback_query_handler(
        get_invite_link_to_group_from_municipal,
        cb_organization_menu.filter(action='choose_municipal',
                                    name='objects'),
        state=OrganizationManagement.choose_municipal,
    )
    dp.register_callback_query_handler(
        organization_menu,
        cb_create_event.filter(action='choose_district', name='back',
                               value='back'),
        state=CreateEvent.choose_district,
    )
    dp.register_callback_query_handler(
        choose_district_for_event,
        cb_organization_menu.filter(action='create_event', name='create_event'),
        state=OrganizationManagement.menu,
    )
    dp.register_callback_query_handler(
        choose_district_for_event,
        SeveralCallbackDataFilter([
            cb_create_event.filter(
                action='choose_district', name='page'),
            cb_create_event.filter(
                action='choose_district', name='objects')
        ]),
        state=CreateEvent.choose_district,
    )
    dp.register_callback_query_handler(
        choose_municipal_for_event,
        SeveralCallbackDataFilter([
            cb_create_event.filter(
                action='choose_municipal', name='page'),
            cb_create_event.filter(
                action='choose_municipal', name='objects')
        ]),
        state=CreateEvent.choose_municipal,
    )
    dp.register_callback_query_handler(
        choose_district_for_event,
        cb_create_event.filter(action='choose_municipal', name='back',
                               value='back'),
        state=CreateEvent.choose_municipal,
    )
    dp.register_callback_query_handler(
        choose_type_for_event,
        cb_create_event.filter(action='choose_type', name='objects'),
        state=CreateEvent.choose_type,
    )
    dp.register_callback_query_handler(
        choose_municipal_for_event,
        cb_create_event.filter(action='choose_type', name='back', value='back'),
        state=CreateEvent.choose_type,
    )
    dp.register_callback_query_handler(
        choose_eco_activity_for_event,
        SeveralCallbackDataFilter([
            cb_create_event.filter(action='choose_activity', name='page'),
            cb_create_event.filter(action='choose_activity', name='objects'),
        ]),
        state=CreateEvent.choose_activity,
    )
    dp.register_callback_query_handler(
        choose_type_for_event,
        cb_create_event.filter(action='choose_activity', name='back',
                               value='back'),
        state=CreateEvent.choose_activity,
    )

    dp.register_callback_query_handler(
        choose_eco_activity_for_event,
        cb_create_event.filter(action='set_name', name='back', value='back'),
        state=CreateEvent.set_name,
    )
    dp.register_message_handler(
        set_name_for_event, state=CreateEvent.set_name,
    )
    dp.register_callback_query_handler(
        set_name_for_event,
        cb_create_event.filter(action='set_description', name='back',
                               value='back'),
        state=CreateEvent.set_description,
    )
    dp.register_message_handler(
        set_description_for_event,
        state=CreateEvent.set_description,
    )
    dp.register_callback_query_handler(
        set_description_for_event,
        cb_create_event.filter(action='confirm', name='back', value='back'),
        state=CreateEvent.confirm,
    )
    dp.register_callback_query_handler(
        confirm_for_event,
        cb_create_event.filter(action='confirm', name='confirm',
                               value='confirm'),
        state=CreateEvent.confirm,
    )
    dp.register_callback_query_handler(
        choose_volunteer_type_for_event,
        SeveralCallbackDataFilter([
            cb_create_event.filter(action='choose_volunteer_type', name='page'),
            cb_create_event.filter(action='choose_volunteer_type',
                                   name='objects'),
            cb_create_event.filter(action='choose_volunteer_type', name='next'),
        ]),
        state=CreateEvent.choose_volunteer_type,
    )
    dp.register_callback_query_handler(
        choose_type_for_event,
        cb_create_event.filter(action='choose_volunteer_type', name='back',
                               value='back'),
        state=CreateEvent.choose_volunteer_type
    )
    dp.register_callback_query_handler(
        choose_volunteer_type_for_event,
        cb_create_event.filter(action='set_volunteer_description', name='back',
                               value='back'),
        state=CreateEvent.set_volunteer_description,
    )
    dp.register_message_handler(
        set_volunteer_description_for_event,
        state=CreateEvent.set_volunteer_description,
    )
    dp.register_callback_query_handler(
        set_volunteer_description_for_event,
        cb_create_event.filter(action='confirm_volunteer', name='back',
                               value='back'),
        state=CreateEvent.confirm_volunteer,
    )
    dp.register_callback_query_handler(
        confirm_volunteer_for_event,
        cb_create_event.filter(action='confirm_volunteer', name='confirm',
                               value='confirm', ),
        state=CreateEvent.confirm_volunteer,
    )
