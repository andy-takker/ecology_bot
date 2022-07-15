from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.default.paginate_keyboard import get_paginate_keyboard


def get_district_keyboard(districts, callback_data:CallbackData,
                          page=1, per_page=10,
                          chose_districts=None, with_chose=True,) -> InlineKeyboardMarkup:
    return get_paginate_keyboard(
        objects=districts,
        callback_data=callback_data,
        action='choose_district',
        page=page,
        per_page=per_page,
        with_chose=with_chose,
        cache_objects=chose_districts,
    )
