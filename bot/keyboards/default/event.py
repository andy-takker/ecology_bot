from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import EventType
from keyboards.default.paginate_keyboard import get_paginate_keyboard
from keyboards.inline.callback_data import cb_create_event

EVENT_TEXT = {
    EventType.DEFAULT: 'Объявление о мероприятии',
    EventType.RECRUITMENT: 'Нужны волонтеры на мероприятие',
}


def get_event_type_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=EVENT_TEXT[i],
                              callback_data=cb_create_event.new(
                                  action='choose_type', value=i.value,
                                  name='objects'))] for i in EventType])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="Назад", callback_data=cb_create_event.new(
            action='choose_type', value='back', name='back'))
    ])
    return keyboard


def get_confirm_event_keyboard(action='confirm'):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отправить рассылку!",
                callback_data=cb_create_event.new(
                    action=action,
                    value='confirm',
                    name='confirm'
                )
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=cb_create_event.new(
                    action=action,
                    value='back',
                    name='back'
                )
            )
        ]])

    return keyboard


def get_volunteer_type_keyboard(volunteer_types, page=1,per_page=10,
                                chose_volunteer_types=None,
                                with_chose=True,callback_data=cb_create_event)-> InlineKeyboardMarkup:
    return get_paginate_keyboard(
        objects=volunteer_types,
        callback_data=callback_data,
        action='choose_volunteer_type',
        page=page,
        per_page=per_page,
        with_chose=with_chose,
        cache_objects=chose_volunteer_types,
    )

