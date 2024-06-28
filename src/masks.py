import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename="../logs/application.log",
                    filemode='w')

logger = logging.getLogger("masks")


def get_mask_card(number: str) -> str:
    """Функция принимает номер в виде строки и возвращает замаскированную строку номера карты"""
    logger.info(f"Принимаем номер карты: {number}")
    if len(number) > 0:
        if len(number) == 16:
            new_string = f"{number[0:4]} {number[4:6]}** **** {number[12:]}"
            logger.info(f"Возвращаем маску карты: {new_string}")
            return new_string
        else:
            logger.info(f"Ошибка, возвращаем пустую строку")
            return ""
    return ""


def get_mask_account(number: str) -> str:
    """Функция принимает номер в виде строки и возвращает замаскированную строку номера счёта"""
    logger.info(f"Принимаем номер счёта: {number}")
    if len(number) > 0:
        if len(number) == 20:
            new_string = f"**{number[-4::]}"
            logger.info(f"Возвращаем маску счёта: {new_string}")
            return new_string
        else:
            logger.info(f"Ошибка, возвращаем пустую строку")
            return ""
    return ""
