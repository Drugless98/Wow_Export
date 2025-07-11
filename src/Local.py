import os


def write_json(json_str: str):
    with open("Items.json", "w+") as file:
        file.write(json_str)