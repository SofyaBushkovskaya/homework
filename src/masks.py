def get_mask_card(number: str) -> str:
    """Функция принимает номер в виде строки и возвращает замаскированную строку номера карты"""
    if len(number) > 0:
        if len(number) == 16:
            new_string = f"{number[0:4]} {number[4:6]}** **** {number[12:]}"
            return new_string
        else:
            return ""
    return ""


def get_mask_account(number: str) -> str:
    """Функция принимает номер в виде строки и возвращает замаскированную строку номера счёта"""
    if len(number) > 0:
        if len(number) == 20:
            new_string = f"**{number[-4::]}"
            return new_string
        else:
            return ""
    return ""
