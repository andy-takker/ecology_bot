from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from database import EventType, Event
from keyboards.default.activity import get_activity_keyboard
from keyboards.default.back import get_back_keyboard
from keyboards.default.district import get_district_keyboard
from keyboards.default.event import get_event_type_keyboard, \
    get_confirm_event_keyboard, get_volunteer_type_keyboard
from keyboards.default.municipal import get_municipal_keyboard
from keyboards.default.organization import get_organization_keyboard
from keyboards.inline.callback_data import cb_create_event
from services.repository import Repo
from states.create_event import CreateEvent
from states.management import OrganizationManagement
from workers.mailing import execute_mailing

CHOOSING_DISTRICT_MESSAGE = "Создаем событие. \nВ каком районе пройдет мероприятие?"


async def choose_district_for_event(query: CallbackQuery, callback_data: dict,
                                    state: FSMContext, repo: Repo) -> None:
    """Выбираем район для события"""
    await query.message.edit_reply_markup(reply_markup=None)
    await CreateEvent.first()
    districts = await repo.get_districts()
    async with state.proxy() as data:
        match callback_data['name']:
            case 'objects':
                """Навигация"""
                district_id = int(callback_data['value'])
                data['district_id'] = district_id
                municipals = await repo.get_municipals_by_districts(
                    district_ids=[district_id])
                await CreateEvent.choose_municipal.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="В каком МО пройдет мероприятие?",
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_create_event)
                )
            case 'page':
                if data.get('districts') is None:
                    data['districts'] = {}
                data['districts']['page'] = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_district_keyboard(
                        districts=districts,
                        page=data['districts'].get('page', 1),
                        chose_districts=None,
                        with_chose=False,
                        callback_data=cb_create_event,
                    )

                )
            case _:
                await query.bot.send_message(chat_id=query.from_user.id,
                                             text='Создаем событие')
                data['districts'] = {}
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="В каком районе пройдет мероприятие?",
                    reply_markup=get_district_keyboard(districts=districts,
                                                       with_chose=False,
                                                       callback_data=cb_create_event),
                )


async def choose_municipal_for_event(query: CallbackQuery, callback_data: dict,
                                     state: FSMContext, repo: Repo) -> None:
    """Выбираем МО для события"""
    await query.message.edit_reply_markup(reply_markup=None)
    await CreateEvent.choose_municipal.set()
    async with state.proxy() as data:
        district_id = data['district_id']
        municipals = await repo.get_municipals_by_districts(
            district_ids=[district_id])
        match callback_data['name']:
            case 'objects':
                municipal_id = int(callback_data['value'])
                data['municipal_id'] = municipal_id
                await CreateEvent.choose_type.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выберите тип объявления?",
                    reply_markup=get_event_type_keyboard(),
                )
            case 'page':
                if data.get('municipals') is None:
                    data['municipals'] = {}
                data['municipals']['page'] = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        page=data['municipals']['page'],
                        callback_data=cb_create_event,
                    )

                )
            case _:
                data['municipals'] = {}
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text='В каком МО пройдет мероприятие?',
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_create_event,
                    ),
                )


async def choose_type_for_event(query: CallbackQuery, callback_data: dict,
                                state: FSMContext, repo: Repo) -> None:
    """Выбираем тип события"""
    await query.message.edit_reply_markup(reply_markup=None)
    await CreateEvent.choose_type.set()

    async with state.proxy() as data:
        match callback_data['value']:
            case EventType.DEFAULT.value:
                data['type'] = EventType.DEFAULT
                await CreateEvent.choose_activity.set()
                data['activities'] = {}
                activities = (await repo.get_organization_full(
                    organization_id=data['organization_id'])).eco_activities
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выберите тип активности мероприятия."
                         " На основе ее придет сообщение подписчикам.",
                    reply_markup=get_activity_keyboard(activities=activities,
                                                       with_chose=False,
                                                       callback_data=cb_create_event)
                )
            case EventType.RECRUITMENT.value:
                data['type'] = EventType.RECRUITMENT
                await CreateEvent.choose_volunteer_type.set()
                volunteer_types = await repo.get_volunteer_types()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Какой тип волонтеров требуется?",
                    reply_markup=get_volunteer_type_keyboard(
                        volunteer_types=volunteer_types,
                        with_chose=True,
                    )
                )
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выберите тип объявления?",
                    reply_markup=get_event_type_keyboard(),
                )


async def choose_volunteer_type_for_event(query: CallbackQuery,
                                          callback_data: dict,
                                          state: FSMContext,
                                          repo: Repo) -> None:
    """Выбираем типы волонтеров, которые нужны для события"""
    await query.message.edit_reply_markup(reply_markup=None)
    await CreateEvent.choose_volunteer_type.set()
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
                        volunteer_types=volunteer_types,
                        page=data['volunteer_types'].get('page', 1),
                        chose_volunteer_types=data['volunteer_types'].keys(),
                        with_chose=True
                    )
                )
            case 'next':
                data['volunteer_ids'] = [i for i in data['volunteer_types'] if
                                         i != 'page']
                await CreateEvent.set_volunteer_description.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Напиши текст вакансии, который получат волонтеры:",
                    reply_markup=get_back_keyboard(
                        callback_data=cb_create_event,
                        action='set_volunteer_description')
                )
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Какой тип волонтеров требуется?",
                    reply_markup=get_volunteer_type_keyboard(
                        volunteer_types=volunteer_types,
                        with_chose=True,
                    )
                )


