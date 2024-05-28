import pytest
from src.widget import get_new_data, get_mask_account_card


def tset_get_mask_account_card() -> None:
    assert get_mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"


@pytest.mark.parametrize(
    "str_number, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_get_mask_account(str_number: str, expected: str) -> None:
    assert get_mask_account_card(str_number) == expected


def test_get_date_new() -> None:
    assert get_new_data("2018-07-11T02:26:18.671407") == "11.07.2018"


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("", ""),
        ("2018-07-11T02:26:18.67140", ""),
        ("2018-07-11T02:26:18.671407231", ""),
    ],
)
def test_get_date_new_parametrize(date_string: str, expected: str) -> None:
    assert get_new_data(date_string) == expected
