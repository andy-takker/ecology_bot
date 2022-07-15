from aiogram.dispatcher.filters.state import State, StatesGroup


class VolunteerRegister(StatesGroup):
    choose_district = State()
    choose_municipal = State()
    enter_name = State()
    choose_activity_type = State()


class OrganizationRegistration(StatesGroup):
    choosing_activities = State()
    choosing_districts = State()
    enter_name = State()
    moderating = State()


