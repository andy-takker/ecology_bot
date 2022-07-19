import enum
from typing import List

from flask_login import UserMixin
from sqlalchemy import Column, BigInteger, ForeignKey, String, Boolean, \
    DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from werkzeug.security import check_password_hash, generate_password_hash

from database.base import Base
from database.mixins import PkMixin, TimestampMixin


class EventType(enum.Enum):
    """Типы событий"""
    DEFAULT = 'DEFAULT'  # Обычное событие
    RECRUITMENT = 'RECRUITMENT'  # Нужны волонтеры


class EcoActivity(PkMixin, Base):
    """Экологические активности"""
    name = Column(String, unique=True, nullable=False, index=True)

    organizations = relationship('Organization',
                                 secondary='eco_activity_organization',
                                 back_populates='eco_activities', )

    events = relationship('Event', secondary='eco_activity_event',
                          back_populates='eco_activities')
    profiles = relationship('Profile', secondary='eco_activity_profile',
                            back_populates='eco_activities')

    def __str__(self):
        return self.name


class District(PkMixin, Base):
    """Район"""
    name = Column(String, unique=True, nullable=False, index=True)

    organizations = relationship('Organization',
                                 secondary='district_organization',
                                 back_populates='districts')

    municipals = relationship('Municipal', back_populates='district')
    events = relationship('Event', secondary='district_event',
                          back_populates='districts')

    def __str__(self):
        return self.name


class User(PkMixin, TimestampMixin, Base):
    """Пользователи"""
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    is_admin = Column(Boolean, default=False)

    organizations: List = relationship('Organization', back_populates='creator')
    profile = relationship('Profile', back_populates='user', uselist=False)

    @property
    def has_unchecked_organizations(self) -> bool:
        return any(map(lambda organization: not organization.is_checked,
                       self.organizations))

    @property
    def has_checked_organizations(self) -> bool:
        return any(map(lambda organization: organization.is_checked,
                       self.organizations))

    def __str__(self) -> str:
        return f'User ({self.telegram_id})'

class Profile(PkMixin, TimestampMixin, Base):
    """Профиль пользователя"""
    user_id = Column(BigInteger, ForeignKey('user.id'), index=True,
                     nullable=False, unique=True)

    municipal_id = Column(BigInteger, ForeignKey('municipal.id'), index=True,
                          nullable=False)

    is_event_organizer = Column(Boolean, index=True, default=False)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)

    user = relationship('User', back_populates='profile', uselist=False)

    eco_activities = relationship(
        'EcoActivity',
        secondary='eco_activity_profile',
        back_populates='profiles',
    )
    volunteer_types = relationship(
        'VolunteerType',
        secondary='volunteer_type_profile',
        back_populates='profiles',
    )
    municipal = relationship('Municipal', back_populates='profiles')

    def __str__(self):
        return f'Profile {self.id} ({self.user_id})'

    @property
    def info(self) -> str:
        msg = f"Район: {self.municipal}\n\n" \
               f"Активности: \n{ ','.join(e.name for e in self.eco_activities)}"
        if self.is_event_organizer:
            msg += '\n\n' \
                   'Ты также подписан(а) на сообщения об организации мероприятий.\n' \
                   f'Имя: {self.name}\nВозраст: {self.age}\n' \
                   f'Виды помощи, которые ты указал(а):\n{ ", ".join(v.name for v in self.volunteer_types)}'
        return msg

class Organization(PkMixin, TimestampMixin, Base):
    """Организации"""
    creator_id = Column(BigInteger, ForeignKey('user.id'), index=True,
                        nullable=False)
    name = Column(String, index=True)
    is_checked = Column(Boolean, default=False)
    is_superorganization = Column(Boolean, default=False)

    creator = relationship('User', back_populates='organizations')
    eco_activities = relationship(
        'EcoActivity',
        secondary='eco_activity_organization',
        back_populates='organizations',
    )
    districts = relationship(
        'District',
        secondary='district_organization',
        back_populates='organizations',
    )
    events = relationship('Event', back_populates='organization')

    def __str__(self):
        return self.name


class VolunteerType(PkMixin, Base):
    name = Column(String, index=True)

    events = relationship('Event', secondary='volunteer_type_event',
                          back_populates='volunteer_types')
    profiles = relationship('Profile', secondary='volunteer_type_profile',
                            back_populates='volunteer_types')

    def __str__(self):
        return self.name


class EcoActivityOrganization(PkMixin, Base):
    eco_activity_id = Column(
        BigInteger,
        ForeignKey('eco_activity.id'),
        index=True,
        nullable=False,
    )
    organization_id = Column(
        BigInteger,
        ForeignKey('organization.id'),
        index=True,
        nullable=False,
    )


