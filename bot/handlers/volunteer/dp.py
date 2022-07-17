from aiogram import Dispatcher

from filters.several import SeveralCallbackDataFilter
from handlers.commands import user_start
from handlers.volunteer.management import volunteer_menu, \
    volunteer_activity_menu, volunteer_filter_events_menu
from handlers.volunteer.registration import choose_district_for_volunteer, \
    choose_municipal_for_volunteer, choose_eco_activities_for_volunteer
from keyboards.inline.callback_data import cb_start, cb_volunteer_register, \
    cb_volunteer_menu
from states.management import VolunteerManagement
from states.registration import VolunteerRegister


def register_volunteer(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        choose_district_for_volunteer,
        cb_start.filter(name='register_volunteer'),
        state='*',
    )
    dp.register_callback_query_handler(
        choose_district_for_volunteer,
        SeveralCallbackDataFilter([
            cb_volunteer_register.filter(name='objects'),
            cb_volunteer_register.filter(name='page'),
        ]),
        state=VolunteerRegister.choose_district,
    )
    dp.register_callback_query_handler(
        user_start,
        cb_volunteer_register.filter(action='choose_district', name='back',
                                     value='back'),
        state=VolunteerRegister.choose_district
    )
    dp.register_callback_query_handler(
        choose_municipal_for_volunteer,
        SeveralCallbackDataFilter([
            cb_volunteer_register.filter(name='objects'),
            cb_volunteer_register.filter(name='page'),
        ]),
        state=VolunteerRegister.choose_municipal,
    )
    dp.register_callback_query_handler(
        choose_district_for_volunteer,
        cb_volunteer_register.filter(action='choose_municipal', name='back',
                                     value='back'),
        state=VolunteerRegister.choose_municipal,
    )
    dp.register_callback_query_handler(
        choose_eco_activities_for_volunteer,
        SeveralCallbackDataFilter([
            cb_volunteer_register.filter(name='objects'),
            cb_volunteer_register.filter(name='page'),
            cb_volunteer_register.filter(name='next'),
        ]),
        state=VolunteerRegister.choose_activity_type,
    )
    dp.register_callback_query_handler(
        choose_municipal_for_volunteer,
        cb_volunteer_register.filter(
            action='choose_activity',
            name='back',
            value='back',
        ),
        state=VolunteerRegister.choose_activity_type,
    )
    dp.register_callback_query_handler(
        volunteer_menu,
        cb_start.filter(name='volunteer_menu'),
        state='*',
    )
    dp.register_callback_query_handler(
        volunteer_activity_menu,
        cb_volunteer_menu.filter(name='volunteer_menu', action='eco_activity'),
        state=VolunteerManagement.menu,
    )
    dp.register_callback_query_handler(
        volunteer_menu,
        cb_volunteer_menu.filter(action='volunteer_menu', name='back',
                                 value='back'),
        state=VolunteerManagement.activity_info,
    )
    dp.register_callback_query_handler(
        volunteer_filter_events_menu,
        cb_volunteer_menu.filter(name='volunteer_menu',
                                 action='filter_my_events',
                                 ),
        state=VolunteerManagement.menu,
    )
    dp.register_callback_query_handler(
        volunteer_menu,
        cb_volunteer_menu.filter(action='volunteer_menu', name='back',
                                 value='back'),
        state=VolunteerManagement.filter_events,
    )
