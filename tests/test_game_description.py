import os
import unittest
from unittest.mock import MagicMock, patch

from scraping.extraction import get_game_info
from scraping.models import GameInfo
from tests.utils import get_resources_path, read_file


class TestGetGameInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.resources_path = get_resources_path(__file__)
        # Setup mock HTML content for different scenarios
        mock_valid_game_path = os.path.join(
            self.resources_path, "mock_valid_game_basic_info_page.html"
        )
        self.valid_game_html = read_file(mock_valid_game_path)
        mock_missing_game_path = os.path.join(
            self.resources_path, "mock_missing_game_page.html"
        )
        self.missing_game_html = read_file(mock_missing_game_path)
        mock_incomplete_game_path = os.path.join(
            self.resources_path, "mock_incomplete_game_page.html"
        )
        self.incomplete_game_html = read_file(mock_incomplete_game_path)

    @patch("scraping.extraction.requests.get")
    def test_valid_game_page(self, mock_get: MagicMock) -> None:
        """Test extracting info from a valid game page URL."""
        mock_get.return_value = MagicMock(status_code=200, text=self.valid_game_html)
        game_info = get_game_info("https://www.notmetacritic.com/game/valid-game")
        self.assertIsNotNone(game_info)
        self.assertIsInstance(game_info, GameInfo)

    @patch("scraping.extraction.requests.get")
    def test_invalid_url_format(self, mock_get: MagicMock) -> None:
        """Test handling of invalid URL format."""
        with self.assertRaises(ValueError):
            get_game_info("https://www.notmetacritic.com/game/invalid-url")

    @patch("scraping.extraction.requests.get")
    def test_non_existent_game_page(self, mock_get: MagicMock) -> None:
        """Test handling of non-existent game page URL."""
        mock_get.return_value = MagicMock(status_code=404, text=self.missing_game_html)
        with self.assertRaises(ValueError):
            get_game_info("https://www.notmetacritic.com/game/non-existent-game")

    @patch("scraping.extraction.requests.get")
    def test_empty_or_incomplete_game_page(self, mock_get: MagicMock) -> None:
        """Test handling of empty or incomplete game page."""
        mock_get.return_value = MagicMock(
            status_code=200, text=self.incomplete_game_html
        )
        with self.assertRaises(ValueError):
            get_game_info("https://www.notmetacritic.com/game/incomplete-game")
