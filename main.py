import json
import os
import pandas
from copy import deepcopy


def read_json(filename):
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Error when reading {filename}")

    return data


def create_dataframe(data):
    return json_to_dataframe(data)


def generate_csv(df, filename):
    df.to_csv("output/" + filename + ".csv")


def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for item in data:
                [rows.append(elem) for elem in flatten_list(flatten_json(item, prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pandas.DataFrame(flatten_json(data_in))


def main():
    for file in os.listdir("data"):
        data = read_json("data/" + file)
        df = create_dataframe(data)
        f_name, f_ext = os.path.splitext(file)
        generate_csv(df, f_name)


main()
