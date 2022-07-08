from aiogram.utils.callback_data import CallbackData

action_callback_start = CallbackData('start', 'name')
action_callback_organization_register = CallbackData(
    'organization_register', 'action', 'name', 'value')
action_callback_organization_menu = CallbackData(
    'organization_menu', 'action', 'name', 'value',
)
action_callback_admin_menu = CallbackData(
    'admin_menu', 'action', 'name', 'value',
)