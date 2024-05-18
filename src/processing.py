def filter_by_state(transactions: list, state: str = "EXECUTED") -> list:
    """Функция принимает на вход список словарей и значение для ключа 'state'
        (опциональный параметр со значением по умолчанию 'EXECUTED') и возвращает
        новый список, содержащий только те словари, у которых ключ 'state' содержит
        переданное в функцию значение."""
    filter_transactions = []
    for transaction in transactions:
        if transaction.get("state") == state:
            filter_transactions.append(transaction)
    return filter_transactions
