from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import Organization, User
from keyboards.default.paginate_keyboard import get_paginate_keyboard
from keyboards.inline.callback_data import cb_organization_menu, \
    cb_start


def get_organization_keyboard(user: User) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text='Добавьте событие',
            callback_data=cb_organization_menu.new(
                name='create_event',
                action='create_event',
                value=True,
            )),
        ],
        [InlineKeyboardButton(
            text='Мои организации',
            callback_data=cb_start.new(
                name='choose_organization',
            )),
        ], [
            InlineKeyboardButton(
                text='Вступить в чат по вашему МО',
                callback_data=cb_organization_menu.new(
                    name='enter_chat',
                    action='enter',
                    value=True,
                )
            )
        ]
    ]
    if not user.has_unchecked_organizations:
        buttons.append([InlineKeyboardButton(
            text='Добавить еще одну организацию',
            callback_data=cb_start.new(
                'add_organization'))])
    buttons.append([
            InlineKeyboardButton(
                text='Выйти из меню организации',
                callback_data=cb_start.new(
                    name='go_to_main_menu',
                )
            )
        ])
    organize_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return organize_keyboard


def get_checked_organizations_keyboard(organizations: List[Organization],
                                       page=1, per_page=10):
    return get_paginate_keyboard(
        objects=organizations,
        callback_data=cb_organization_menu,
        action='choose_organization',
        page=page,
        per_page=per_page,
        with_chose=False,
    )
