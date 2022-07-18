from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.default.back import get_back_keyboard


def get_yes_back_keyboard(callback_data: CallbackData,
                          action: str) -> InlineKeyboardMarkup:
    keyboard = get_back_keyboard(callback_data=callback_data, action=action)
    keyboard.inline_keyboard.insert(0, [InlineKeyboardButton(
        text='Да',
        callback_data=callback_data.new(action=action, name='yes', value='yes')
    )])
    return keyboard
