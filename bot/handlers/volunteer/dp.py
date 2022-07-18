from aiogram import Dispatcher

from filters.several import SeveralCallbackDataFilter
from handlers.commands import user_start
from handlers.volunteer.management import volunteer_menu, \
    volunteer_activity_menu, volunteer_filter_events_menu, \
    volunteer_change_activity_menu, volunteer_change_district_menu, \
    volunteer_change_municipal_menu, volunteer_info_profile_menu, \
    volunteer_delete_profile_menu, volunteer_input_name_organizer, \
    volunteer_input_age_organizer, choose_volunteer_type_for_event
from handlers.volunteer.registration import choose_district_for_volunteer, \
    choose_municipal_for_volunteer, choose_eco_activities_for_volunteer
from keyboards.inline.callback_data import cb_start, cb_volunteer_register, \
    cb_volunteer_menu
from states.management import VolunteerManagement, VolunteerOrganizer
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
    dp.register_callback_query_handler(
        volunteer_change_activity_menu,
        cb_volunteer_menu.filter(name='volunteer_menu',
                                 action='change_activity', ),
        state=VolunteerManagement.menu,
    )
    dp.register_callback_query_handler(
        volunteer_change_activity_menu,
        SeveralCallbackDataFilter([
            cb_volunteer_menu.filter(action='choose_activity', name='objects'),
            cb_volunteer_menu.filter(action='choose_activity', name='page'),
            cb_volunteer_menu.filter(action='choose_activity', name='next'),
        ]),
        state=VolunteerManagement.change_activity,
    )
    dp.register_callback_query_handler(
        volunteer_menu,
        cb_volunteer_menu.filter(action='choose_activity', name='back',
                                 value='back'),
        state=VolunteerManagement.change_activity,
    )
    dp.register_callback_query_handler(
        volunteer_change_district_menu,
        cb_volunteer_menu.filter(name='volunteer_menu',
                                 action='change_district'),
        state=VolunteerManagement.menu,
    )
    dp.register_callback_query_handler(
        volunteer_change_district_menu,
        SeveralCallbackDataFilter([
            cb_volunteer_menu.filter(action='choose_district', name='objects'),
            cb_volunteer_menu.filter(action='choose_district', name='page'),
        ]),
        state=VolunteerManagement.change_district,
    )
    dp.register_callback_query_handler(
        user_start,
        cb_volunteer_menu.filter(action='choose_district', name='back',
                                 value='back'),
        state=VolunteerManagement.change_district
    )
    dp.register_callback_query_handler(
        volunteer_change_municipal_menu,
        SeveralCallbackDataFilter([
            cb_volunteer_menu.filter(action='choose_municipal', name='objects'),
            cb_volunteer_menu.filter(action='choose_municipal', name='page'),
        ]),
        state=VolunteerManagement.change_municipal,
    )
    dp.register_callback_query_handler(
        volunteer_change_district_menu,
        cb_volunteer_menu.filter(action='choose_municipal', name='back',
                                 value='back'),
        state=VolunteerManagement.change_municipal,
    )
    dp.register_callback_query_handler(
        volunteer_info_profile_menu,
        cb_volunteer_menu.filter(name='volunteer_menu', action='info_profile'),
        state=VolunteerManagement.menu,
    )
    dp.register_callback_query_handler(
        volunteer_delete_profile_menu,
        cb_volunteer_menu.filter(name='volunteer_menu',
                                 action='delete_profile', ),
        state=VolunteerManagement.menu,
    )
    dp.register_callback_query_handler(
        volunteer_menu,
        cb_volunteer_menu.filter(action='delete_profile', value='back',
                                 name='back'),
        state=VolunteerManagement.delete_profile,
    )
    dp.register_callback_query_handler(
        volunteer_delete_profile_menu,
        cb_volunteer_menu.filter(action='delete_profile', value='yes',
                                 name='yes'),
        state=VolunteerManagement.delete_profile,
    )
    dp.register_callback_query_handler(
        volunteer_input_name_organizer,
        cb_volunteer_menu.filter(name='volunteer_menu',
                                 action='help_event_organize'),
        state=VolunteerManagement.menu,
    )
    dp.register_callback_query_handler(
        volunteer_menu,
        cb_volunteer_menu.filter(action='input_name', value='back',
                                 name='back'),
        state=VolunteerOrganizer.input_name,
    )
    dp.register_message_handler(
        volunteer_input_name_organizer,
        state=VolunteerOrganizer.input_name,
    )
    dp.register_callback_query_handler(
        volunteer_input_name_organizer,
        cb_volunteer_menu.filter(action='input_age', value='back', name='back'),
        state=VolunteerOrganizer.input_age,
    )
    dp.register_message_handler(
        volunteer_input_age_organizer,
        state=VolunteerOrganizer.input_age,
    )
    dp.register_callback_query_handler(
        choose_volunteer_type_for_event,
        SeveralCallbackDataFilter([
            cb_volunteer_menu.filter(action='choose_volunteer_type', name='page'),
            cb_volunteer_menu.filter(action='choose_volunteer_type',
                                   name='objects'),
            cb_volunteer_menu.filter(action='choose_volunteer_type', name='next'),
        ]),
        state=VolunteerOrganizer.choose_volunteer_type,
    )