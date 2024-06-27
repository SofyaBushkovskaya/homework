import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import requests
from dotenv import load_dotenv
from src.external_api import currency_conversion

load_dotenv(".env")

API_KEY = os.getenv("API_KEY")


class TestConvertToRub(unittest.TestCase):

    def test_convert_rub_to_rub(self) -> None:
        transaction = {"operationAmount": {"amount": 100, "currency": {"code": "RUB"}}}

        result = currency_conversion(transaction)
        self.assertEqual(result, 100)

    def test_convert_other_currency_to_rub(self) -> None:
        transaction = {"operationAmount": {"amount": 100, "currency": {"code": "GBP"}}}

        result = currency_conversion(transaction)
        self.assertEqual(result, 0.0)

    @patch("requests.get")
    def test_api_failure(self, mock_get: MagicMock) -> None:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException(response=mock_response)
        mock_get.return_value = mock_response

        transaction = {"operationAmount": {"amount": 1, "currency": {"code": "USD"}}}

        result = currency_conversion(transaction)
        self.assertEqual(result, 0.0)
