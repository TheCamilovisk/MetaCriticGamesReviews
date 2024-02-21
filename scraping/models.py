from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class GameURL:
    """Model to represent the mapping between a game title and it's page URL."""

    title: str
    url: str


@dataclass(frozen=True)
class GameInfo:
    """
    A dataclass for storing detailed information about a video game.

    Attributes:
        title (str): The title of the game.
        url (str): The URL of the game's specific page on Metacritic.
        description (str): A brief description of the game.
        release_date (str): The first release date of the game.
        genres (List[str]): A list of genres the game belongs to.
        platforms (List[str]): A list of platforms the game is available on.
        developers (List[str]): A list of developers who made the game.
        publishers (List[str]): A list of publishers who published the game.
        critics_score (int): The aggregate score given by critics.
        users_score (float): The average score given by users.
        critics_reviews_link (str): The URL to the critics' reviews page.
        users_reviews_link (str): The URL to the users' reviews page.
    """

    title: str
    url: str
    description: str
    release_date: str
    genres: List[str]
    platforms: List[str]
    developers: List[str]
    publishers: List[str]
    critics_score: int
    users_score: float
    critics_reviews_link: str
    users_reviews_link: str


@dataclass(frozen=True)
class GameReview:
    """
    Represents a game review.

    Attributes:
        username (str): The username of the individual who submitted the review.
        date (datetime): The date when the review was posted. Expected to be a datetime object.
        score (int): The score given to the game by the reviewer, typically on a scale from 0 to 10.
        quote (str): The text of the review submitted by the user.
        review_platform (str): The platform for which the review was written (e.g., PC, PS4, Xbox One).
    """

    username: str
    date: datetime
    score: int
    quote: str
    review_platform: str
