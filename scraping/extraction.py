from typing import List

import requests

from scraping.models import GameURL


def get_best_games_list(n_pages: int = 1) -> List[GameURL]:
    """Get the list of the best games of all time for the "n_pages" first pages in https://www.metacritic.com/browse/game/.  # noqa: E501

    Each page contains a list of at most 24 games. So, if we want to get the list for 4 pages, we'll have 96 game URLS.

    Args:
        n_pages (int, optional): The desired number of pages to retrieve the game URLS from. If < 0, all pages will be scraped. Defaults to 1.

    Returns:
        List[GameURL]: _description_
    """
    return []
