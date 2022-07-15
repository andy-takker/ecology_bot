from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import User
from keyboards.inline.callback_data import cb_start


def get_start_keyboard(user: User) -> InlineKeyboardMarkup:
    keys = []
    if user.profile is None:
        keys.append([
            InlineKeyboardButton(
                text='Зарегистрировать профиль волонтера',
                callback_data=cb_start.new('register_volunteer'),
            )
        ])
    else:
        keys.append([
            InlineKeyboardButton(
                text='Перейти к профилю волонтера',
                callback_data=cb_start.new('volunteer_menu'),
            )
        ])
    keys.append([InlineKeyboardButton(text='Что может этот бот?',
                                      callback_data=cb_start.new(
                                          'help'))])
    if not user.has_unchecked_organizations:
        keys.append([InlineKeyboardButton(
            text='Добавьте свою организацию',
            callback_data=cb_start.new('add_organization')), ])
    if user.has_checked_organizations:
        keys.append([InlineKeyboardButton(
            text="Управление своими организациями",
            callback_data=cb_start.new('choose_organization', ))])
    start_keyboard = InlineKeyboardMarkup(inline_keyboard=keys)
    return start_keyboard
