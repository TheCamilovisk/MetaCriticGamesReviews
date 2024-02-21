import os
import unittest
from unittest.mock import MagicMock, patch

import requests

from scraping.extraction import get_game_reviews
from tests.utils import get_resources_path, read_jsonlines_file


class TestGameReviews(unittest.TestCase):
    """
    Test suite for the `get_game_reviews` function.
    """

    def setUp(self) -> None:
        self.resources_path = get_resources_path
        # Setup mock output for different scenarios
        mock_valid_response_path = os.path.join(
            self.resources_path, "mock_valid_response.jsonl"
        )
        self.valid_response = read_jsonlines_file(mock_valid_response_path)

        self.valid_endpoint = "http://example.com/reviews"
        self.invalid_endpoint = "http://invalidurl.com"

    @patch("scraping.extraction.requests.get")
    def test_valid_response(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with a valid response containing multiple reviews.
        """
        mock_get.return_value.json = MagicMock(return_value=self.valid_response)
        result = get_game_reviews(self.valid_endpoint)
        self.assertEqual(len(result), 2, "Expected two reviews in the result")

    @patch("scraping.extraction.requests.get")
    def test_empty_response(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with an empty response.
        """
        mock_get.return_value.json = MagicMock(return_value=[])
        result = get_game_reviews(self.valid_endpoint)
        self.assertEqual(len(result), 0, "Expected an empty result list")

    @patch("scraping.extraction.requests.get")
    def test_single_review_response(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with a response containing a single review.
        """
        mock_get.return_value.json = MagicMock(return_value=[self.valid_response[0]])
        result = get_game_reviews(self.valid_endpoint)
        self.assertEqual(len(result), 1, "Expected a single review in the result")

    @patch("scraping.extraction.requests.get")
    def test_invalid_url(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with an invalid URL.
        """
        mock_get.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(requests.exceptions.ConnectionError):
            get_game_reviews(self.invalid_endpoint)

    @patch("scraping.extraction.requests.get")
    def test_invalid_json(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with an invalid JSON response.
        """
        mock_get.return_value.json = MagicMock(side_effect=ValueError("Invalid JSON"))
        with self.assertRaises(ValueError):
            get_game_reviews(self.valid_endpoint)

    @patch("scraping.extraction.requests.get")
    def test_unexpected_json_structure(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with an unexpected JSON structure.
        """
        mock_get.return_value.json = MagicMock(return_value={"unexpected": "structure"})
        with self.assertRaises(ValueError):
            get_game_reviews(self.valid_endpoint)


if __name__ == "__main__":
    unittest.main()
