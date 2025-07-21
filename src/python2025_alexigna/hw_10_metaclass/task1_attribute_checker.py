from typing import Any


class AttributeCheckerMeta(type):
    def __init__(cls, name: str, bases: tuple[type, ...], attributes: dict[str, Any]) -> None:
        if len(bases) == 0:
            super().__init__(name, bases, attributes)
            return

        required_attrs = getattr(cls, "required_attributes", [])

        for attr in required_attrs:
            if not hasattr(cls, attr):
                raise TypeError(f"В классе '{name}' отсутствует атрибут '{attr}'")

        super().__init__(name, bases, attributes)


class PluginBase(metaclass=AttributeCheckerMeta):
    required_attributes = ["name", "version"]


class Plugin(PluginBase):
    name = "MyPlugin"
    version = "1.0"


class BrokenPlugin(PluginBase):
    name = "MyOtherPlugin"
