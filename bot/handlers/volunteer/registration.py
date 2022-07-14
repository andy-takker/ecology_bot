from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.district import get_district_keyboard
from services.repository import Repo
from states.registration import RegisterVolunteer


async def choose_district_for_valunteer(query: CallbackQuery, callback_data: dict, state: FSMContext, repo: Repo) -> None:
    """Выбираем район, к которому будет относиться волонтер"""
    await query.message.edit_reply_markup(reply_markup=None)
    await RegisterVolunteer.choose_district.set()
    districts = await repo.get_districts()
    async with state.proxy() as data:
        match callback_data['name']:
            case 'objects':
                pass
            case 'page':
                pass
            case _:
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text='Выберите район',
                )
                data['districts'] = {}
                await query.bot.send_message(
                    chat_id=query.from_user.id,
                    text="В каком районе вы находитесь?",
                    reply_markup=get_district_keyboard(districts=districts,
                                                       with_chose=False,)
                )