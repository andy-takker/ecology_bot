from aiogram.types import InlineKeyboardMarkup

from keyboards.default.paginate_keyboard import get_paginate_keyboard
from keyboards.inline.callback_data import action_callback_organization_register


def get_district_keyboard(districts, page=1, per_page=10,
                          chose_districts=None) -> InlineKeyboardMarkup:
    return get_paginate_keyboard(
        objects=districts,
        callback_data=action_callback_organization_register,
        action='choose_district',
        page=page,
        per_page=per_page,
        with_chose=True,
        cache_objects=chose_districts,
    )
