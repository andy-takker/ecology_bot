from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.commands import user_start
from keyboards.default.activity import get_activity_keyboard
from keyboards.default.back import get_back_keyboard
from keyboards.default.district import get_district_keyboard
from keyboards.default.event import get_volunteer_type_keyboard
from keyboards.default.municipal import get_municipal_keyboard
from keyboards.default.volunteer import get_volunteer_keyboard
from keyboards.default.yes_back import get_yes_back_keyboard
from keyboards.inline.callback_data import cb_volunteer_menu
from services.repository import Repo
from states.management import VolunteerManagement, VolunteerOrganizer


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


async def volunteer_change_activity_menu(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerManagement.change_activity.set()
    activities = await repo.get_activities()
    async with state.proxy() as data:
        if data.get('eco_activities') is None:
            data['eco_activities'] = {}
        match callback_data['name']:
            case 'objects' | 'page':
                if callback_data['name'] == 'objects':
                    eco_activity_id = int(callback_data['value'])
                    if eco_activity_id not in data['eco_activities'].keys():
                        data['eco_activities'][eco_activity_id] = True
                    else:
                        del data['eco_activities'][eco_activity_id]
                else:
                    data['eco_activities']['page'] = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_activity_keyboard(
                        activities=activities,
                        callback_data=cb_volunteer_menu,
                        page=data['eco_activities'].get('page', 1),
                        chose_activities=data['eco_activities'].keys(),
                        with_chose=True
                    )
                )
            case 'next':
                activity_ids = [i for i in data['eco_activities'] if
                                i != 'page']
                await repo.update_profile(user_id=query.from_user.id,
                                          activity_ids=activity_ids)
                await state.finish()
                await VolunteerManagement.menu.set()
                user = await repo.get_user(query.from_user.id)
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text='Активности обновлены!\n'
                         'Теперь ты будешь получать уведомления о таких событиях!',
                    reply_markup=get_volunteer_keyboard(user=user)
                )
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выбери интересующие тебя активности."
                         "По ним тебе будет приходит информация.",
                    reply_markup=get_activity_keyboard(
                        activities=activities,
                        callback_data=cb_volunteer_menu,
                        chose_activities=data['eco_activities'].keys(),
                        with_chose=True,
                    )
                )


async def volunteer_change_district_menu(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerManagement.change_district.set()
    districts = await repo.get_districts()
    async with state.proxy() as data:
        match callback_data['name']:
            case 'objects':
                district_id = int(callback_data['value'])
                municipals = await repo.get_municipals_by_districts(
                    [district_id])
                data['district_id'] = district_id
                await VolunteerManagement.change_municipal.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выбери муниципальное образование",
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_volunteer_menu,
                    )
                )
            case 'page':
                page = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_district_keyboard(
                        callback_data=cb_volunteer_menu,
                        districts=districts,
                        with_chose=False,
                        page=page,
                    )
                )
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="В каком районе вы находитесь?",
                    reply_markup=get_district_keyboard(
                        districts=districts,
                        callback_data=cb_volunteer_menu,
                        with_chose=False,
                    )
                )


async def volunteer_change_municipal_menu(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerManagement.change_municipal.set()
    async with state.proxy() as data:
        municipals = await repo.get_municipals_by_districts(
            [data['district_id']])
        if 'eco_activities' in data:
            del data['eco_activities']
        match callback_data['name']:
            case 'objects':
                municipal_id = int(callback_data['value'])
                await repo.update_profile(user_id=query.from_user.id,
                                          municipal_id=municipal_id)
                await state.finish()
                await VolunteerManagement.menu.set()
                user = await repo.get_user(query.from_user.id)
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text='Теперь ты будешь получать уведомления о событиях в '
                         'новом районе!',
                    reply_markup=get_volunteer_keyboard(user=user)
                )
            case 'page':
                page = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_volunteer_menu,
                        page=page
                    )
                )
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выбери муниципальное образование",
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_volunteer_menu,
                    )
                )


async def volunteer_info_profile_menu(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    profile = await repo.get_profile(user_id=query.from_user.id)
    user = await repo.get_user(user_id=query.from_user.id)

    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=profile.info,
        reply_markup=get_volunteer_keyboard(user=user)
    )


