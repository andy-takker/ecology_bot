from aiogram.utils.callback_data import CallbackData

PAGE = 'page'
OBJECTS = 'objects'

cb_start = CallbackData('start', 'name')
cb_organization_register = CallbackData(
    'organization_register', 'action', 'name', 'value')
cb_organization_menu = CallbackData(
    'organization_menu', 'action', 'name', 'value',
)
cb_admin_menu = CallbackData(
    'admin_menu', 'action', 'name', 'value',
)
cb_create_event = CallbackData(
    'create_event', 'action', 'name', 'value',
)
cb_volunteer_register = CallbackData(
    'volunteer_register', 'action', 'name', 'value',
)
cb_volunteer_menu = CallbackData(
    'volunteer_menu', 'action', 'name', 'value',
)