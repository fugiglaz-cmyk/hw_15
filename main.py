"""Головний файл: меню програми та обробка помилок."""

import csv
import json
from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any

import FileOperations
import DirectoryOperations


@contextmanager
def ExecutionTimer(name: str) -> Iterator[None]:
    """Вимірює, скільки часу виконується операція.

    Args:
        name: Назва операції.

    Yields:
        Нічого (None).
    """
    start = perf_counter()
    try:
        yield
    finally:
        end = perf_counter()
        print(f"{name}: {end - start:.6f} секунд")


MENU = """
1  - Створити файл
2  - Прочитати файл
3  - Записати у файл
4  - Додати текст у файл
5  - Копіювати файл
6  - Видалити файл
7  - Створити папку
8  - Видалити порожню папку
9  - Показати вміст папки
10 - Знайти файли за розширенням
11 - Показати вміст папки (з переходом у неї)
12 - Імпортувати користувачів із JSON
13 - Експортувати користувачів у CSV
14 - Прочитати CSV
15 - Фільтрувати користувачів за параметром
16 - Фільтрувати користувачів за віком
0  - Вихід
"""


def run_command(
        choice: str, users: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Виконує одну команду з меню.

    Args:
        choice: Номер команди.
        users: Список завантажених користувачів.

    Returns:
        Список користувачів (новий після імпорту або читання CSV).

    Raises:
        OSError: Помилка під час роботи з файлом або папкою.
        ValueError: Введено неправильне значення.
        csv.Error: Помилка в CSV.
    """
    if choice == "1":
        name = input("Назва файлу: ")
        with ExecutionTimer("Створення"):
            FileOperations.create_of_file(name)

    elif choice == "2":
        name = input("Назва файлу: ")
        with ExecutionTimer("Читання"):
            FileOperations.reading(name)

    elif choice == "3":
        name = input("Назва файлу: ")
        text = input("Введіть текст: ")
        with ExecutionTimer("Запис"):
            FileOperations.writing(name, text)

    elif choice == "4":
        name = input("Назва файлу: ")
        text = input("Введіть текст: ")
        with ExecutionTimer("Додавання"):
            FileOperations.adding(name, text)

    elif choice == "5":
        name = input("Який файл копіювати: ")
        copy_name = input("Назва копії: ")
        with ExecutionTimer("Копіювання"):
            FileOperations.copying(name, copy_name)

    elif choice == "6":
        name = input("Назва файлу: ")
        with ExecutionTimer("Видалення"):
            FileOperations.remover(name)

    elif choice == "7":
        name = input("Назва папки: ")
        with ExecutionTimer("Створення папки"):
            DirectoryOperations.create(name)

    elif choice == "8":
        name = input("Назва папки: ")
        with ExecutionTimer("Видалення папки"):
            DirectoryOperations.remove(name)

    elif choice == "9":
        name = input("Назва папки: ")
        with ExecutionTimer("Список файлів"):
            DirectoryOperations.dir_list(name)

    elif choice == "10":
        name = input("Назва папки: ")
        file_type = input("Розширення (наприклад txt): ") or "txt"
        with ExecutionTimer("Пошук"):
            DirectoryOperations.rec_search(name, file_type)

    elif choice == "11":
        name = input("Назва папки: ")
        with DirectoryOperations.DirectoryContextManager(name):
            DirectoryOperations.dir_list(".")

    elif choice == "12":
        name = input("Назва JSON-файлу: ")
        with ExecutionTimer("Імпорт"):
            users = FileOperations.import_users(name)
        print(f"Імпортовано користувачів: {len(users)}")
        FileOperations.print_users(users)

    elif choice == "13":
        name = input("Назва CSV-файлу: ")
        with ExecutionTimer("Експорт"):
            FileOperations.export_users(users, name)

    elif choice == "14":
        name = input("Назва CSV-файлу: ")
        with ExecutionTimer("Читання CSV"):
            users = FileOperations.read_csv(name)
        FileOperations.print_users(users)

    elif choice == "15":
        key = input("Параметр (наприклад city): ")
        value = input("Значення (наприклад Kyiv): ")
        result = FileOperations.filter_users(users, key, value)
        FileOperations.print_users(result)

    elif choice == "16":
        min_age = int(input("Мінімальний вік: "))
        result = FileOperations.filter_by_age(users, min_age)
        FileOperations.print_users(result)

    else:
        print("Немає такої команди")

    return users


def main() -> None:
    """Запускає меню, поки користувач не вибере 0.

    Тут обробляються всі помилки, тому програма не падає.
    """
    users: list[dict[str, Any]] = []

    while True:
        print(MENU)
        choice = input("Виберіть команду: ")
        if choice == "0":
            print("До побачення!")
            break
        try:
            users = run_command(choice, users)
        except FileNotFoundError:
            print("Помилка: файл або папку не знайдено")
        except PermissionError:
            print("Помилка: немає дозволу")
        except FileExistsError:
            print("Помилка: такий файл або папка вже існує")
        except IsADirectoryError:
            print("Помилка: це папка, а потрібен файл")
        except NotADirectoryError:
            print("Помилка: це не папка")
        except json.JSONDecodeError as error:
            print(f"Помилка в JSON, рядок {error.lineno}")
        except UnicodeDecodeError:
            print("Помилка: файл не в кодуванні UTF-8")
        except ValueError as error:
            print(f"Неправильне значення: {error}")
        except csv.Error as error:
            print(f"Помилка в CSV: {error}")
        except OSError as error:
            # усі інші системні помилки (цей блок має бути після них)
            print(f"Системна помилка: {error}")


if __name__ == "__main__":
    main()
