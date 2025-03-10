from typing import Any


class Row(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = Row(v)

    def __getattr__(self, item: str) -> Any:
        if item in self:
            return self[item]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

    def __getattribute__(self, item: str) -> Any:
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self.__getattr__(item)

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value
