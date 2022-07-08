from database import Municipal
from keyboards.default.paginate_keyboard import get_paginate_keyboard
from keyboards.inline.callback_data import action_callback_organization_menu


def get_municipal_keyboard(municipals: list[Municipal], page=1, per_page=10):
    return get_paginate_keyboard(
        objects=municipals,
        callback_data=action_callback_organization_menu,
        action='choose_municipal',
        page=page,
        per_page=per_page,
        with_chose=False
    )
