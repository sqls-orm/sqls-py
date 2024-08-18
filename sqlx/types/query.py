from __future__ import annotations


class Query:
    def __init__(self):
        self._parts: list[str] = list()

    def update(self, value: str) -> Query:
        self._parts.append(value)
        return self

    def parse(self) -> str:
        return f'{' '.join(self._parts)};'
