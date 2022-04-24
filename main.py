import json
import os


def read_json(filename):
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Error when reading {filename}")

    return data


def flatten_json(data):
    d = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            d[key] = value
        else:
            for k, v in value.items():
                d[key + "_" + k] = v
    return d


def generate_csv_data(data):
    collumns = data.keys()
    csv_data = ",".join(collumns) + "\n"
    row = list()
    for col in collumns:
        row.append(str(data[col]))

    csv_data += ",".join(row) + "\n"
    return csv_data


def write_to_csv(data, filepath):
    try:
        with open(filepath, "w+") as f:
            f.write(data)
    except:
        raise Exception(f"Error when wrtring to file form {filepath}")


def main():
    for file in os.listdir("data"):
        data = read_json(file)
        flat_data = flatten_json(data)
        csv_data = generate_csv_data(flat_data)
        write_to_csv(csv_data, "data.csv")


main()