async def set_volunteer_description_for_event(obj: CallbackQuery | Message,
                                              state: FSMContext,
                                              repo: Repo) -> None:
    if isinstance(obj, CallbackQuery):
        await CreateEvent.set_volunteer_description.set()
        await obj.message.edit_reply_markup(reply_markup=None)
        await CreateEvent.set_volunteer_description.set()
        await obj.bot.send_message(
            chat_id=obj.from_user.id,
            text="Напиши текст вакансии, который получат волонтеры:",
            reply_markup=get_back_keyboard(
                callback_data=cb_create_event,
                action='set_volunteer_description')
        )
    elif isinstance(obj, Message):
        async with state.proxy() as data:
            await CreateEvent.confirm_volunteer.set()
            data['description'] = obj.text
            volunteer_types = await repo.get_volunteer_types(
                ids=data['volunteer_types'])
            await obj.bot.send_message(
                chat_id=obj.from_user.id,
                text=f'Вам потребуются волонтеры: {", ".join([str(v) for v in volunteer_types]).lower()}\n'
                     f'Текст, который они увидят:\n{data["description"]}',
                reply_markup=get_confirm_event_keyboard(
                    action='confirm_volunteer'),
            )


async def confirm_volunteer_for_event(query: CallbackQuery, callback_data: dict,
                                      state: FSMContext, repo: Repo) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        event: Event = await repo.create_volunteer_event(data=data)
        execute_mailing.delay(event.id)
        organization_id = data['organization_id']
    await state.finish()
    await OrganizationManagement.menu.set()
    user = await repo.get_user(user_id=query.from_user.id)
    async with state.proxy() as data:
        data['organization_id'] = organization_id

    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=f"Рассылка создана!",
        reply_markup=get_organization_keyboard(user=user)
    )


async def choose_eco_activity_for_event(query: CallbackQuery,
                                        callback_data: dict, state: FSMContext,
                                        repo: Repo) -> None:
    """Выбираем эко активность, с которой связано событие (для Default)"""
    await query.message.edit_reply_markup(reply_markup=None)
    await CreateEvent.choose_activity.set()
    async with state.proxy() as data:
        match callback_data['name']:
            case 'objects':
                activity_id = int(callback_data['value'])
                data['activity_id'] = activity_id
                await CreateEvent.set_name.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Напиши название мероприятия",
                    reply_markup=get_back_keyboard(
                        callback_data=cb_create_event, action='set_name')
                )
            case 'page':
                activities = (await repo.get_organization_full(
                    organization_id=data['organization_id'])).eco_activities
                if data.get('activities') is None:
                    data['activities'] = {}
                data['activities']['page'] = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_activity_keyboard(
                        activities=activities,
                        with_chose=False,
                        page=data['activities']['page'],
                        callback_data=cb_create_event,
                    ))
            case _:
                data['activities'] = {}
                activities = (await repo.get_organization_full(
                    organization_id=data['organization_id'])).eco_activities
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выберите тип активности мероприятия."
                         " На основе ее придет сообщение подписчикам.",
                    reply_markup=get_activity_keyboard(activities=activities,
                                                       with_chose=False,
                                                       callback_data=cb_create_event)
                )


async def set_name_for_event(obj: CallbackQuery | Message,
                             state: FSMContext, repo: Repo) -> None:
    if isinstance(obj, CallbackQuery):
        await CreateEvent.set_name.set()
        await obj.message.edit_reply_markup(reply_markup=None)
        await obj.bot.send_message(
            chat_id=obj.from_user.id,
            text="Напиши название мероприятия",
            reply_markup=get_back_keyboard(
                callback_data=cb_create_event, action='set_name')
        )
    elif isinstance(obj, Message):
        async with state.proxy() as data:
            await CreateEvent.set_description.set()
            data['name'] = obj.text
            await obj.bot.send_message(
                chat_id=obj.from_user.id,
                text="Напиши анонс, который получат участники вашего мероприятия",
                reply_markup=get_back_keyboard(
                    callback_data=cb_create_event, action='set_description',
                )
            )


async def set_description_for_event(obj: CallbackQuery | Message,
                                    state: FSMContext, repo: Repo) -> None:
    if isinstance(obj, CallbackQuery):
        await CreateEvent.set_description.set()
        await obj.message.edit_reply_markup(reply_markup=None)
        await obj.bot.send_message(
            chat_id=obj.from_user.id,
            text="Напиши анонс, который получат участники вашего мероприятия",
            reply_markup=get_back_keyboard(
                callback_data=cb_create_event, action='set_description',
            )
        )
    elif isinstance(obj, Message):
        async with state.proxy() as data:
            await CreateEvent.confirm.set()
            data['description'] = obj.text
            await obj.bot.send_message(
                chat_id=obj.from_user.id,
                text=f'Ваше событие: {data["name"]}\nТекст: {data["description"]}',
                reply_markup=get_confirm_event_keyboard(),
            )


async def confirm_for_event(query: CallbackQuery, callback_data: dict,
                            state: FSMContext, repo: Repo) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        event: Event = await repo.create_event(data=data)
        execute_mailing.delay(event.id)
        organization_id = data['organization_id']
    await state.finish()
    await OrganizationManagement.menu.set()
    async with state.proxy() as data:
        data['organization_id'] = organization_id
    user = await repo.get_user(user_id=query.from_user.id)

    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=f"Событие {event.name} создано!",
        reply_markup=get_organization_keyboard(user=user)
    )
