from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def get_back_keyboard(callback_data: CallbackData,
                      action: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text='Назад',
        callback_data=callback_data.new(action=action, name='back',
                                        value='back')
    )]])
