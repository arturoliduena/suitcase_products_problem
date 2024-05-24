import os
import sys
import Settings
from program import execute


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
            execute("greedy", n, input_file, output_file)


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


if __name__ == '__main__':
    sys.exit(run())
