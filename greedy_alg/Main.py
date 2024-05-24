import os
import sys
from program import execute
from Heuristics.datParser import DATParser

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


def run():
    all_inputs = os.listdir("input")
    for dataset in ["uniform", "size_sm", "size_lg", "weight_sm", "weight_lg"]:
        print(f"Using dataset: {dataset}")

        output_file = open(os.path.join("output_test", f"{dataset}.csv"), 'w')
        input_files = list(filter(lambda x: x.startswith(dataset), all_inputs))

        # Write csv header
        print_header(output_file)

        # Run all instances in the dataset
        for (n, f) in enumerate(input_files):
            print(f"{n} out of 50...")
            # Load data
            input_file = os.path.join("input", f)
            # Output line
            line = []

            # Add an indicator of the number of the dataset in case it's needed for analyzing data
            if settings_values["file_num"]:
                line.append(n)
            data = DATParser.parse(input_file)

            # Run algorithms
            for cost_fn_name in ["weight", "size_linear", "size_quad", "combined_linear", "combined_quad"]:
                res, dt = execute("greedy", data, cost_fn_name)
                print_result(line, res, dt)

            # Write to file
            output_file.write(",".join(map(str, line)))
            output_file.write("\n")


def print_result(output, res, time):
    (total_price, total_weight, selected, _) = res
    if settings_values["price"]:
        output.append(total_price)
    if settings_values["weight"]:
        output.append(total_weight)
    if settings_values["solution_elem"]:
        output.append(len(selected))
    if settings_values["time"]:
        output.append(time)


def print_header(file):
    header = []
    if settings_values["file_num"]:
        header.append("file")
    print_alg_header(header, "weight")
    print_alg_header(header, "size_linear")
    print_alg_header(header, "size_quad")
    print_alg_header(header, "combined_linear")
    print_alg_header(header, "combined_quad")
    file.write(",".join(header))
    file.write("\n")


def print_alg_header(header, alg):
    if settings_greedy[alg]:
        if settings_values["price"]:
            header.append(f"{alg}")
        if settings_values["weight"]:
            header.append(f"{alg}_w")
        if settings_values["solution_elem"]:
            header.append(f"{alg}_s")
        if settings_values["time"]:
            header.append(f"{alg}_t")
    if settings_local_search[alg]:
        if settings_values["price"]:
            header.append(f"{alg}_ls")
        if settings_values["weight"]:
            header.append(f"{alg}_ls_w")
        if settings_values["solution_elem"]:
            header.append(f"{alg}_ls_s")
        if settings_values["time"]:
            header.append(f"{alg}_ls_t")


if __name__ == '__main__':
    sys.exit(run())
