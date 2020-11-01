import re

from typing import Union
from typing import Dict
from typing import Optional
from typing import Any


RE_VALIDATE_KEY = re.compile(r'^([0-9]+|[_a-zA-Z][0-9a-zA-Z_]*)(\.([0-9]+|[_a-zA-Z][0-9a-zA-Z_]*))*$')


class Option:
    def __init__(self, value: Any = None, type_: type = None) -> None:
        self._type = type_ if type_ is not None else type(value) if value is not None else None

        if value is None:
            self._value = None
        else:
            self.value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value):
        if self._type is not None and not isinstance(value, self._type):
            try:
                value = self._type(value)
            except BaseException:
                raise TypeError(f'Value {repr(value)} not of type {self._type}')
        self._value = value

    @property
    def type(self) -> Optional[type]:
        return self._type


OptionOrConfigManagerType = Union[Option, 'ConfigManager']


class ConfigManager:
    NAMESPACE_SEPARATOR = '.'

    def __init__(self):
        self.__values: Dict[str, OptionOrConfigManagerType] = dict()

    def __get_attr(self, key):
        if key not in self.__values:
            raise AttributeError(f"Invalid attribute '{key}'")

        return self.__values[key]

    def __call__(self, key: str, value: Any = None, type_: type = None) -> OptionOrConfigManagerType:
        assert RE_VALIDATE_KEY.match(key), f"Invalid key '{key}'"

        key, *rest = key.split(self.NAMESPACE_SEPARATOR, 1)
        if not rest:
            self.__values[key] = Option(value=value, type_=type_)
        else:
            obj = self.__values.get(key, ConfigManager())
            assert isinstance(obj, ConfigManager)
            self.__values[key] = obj(rest[0], value=value, type_=type_)

        return self

    def __getattr__(self, item: str) -> OptionOrConfigManagerType:
        if item.startswith(f'_{self.__class__.__name__}__'):
            return self.__dict__.get(item, self.__class__.__dict__.get(item))

        result = self.__get_attr(item)
        return result.value if isinstance(result, Option) else result

    def __setattr__(self, name, value):
        if name.startswith(f'_{self.__class__.__name__}__'):
            self.__dict__[name] = value
            return

        result = self.__get_attr(name)
        if isinstance(result, Option):
            result.value = value
        else:
            raise AttributeError(f"Cannot override inner attribute '{name}'. Delete it first")

    def __delattr__(self, key):
        if key not in self.__values:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")

        del self.__values[key]

    def __getitem__(self, item) -> OptionOrConfigManagerType:
        key, *rest = item.split(self.NAMESPACE_SEPARATOR, 1)
        if not rest:
            result = self.__values[key]
            return result.value if isinstance(result, Option) else result

        return self.__values[key][rest[0]]

    def __setitem__(self, item, value):
        key, *rest = item.split(self.NAMESPACE_SEPARATOR, 1)
        if not rest:
            self.__values[key].value = value
            return

        self.__values[key][rest[0]] = value

    def __delitem__(self, item):
        key, *rest = item.split(self.NAMESPACE_SEPARATOR, 1)
        if not rest:
            del self.__values[key]
            return

        del self.__values[key][rest[0]]
