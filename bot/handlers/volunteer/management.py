from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.back import get_back_keyboard
from keyboards.default.volunteer import get_volunteer_keyboard
from keyboards.inline.callback_data import cb_volunteer_menu
from services.repository import Repo
from states.management import VolunteerManagement


async def volunteer_menu(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerManagement.menu.set()
    user = await repo.get_user(user_id=query.from_user.id)
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text='Меню волонтера',
        reply_markup=get_volunteer_keyboard(user=user),
    )


async def volunteer_activity_menu(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerManagement.activity_info.set()
    eco_activity_id = int(callback_data['value'])
    profile = await repo.get_profile(user_id=query.from_user.id)
    organizations = await repo.get_organizations_by_profile(
        profile=profile,
        eco_activity_id=eco_activity_id,
    )
    msgs = []
    if organizations:
        msgs.append("В твоем районе c такой активностью"
                    " есть вот эти организации:\n")
        for org in organizations:
            msgs.append(f'*{org.name}*\n')
    else:
        msgs.append("В твоем районе не зарегистрированы экологические"
                    " организации с такой направленностью. "
                    "Попробуй выбрать другой район. ")
    msgs.append("Тебе обязательно придут уведомления о мероприятиях. ")
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=''.join(msgs),
        reply_markup=get_back_keyboard(
            callback_data=cb_volunteer_menu,
            action='volunteer_menu',
        ), parse_mode=types.ParseMode.MARKDOWN,
    )


async def volunteer_filter_events_menu(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerManagement.filter_events.set()
    profile = await repo.get_profile(user_id=query.from_user.id)
    events = await repo.get_events_for_profile(profile=profile)
    for e in events:
        event = await repo.get_event(event_id=e.id)
        await query.bot.send_message(
            chat_id=query.from_user.id,
            text=event.message,
            parse_mode=types.ParseMode.MARKDOWN,
        )
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=f'Под твой профиль подходит {len(events)} мероприятий',
        reply_markup=get_back_keyboard(
            callback_data=cb_volunteer_menu,
            action='volunteer_menu',
        )
    )
