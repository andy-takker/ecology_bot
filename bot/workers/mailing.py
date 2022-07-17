import asyncio

from aiogram import Bot, types

from config import get_settings
from database.engine import get_async_session_maker
from services.repository import Repo
from workers.celery import celery


@celery.task(name='execute_mailing', bind=True, track_started=True)
def execute_mailing(self, event_id: int) -> None:
    asyncio.run(_execute_mailing(event_id))


async def _execute_mailing(event_id: int) -> None:
    """Выполняет рассылку по волонтерам"""
    print('test')
    settings = get_settings()
    AsyncSession = get_async_session_maker(
        db_url=settings.SQLALCHEMY_DATABASE_URI)
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    session = AsyncSession()
    repo = Repo(session=session)
    event = await repo.get_event(event_id)
    profiles = await repo.get_profiles_for_event(event=event)
    for profile in profiles:
        await bot.send_message(chat_id=profile.user.telegram_id, text=event.message,parse_mode=types.ParseMode.MARKDOWN)
    await bot.close()
    print('close test')
