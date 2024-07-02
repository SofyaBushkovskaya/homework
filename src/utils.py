import json
import logging
import os.path

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
