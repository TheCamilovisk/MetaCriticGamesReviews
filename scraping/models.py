from dataclasses import dataclass


@dataclass(frozen=True)
class GameURL:
    """Model to represent the mapping between a game title and it's page URL.
    """
    title: str
    url: str
