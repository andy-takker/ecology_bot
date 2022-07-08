from aiogram.dispatcher.filters.state import State, StatesGroup


class VolunteerRegistration(StatesGroup):
    enter_name = State()
    choosing_region = State()
    choosing_municipal_area = State()
    choosing_activity_type = State()


class OrganizationRegistration(StatesGroup):
    start = State()
    choosing_activities = State()
    choosing_districts = State()
    enter_name = State()
    moderating = State()


