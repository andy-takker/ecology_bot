from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import CallbackQuery, Message
from loguru import logger

from config import get_settings
from keyboards.default.activity import get_activity_keyboard
from keyboards.default.back import get_back_keyboard
from keyboards.default.district import get_district_keyboard
from keyboards.default.start import get_start_keyboard
from keyboards.inline.callback_data import cb_organization_register
from services.repository import Repo
from states.registration import OrganizationRegistration

START_MESSAGE = """
Зарегистрируй организацию в боте.
Для начала выбери тип активности:
"""


async def choose_activities(call: CallbackQuery, state: FSMContext,
                            repo: Repo):
    await state.reset_state(with_data=False)
    await call.message.edit_reply_markup(reply_markup=None)
    await OrganizationRegistration.choosing_activities.set()
    async with state.proxy() as data:
        data['districts'] = {}
        data['activities'] = {}
    activities = await repo.get_activities()
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=START_MESSAGE,
        reply_markup=get_activity_keyboard(
            activities=activities,
            callback_data=cb_organization_register,
        ),
    )


CHOOSING_DISTRICTS_MESSAGE = """
Выбери районы, в которых есть активность твоей организации
"""


async def save_activities(query: CallbackQuery, state: FSMContext, repo: Repo):
    """Выбор активности и переход к выбору районов"""
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        activity_ids = [i for i in data['activities'].keys() if
                        i != 'page']
        data['activities'] = activity_ids
    await OrganizationRegistration.next()
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=CHOOSING_DISTRICTS_MESSAGE,
        reply_markup=get_district_keyboard(
            districts=await repo.get_districts(),
            callback_data=cb_organization_register),
    )


async def navigate_and_update_activities(query: CallbackQuery,
                                         callback_data: dict,
                                         state: FSMContext, repo: Repo):
    """Навигация и выбор активностей"""
    async with state.proxy() as data:
        if callback_data['name'] == 'objects':
            activity_id = int(callback_data['value'])
            if activity_id not in data['activities'].keys():
                data['activities'][activity_id] = True
            else:
                del data['activities'][activity_id]
        elif callback_data['name'] == 'page':
            data['activities']['page'] = int(callback_data['value'])
        activities = await repo.get_activities()
        await query.message.edit_reply_markup(
            reply_markup=get_activity_keyboard(
                activities=activities,
                callback_data=cb_organization_register,
                page=data['activities'].get('page', 1),
                chose_activities=data['activities'].keys()),
        )


ENTER_NAME_MESSAGE = """
Введите название вашей организации или инициативной группы.
Например: "Поющие в кустах сакуры, залитой лунным светом"
"""


async def save_districts(query: CallbackQuery,
                         state: FSMContext):
    logger.warning(state)
    await query.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        districts_ids = [i for i in data['districts'].keys() if
                         i != 'page']
        logger.info(f'Districts: {data}')
        data['districts_ids'] = districts_ids
    await OrganizationRegistration.next()
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=ENTER_NAME_MESSAGE,
        reply_markup=get_back_keyboard(callback_data=cb_organization_register,action='input_name')
    )


async def navigate_and_update_districts(query: CallbackQuery,
                                        callback_data: dict,
                                        state: FSMContext,
                                        repo: Repo):
    """Навигация и выбор районов"""

    await OrganizationRegistration.choosing_districts.set()
    async with state.proxy() as data:
        logger.warning(f'nav districts: {data}')
        if callback_data['name'] == 'objects':
            district_id = int(callback_data['value'])
            if district_id not in data.keys():
                data['districts'][district_id] = True
            else:
                del data['districts'][district_id]

        if callback_data['name'] == 'page':
            page = int(callback_data['value'])
            data['districts']['page'] = page
        await query.message.edit_reply_markup(
            reply_markup=get_district_keyboard(
                districts=await repo.get_districts(),
                callback_data=cb_organization_register,
                page=data['districts'].get('page', 1),
                chose_districts=data['districts'].keys())
        )


async def save_name(msg: Message, state: FSMContext, repo: Repo):
    async with state.proxy() as data:
        districts = await repo.get_districts(data['districts_ids'])
        activities = await repo.get_activities(data['activities'])
    await state.finish()

    await repo.create_organization(
        creator_id=(await repo.get_user(user_id=msg.from_user.id)).id,
        name=msg.text, districts=districts,
        eco_activities=activities)
    await msg.bot.send_message(
        chat_id=msg.from_user.id,
        text=f'Название вашей организации: "{msg.text}"\n'
             f'Организация направлена на модерацию. Ожидайте!',
        reply_markup=get_start_keyboard(
            user=await repo.get_user(user_id=msg.from_user.id)))
    settings = get_settings()
    for admin in settings.ADMINS:
        await msg.bot.send_message(
            chat_id=admin,
            text=f'Добавлена новая организация: {msg.text}.\n'
                 f'Нужно промодерировать!'
        )
