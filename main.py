import os
import csv
import json
import shutil
from pathlib import Path
from contextlib import contextmanager
from time import perf_counter
import FileOperations
import DirectoryOperations

"""def class_definer(name):
    class_name = input("Enter class of file: ")
    if class_name == "file":
        print("Created an object of class file")
        return FileOperations(name)
    elif class_name == "directory":
        print("Created an object of class directory")
        return DirectoryOperations(name)
    else:
        print("Invalid class name")
        return None
"""


@contextmanager
def open_close_file(name):
    pass



@contextmanager
def timer(name):
    start = perf_counter()
    try:
        yield
    finally:
        end = perf_counter()
        print(
            f'{name}: {end - start:.6f} seconds')

@contextmanager
def change_directory(path):
    previous_directory = os.getcwd()
    try:
        os.chdir(path)
        print(f'Current directory: {os.getcwd()}')
        yield
    finally:
        os.chdir(previous_directory)
        print(f'Restored directory: {os.getcwd()}')


dir_name = input("Enter the name of directory:")
DirectoryOperations.dir_list(dir_name)