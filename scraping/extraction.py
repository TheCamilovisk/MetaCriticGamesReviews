import sys
from datetime import datetime
from requests import JSONDecodeError
from typing import List

import requests
from bs4 import BeautifulSoup

from scraping.models import GameInfo, GameReview, GameURL


def get_best_games_list(n_pages: int = 1) -> List[GameURL]:
    """Get the list of the best games of all time for the "n_pages" first pages in https://www.metacritic.com/browse/game/.  # noqa: E501

    Args:
        n_pages (int, optional): The desired number of pages to retrieve the game URLS from. Defaults to 1.

    Returns:
        List[GameURL]: _description_
    """
    base_url = "https://www.metacritic.com"
    browse_path = "/browse/games/score/metascore/all/filtered"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    game_urls = []

    for page in range(n_pages):
        url = f"{base_url}{browse_path}?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            raise requests.exceptions.HTTPError(f"Couldn't find {url}!")
        elif response.status_code == 500:
            raise requests.exceptions.ConnectionError("Internal server error!")

        soup = BeautifulSoup(response.content, "html.parser")
        game_cards = soup.find_all(
            "div", class_="c-finderProductCard c-finderProductCard-game"
        )
        for game_card in game_cards:
            anchor = game_card.find("a", class_="c-finderProductCard_container")
            if anchor:
                game_title = anchor.find(
                    "div", class_="c-finderProductCard_title"
                ).get_text(strip=True)
                game_url = base_url + anchor["href"]
                game_urls.append(
                    GameURL(
                        title=".".join(game_title.split(".")[1:]).strip(),
                        url=game_url,
                    )
                )

    return game_urls


def get_game_details(game_page_url: str) -> dict:
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
    response = requests.get(game_page_url)
    response.raise_for_status()

    if response.status_code == 404:
        raise requests.exceptions.HTTPError(f"Couldn't find {game_page_url}!")
    elif response.status_code == 500:
        raise requests.exceptions.ConnectionError("Internal server error!")

    soup = BeautifulSoup(response.content, "html.parser")

    try:
        description = soup.find(
            "div",
            class_="c-pageProductDetails_description g-outer-spacing-bottom-xlarge",
        ).text.strip()
        platforms_div = soup.find(
            "div", class_="c-gameDetails_Platforms u-flexbox u-flexbox-row"
        )
        platforms = [
            platform.text.strip() for platform in platforms_div.find("ul").findAll("li")
        ]
        release_date = (
            soup.find("div", class_="c-gameDetails_ReleaseDate u-flexbox u-flexbox-row")
            .findAll("span")[1]
            .text.strip()
        )
        developers_div = soup.find(
            "div", class_="c-gameDetails_Developer u-flexbox u-flexbox-row"
        )
        developers = [
            developer.text.strip() for developer in developers_div.find("ul").find("li")
        ]
        publishers = (
            soup.find("div", class_="c-gameDetails_Distributor u-flexbox u-flexbox-row")
            .findAll("span")[1]
            .text.strip()
        )
        genres_div = soup.find(
            "div",
            class_="c-gameDetails_sectionContainer u-flexbox u-flexbox-row u-flexbox-alignBaseline",
        )
        genres = [
            genre.text.strip()
            for genre in genres_div.findAll("span", class_="c-globalButton_label")
        ]
    except AttributeError:
        raise ValueError(
            "Failed to parse the game page. The structure of the page might have changed."
        )

    return dict(
        description=description,
        release_date=release_date,
        genres=genres,
        platforms=platforms,
        developers=developers,
        publishers=publishers,
    )


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
    response = requests.get(game_page_url)
    response.raise_for_status()

    if response.status_code == 404:
        raise requests.exceptions.HTTPError(f"Couldn't find {game_page_url}!")
    elif response.status_code == 500:
        raise requests.exceptions.ConnectionError("Internal server error!")

    soup = BeautifulSoup(response.content, "html.parser")

    try:
        title = soup.find(
            "div",
            class_="c-productHero_title g-inner-spacing-bottom-medium g-outer-spacing-top-medium",
        ).text.strip()
        critics_score = int(
            soup.find(
                "div",
                class_="c-productScoreInfo u-clearfix g-inner-spacing-bottom-medium",
            )
            .find("div", class_="c-productScoreInfo_scoreNumber u-float-right")
            .text
        )
        users_score = float(
            soup.find("div", class_="c-productScoreInfo u-clearfix")
            .find("div", "c-productScoreInfo_scoreNumber u-float-right")
            .text
        )
        critics_reviews_link = game_page_url + "/critic-reviews"
        users_reviews_link = game_page_url + "/user-reviews"

    except AttributeError:
        raise ValueError(
            "Failed to parse the game page. The structure of the page might have changed."
        )

    game_details = get_game_details(game_page_url + "/details")

    return GameInfo(
        title=title,
        url=game_page_url,
        critics_score=critics_score,
        users_score=users_score,
        critics_reviews_link=critics_reviews_link,
        users_reviews_link=users_reviews_link,
        **game_details,
    )


def get_game_reviews(game_reviews_endpoint: str) -> List[GameReview]:
    """
    Fetches and returns a list of game reviews from a specified API endpoint.

    This function contacts an API endpoint that provides game reviews in a JSON format.
    Each review is then transformed into a GameReview object. The function handles the conversion
    of date strings to datetime objects and ensures that the returned list contains only valid
    GameReview instances.

    Parameters:
        game_reviews_endpoint (str): The URL of the API endpoint where game reviews can be retrieved.

    Returns:
        List[GameReview]: A list of GameReview objects containing the data for each game review
        fetched from the API.

    Raises:
        HTTPError: If the request to the API endpoint fails or returns an error status.
        JSONDecodeError: If the response from the API cannot be decoded as JSON.
        ValueError: If data from the API does not conform to the expected structure or types.
    """
    try:
        response = requests.get(game_reviews_endpoint)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.exceptions.HTTPError as e:
        raise requests.HTTPError(f"HTTP error occurred: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

    reviews_json = response.json()

    game_reviews = []
    for review_data in reviews_json:
        try:
            # Ensure all data is correctly typed
            username = str(review_data["username"])
            date = datetime.strptime(review_data["date"], "%Y-%m-%d")
            score = int(review_data["score"])
            quote = str(review_data["quote"])
            review_platform = str(review_data["review_platform"])

            game_reviews.append(
                GameReview(username, date, score, quote, review_platform)
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error processing review data: {e}")

    return game_reviews
