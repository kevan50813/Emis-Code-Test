import json
import os
import pandas
import datetime
from copy import deepcopy


# read the JSON file to a string using pythons JSON libery
def read_json(filename):
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Error when reading {filename}")

    return data


# turn the output into a csv in the output folder there is one csv for each JSON
def generate_csv(df, filename):
    df.to_csv("output/" + filename + ".csv")


def cross_join(left, right):
    rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            rows.append(deepcopy(temp_row))
    return rows


# take the list of rows and flatten them from N to 1
def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


# convernt N-dimential JSON so 1D,
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
        rows = [{prev_heading[1:]: data}]  # trim the rows
    return rows


# flatten the JSON form an N-dimentional array to a 1D array and convert to dataframe
def create_dataframe(data):
    flat_data = flatten_json(data)
    return pandas.DataFrame(flat_data)


def main():
    st = datetime.datetime.now()
    for file in os.listdir("data"):
        f_st = datetime.datetime.now()
        data = read_json("data/" + file)
        df = create_dataframe(data)
        f_name, f_ext = os.path.splitext(file)
        generate_csv(df, f_name)
        f_et = datetime.datetime.now()
        f_exe_time = f_et - f_st
        print('Execution time for file', f_name, ':', f_exe_time, 'seconds')
    et = datetime.datetime.now()
    exe_time = et - st
    print('Total Execution time:', exe_time, 'seconds')


main()
