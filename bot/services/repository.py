from typing import Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import Connection, select
from sqlalchemy.orm import selectinload

from database.models import User, District, EcoActivity, Organization, \
    Municipal, DistrictOrganization


class Repo:
    """Database abstraction layer"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int) -> Optional[User]:
        query = select(User).filter_by(telegram_id=user_id).options(
            selectinload(User.organizations), selectinload(User.profile))
        result = (await self.session.execute(query)).scalar()
        return result

    async def create_user(self, telegram_id: int):
        async with self.session:
            user = User(telegram_id=telegram_id)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def get_districts(self, ids: list[int] = None):
        query = select(District)
        if ids is not None:
            query = query.filter(District.id.in_(ids))

        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_activities(self, ids: list[int] = None):
        query = select(EcoActivity)
        if ids is not None:
            query = query.filter(EcoActivity.id.in_(ids))
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def create_organization(self, creator_id: int, name: str,
                                  districts: list[District],
                                  eco_activities: list[EcoActivity]):
        async with self.session:
            organization = Organization(creator_id=creator_id, name=name,
                                        eco_activities=eco_activities,
                                        districts=districts)
            self.session.add(organization)
            await self.session.commit()

    async def get_checked_organizations(self, user_id: int) -> list[
        Organization]:
        query = select(Organization).join(User).filter(
            User.telegram_id == user_id, Organization.is_checked)
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_organization(self, organization_id: int) -> Optional[
        Organization]:
        query = select(Organization).filter_by(id=organization_id)
        result = (await self.session.execute(query)).scalar()
        return result

    async def get_municipals_by_organization(self, organization_id: int) -> \
    Optional[list[Municipal]]:
        query = select(Municipal).join(DistrictOrganization,
                                       Municipal.district_id == DistrictOrganization.district_id).filter(
            DistrictOrganization.organization_id == organization_id)
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_municipal(self, municipal_id: int) -> Optional[Municipal]:
        query = select(Municipal).filter_by(id=municipal_id)
        result = (await self.session.execute(query)).scalar()
        return result

    async def get_organization_full_info(self, organization_id: int) -> str:
        query = select(Organization).filter_by(id=organization_id).options(
            selectinload(Organization.districts),
            selectinload(Organization.eco_activities,
                         selectinload(Organization.creator),
                         selectinload(Organization.creator,
                                      Organization.creator.profile))
        )
        result: Optional[Organization] = (
            await self.session.execute(query)).scalar()

        info = f"Название: {result.name}\n"
        return info

    async def get_unchecked_organizations(self) -> list[Organization]:
        query = select(Organization).filter(Organization.is_checked == False)
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def check_organization(self, organization_id: int):
        async with self.session:
            organization: Organization = await self.session.get(Organization,
                                                                organization_id)
            organization.is_checked = True
            await self.session.commit()
