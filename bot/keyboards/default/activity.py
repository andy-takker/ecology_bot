from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.paginate_keyboard import get_paginate_keyboard
from keyboards.inline.callback_data import cb_organization_register


def get_activity_keyboard(activities, page=1, per_page=10,
                          chose_activities=None, with_chose=True,callback_data=cb_organization_register) -> InlineKeyboardMarkup:

    return get_paginate_keyboard(
        objects=activities,
        callback_data=callback_data,
        action='choose_activity',
        page=page,
        per_page=per_page,
        with_chose=with_chose,
        cache_objects=chose_activities,
    )