async def volunteer_delete_profile_menu(
        query: CallbackQuery, callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    await VolunteerManagement.delete_profile.set()
    print(callback_data)
    match callback_data['name']:
        case 'volunteer_menu':
            await query.message.edit_reply_markup(reply_markup=None)
            await query.bot.send_message(
                chat_id=query.from_user.id,
                text='Ты действительно хочешь удалить профиль волонтера?',
                reply_markup=get_yes_back_keyboard(
                    callback_data=cb_volunteer_menu,
                    action='delete_profile')
            )
        case 'yes':
            await repo.delete_profile(user_id=query.from_user.id)
            await user_start(query, repo, state)


async def volunteer_input_name_organizer(
        tg_object: CallbackQuery | Message,
        state: FSMContext,
        repo: Repo) -> None:
    await VolunteerOrganizer.input_name.set()
    if isinstance(tg_object, CallbackQuery):
        await tg_object.message.edit_reply_markup(reply_markup=None)
        await tg_object.bot.send_message(
            chat_id=tg_object.from_user.id,
            text="Напиши свое имя и фамилию",
            reply_markup=get_back_keyboard(callback_data=cb_volunteer_menu,
                                           action='input_name')
        )
    else:
        async with state.proxy() as data:
            data['name'] = tg_object.text
        await VolunteerOrganizer.input_age.set()
        await tg_object.bot.send_message(
            chat_id=tg_object.from_user.id,
            text="Сколько тебе лет?",
            reply_markup=get_back_keyboard(callback_data=cb_volunteer_menu,
                                           action='input_age')
        )


def get_age(d: str) -> int:
    try:
        return int(d)
    except ValueError:
        return 0


async def volunteer_input_age_organizer(tg_object: CallbackQuery | Message,
                                        state: FSMContext, repo: Repo) -> None:
    if isinstance(tg_object, Message):
        async with state.proxy() as data:
            data['age'] = get_age(tg_object.text)
        await VolunteerOrganizer.choose_volunteer_type.set()
        volunteer_types = await repo.get_volunteer_types()
        await tg_object.bot.send_message(
            chat_id=tg_object.from_user.id,
            text='Какие типы волонтерств тебе нравятся?',
            reply_markup=get_volunteer_type_keyboard(
                volunteer_types=volunteer_types,
                with_chose=True,
                callback_data=cb_volunteer_menu,
            )
        )
    else:
        await VolunteerOrganizer.input_age.set()
        await tg_object.bot.send_message(
            chat_id=tg_object.from_user.id,
            text="Сколько тебе лет?",
            reply_markup=get_back_keyboard(callback_data=cb_volunteer_menu,
                                           action='input_age')
        )


async def choose_volunteer_type_for_event(query: CallbackQuery,
                                          callback_data: dict,
                                          state: FSMContext,
                                          repo: Repo) -> None:
    """Выбираем типы волонтеров, которые нужны для события"""
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerOrganizer.choose_volunteer_type.set()
    volunteer_types = await repo.get_volunteer_types()
    async with state.proxy() as data:
        if 'volunteer_types' not in data:
            data['volunteer_types'] = {}
        match callback_data['name']:
            case 'objects' | 'page':
                if callback_data['name'] == 'objects':
                    volunteer_type_id = int(callback_data['value'])
                    if volunteer_type_id not in data['volunteer_types'].keys():
                        data['volunteer_types'][volunteer_type_id] = True
                    else:
                        del data['volunteer_types'][volunteer_type_id]
                else:
                    data['volunteer_types']['page'] = int(
                        callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_volunteer_type_keyboard(
                        callback_data=cb_volunteer_menu,
                        volunteer_types=volunteer_types,
                        page=data['volunteer_types'].get('page', 1),
                        chose_volunteer_types=data['volunteer_types'].keys(),
                        with_chose=True
                    )
                )
            case 'next':
                await repo.update_profile(
                    user_id=query.from_user.id,
                    is_event_organizer=True,
                    age=data['age'],
                    name=data['name'],
                    volunteer_type_ids=[i for i in data['volunteer_types'] if
                                         i != 'page']
                )
                await state.finish()
                await VolunteerManagement.menu.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Теперь тебе будут приходить уведомления об организации"
                         " волонтерских мероприятий",
                    reply_markup=get_volunteer_keyboard(user=await repo.get_user(query.from_user.id))
                )
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Какие типы волонтерств тебе нравятся?",
                    reply_markup=get_volunteer_type_keyboard(
                        callback_data=cb_volunteer_menu,
                        volunteer_types=volunteer_types,
                        with_chose=True,
                    )
                )
