from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import Organization
from keyboards.default.paginate_keyboard import get_paginate_keyboard
from keyboards.inline.callback_data import action_callback_admin_menu


def get_admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(
        text="Организации на модерации",
        callback_data=action_callback_admin_menu.new(
            action='moderate', value='-', name='-',
        ))]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_unchecked_organizations_keyboard(organizations: list[Organization],
                                         page=1, per_page=10):
    return get_paginate_keyboard(
        objects=organizations,
        callback_data=action_callback_admin_menu,
        action='choose_organization',
        page=page,
        per_page=per_page,
        with_chose=False,
    )
