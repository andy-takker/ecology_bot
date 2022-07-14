from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateEvent(StatesGroup):
    choose_district = State()
    choose_municipal = State()
    choose_type = State()
    choose_volunteer_type = State()
    set_volunteer_description = State()
    confirm_volunteer = State()
    choose_activity = State()
    set_name = State()
    set_description = State()
    confirm = State()
