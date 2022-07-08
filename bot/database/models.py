from typing import List

from sqlalchemy import Column, BigInteger, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from database.base import Base
from database.mixins import PkMixin, TimestampMixin


class EcoActivity(PkMixin, Base):
    """Экологические активности"""
    name = Column(String, unique=True, nullable=False, index=True)

    organizations = relationship('Organization',
                                 secondary='eco_activity_organization',
                                 back_populates='eco_activities', )

    def __str__(self):
        return self.name


class District(PkMixin, Base):
    name = Column(String, unique=True, nullable=False, index=True)

    organizations = relationship('Organization',
                                 secondary='district_organization',
                                 back_populates='districts')

    municipals = relationship('Municipal', back_populates='district')

    def __str__(self):
        return self.name


class User(PkMixin, TimestampMixin, Base):
    """Пользователи"""
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    is_superuser = Column(Boolean, default=False)

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


class Profile(PkMixin, TimestampMixin, Base):
    """Профиль пользователя"""
    user_id = Column(BigInteger, ForeignKey('user.id'), index=True,
                     nullable=False, unique=True)

    user = relationship('User', back_populates='profile', uselist=False)


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

    def __str__(self):
        return f"{self.name}"
