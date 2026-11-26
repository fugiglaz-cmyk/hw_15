import os
from pathlib import Path


def create(dir_name):
    os.mkdir(dir_name)

def remove(dir_name):
    os.rmdir(dir_name)

def dir_list(dir_name):
    files = os.listdir(dir_name)
    for filename in files:
        print(filename)

def rec_search(dir_name, type = "txt"):
    path = Path(dir_name)
    for file in path.rglob(f"*.{type}"):
        print(file)
