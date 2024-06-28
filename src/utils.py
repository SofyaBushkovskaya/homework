import json
import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))
file_transaction_json = os.path.join(current_dir, "../data", "operations.json")


def financial_transactions(file_path: str) -> list:
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            operations_info = json.load(json_file)
            if isinstance(operations_info, list):
                return operations_info

            else:
                return []

    except Exception as e:
        print(f"Ошибка {e}")
        return []


print(financial_transactions(file_transaction_json))
