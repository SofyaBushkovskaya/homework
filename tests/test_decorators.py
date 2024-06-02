import os.path
from typing import Union

import pytest
from src.decorators import log


def test_log_file() -> None:
    """Тест записи в файл при успешной работе функции."""

    @log(filename="mylog.txt")
    def example_function(x: int, y: int) -> Union[int, float]:
        return x * y

    result = example_function(3, 10)
    with open(os.path.join(r"../log", "mylog.txt"), "rt") as file:
        for line in file:
            message = line

    assert message == "example_function ok. Result: 30\n"
    assert result == 30


def test_log_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест вывода в консоль при успешной работе функции."""

    @log()
    def example_function(x: int, y: int) -> Union[int, float]:
        return x * y

    result = example_function(3, 10)
    captured = capsys.readouterr()

    assert captured.out == "example_function ok. Result: 30\n"
    assert result == 30


def test_log_file_raise() -> None:
    """Тест записи в файл если произошла ошибка"""

    @log(filename="mylog.txt")
    def example_function(x: int, y: int) -> Union[int, float]:
        raise ValueError("Что то пошло не так")

    with pytest.raises(ValueError, match="Что то пошло не так"):
        example_function(3, 10)

    with open(os.path.join(r"../log", "mylog.txt"), "rt") as file:
        for line in file:
            massage = line

    assert massage == "example_function ValueError: Что то пошло не так. Inputs: (3, 10) {}\n"


def test_log_console_raise(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест вывода в консоль, если произошла ошибка."""

    @log()
    def example_function(x: int, y: int) -> Union[int, float]:
        raise ValueError("Что то пошло не так")

    with pytest.raises(ValueError, match="Что то пошло не так"):
        example_function(3, 10)

    captured = capsys.readouterr()
    assert captured.out == "example_function ValueError: Что то пошло не так. Inputs: (3, 10) {}\n"
