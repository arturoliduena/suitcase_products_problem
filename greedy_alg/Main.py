import os
import glob
import sys
from program import execute
from Heuristics.datParser import DATParser
import pandas as pd
import numpy as np
settings_values = {
    "file_num": True,
    "time": True,
    "price": True,
    "weight": False,
    "solution_elem": False,
}
settings_greedy = {
    "weight": True,
    "size_linear": True,
    "size_quad": True,
    "combined_linear": True,
    "combined_quad": True
}
settings_local_search = {
    "weight": True,
    "size_linear": True,
    "size_quad": True,
    "combined_linear": True,
    "combined_quad": True
}


def run(algorithm, cost_fn_list, output_file):
    # Get a list of all files in the folder
    files = glob.glob(os.path.join("input", '*.dat'))
    columns = get_column_names(cost_fn_list)
    rows = []
    # Run all instances in the dataset
    for file_path in files:
        file_name = os.path.basename(file_path)
        print(f"executing file: {file_name} ...")
        data = DATParser.parse(file_path)
        # Output row
        row = [file_name, data.c, data.x, data.y, data.n]

        # Run algorithms
        for cost_fn_name in cost_fn_list:
            solution, res_search = execute(
                algorithm, data, cost_fn_name)
            row.extend([solution.price, solution.weight, solution.space, len(
                solution.selected), solution.time, res_search.price, res_search.weight, res_search.space, len(res_search.selected), res_search.time])
            # print_result(line, res, dt, res_search, dt_search)
        rows.append(row)

    df = pd.DataFrame(np.array(rows), columns=columns)
    df.to_csv(output_file, index=False)
    print(df)


def get_column_names(cost_fn_list: list):
    columns = ['file_name', 'x', 'y', 'c', 'n']
    for cost_fn_name in cost_fn_list:
        columns.extend([
            f"{cost_fn_name}_price",
            f"{cost_fn_name}_weight",
            f"{cost_fn_name}_space",
            f"{cost_fn_name}_selected",
            f"{cost_fn_name}_time",
            f"{cost_fn_name}_price_ls",
            f"{cost_fn_name}_weight_ls",
            f"{cost_fn_name}_space_ls",
            f"{cost_fn_name}_selected_ls",
            f"{cost_fn_name}_time_ls",
        ])
    return columns


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python Main.py <algorithm> <cost_fn_list> <output_file>")
        sys.exit(1)

    algorithm = sys.argv[1]
    cost_fn_list = sys.argv[2].split(",")
    output_file = sys.argv[3]

    run(algorithm, cost_fn_list, output_file)
    sys.exit(run(algorithm, cost_fn_list, output_file))
