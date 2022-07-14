from typing import Iterable, Union, Sized, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

CHECKBOX = "\U00002705"


def get_paginate_keyboard(objects: List, callback_data: CallbackData,
                          action: str,
                          page: int = 1, per_page: int = 10,
                          with_chose: bool = False,
                          cache_objects: Union[Sized, Iterable] = None,
                          ) -> InlineKeyboardMarkup:
    if with_chose and not cache_objects:
        cache_objects = []

    offset = (page - 1) * per_page
    buttons = []
    for i in range(offset, min(offset + per_page, len(objects))):
        cb_data = callback_data.new(action=action, name='objects',
                                    value=objects[i].id)
        text = str(objects[i])
        if with_chose and objects[i].id in cache_objects:
            text = f"{CHECKBOX}\t{text}"

        buttons.append([InlineKeyboardButton(text=text, callback_data=cb_data)])

    nav_keys = []
    if page > 1:
        nav_keys.append(InlineKeyboardButton(
            '<', callback_data=callback_data.new(action=action, name='page',
                                                 value=page - 1)
        ))
    if page < (len(objects) + per_page - 1) // per_page:
        nav_keys.append(InlineKeyboardButton(
            '>', callback_data=callback_data.new(action=action, name='page',
                                                 value=page + 1)
        ))

    if nav_keys:
        buttons.append(nav_keys)
    if with_chose:
        buttons.append([InlineKeyboardButton(
            'Далее',
            callback_data=callback_data.new(action=action, name='next',
                                            value='next'))])
    buttons.append([InlineKeyboardButton(
        'Назад', callback_data=callback_data.new(action=action, name='back',
                                                 value='back')
    )])
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[*buttons]
    )
    return keyboard
