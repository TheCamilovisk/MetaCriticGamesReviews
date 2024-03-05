import json
import os
import unittest
from copy import deepcopy
from unittest.mock import MagicMock, patch

from scraping.extraction import get_game_reviews
from tests.utils import get_resources_path


class TestGameReviews(unittest.TestCase):
    """
    Test suite for the `get_game_reviews` function.
    """

    def setUp(self) -> None:
        self.resources_path = get_resources_path(__file__)
        # Setup mock output for different scenarios
        mock_valid_response_path = os.path.join(
            self.resources_path, "mock_valid_response.jsonl"
        )
        with open(mock_valid_response_path, "r") as file:
            self.valid_response = json.load(file)
        self.single_response = deepcopy(self.valid_response)
        self.single_response["data"]["items"] = [self.single_response["data"]["items"][0]]

        self.valid_endpoint = "http://example.com/reviews"
        self.invalid_endpoint = "http://invalidurl.com"

    @patch("scraping.extraction.requests.get")
    def test_valid_response(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with a valid response containing multiple reviews.
        """
        mock_get.return_value.json = MagicMock(return_value=self.valid_response)
        result = [items for items in get_game_reviews(self.valid_endpoint)]
        self.assertEqual(len(result), 2, "Expected two reviews in the result")

    @patch("scraping.extraction.requests.get")
    def test_single_review_response(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with a response containing a single review.
        """
        print(self.single_response)
        mock_get.return_value.json = MagicMock(return_value=self.single_response)
        result = [items for items in get_game_reviews(self.valid_endpoint)]
        self.assertEqual(len(result), 1, "Expected a single review in the result")

    @patch("scraping.extraction.requests.get")
    def test_invalid_url(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with an invalid URL.
        """
        mock_get.side_effect = Exception
        with self.assertRaises(Exception):
            list(get_game_reviews(self.invalid_endpoint))

    @patch("scraping.extraction.requests.get")
    def test_invalid_json(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with an invalid JSON response.
        """
        mock_get.return_value.json = MagicMock(side_effect=ValueError("Invalid JSON"))
        with self.assertRaises(ValueError):
            list(get_game_reviews(self.valid_endpoint))

    @patch("scraping.extraction.requests.get")
    def test_unexpected_json_structure(self, mock_get: MagicMock) -> None:
        """
        Test fetching game reviews with an unexpected JSON structure.
        """
        mock_get.return_value.json = MagicMock(return_value=[{"unexpected": "structure"}])
        with self.assertRaises(ValueError):
            list(get_game_reviews(self.valid_endpoint))


if __name__ == "__main__":
    unittest.main()
