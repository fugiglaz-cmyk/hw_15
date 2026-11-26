"""Робота з папками."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def DirectoryContextManager(path: str) -> Iterator[None]:
    """Тимчасово переходить в іншу папку.

    Після роботи повертає попередню папку, навіть якщо була помилка.

    Args:
        path: Папка, в яку треба перейти.

    Yields:
        Нічого (None).

    Raises:
        FileNotFoundError: Папку не знайдено.
        NotADirectoryError: Це не папка.
        PermissionError: Немає дозволу.
    """
    previous_directory = os.getcwd()
    os.chdir(path)
    try:
        print(f"Поточна папка: {os.getcwd()}")
        yield
    finally:
        os.chdir(previous_directory)
        print(f"Повернулися в папку: {os.getcwd()}")


def create(dir_name: str) -> None:
    """Створює нову папку.

    Args:
        dir_name: Назва папки.

    Raises:
        FileExistsError: Така папка або файл уже існує.
    """
    os.mkdir(dir_name)
    print(f"Папку {dir_name} створено")


def remove(dir_name: str) -> None:
    """Видаляє порожню папку.

    Args:
        dir_name: Назва папки.

    Raises:
        FileNotFoundError: Папку не знайдено.
        OSError: Папка не порожня.
    """
    os.rmdir(dir_name)
    print(f"Папку {dir_name} видалено")


def dir_list(dir_name: str) -> None:
    """Показує, що є всередині папки.

    Args:
        dir_name: Назва папки.

    Raises:
        FileNotFoundError: Папку не знайдено.
        NotADirectoryError: Це не папка.
    """
    files = os.listdir(dir_name)
    if not files:
        print("Папка порожня")
    for filename in files:
        print(filename)


def rec_search(dir_name: str, file_type: str = "txt") -> None:
    """Шукає файли за розширенням у папці та вкладених папках.

    Args:
        dir_name: Папка, де шукати.
        file_type: Розширення без крапки, наприклад "txt".

    Raises:
        FileNotFoundError: Папку не знайдено.
        NotADirectoryError: Це не папка.
    """
    os.listdir(dir_name)

    found = False
    for file in Path(dir_name).rglob(f"*.{file_type}"):
        print(file)
        found = True

    if not found:
        print("Нічого не знайдено")
