from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.default.admin import get_admin_keyboard, \
    get_unchecked_organizations_keyboard
from services.repository import Repo
from states.admin import AdminStates


async def get_admin_menu(tg_obj: Union[CallbackQuery, Message], repo: Repo,
                         state: FSMContext):
    await state.reset_state(with_data=False)
    await AdminStates.main_menu.set()
    await tg_obj.bot.send_message(
        chat_id=tg_obj.from_user.id,
        text='Вы попали в меню администратора бота',
        reply_markup=get_admin_keyboard(),
    )


async def get_organizations_for_moderating(query: CallbackQuery, repo: Repo,
                                           state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=None)
    organizations = await repo.get_unchecked_organizations()
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text="Выберите организацию для модерации:",
        reply_markup=get_unchecked_organizations_keyboard(
            organizations=organizations)
    )


async def moderate_organization(query: CallbackQuery, callback_data: dict,
                                 state: FSMContext,repo: Repo):
    await query.message.edit_reply_markup(reply_markup=None)
    organization_id = int(callback_data['value'])
    await repo.check_organization(organization_id)
    await query.bot.send_message(chat_id=query.from_user.id, text="Организация проверена!")