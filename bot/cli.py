import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from config import get_settings
from database.engine import get_async_session_maker
from filters.role import RoleFilter, AdminFilter
from handlers.admin.dp import register_admin
from handlers.commands import register_commands
from handlers.organization.dp import register_organization
from handlers.volunteer.dp import register_volunteer
from middlewares.database import DatabaseMiddleWare
from middlewares.role import RoleMiddleware


async def main():
    logger.warning("Starting bot!")
    settings = get_settings()
    if True:
        storage = MemoryStorage()
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot, storage=storage)

    async_session_maker = get_async_session_maker(db_url=settings.SQLALCHEMY_DATABASE_URI)
    dp.middleware.setup(
        DatabaseMiddleWare(async_session_maker=async_session_maker))
    dp.middleware.setup(RoleMiddleware(settings.ADMINS))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    register_admin(dp=dp)
    register_commands(dp=dp)
    register_organization(dp=dp)
    register_volunteer(dp=dp)


    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        bot.get_session().close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped!")


if __name__ == '__main__':
    cli()
