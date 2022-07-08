from aiogram import Dispatcher

from handlers.admin.management import get_organizations_for_moderating, \
    moderate_organization
from keyboards.inline.callback_data import action_callback_admin_menu
from states.admin import AdminStates


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        get_organizations_for_moderating,
        action_callback_admin_menu.filter(action='moderate'),
        is_admin=True,
        state=AdminStates.main_menu,
    )
    dp.register_callback_query_handler(
        moderate_organization,
        action_callback_admin_menu.filter(action='choose_organization'),
        is_admin=True,
        state=AdminStates.main_menu,
    )
