from aiogram.dispatcher.filters.state import StatesGroup, State


class OrganizationManagement(StatesGroup):
    menu = State()
    choose_municipal = State()


class VolunteerManagement(StatesGroup):
    menu = State()
    activity_info = State()
    change_activity = State()
    change_district = State()
    change_municipal = State()
