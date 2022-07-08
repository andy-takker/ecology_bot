from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.paginate_keyboard import get_paginate_keyboard
from keyboards.inline.callback_data import action_callback_organization_register


def get_activity_keyboard(activities, page=1, per_page=10,
                          chose_activities=None) -> InlineKeyboardMarkup:

    return get_paginate_keyboard(
        objects=activities,
        callback_data=action_callback_organization_register,
        action='choose_activity',
        page=page,
        per_page=per_page,
        with_chose=True,
        cache_objects=chose_activities,
    )
