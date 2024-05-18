from src.masks import get_mask_account, get_mask_card


def get_mask_account_card(number: str) -> str:
    """Функция принимает строки и маскирует номер карты или счёта"""
    if len(number) > 0:
        if len(number.split()[-1]) == 16:
            new_number = get_mask_card(number.split()[-1])
            result = f"{number[:-16]}{new_number}"
            return result
        elif len(number.split()[-1]) == 20:
            new_number = get_mask_account(number.split()[-1])
            result = f"{number[:-20]}{new_number}"
            return result
    return ""


def get_new_data(old_data: str) -> str:
    """Функция принимает строку с датой и форматирует её"""
    if len(old_data) > 0:
        if len(old_data) == 26:
            result = old_data[:10].split("-")
            new_data = ".".join(result[::-1])
            return new_data
        else:
            return ""
    return ""
