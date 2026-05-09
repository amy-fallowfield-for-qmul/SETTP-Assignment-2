from abc import ABCMeta
from typing import Any, Dict, Optional, Type


class SingletonMeta(type):
    """Metaclass that turns a class into a singleton"""

    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @property
    def _instance(cls) -> Optional[Any]:
        return cls._instances.get(cls)

    @_instance.setter
    def _instance(cls, value: Optional[Any]) -> None:
        if value is None:
            cls._instances.pop(cls, None)
        else:
            cls._instances[cls] = value

    def clear_instance(cls) -> None:
        SingletonMeta._instances.pop(cls, None)


class SingletonABCMeta(SingletonMeta, ABCMeta):
    """
    Combines SingletonMeta with ABCMeta
    to allow classes to inherit from both metaclasses
    """

    pass
