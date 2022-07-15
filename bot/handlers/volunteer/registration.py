from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.activity import get_activity_keyboard
from keyboards.default.district import get_district_keyboard
from keyboards.default.municipal import get_municipal_keyboard
from keyboards.default.volunteer import get_volunteer_keyboard
from keyboards.inline.callback_data import cb_volunteer_register
from services.repository import Repo
from states.management import VolunteerManagement
from states.registration import VolunteerRegister


async def choose_district_for_volunteer(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    """Выбираем район, к которому будет относиться волонтер"""
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerRegister.choose_district.set()
    districts = await repo.get_districts()
    async with state.proxy() as data:
        match callback_data['name']:
            case 'objects':
                district_id = int(callback_data['value'])
                municipals = await repo.get_municipals_by_districts(
                    [district_id])
                data['district_id'] = district_id
                await VolunteerRegister.choose_municipal.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выбери муниципальное образование",
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_volunteer_register,
                    )
                )
            case 'page':
                page = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_district_keyboard(
                        callback_data=cb_volunteer_register,
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
                        callback_data=cb_volunteer_register,
                        with_chose=False,
                    )
                )


async def choose_municipal_for_volunteer(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    """Выбираем муниципальный округ, к которому будет относиться волонтер"""
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerRegister.choose_municipal.set()
    async with state.proxy() as data:
        municipals = await repo.get_municipals_by_districts(
            [data['district_id']])
        if 'eco_activities' in data:
            del data['eco_activities']
        match callback_data['name']:
            case 'objects':
                data['municipal_id'] = int(callback_data['value'])
                activities = await repo.get_activities()
                await VolunteerRegister.choose_activity_type.set()
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выбери интересующие тебя активности."
                         "По ним тебе будет приходит информация.",
                    reply_markup=get_activity_keyboard(
                        activities=activities,
                        callback_data=cb_volunteer_register,
                        with_chose=True,
                    )
                )
            case 'page':
                page = int(callback_data['value'])
                await query.message.edit_reply_markup(
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_volunteer_register,
                        page=page
                    )
                )
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выбери муниципальное образование",
                    reply_markup=get_municipal_keyboard(
                        municipals=municipals,
                        callback_data=cb_volunteer_register,
                    )
                )


async def choose_eco_activities_for_volunteer(
        query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        repo: Repo,
) -> None:
    """Выбираем активности, по которым будут приходить уведомления"""
    await query.message.edit_reply_markup(reply_markup=None)
    await VolunteerRegister.choose_activity_type.set()
    async with state.proxy() as data:
        if data.get('eco_activities') is None:
            data['eco_activities'] = {}
        activities = await repo.get_activities()
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
                        callback_data=cb_volunteer_register,
                        page=data['eco_activities'].get('page', 1),
                        chose_activities=data['eco_activities'].keys(),
                        with_chose=True
                    )
                )
            case 'next':
                data['eco_activities'] = [i for i in data['eco_activities'] if i != 'page']
                data['user_id'] = query.from_user.id
                await repo.create_profile(data=data)
                await state.finish()
                await VolunteerManagement.menu.set()
                user = await repo.get_user(user_id=query.from_user.id)
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text='Мы пришлем тебе уведомления на основе подписок!'
                         'Также ты можешь зайти в меню каждой подписки и'
                         'посмотреть подробности',
                    reply_markup=get_volunteer_keyboard(user=user),
                )
            case '_':
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="Выбери интересующие тебя активности."
                         "По ним тебе будет приходит информация.",
                    reply_markup=get_activity_keyboard(
                        activities=activities,
                        callback_data=cb_volunteer_register,
                        chose_activities=data['eco_activities'].keys(),
                        with_chose=True,
                    )
                )
