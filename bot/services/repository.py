from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.models import User, District, EcoActivity, Organization, \
    Municipal, DistrictOrganization, Event, VolunteerType, Profile, \
    EcoActivityOrganization, EcoActivityProfile, EcoActivityEvent, \
    MunicipalEvent, VolunteerTypeProfile, VolunteerTypeEvent


class Repo:
    """Database abstraction layer"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int) -> Optional[User]:
        query = select(User).filter_by(telegram_id=user_id).options(
            selectinload(User.organizations),
            selectinload(User.profile).selectinload(Profile.eco_activities),
        )
        result = (await self.session.execute(query)).scalar()
        return result

    async def create_user(self, telegram_id: int, is_admin: bool = False):
        async with self.session:
            user = User(telegram_id=telegram_id, is_admin=is_admin)
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

    async def get_municipals(self, ids: list[int] = None) -> Optional[
        list[Municipal]]:
        query = select(Municipal)
        if ids is not None:
            query = query.filter(Municipal.id.in_(ids))
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_activities(self, ids: list[int] = None) -> list[EcoActivity]:
        query = select(EcoActivity)
        if ids is not None:
            query = query.filter(EcoActivity.id.in_(ids))
        return (await self.session.execute(query)).scalars().all()

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

    async def get_municipals_by_districts(self, district_ids: list[int]) -> \
            Optional[list[Municipal]]:
        query = select(Municipal).filter(
            Municipal.district_id.in_(district_ids))
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_municipal(self, municipal_id: int) -> Optional[Municipal]:
        query = select(Municipal).filter_by(id=municipal_id)
        result = (await self.session.execute(query)).scalar()
        return result

    async def get_organization_full(self, organization_id: int) -> Optional[
        Organization]:
        query = select(Organization).filter_by(id=organization_id).options(
            selectinload(Organization.districts),
            selectinload(Organization.eco_activities),
            selectinload(Organization.creator),
        )
        result: Optional[Organization] = (
            await self.session.execute(query)).scalars().first()
        return result

    async def get_organization_full_info(self, organization_id: int) -> str:
        organization = await self.get_organization_full(organization_id)

        name = f"Название: {organization.name}\n\n"
        districts = f"Районы: {', '.join([str(d) for d in organization.districts])}\n"
        eco_activities = f"Активности: {', '.join([str(e) for e in organization.eco_activities])}"
        return name + districts + eco_activities

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

    async def create_event(self, data: dict) -> Event:
        async with self.session:
            event = Event()
            event.name = data.get('name')
            event.description = data.get('description')
            event.type = data.get('type')
            event.organization_id = data.get('organization_id')
            event.eco_activities.extend(
                await self.get_activities([data.get('activity_id')]))
            event.districts.extend(
                await self.get_districts([data.get('district_id')]))
            event.municipals.extend(
                await self.get_municipals([data.get('municipal_id')]))
            self.session.add(event)
            await self.session.commit()
            await self.session.refresh(event)
            return event

    async def get_volunteer_types(self, ids: list[int] = None) -> list[
        VolunteerType]:
        query = select(VolunteerType)
        if ids is not None:
            query = query.filter(VolunteerType.id.in_(ids))
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def create_volunteer_event(self, data):
        print(data)
        async with self.session:
            event = Event()
            event.name = ""
            event.description = data.get('description')
            event.organization_id = data.get('organization_id')
            event.districts.extend(
                await self.get_districts(ids=[data.get('district_id')])),
            event.municipals.extend(
                await self.get_municipals(ids=[data.get('municipal_id')])),
            event.type = data.get('type')
            event.volunteer_types.extend(
                await self.get_volunteer_types(ids=data.get('volunteer_ids')))
            self.session.add(event)
            await self.session.commit()
            await self.session.refresh(event)
            return event

    async def get_event(self, event_id: int) -> Optional[Event]:
        query = select(Event).filter_by(id=event_id).options(
            selectinload(Event.districts),
            selectinload(Event.municipals),
            selectinload(Event.eco_activities),
            selectinload(Event.volunteer_types),
            selectinload(Event.organization),
        )
        result: Optional[Organization] = (
            await self.session.execute(query)).scalars().first()
        return result

    async def create_profile(self, data: dict) -> Profile:
        async with self.session:
            profile = Profile()
            profile.user_id = (await self.get_user(data.get('user_id'))).id
            profile.municipal_id = data['municipal_id']
            profile.eco_activities = await self.get_activities(
                ids=data['eco_activities'])
            self.session.add(profile)
            await self.session.commit()
            await self.session.refresh(profile)
            return profile

    async def get_profile(self, user_id: int) -> Optional[Profile]:
        query = select(Profile) \
            .join(User, User.id == Profile.user_id) \
            .filter(User.telegram_id == user_id) \
            .options(
            selectinload(Profile.municipal),
            selectinload(Profile.eco_activities),
            selectinload(Profile.volunteer_types),
        )
        result = (await self.session.execute(query)).scalars().first()
        return result

    async def get_organizations_by_profile(
            self, profile: Profile, eco_activity_id: int) -> list[Organization]:
        query = select(Organization) \
            .join(DistrictOrganization,
                  Organization.id == DistrictOrganization.organization_id) \
            .join(EcoActivityOrganization,
                  Organization.id == EcoActivityOrganization.organization_id) \
            .filter(
            EcoActivityOrganization.eco_activity_id == eco_activity_id,
            DistrictOrganization.district_id == profile.municipal.district_id
        )
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_profiles_for_event(self, event: Event) -> list[Profile]:
        """Возвращает список профилей для рассылок событий"""

        query = select(Profile).options(selectinload(Profile.user)) \
            .join(EcoActivityProfile,
                  Profile.id == EcoActivityProfile.profile_id) \
            .join(EcoActivityEvent,
                  EcoActivityProfile.eco_activity_id == EcoActivityEvent.eco_activity_id) \
            .join(MunicipalEvent,
                  MunicipalEvent.event_id == EcoActivityEvent.event_id) \
            .filter(EcoActivityEvent.event_id == event.id,
                    MunicipalEvent.municipal_id == Profile.municipal_id)
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_events_for_profile(self, profile: Profile) -> list[Event]:
        query = select(Event) \
            .join(EcoActivityEvent, Event.id == EcoActivityEvent.event_id) \
            .join(EcoActivityProfile,
                  EcoActivityEvent.eco_activity_id == EcoActivityProfile.eco_activity_id) \
            .join(MunicipalEvent, Event.id == MunicipalEvent.event_id) \
            .filter(EcoActivityProfile.profile_id == profile.id,
                    MunicipalEvent.municipal_id == profile.municipal_id)
        events = (await self.session.execute(query)).scalars().all()
        if profile.is_event_organizer:
            query = select(Event) \
                .join(VolunteerTypeEvent,
                      VolunteerTypeEvent.event_id == Event.id) \
                .join(MunicipalEvent, Event.id == MunicipalEvent.event_id) \
                .join(VolunteerTypeProfile, VolunteerTypeEvent.volunteer_type_id == VolunteerTypeProfile.volunteer_type_id)\
                .filter(MunicipalEvent.municipal_id == profile.municipal_id, VolunteerTypeProfile.profile_id == profile.id)
            result = (await self.session.execute(query)).scalars().all()
            events.extend(result)
        return events

    async def get_admins(self) -> list[User]:
        query = select(User).filter_by(is_admin=True)
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def update_profile(self, user_id: int, activity_ids=None,
                             municipal_id=None,
                             age=None,
                             name=None,
                             volunteer_type_ids=None,
                             is_event_organizer=None):
        query = select(Profile).options(
            selectinload(Profile.eco_activities),
            selectinload(Profile.volunteer_types)) \
            .join(User, User.id == Profile.user_id).filter(
            User.telegram_id == user_id)
        async with self.session:
            profile = (await self.session.execute(query)).scalars().first()
            if municipal_id is not None:
                profile.municipal_id = municipal_id
            if activity_ids is not None:
                profile.eco_activities = await self.get_activities(
                    ids=activity_ids)
            if age is not None:
                profile.age = age
            if name is not None:
                profile.name = name
            if volunteer_type_ids is not None:
                profile.volunteer_types = await self.get_volunteer_types(
                    ids=volunteer_type_ids)
            if is_event_organizer is not None:
                profile.is_event_organizer = is_event_organizer
            await self.session.commit()

    async def delete_profile(self, user_id: int) -> None:
        async with self.session:
            query = select(Profile).join(User,
                                         User.id == Profile.user_id).filter(
                User.telegram_id == user_id)
            profile = (await self.session.execute(query)).scalars().first()
            if profile is not None:
                await self.session.delete(profile)
            await self.session.commit()

    async def get_profiles_for_recruitment(self, event: Event) -> list[Profile]:
        query = select(Profile) \
            .join(VolunteerTypeProfile,
                  Profile.id == VolunteerTypeProfile.profile_id) \
            .join(VolunteerTypeEvent,
                  VolunteerTypeProfile.volunteer_type_id == VolunteerTypeEvent.volunteer_type_id) \
            .filter(VolunteerTypeEvent.event_id == event.id,
                    Profile.is_event_organizer == True)
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_district(self, name) -> Optional[District]:
        query = select(District).filter_by(name=name)
        return (await self.session.execute(query)).scalars().first()

    async def get_municipal_by_name_and_district(self, name,district) -> Optional[District]:
        query = select(Municipal).filter_by(name=name,district_id=district.id)
        return (await self.session.execute(query)).scalars().first()

    async def update_chat_link(self,municipal, chat_link):
        async with self.session:
            municipal.invite_link = chat_link
            await self.session.commit()