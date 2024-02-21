from dataclasses import dataclass


@dataclass(frozen=True)
class GameURL:
    title: str
    url: str
