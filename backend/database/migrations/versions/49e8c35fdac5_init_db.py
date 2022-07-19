"""Init db

Revision ID: 49e8c35fdac5
Revises: 
Create Date: 2022-07-17 19:23:58.261921

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
from database import EventType

revision = '49e8c35fdac5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('district',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_district_id'), 'district', ['id'], unique=False)
    op.create_index(op.f('ix_district_name'), 'district', ['name'], unique=True)
    op.create_table('eco_activity',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eco_activity_id'), 'eco_activity', ['id'], unique=False)
    op.create_index(op.f('ix_eco_activity_name'), 'eco_activity', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_telegram_id'), 'user', ['telegram_id'], unique=True)
    op.create_table('volunteer_type',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_volunteer_type_id'), 'volunteer_type', ['id'], unique=False)
    op.create_index(op.f('ix_volunteer_type_name'), 'volunteer_type', ['name'], unique=False)
    op.create_table('municipal',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('district_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('invite_link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('district_id', 'name')
    )
    op.create_index(op.f('ix_municipal_district_id'), 'municipal', ['district_id'], unique=False)
    op.create_index(op.f('ix_municipal_id'), 'municipal', ['id'], unique=False)
    op.create_index(op.f('ix_municipal_name'), 'municipal', ['name'], unique=False)
    op.create_table('organization',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('creator_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('is_checked', sa.Boolean(), nullable=True),
    sa.Column('is_superorganization', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organization_creator_id'), 'organization', ['creator_id'], unique=False)
    op.create_index(op.f('ix_organization_id'), 'organization', ['id'], unique=False)
    op.create_index(op.f('ix_organization_name'), 'organization', ['name'], unique=False)
    op.create_table('district_organization',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('district_id', sa.BigInteger(), nullable=False),
    sa.Column('organization_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_district_organization_district_id'), 'district_organization', ['district_id'], unique=False)
    op.create_index(op.f('ix_district_organization_id'), 'district_organization', ['id'], unique=False)
    op.create_index(op.f('ix_district_organization_organization_id'), 'district_organization', ['organization_id'], unique=False)
    op.create_table('eco_activity_organization',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('eco_activity_id', sa.BigInteger(), nullable=False),
    sa.Column('organization_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['eco_activity_id'], ['eco_activity.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eco_activity_organization_eco_activity_id'), 'eco_activity_organization', ['eco_activity_id'], unique=False)
    op.create_index(op.f('ix_eco_activity_organization_id'), 'eco_activity_organization', ['id'], unique=False)
    op.create_index(op.f('ix_eco_activity_organization_organization_id'), 'eco_activity_organization', ['organization_id'], unique=False)
    op.create_table('event',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('type', sqlalchemy_utils.types.choice.ChoiceType(EventType), nullable=True),
    sa.Column('organization_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_id'), 'event', ['id'], unique=False)
    op.create_index(op.f('ix_event_name'), 'event', ['name'], unique=False)
    op.create_index(op.f('ix_event_organization_id'), 'event', ['organization_id'], unique=False)
    op.create_index(op.f('ix_event_type'), 'event', ['type'], unique=False)
    op.create_table('profile',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('municipal_id', sa.BigInteger(), nullable=False),
    sa.Column('is_event_organizer', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['municipal_id'], ['municipal.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_id'), 'profile', ['id'], unique=False)
    op.create_index(op.f('ix_profile_is_event_organizer'), 'profile', ['is_event_organizer'], unique=False)
    op.create_index(op.f('ix_profile_municipal_id'), 'profile', ['municipal_id'], unique=False)
    op.create_index(op.f('ix_profile_user_id'), 'profile', ['user_id'], unique=True)
    op.create_table('district_event',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('district_id', sa.BigInteger(), nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_district_event_district_id'), 'district_event', ['district_id'], unique=False)
    op.create_index(op.f('ix_district_event_event_id'), 'district_event', ['event_id'], unique=False)
    op.create_index(op.f('ix_district_event_id'), 'district_event', ['id'], unique=False)
    op.create_table('eco_activity_event',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('eco_activity_id', sa.BigInteger(), nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['eco_activity_id'], ['eco_activity.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eco_activity_event_eco_activity_id'), 'eco_activity_event', ['eco_activity_id'], unique=False)
    op.create_index(op.f('ix_eco_activity_event_event_id'), 'eco_activity_event', ['event_id'], unique=False)
    op.create_index(op.f('ix_eco_activity_event_id'), 'eco_activity_event', ['id'], unique=False)
    op.create_table('eco_activity_profile',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('profile_id', sa.BigInteger(), nullable=False),
    sa.Column('eco_activity_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['eco_activity_id'], ['eco_activity.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eco_activity_profile_eco_activity_id'), 'eco_activity_profile', ['eco_activity_id'], unique=False)
    op.create_index(op.f('ix_eco_activity_profile_id'), 'eco_activity_profile', ['id'], unique=False)
    op.create_index(op.f('ix_eco_activity_profile_profile_id'), 'eco_activity_profile', ['profile_id'], unique=False)
    op.create_table('mailing',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_executed', sa.Boolean(), nullable=True),
    sa.Column('start_execute_datetime', sa.DateTime(), nullable=True),
    sa.Column('end_execute_datetime', sa.DateTime(), nullable=True),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mailing_end_execute_datetime'), 'mailing', ['end_execute_datetime'], unique=False)
    op.create_index(op.f('ix_mailing_event_id'), 'mailing', ['event_id'], unique=False)
    op.create_index(op.f('ix_mailing_id'), 'mailing', ['id'], unique=False)
    op.create_index(op.f('ix_mailing_is_executed'), 'mailing', ['is_executed'], unique=False)
    op.create_index(op.f('ix_mailing_start_execute_datetime'), 'mailing', ['start_execute_datetime'], unique=False)
    op.create_table('municipal_event',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('municipal_id', sa.BigInteger(), nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['municipal_id'], ['municipal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_municipal_event_event_id'), 'municipal_event', ['event_id'], unique=False)
    op.create_index(op.f('ix_municipal_event_id'), 'municipal_event', ['id'], unique=False)
    op.create_index(op.f('ix_municipal_event_municipal_id'), 'municipal_event', ['municipal_id'], unique=False)
    op.create_table('volunteer_type_event',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('volunteer_type_id', sa.BigInteger(), nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['volunteer_type_id'], ['volunteer_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_volunteer_type_event_event_id'), 'volunteer_type_event', ['event_id'], unique=False)
    op.create_index(op.f('ix_volunteer_type_event_id'), 'volunteer_type_event', ['id'], unique=False)
    op.create_index(op.f('ix_volunteer_type_event_volunteer_type_id'), 'volunteer_type_event', ['volunteer_type_id'], unique=False)
    op.create_table('volunteer_type_profile',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('volunteer_type_id', sa.BigInteger(), nullable=False),
    sa.Column('profile_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.ForeignKeyConstraint(['volunteer_type_id'], ['volunteer_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_volunteer_type_profile_id'), 'volunteer_type_profile', ['id'], unique=False)
    op.create_index(op.f('ix_volunteer_type_profile_profile_id'), 'volunteer_type_profile', ['profile_id'], unique=False)
    op.create_index(op.f('ix_volunteer_type_profile_volunteer_type_id'), 'volunteer_type_profile', ['volunteer_type_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_volunteer_type_profile_volunteer_type_id'), table_name='volunteer_type_profile')
    op.drop_index(op.f('ix_volunteer_type_profile_profile_id'), table_name='volunteer_type_profile')
    op.drop_index(op.f('ix_volunteer_type_profile_id'), table_name='volunteer_type_profile')
    op.drop_table('volunteer_type_profile')
    op.drop_index(op.f('ix_volunteer_type_event_volunteer_type_id'), table_name='volunteer_type_event')
    op.drop_index(op.f('ix_volunteer_type_event_id'), table_name='volunteer_type_event')
    op.drop_index(op.f('ix_volunteer_type_event_event_id'), table_name='volunteer_type_event')
    op.drop_table('volunteer_type_event')
    op.drop_index(op.f('ix_municipal_event_municipal_id'), table_name='municipal_event')
    op.drop_index(op.f('ix_municipal_event_id'), table_name='municipal_event')
    op.drop_index(op.f('ix_municipal_event_event_id'), table_name='municipal_event')
    op.drop_table('municipal_event')
    op.drop_index(op.f('ix_mailing_start_execute_datetime'), table_name='mailing')
    op.drop_index(op.f('ix_mailing_is_executed'), table_name='mailing')
    op.drop_index(op.f('ix_mailing_id'), table_name='mailing')
    op.drop_index(op.f('ix_mailing_event_id'), table_name='mailing')
    op.drop_index(op.f('ix_mailing_end_execute_datetime'), table_name='mailing')
    op.drop_table('mailing')
    op.drop_index(op.f('ix_eco_activity_profile_profile_id'), table_name='eco_activity_profile')
    op.drop_index(op.f('ix_eco_activity_profile_id'), table_name='eco_activity_profile')
    op.drop_index(op.f('ix_eco_activity_profile_eco_activity_id'), table_name='eco_activity_profile')
    op.drop_table('eco_activity_profile')
    op.drop_index(op.f('ix_eco_activity_event_id'), table_name='eco_activity_event')
    op.drop_index(op.f('ix_eco_activity_event_event_id'), table_name='eco_activity_event')
    op.drop_index(op.f('ix_eco_activity_event_eco_activity_id'), table_name='eco_activity_event')
    op.drop_table('eco_activity_event')
    op.drop_index(op.f('ix_district_event_id'), table_name='district_event')
    op.drop_index(op.f('ix_district_event_event_id'), table_name='district_event')
    op.drop_index(op.f('ix_district_event_district_id'), table_name='district_event')
    op.drop_table('district_event')
    op.drop_index(op.f('ix_profile_user_id'), table_name='profile')
    op.drop_index(op.f('ix_profile_municipal_id'), table_name='profile')
    op.drop_index(op.f('ix_profile_is_event_organizer'), table_name='profile')
    op.drop_index(op.f('ix_profile_id'), table_name='profile')
    op.drop_table('profile')
    op.drop_index(op.f('ix_event_type'), table_name='event')
    op.drop_index(op.f('ix_event_organization_id'), table_name='event')
    op.drop_index(op.f('ix_event_name'), table_name='event')
    op.drop_index(op.f('ix_event_id'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_eco_activity_organization_organization_id'), table_name='eco_activity_organization')
    op.drop_index(op.f('ix_eco_activity_organization_id'), table_name='eco_activity_organization')
    op.drop_index(op.f('ix_eco_activity_organization_eco_activity_id'), table_name='eco_activity_organization')
    op.drop_table('eco_activity_organization')
    op.drop_index(op.f('ix_district_organization_organization_id'), table_name='district_organization')
    op.drop_index(op.f('ix_district_organization_id'), table_name='district_organization')
    op.drop_index(op.f('ix_district_organization_district_id'), table_name='district_organization')
    op.drop_table('district_organization')
    op.drop_index(op.f('ix_organization_name'), table_name='organization')
    op.drop_index(op.f('ix_organization_id'), table_name='organization')
    op.drop_index(op.f('ix_organization_creator_id'), table_name='organization')
    op.drop_table('organization')
    op.drop_index(op.f('ix_municipal_name'), table_name='municipal')
    op.drop_index(op.f('ix_municipal_id'), table_name='municipal')
    op.drop_index(op.f('ix_municipal_district_id'), table_name='municipal')
    op.drop_table('municipal')
    op.drop_index(op.f('ix_volunteer_type_name'), table_name='volunteer_type')
    op.drop_index(op.f('ix_volunteer_type_id'), table_name='volunteer_type')
    op.drop_table('volunteer_type')
    op.drop_index(op.f('ix_user_telegram_id'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_eco_activity_name'), table_name='eco_activity')
    op.drop_index(op.f('ix_eco_activity_id'), table_name='eco_activity')
    op.drop_table('eco_activity')
    op.drop_index(op.f('ix_district_name'), table_name='district')
    op.drop_index(op.f('ix_district_id'), table_name='district')
    op.drop_table('district')
    # ### end Alembic commands ###