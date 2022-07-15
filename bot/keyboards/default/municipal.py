from aiogram.utils.callback_data import CallbackData

from database import Municipal
from keyboards.default.paginate_keyboard import get_paginate_keyboard


def get_municipal_keyboard(municipals: list[Municipal],
                           callback_data: CallbackData,
                           page=1, per_page=10):
    return get_paginate_keyboard(
        objects=municipals,
        callback_data=callback_data,
        action='choose_municipal',
        page=page,
        per_page=per_page,
        with_chose=False
    )
