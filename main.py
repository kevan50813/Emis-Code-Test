import json
import os


def read_json(filename: str) -> dir:
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Error when reading {filename}")

    return data


def flatten_json(data: dict) -> dict:
    d = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            d[key] = value
        else:
            for k, v in value.items():
                d[key + "_" + k] = v
    return d


def generate_csv_data(data: dict) -> str:
    collumns = data.keys()
    csv_data = ",".join(collumns) + "\n"
    row = list()
    for col in collumns:
        row.append(str(data[col]))

    csv_data += ",".join(row) + "\n"
    return csv_data
