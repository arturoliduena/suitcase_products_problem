import os
import sys
import time

import Settings
import cost
from greedy import greedy
from localsearch import local_search
from Heuristics.datParser import DATParser

def run():
    all_inputs = os.listdir("input")
    for dataset in Settings.datasets:
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
            pre_data = DATParser.parse(input_file)
            l = build_input_list(pre_data.p, pre_data.w, pre_data.s)
            max_weight = pre_data.c
            data = (pre_data.c, pre_data.x, pre_data.y, l)

            # Output line
            line = []

            # Add an indicator of the number of the dataset in case it's needed for analyzing data
            if Settings.values["file_num"]:
                line.append(n)

            # Run algorithms
            # Weight
            run_alg(line, "weight", cost.weight, data)
            run_alg(line, "size_linear", cost.size_linear, data)
            run_alg(line, "size_quad", cost.size_quad, data)
            run_alg(line, "combined_linear", cost.combined_linear, data)
            run_alg(line, "combined_quad", cost.combined_quad, data)

            # Write to file
            output_file.write(",".join(map(str, line)))
            output_file.write("\n")


def print_header(file):
    header = []
    if Settings.values["file_num"]:
        header.append("file")
    print_alg_header(header, "weight")
    print_alg_header(header, "size_linear")
    print_alg_header(header, "size_quad")
    print_alg_header(header, "combined_linear")
    print_alg_header(header, "combined_quad")
    file.write(",".join(header))
    file.write("\n")


def print_alg_header(header, alg):
    if Settings.greedy[alg]:
        if Settings.values["price"]:
            header.append(f"{alg}")
        if Settings.values["weight"]:
            header.append(f"{alg}_w")
        if Settings.values["solution_elem"]:
            header.append(f"{alg}_s")
        if Settings.values["time"]:
            header.append(f"{alg}_t")
    if Settings.local_search[alg]:
        if Settings.values["price"]:
            header.append(f"{alg}_ls")
        if Settings.values["weight"]:
            header.append(f"{alg}_ls_w")
        if Settings.values["solution_elem"]:
            header.append(f"{alg}_ls_s")
        if Settings.values["time"]:
            header.append(f"{alg}_ls_t")


def run_alg(line, label, alg, data):
    (max_weight, width, height, candidates) = data
    if Settings.greedy[label]:
        t = time.time_ns()
        res = greedy(max_weight, width, height, candidates, alg)
        dt = time.time_ns() - t
        print_result(line, res, dt)
        if Settings.greedy[label]:
            t = time.time_ns()
            (total_price, total_weight, selected, rest) = res
            res = local_search(total_weight, total_price, max_weight, selected, rest)
            dt = time.time_ns() - t
            print_result(line, res, dt)


def print_result(output, res, time):
    (total_price, total_weight, selected, _) = res
    if Settings.values["price"]:
        output.append(total_price)
    if Settings.values["weight"]:
        output.append(total_weight)
    if Settings.values["solution_elem"]:
        output.append(len(selected))
    if Settings.values["time"]:
        output.append(time)


def build_input_list(price, weight, side):
    output = []
    for i in range(len(price)):
        output.append((price[i], weight[i], side[i]))
    return output


if __name__ == '__main__':
    sys.exit(run())