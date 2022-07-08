from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.municipal import get_municipal_keyboard
from keyboards.default.organization import get_checked_organizations_keyboard, \
    get_organization_keyboard
from services.repository import Repo
from states.management import OrganizationManagement


async def choose_organization(query: CallbackQuery, callback_data: dict,
                              state: FSMContext, repo: Repo):
    await query.message.edit_reply_markup(reply_markup=None)
    organizations = await repo.get_checked_organizations(
        user_id=query.from_user.id)
    await OrganizationManagement.menu.set()
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=f"Выберите организацию",
        reply_markup=get_checked_organizations_keyboard(organizations),
    )


async def organization_menu(query: CallbackQuery, callback_data: dict,
                            state: FSMContext, repo: Repo):
    await query.message.edit_reply_markup(reply_markup=None)
    organization_id = int(callback_data['value'])
    organization = await repo.get_organization(organization_id=organization_id)
    async with state.proxy() as data:
        data['organization_id'] = organization_id
    user = await repo.get_user(user_id=query.from_user.id)
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=f'Сейчас Вы действуете от лица организации: "{organization}"',
        reply_markup=get_organization_keyboard(user=user)
    )


async def get_invite_link_choose_municipal(query: CallbackQuery,
                                           callback_data: dict,
                                           state: FSMContext, repo: Repo):
    await query.message.edit_reply_markup(reply_markup=None)
    await OrganizationManagement.choose_municipal.set()
    async with state.proxy() as data:
        organization_id = data['organization_id']
    municipals = await repo.get_municipals_by_organization(organization_id)
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text="Выберите муниципальный округ для получения ссылки в чат",
        reply_markup=get_municipal_keyboard(municipals),
    )


async def get_invite_link_navigate_municipal(query: CallbackQuery,
                                             callback_data: dict,
                                             state: FSMContext, repo: Repo):
    async with state.proxy() as data:
        organization_id = data['organization_id']
        municipals = await repo.get_municipals_by_organization(organization_id)
        if callback_data['name'] == 'page':
            data['municipal_page'] = int(callback_data['value'])
        await query.message.edit_reply_markup(
            reply_markup=get_municipal_keyboard(municipals=municipals,
                                                page=data.get(
                                                    'municipal_page', 1),
                                                )
        )


async def get_invite_link_to_group_from_municipal(query: CallbackQuery,
                                                  callback_data: dict,
                                                  state: FSMContext,
                                                  repo: Repo):
    user = await repo.get_user(user_id=query.from_user.id)
    await query.message.edit_reply_markup(reply_markup=None)
    municipal_id = int(callback_data['value'])
    municipal = await repo.get_municipal(municipal_id=municipal_id)
    await OrganizationManagement.menu.set()
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=f"Ссылка на чат: {municipal.invite_link}",
        reply_markup=get_organization_keyboard(user=user),
    )
