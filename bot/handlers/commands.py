from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import default_state
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import Message, CallbackQuery

from handlers.admin.management import get_admin_menu
from keyboards.default.start import get_start_keyboard
from keyboards.inline.callback_data import cb_start, \
    cb_organization_menu
from services.repository import Repo

ONBOARDING_MESSAGE = """
Привет! Это пилотная версия экобота Союза экологических организаций. В нем вы
сможете найти себе активности по душе.

Для начала мы выбрали Ленобласть, но далее будем масштабировать. Если вы из
другого региона, нажмите на кнопку "Другой регион".

Ваша активность поможет развитию бота!
"""

RETURN_MESSAGE = """
С возвращением!
"""
HELP_MESSAGE = """
С помощью нашего бота волонтеры могут получать персонализированные уведомления о мероприятиях и волонтерских вакансиях в своем районе, а экологически активные сообщества - найти волонтеров и привлечь участников на свои мероприятия и акции.
Бот может пригласить Вас в чат, где собрались экоактивисты из Вашего мо. Общайтесь, делитесь опытом, объединяйтесь для создания эко-событий! 
Всем пользователям бота доступна справочная информация: адреса пунктов приема вторсырья, контакты фондов и приютов и другая. 
Это пилотная версия, и со временем функционал будет расширен.
"""


async def user_start(tg_obj: Union[Message, CallbackQuery], repo: Repo,
                     state: FSMContext):
    await state.reset_state(with_data=True)
    user = await repo.get_user(tg_obj.from_user.id)
    if isinstance(tg_obj, Message):
        text = ONBOARDING_MESSAGE
        if user is not None:
            text = RETURN_MESSAGE
        else:
            await repo.create_user(telegram_id=tg_obj.from_user.id)
            user = await repo.get_user(user_id=tg_obj.from_user.id)
    else:
        text = 'Выберите пункт'
        await tg_obj.message.edit_reply_markup(reply_markup=None)
    await tg_obj.bot.send_message(chat_id=tg_obj.from_user.id, text=text,
                                  reply_markup=get_start_keyboard(user=user))


async def get_help(tg_obj: Union[CallbackQuery, Message], repo: Repo,
                   state: FSMContext):
    user = await repo.get_user(tg_obj.from_user.id)
    start_keyboard = get_start_keyboard(user=user)
    if isinstance(tg_obj, CallbackQuery):
        await tg_obj.message.edit_reply_markup(reply_markup=None)
    await tg_obj.bot.send_message(
        chat_id=tg_obj.from_user.id,
        text=HELP_MESSAGE,
        reply_markup=start_keyboard,
    )


async def set_municipal_chat_link(message: Message, repo: Repo) -> None:
    _, district, municipal, chat_link = message.text.split(' ')
    district = district.replace('_', ' ')
    municipal = municipal.replace('_', ' ')
    district = await repo.get_district(name=district)
    if district is not None:
        municipal = await repo.get_municipal_by_name_and_district(
            name=municipal,
            district=district,
        )
        if municipal is not None:
            await repo.update_chat_link(municipal, chat_link)
            await message.bot.send_message(
                chat_id=message.from_user.id,
                text='Ссылка обновлена!',
            )
            return
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text='МО не найдено!',
        )
        return
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text='Район не найден!'
    )


def register_commands(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state="*")
    dp.register_callback_query_handler(
        user_start,
        cb_organization_menu.filter(action='choose_organization',
                                    name='back', value='back'),
        state=default_state)
    dp.register_message_handler(get_help, commands=['help'], state='*', )
    dp.register_callback_query_handler(get_help, cb_start.filter(
        name='help'), state='*')
    dp.register_callback_query_handler(
        user_start,
        cb_start.filter(name='go_to_main_menu'), state='*')

    dp.register_message_handler(get_admin_menu, commands=['admin'], state='*',
                                is_admin=True)

    dp.register_message_handler(set_municipal_chat_link,
                                commands=['setmunicipal'], state='*',
                                is_admin=True)