class DistrictOrganization(PkMixin, Base):
    district_id = Column(
        BigInteger,
        ForeignKey('district.id'),
        index=True,
        nullable=False,
    )
    organization_id = Column(
        BigInteger,
        ForeignKey('organization.id'),
        index=True,
        nullable=False,
    )


class Municipal(PkMixin, Base):
    """Муниципальный округ"""
    __table_args__ = (
        UniqueConstraint('district_id', 'name'),
    )
    district_id = Column(
        BigInteger,
        ForeignKey('district.id'),
        index=True,
        nullable=False,
    )
    name = Column(
        String,
        index=True,
        nullable=False,
    )
    invite_link = Column(
        String,
        nullable=True,
    )

    district = relationship('District', back_populates='municipals')
    events = relationship('Event', secondary='municipal_event',
                          back_populates='municipals')
    profiles = relationship('Profile', back_populates='municipal')

    def __str__(self):
        return f"{self.name}"


class Event(PkMixin, TimestampMixin, Base):
    """Событие"""
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    type = Column(ChoiceType(EventType, impl=String()), index=True)
    organization_id = Column(BigInteger, ForeignKey('organization.id'),
                             index=True, nullable=False)

    mailing = relationship('Mailing', back_populates='event', uselist=False)
    organization = relationship('Organization', back_populates='events')

    districts = relationship('District', secondary='district_event',
                             back_populates='events')
    eco_activities = relationship('EcoActivity', secondary='eco_activity_event',
                                  back_populates='events')
    municipals = relationship('Municipal', secondary='municipal_event',
                              back_populates='events')

    volunteer_types = relationship('VolunteerType',
                                   secondary='volunteer_type_event',
                                   back_populates='events')

    def __str__(self):
        return self.name

    @property
    def message(self):
        if self.type == EventType.DEFAULT:
            return f"В МО {self.municipals[0]} проходит мероприятие *\"{self.name}\"*\n" \
                   f"Оно относится к активностям: {', '.join(a.name for a in self.eco_activities).lower()}\n " \
                   f"\nОписание:\n{self.description} \n\n Его проводит организация *\"{self.organization}\"*"
        elif self.type == EventType.RECRUITMENT:
            return f"Организации *\"{self.organization}\"* нужны: " \
                   f"{', '.join(v.name for v in self.volunteer_types).lower()} волонтеры в МО " \
                   f"*{self.municipals[0]}*\n\nОписание:\n{self.description}"
        return ""


class VolunteerTypeEvent(PkMixin, Base):
    volunteer_type_id = Column(
        BigInteger,
        ForeignKey('volunteer_type.id'),
        index=True,
        nullable=False,
    )
    event_id = Column(
        BigInteger,
        ForeignKey('event.id'),
        index=True,
        nullable=False,
    )


class VolunteerTypeProfile(PkMixin, Base):
    volunteer_type_id = Column(
        BigInteger,
        ForeignKey('volunteer_type.id'),
        index=True,
        nullable=False,
    )
    profile_id = Column(
        BigInteger,
        ForeignKey('profile.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )


class DistrictEvent(PkMixin, Base):
    district_id = Column(
        BigInteger,
        ForeignKey('district.id'),
        index=True,
        nullable=False,
    )
    event_id = Column(
        BigInteger,
        ForeignKey('event.id'),
        index=True,
        nullable=False,
    )


class MunicipalEvent(PkMixin, Base):
    municipal_id = Column(BigInteger, ForeignKey('municipal.id'), index=True,
                          nullable=False)
    event_id = Column(
        BigInteger,
        ForeignKey('event.id'),
        index=True,
        nullable=False,
    )


class EcoActivityEvent(PkMixin, Base):
    eco_activity_id = Column(
        BigInteger,
        ForeignKey('eco_activity.id'),
        index=True,
        nullable=False,
    )
    event_id = Column(
        BigInteger,
        ForeignKey('event.id'),
        index=True,
        nullable=False,
    )


class Mailing(PkMixin, TimestampMixin, Base):
    """Рассылка"""
    is_executed = Column(Boolean, index=True, default=False)
    start_execute_datetime = Column(DateTime, nullable=True, index=True)
    end_execute_datetime = Column(DateTime, nullable=True, index=True)
    event_id = Column(BigInteger, ForeignKey('event.id'), index=True,
                      nullable=False)

    event = relationship('Event', back_populates='mailing', uselist=False)

    def __str__(self):
        return f"{self.id} Mailing (executed: {self.is_executed})"


class EcoActivityProfile(PkMixin, Base):
    profile_id = Column(BigInteger, ForeignKey('profile.id',ondelete='CASCADE'), index=True,
                        nullable=False)
    eco_activity_id = Column(BigInteger, ForeignKey('eco_activity.id'),
                             index=True, nullable=False)


class Employee(Base, PkMixin, TimestampMixin, UserMixin):
    login = Column(String(30))
    password_hash = Column(String, nullable=False)

    def get_id(self) -> int:
        return self.id

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
