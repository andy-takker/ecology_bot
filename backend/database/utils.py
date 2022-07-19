from sqlalchemy.ext.asyncio import AsyncSession

from services.repository import Repo


async def add_admin_users(session: AsyncSession, admin_ids: list[int]):
    repo = Repo(session=session)
    for user_id in admin_ids:
        user = await repo.get_user(user_id)
        if user is None:
            await repo.create_user(telegram_id=user_id, is_admin=True)
