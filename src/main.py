import datetime
import os
from typing import Any

import pandas as pd
from src.processing import filter_by_state, sort_by_date
from src.utils import (
    financial_transactions,
    get_transactions_filter_by_key,
    get_transactions_filter_by_rub,
    get_transactions_filter_by_rub_csv,
    get_transactions_filter_by_rub_xlsx,
    get_transactions_info_csv,
    get_transactions_info_excel,
)
from src.widget import get_mask_account_card


def main() -> Any:
    """Функция,которая отвечает за основную логику проекта и связывает функциональности между собой."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("Введите номер пункта: ")

        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "../data", "operations.json")
            transactions = financial_transactions(file_path)
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "../data", "transactions.csv")
            transactions = get_transactions_info_csv(file_path)
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "../data", "transactions_excel.xlsx")
            transactions = get_transactions_info_excel(file_path)
            break

        else:
            print("Некорректный выбор. Попробуйте еще раз.")
            continue
    while True:
        choice = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING:\n"
        )
        if choice.upper() == "CANCELED":
            transactions_state = filter_by_state(transactions, "CANCELED")

            break
        elif choice.upper() == "PENDING":
            transactions_state = filter_by_state(transactions, "PENDING")

            break
        elif choice.upper() == "EXECUTED":
            transactions_state = filter_by_state(transactions)
            break
        else:
            print("Некорректный выбор. Попробуйте еще раз.")
            continue
    while True:
        user_input = input("Отсортировать операции по дате?  Да/Нет\n").lower()
        if user_input == "да":
            if (
                input("Отсортировать по возрастанию или по убыванию?  по возрастанию/по убыванию\n").lower()
                == "по возрастанию"
            ):
                transactions = sort_by_date(transactions_state, False)
                break

            else:
                transactions = sort_by_date(transactions_state)
                break
        elif user_input == "нет":
            break
        else:
            print("Некорректный выбор. Попробуйте еще раз.")
            continue
    while True:
        user_input = input("Выводить только рублевые тразакции? Да/Нет\n").lower()
        if user_input == "да":
            if file_path.endswith(".json"):
                transactions = get_transactions_filter_by_rub(transactions, "RUB")
            elif file_path.endswith(".csv"):
                transactions = get_transactions_filter_by_rub_csv(transactions, "RUB")
            elif file_path.endswith(".xlsx"):
                transactions = get_transactions_filter_by_rub_xlsx(transactions, "RUB")
            break
        elif user_input == "нет":
            break
        else:
            print("Некорректный выбор. Попробуйте еще раз.")
            continue
    while True:
        user_input = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет:\n").lower()
        if user_input == "да":
            search_key = input("Видите слово для поиска: ")
            transactions = get_transactions_filter_by_key(transactions, search_key)
            break
        elif user_input == "нет":
            break
        else:
            print("Некорректный выбор. Попробуйте еще раз.")
            continue
    if transactions == []:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    elif len(transactions) > 0:
        print(f"Всего банковских операций в выборке: {len(transactions)}")

    for transaction in transactions:
        date = datetime.datetime.fromisoformat(transaction["date"]).strftime("%d.%m.%Y")
        if (
            file_path.endswith(".json")
            and "from" in transaction
            and (pd.notnull(transaction["from"]) or transaction["from"] != "")
        ):
            from_ = get_mask_account_card(transaction["from"])
        elif file_path.endswith(".xlsx") and "from" in transaction and pd.notnull(transaction["from"]):
            from_ = get_mask_account_card(transaction["from"])
        elif file_path.endswith(".csv") and "from" in transaction and transaction["from"] != "":
            from_ = get_mask_account_card(transaction["from"])
        else:
            from_ = "0"
        to_ = get_mask_account_card(transaction["to"])
        description = transaction["description"]
        if file_path.endswith(".json"):
            amount = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["name"]
        elif file_path.endswith(".csv") or file_path.endswith(".xlsx"):
            amount = transaction["amount"]
            currency = transaction["currency_name"]

        print("Распечатываю итоговый список транзакций...")
        print(f"{date} {description}\n{from_} -> {to_}\nСумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
