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
    for dataset in ["uniform", "side_sm", "side_lg", "weight_sm", "weight_lg"]:
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
            line.append(f)
            data = DATParser.parse(input_file)

            # Run algorithms
            for cost_fn_name in ["price", "weight", "side_linear", "side_quad", "combined_linear", "combined_quad"]:
                res, dt, res_search, dt_search = execute("greedy", data, cost_fn_name)
                #print(f"Greedy price {res[0]}, LS price {res_search[0]}")
                print_result(line, res, dt, res_search, dt_search)

            # Write to file
            output_file.write(",".join(map(str, line)))
            output_file.write("\n")


def print_result(output, res, time, res_search, time_search):
    (price, weight, size, selected, _) = res
    (price_search, weight_search, selected_search, _) = res_search
    output.append(price)
    output.append(price_search)
    output.append(weight/10000)
    output.append(weight_search/10000)
    output.append(size/10000)
    output.append(len(selected))
    output.append(len(selected_search))
    output.append(time / 1000000)
    output.append(time_search / 1000000)


def print_header(file):
    header = []
    header.append("file")
    print_alg_header(header, "price")
    print_alg_header(header, "weight")
    print_alg_header(header, "side_linear")
    print_alg_header(header, "side_quad")
    print_alg_header(header, "combined_linear")
    print_alg_header(header, "combined_quad")
    file.write(",".join(header))
    file.write("\n")


def print_alg_header(header, alg):
    header.append(f"{alg}_price")
    header.append(f"{alg}_price_ls")
    header.append(f"{alg}_weight")
    header.append(f"{alg}_weight_ls")
    header.append(f"{alg}_size")
    header.append(f"{alg}_elems")
    header.append(f"{alg}_elems_ls")
    header.append(f"{alg}_time")
    header.append(f"{alg}_time_ls")


if __name__ == '__main__':
    sys.exit(run())
