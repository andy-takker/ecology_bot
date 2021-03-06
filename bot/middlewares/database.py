from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from services.repository import Repo


class DatabaseMiddleWare(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, async_session_maker):
        super().__init__()
        self.async_session_maker = async_session_maker

    async def pre_process(self, obj, data, *args):
        session: AsyncSession = self.async_session_maker()
        data["session"] = session
        data["repo"] = Repo(session=session)

    async def post_process(self, obj, data, *args):
        del data["repo"]
        session: AsyncSession = data.get("session")
        await session.close()
