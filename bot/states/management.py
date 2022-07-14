from aiogram.dispatcher.filters.state import StatesGroup, State


class OrganizationManagement(StatesGroup):
    menu = State()
    choose_municipal = State()
