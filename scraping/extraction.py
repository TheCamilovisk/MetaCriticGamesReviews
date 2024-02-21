from typing import List

import requests

from scraping.models import GameInfo, GameURL


def get_best_games_list(n_pages: int = 1) -> List[GameURL]:
    """Get the list of the best games of all time for the "n_pages" first pages in https://www.metacritic.com/browse/game/.  # noqa: E501

    Args:
        n_pages (int, optional): The desired number of pages to retrieve the game URLS from. If < 0, all pages will be scraped. Defaults to 1.

    Returns:
        List[GameURL]: _description_
    """
    return []


def get_game_info(game_page_url: str) -> GameInfo:
    """
    Extracts and returns detailed information about a video game from its Metacritic page.

    This function takes the URL of a game's page on Metacritic and scrapes the page to collect
    essential details about the game, such as its title, description, release date, genres,
    platforms, developers, publishers, critic and user scores, and links to reviews.

    Args:
        game_page_url (str): The URL of the game's specific page on Metacritic.

    Returns:
        GameInfo: An instance of the GameInfo dataclass containing the extracted information.

    Raises:
        ValueError: If the game_page_url is not a valid Metacritic game page URL or data cannot be extracted.
        RequestException: If there's a problem with the network request to the Metacritic page.
        ParsingException: If there's an error parsing the page content (optional, depends on implementation).

    Note:
        This function requires internet access to fetch the page content and might be subject to
        Metacritic's terms of use and rate limiting. Ensure compliance with Metacritic's policies
        when using this function.
    """
    return None
