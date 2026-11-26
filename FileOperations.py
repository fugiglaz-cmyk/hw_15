import os
import shutil


def create_of_file(file_name):
    try:
        file = open(file_name, "x", encoding="utf-8")
        file.close()
        print(f"file {file_name} created")
    except FileExistsError:
        print("File already exists")


def reading(file_name):
    file = open(file_name, "r", encoding="utf-8")
    print(file.read())
    file.close()


def writing(file_name):
    file = open(file_name, "w", encoding="utf-8")
    text = input("Write your text here: ")
    file.write(text)
    file.close()


def adding(file_name):
    file = open(file_name, "a", encoding="utf-8")
    text = input("Write your text here: ")
    file.write(text)
    file.close()

def copying(file_name, copy_file_name):
    shutil.copy2(file_name, copy_file_name)
    print(f"file {file_name} copied to {copy_file_name}")

def remover(file_name):
    os.remove(file_name)
    print(f"file {file_name} removed")