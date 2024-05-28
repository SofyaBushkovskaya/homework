import pytest
from src.masks import get_mask_account, get_mask_card


def test_get_mask_cards(cards: str) -> None:
    assert get_mask_card("7000792289606361") == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "cards, expected",
    [
        ("", ""),
        ("700079228960636", ""),
        ("700079228960636543", ""),
    ],
)
def test_get_mask_cards_parametrize(cards: str, expected: str) -> None:
    assert get_mask_card(cards) == expected


def test_get_mask_account_check() -> None:
    assert get_mask_account("73654108430135874305") == "**4305"


@pytest.mark.parametrize(
    "account, expected",
    [
        ("", ""),
        ("7365410843013587430", ""),
        ("7365410843013587430523", ""),
    ],
)
def test_get_mask_account_parametrize(account: str, expected: str) -> None:
    assert get_mask_account(account) == expected
