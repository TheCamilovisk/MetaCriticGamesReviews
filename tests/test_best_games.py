import os
import unittest
from unittest.mock import MagicMock, patch

from scraping.extraction import get_best_games_list
from scraping.models import GameURL
from tests.utils import get_resources_path, read_file


class TestBestGames(unittest.TestCase):
    def setUp(self) -> None:
        self.resources_path = get_resources_path(__file__)

        mock_page_path = os.path.join(self.resources_path, "mock_page.html")
        self.mock_page_html = read_file(mock_page_path)

    """
    Unit tests for the `get_best_games_list` function in the `scraping` module.
    """

    @patch("scraping.extraction.requests.get")
    def test_get_games_list_success(self, mock_get: MagicMock) -> None:
        """
        Tests successful extraction of games listing (hrefs) from a mocked webpage.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = self.mock_page_html

        expected_links = [
            GameURL("Game 1", "https://example.com/game1"),
            GameURL("Game 2", "https://example.com/game2"),
        ]
        links = get_best_games_list()

        self.assertEqual(links, expected_links)
