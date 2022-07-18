from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import User
from keyboards.inline.callback_data import cb_volunteer_menu, cb_start


def get_volunteer_keyboard(user: User) -> InlineKeyboardMarkup:
    buttons = []
    for eco_activity in user.profile.eco_activities:
        buttons.append([
            InlineKeyboardButton(
                text=eco_activity.name,
                callback_data=cb_volunteer_menu.new(
                    name='volunteer_menu',
                    action='eco_activity',
                    value=eco_activity.id,
                )
            )
        ])
    buttons.extend([[
        InlineKeyboardButton(
            text='Поменять выбранные активности',
            callback_data=cb_volunteer_menu.new(
                name='volunteer_menu',
                action='change_activity',
                value=True,
            )
        )
    ], [
        InlineKeyboardButton(
            text='Поменять район',
            callback_data=cb_volunteer_menu.new(
                name='volunteer_menu',
                action='change_district',
                value=True,
            )
        )
    ]])
    if not user.profile.is_event_organizer:
        buttons.append([
            InlineKeyboardButton(
                text='Хочу помочь организовать экособытие',
                callback_data=cb_volunteer_menu.new(
                    name='volunteer_menu',
                    action='help_event_organize',
                    value=True,
                )
            )
        ])
    buttons.extend([[
        InlineKeyboardButton(
            text='Подходящие события',
            callback_data=cb_volunteer_menu.new(
                name='volunteer_menu',
                action='filter_my_events',
                value=True,
            )
        )
    ], [
        InlineKeyboardButton(
            text='Инфо профиля',
            callback_data=cb_volunteer_menu.new(
                name='volunteer_menu',
                action='info_profile',
                value=True,
            )
        )
    ], [
        InlineKeyboardButton(
            text='Удалить профиль',
            callback_data=cb_volunteer_menu.new(
                name='volunteer_menu',
                action='delete_profile',
                value=True,
            )
        )
    ], [
        InlineKeyboardButton(
            text='Назад',
            callback_data=cb_start.new(
                name='go_to_main_menu',
            )
        )
    ]])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
