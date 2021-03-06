from aiogram.dispatcher.filters.state import StatesGroup, State


class OrganizationManagement(StatesGroup):
    menu = State()
    choose_municipal = State()


class VolunteerManagement(StatesGroup):
    menu = State()
    activity_info = State()
    filter_events = State()
    change_activity = State()
    change_district = State()
    change_municipal = State()
    delete_profile = State()


class VolunteerOrganizer(StatesGroup):
    input_name = State()
    input_age = State()
    choose_volunteer_type = State()
