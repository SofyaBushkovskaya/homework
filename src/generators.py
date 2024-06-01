from typing import Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[dict]:
    """Функция принимает список словарей (или объект-генератор) с банковскими операциями и возвращает итератор,
    который выдаёт по очереди операции, в которых указана заданная валюта."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator:
    """Функция принимает список словарей (или объект-генератор) с банковскими операциями и возвращает генератор,
    который выдает описание каждой операции по очереди."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Generator:
    """Генератор номеров банковских карт в формате ХХХХ ХХХХ ХХХХ ХХХХ
    Диапазоны передаются как параметры генератора."""
    for num in range(start, stop + 1):
        number = "0" * (16 - len(str(num))) + str(num)

        string_to_return = ""
        block_counter = 0

        for digit in number:
            block_counter += 1
            if block_counter <= 4:
                string_to_return += digit
            else:
                string_to_return += " " + digit
                block_counter = 1

        yield string_to_return
