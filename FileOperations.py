"""Робота з файлами та даними користувачів (JSON і CSV)."""

import os
import csv
import json
import shutil
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, TextIO


@contextmanager
def FileContextManager(
        file_name: str, mode: str = "r", newline: str | None = None
) -> Iterator[TextIO]:
    """Відкриває файл і закриває його після роботи.

    Args:
        file_name: Назва файлу.
        mode: Режим: "r" - читати, "w" - записати,
            "a" - додати, "x" - створити.
        newline: Як обробляти кінець рядка (для CSV потрібно "").

    Yields:
        Відкритий файл.

    Raises:
        FileNotFoundError: Файл не знайдено.
        FileExistsError: Файл уже існує (режим "x").
        PermissionError: Немає дозволу.
        IsADirectoryError: Замість файлу вказано папку.
    """
    file = open(file_name, mode, encoding="utf-8", newline=newline)
    try:
        yield file
    finally:
        file.close()


def create_of_file(file_name: str) -> None:
    """Створює новий порожній файл.

    Args:
        file_name: Назва нового файлу.

    Raises:
        FileExistsError: Такий файл уже існує.
    """
    with FileContextManager(file_name, "x"):
        pass
    print(f"Файл {file_name} створено")


def reading(file_name: str) -> None:
    """Читає файл і показує його текст на екрані.

    Args:
        file_name: Назва файлу.

    Raises:
        FileNotFoundError: Файл не знайдено.
    """
    with FileContextManager(file_name) as file:
        print(file.read())


def writing(file_name: str, text: str) -> None:
    """Записує текст у файл. Старий текст стирається.

    Якщо файлу немає, він буде створений.

    Args:
        file_name: Назва файлу.
        text: Текст для запису.
    """
    with FileContextManager(file_name, "w") as file:
        file.write(text)
    print("Текст записано")


def adding(file_name: str, text: str) -> None:
    """Додає текст у кінець файлу.

    Якщо файлу немає, він буде створений.

    Args:
        file_name: Назва файлу.
        text: Текст, який треба додати.
    """
    with FileContextManager(file_name, "a") as file:
        file.write(text)
    print("Текст додано")


def copying(file_name: str, copy_file_name: str) -> None:
    """Копіює файл. Якщо копія вже є, вона буде замінена.

    Args:
        file_name: Який файл копіювати.
        copy_file_name: Назва копії.

    Raises:
        FileNotFoundError: Файл не знайдено.
        OSError: Копія і оригінал - це той самий файл.
    """
    shutil.copy2(file_name, copy_file_name)
    print(f"Файл {file_name} скопійовано в {copy_file_name}")


def remover(file_name: str) -> None:
    """Видаляє файл.

    Args:
        file_name: Назва файлу.

    Raises:
        FileNotFoundError: Файл не знайдено.
    """
    os.remove(file_name)
    print(f"Файл {file_name} видалено")


def import_users(json_name: str) -> list[dict[str, Any]]:
    """Завантажує користувачів із JSON-файлу.

    Args:
        json_name: Назва JSON-файлу.

    Returns:
        Список користувачів. Кожен користувач - це словник.

    Raises:
        FileNotFoundError: Файл не знайдено.
        json.JSONDecodeError: У файлі неправильний JSON.
        ValueError: У файлі не список словників.
    """
    with FileContextManager(json_name) as file:
        users = json.load(file)

    if not isinstance(users, list):
        raise ValueError("У JSON має бути список користувачів")
    for user in users:
        if not isinstance(user, dict):
            raise ValueError("Кожен користувач має бути об'єктом {...}")

    return users


def export_users(users: list[dict[str, Any]], csv_name: str) -> None:
    """Зберігає користувачів у CSV-файл.

    Якщо список порожній, файл не створюється.

    Args:
        users: Список користувачів.
        csv_name: Назва CSV-файлу.
    """
    if not users:
        print("Немає користувачів для експорту")
        return

    columns: list[str] = []
    for user in users:
        for key in user:
            if key not in columns:
                columns.append(key)

    with FileContextManager(csv_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(users)

    print(f"Користувачів збережено у {csv_name}: {len(users)}")


def read_csv(csv_name: str) -> list[dict[str, Any]]:
    """Читає користувачів із CSV-файлу.

    Args:
        csv_name: Назва CSV-файлу.

    Returns:
        Список користувачів. Значення з CSV читаються як текст.

    Raises:
        FileNotFoundError: Файл не знайдено.
        csv.Error: Помилка в CSV.
    """
    with FileContextManager(csv_name, newline="") as file:
        return list(csv.DictReader(file))


def filter_users(
        users: list[dict[str, Any]], key: str, value: str
) -> list[dict[str, Any]]:
    """Шукає користувачів за параметром.

    Великі та малі літери не мають значення.

    Args:
        users: Список користувачів.
        key: Назва параметра, наприклад "city".
        value: Потрібне значення, наприклад "Kyiv".

    Returns:
        Список знайдених користувачів.
    """
    result = []
    for user in users:
        if str(user.get(key, "")).lower() == value.lower():
            result.append(user)
    return result


def filter_by_age(
        users: list[dict[str, Any]], min_age: int
) -> list[dict[str, Any]]:
    """Шукає користувачів, яким не менше ніж min_age років.

    Args:
        users: Список користувачів.
        min_age: Мінімальний вік.

    Returns:
        Список знайдених користувачів.
    """
    result = []
    for user in users:
        age = str(user.get("age", ""))
        # пропускаємо користувачів без правильного віку
        if age.isdecimal() and int(age) >= min_age:
            result.append(user)
    return result


def print_users(users: list[dict[str, Any]]) -> None:
    """Показує користувачів на екрані.

    Args:
        users: Список користувачів.
    """
    if not users:
        print("Користувачів не знайдено")
    for user in users:
        print(user)
