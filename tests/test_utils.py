import json
import unittest
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
from src.utils import financial_transactions, get_transactions_info_csv, get_transactions_info_excel


class TestGetTransactions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"transaction": "data1"}, {"transaction": "data2"}]')
    def test_financial_transactions_valid_file(self, mock_file: MagicMock) -> None:
        expected_data = [{"transaction": "data1"}, {"transaction": "data2"}]
        result = financial_transactions("fake_path.json")
        self.assertEqual(result, expected_data)
        mock_file.assert_called_once_with("fake_path.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_get_transactions_invalid_content(self, mock_file: MagicMock) -> None:
        result = financial_transactions("fake_path.json")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("fake_path.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_get_transactions_empty_file(self, mock_file: MagicMock) -> None:
        result = financial_transactions("fake_path.json")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("fake_path.json", "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_transactions_file_not_found(self, mock_file: MagicMock) -> None:
        result = financial_transactions("fake_path.json")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("fake_path.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='{"transaction": "data"}')
    @patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_get_transactions_json_decode_error(self, mock_json_load: MagicMock, mock_file: MagicMock) -> None:
        result = financial_transactions("fake_path.json")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("fake_path.json", "r", encoding="utf-8")
        mock_json_load.assert_called_once()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"id": "1", "amount": "100"}, {"id": "2", "amount": "200"}]',
    )
    def test_get_transactions_json(self, mock_file: MagicMock) -> None:
        result = financial_transactions("test.json")
        self.assertEqual(result, [{"id": "1", "amount": "100"}, {"id": "2", "amount": "200"}])


class TestGetTransactionsCSV(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "4699552;EXECUTED;2022-03-23T08:29:37Z;23423;Peso;PHP;Discover 7269000803370165;"
        "American Express 1963030970727681;Перевод с карты на карту\n",
    )
    def test_get_transactions_info_csv(self, mock_file: MagicMock) -> None:
        result = get_transactions_info_csv("test.csv")
        self.assertEqual(
            result,
            {
                "id;state;date;amount;currency_name;currency_code;from;to;description": {
                    0: "4699552;EXECUTED;2022-03-23T08:29:37Z;23423;Peso;PHP;Discover "
                    "7269000803370165;American "
                    "Express "
                    "1963030970727681;Перевод "
                    "с "
                    "карты "
                    "на "
                    "карту"
                }
            },
        )


class GetTransactionsInfoExcel(unittest.TestCase):
    data = {
        "id": [4699552.0],
        "state": ["EXECUTED"],
        "date": ["2022-03-23T08:29:37Z"],
        "amount": [23423.0],
        "currency_name": ["Peso"],
        "currency_code": ["PHP"],
        "from": ["Discover 7269000803370165"],
        "to": ["American Express 1963030970727681"],
        "description": ["Перевод с карты на карту"],
    }

    df = pd.DataFrame(data)

    df.to_excel("test.xlsx", index=False)

    @patch("pandas.read_excel", return_value=df)
    def test_get_transactions_info_xlsx(self, mock_read_excel: MagicMock) -> None:
        result = get_transactions_info_excel("test.xlsx")
        self.assertEqual(
            result,
            {
                "amount": {0: 23423.0},
                "currency_code": {0: "PHP"},
                "currency_name": {0: "Peso"},
                "date": {0: "2022-03-23T08:29:37Z"},
                "description": {0: "Перевод с карты на карту"},
                "from": {0: "Discover 7269000803370165"},
                "id": {0: 4699552.0},
                "state": {0: "EXECUTED"},
                "to": {0: "American Express 1963030970727681"},
            },
        )
