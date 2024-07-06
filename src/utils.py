import csv
import json
import logging
import os.path
import re
from collections import Counter

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


# print(financial_transactions(file_transaction_json))


def get_transactions_info_csv(path_to_csv):
    """Функция принимает путь до файла CSV и возвращает данные транзакций"""
    data_list = []
    with open(path_to_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            data_list.append(row)
    return data_list


def get_transactions_info_excel(path_to_xlsx):
    """Функция принимает путь до файла XLSX и возвращает данные транзакций"""
    with open(path_to_xlsx, "rb") as file:
        data = pd.read_excel(file)
        data_ = data.to_dict("records")
        return data_


def get_transactions_by_category(transactions, categories):
    """
    Принимает список словарей с данными о банковских операциях и список категорий операций,
    возвращает словарь, в котором ключи — это названия категорий, а значения — это количество
    операций в каждой категории.
    """
    descriptions = [
        transaction["description"]
        for transaction in transactions
        if "description" in transaction and transaction["description"] in categories
    ]
    category_counts = dict(Counter(descriptions))

    return category_counts


# categories = ["Открытие вклада", "Перевод с карты на карту", "Перевод организации"]
# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, "../data", "transactions_excel.xlsx")
# transactions = get_transactions_info_excel(file_path)
# filter_transaction = get_transactions_by_category(transactions, categories)
# print(filter_transaction)


def get_transactions_filter_by_rub(transactions: list, search_key: str) -> list:
    """Функция фильтрации транзакций по коду валюты"""
    result = []
    for transaction in transactions:
        if (
            "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and re.search(search_key, transaction["operationAmount"]["currency"]["code"], re.IGNORECASE)
        ):
            result.append(transaction)
    return result


def get_transactions_filter_by_rub_csv(transactions: list, search_code: str) -> list:
    """Функция фильтрации транзакций по коду валюты"""
    result = []
    for transaction in transactions:
        if "currency_code" in transaction and re.search(search_code, transaction["currency_code"], re.IGNORECASE):
            result.append(transaction)
    return result


def get_transactions_filter_by_rub_xlsx(transactions: list, search_code: str) -> list:
    """Функция фильтрации транзакций по коду валюты"""
    result = []
    for transaction in transactions:
        if pd.notnull(transaction["currency_code"]) and re.search(
            search_code, transaction["currency_code"], re.IGNORECASE
        ):
            result.append(transaction)
    return result


def get_transactions_filter_by_key(transactions: list, search_key: str) -> list:
    """Функцию, которая принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращать список словарей"""
    result = []
    for transaction in transactions:
        if "description" in transaction and re.search(search_key, transaction["description"], re.IGNORECASE):
            result.append(transaction)
    return result
