import typing
from aiogram import types
from aiogram.dispatcher.filters import AbstractFilter
from aiogram.utils.callback_data import CallbackDataFilter


class SeveralCallbackDataFilter(AbstractFilter):
    def __init__(self, filters: list[CallbackDataFilter]):
        self.filters = filters

    @classmethod
    def validate(cls, full_config: typing.Dict[str, typing.Any]):
        raise ValueError("That filter can't be used in filters factory!")

    async def check(self, query: types.CallbackQuery):
        data = {}
        for f in self.filters:
            try:
                data.update(f.factory.parse(query.data))
            except ValueError:
                pass
        if not data:
            return False
        for f in self.filters:
            for key, value in f.config.items():
                if isinstance(value, (list, tuple, set, frozenset)):
                    if data.get(key) not in value:
                        break
                elif data.get(key) != value:
                    break
            else:
                return {'callback_data': data}
        return False
