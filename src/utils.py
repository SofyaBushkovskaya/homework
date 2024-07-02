import json
import logging
import os.path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="../logs/application.log",
    filemode="w",
)

logger = logging.getLogger("utils")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_transaction_json = os.path.join(current_dir, "../data", "operations.json")


def financial_transactions(file_path: str) -> list:
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            operations_info = json.load(json_file)
            if isinstance(operations_info, list):
                logger.info("Возвращаем список словарей")
                return operations_info
            else:
                logger.info("Файл пустой, содержит не список или не найден")
                return []

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        print(f"Ошибка {e}")
        return []


print(financial_transactions(file_transaction_json))


def get_transactions_info_csv(path_to_csv):
    """Функция принимает путь до файла CSV и возвращает данные транзакций"""
    with open(path_to_csv, "r") as file:
        data = pd.read_csv(file)
        data_ = data.to_dict()
        return data_


def get_transactions_info_excel(path_to_xlsx):
    """Функция принимает путь до файла XLSX и возвращает данные транзакций"""
    with open(path_to_xlsx, "rb") as file:
        data = pd.read_excel(file)
        data_ = data.to_dict()
        return data_
