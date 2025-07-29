import os
from typing import Generic, TypeVar

T = TypeVar("T")


class Parameter(Generic[T]):
    def __init__(
        self,
        env: str,
        type_: type[T] | None = None,
        default: T | None = None,
    ) -> None:
        if type_ is not None:
            self._type: type[T] = type_
        elif default is not None:
            self._type = default.__class__
        else:
            raise TypeError("type_ или default должны быть определены")
        self._env = env
        # todo: уточнить назначение default, могут быть эффекты, когда 0/пустая строка, list/dict.
        # todo: или перейти на default_factory
        self._default = default

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object | None, owner: type) -> T:
        if instance is None:
            return self  # type: ignore[return-value]

        if self.name in instance.__dict__:
            value = instance.__dict__[self.name]
            if not isinstance(value, self._type):
                raise TypeError(
                    f"Значение '{self.name}' должно быть типа '{self._type.__name__}', "
                    f"а получено {type(value).__name__}",
                )
            return value

        env_value = os.getenv(self._env)
        if env_value is not None:
            converted = self._convert_from_str(env_value)
            instance.__dict__[self.name] = converted
            return converted

        if self._default is not None:
            instance.__dict__[self.name] = self._default
            return self._default

        raise AttributeError(
            f"Атрибут '{self.name}' не установлен, окружение '{self._env}' не задано, default отсутствует",
        )

    def __set__(self, instance: object, value: T) -> None:
        if not isinstance(value, self._type):
            raise TypeError(
                f"Значение '{self.name}' должно быть типа '{self._type.__name__}', "
                f"а получено '{type(value).__name__}'",
            )
        instance.__dict__[self.name] = value

    def _convert_from_str(self, value: str) -> T:
        if self._type is bool:
            lower = value.lower()
            if lower in ("true", "1", "yes", "on"):
                return True  # type: ignore [return-value]
            elif lower in ("false", "0", "no", "off"):
                return False  # type: ignore [return-value]
            else:
                raise ValueError(f"Невозможно преобразовать '{value}' в bool")
        try:
            return self._type(value)  # type: ignore [call-arg]
        except Exception as exc:
            raise ValueError(f"Ошибка преобразования '{value}' в {self._type}: {exc}") from None
