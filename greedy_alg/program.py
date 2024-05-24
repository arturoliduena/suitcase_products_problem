import os
import sys
import time
from typing import IO, Any
import argparse
import Settings
import cost
from greedy import greedy
from GRASP import GRASP
from localsearch import local_search
from Heuristics.datParser import DATParser


class Product:
    def __init__(self, price, weight, side):
        self.price = price
        self.weight = weight
        self.side = side

    def __str__(self):
        return f"Product(price={self.price}, weight={self.weight}, side={self.side})"


class Suitcase:
    def __init__(self, max_weight, width, height):
        self.max_weight = max_weight
        self.width = width
        self.height = height

    def __str__(self):
        return f"Suitcase(max_weight={self.max_weight}, width={self.width}, height={self.height}, products={self.products})"


def execute(algorithm: str, file_num: int, input_file: str, output_file: IO[Any]):
    data = DATParser.parse(input_file)
    products = product_list(data)
    suitcase = Suitcase(data.c, data.x, data.y)

    # Output line
    line = []

    # Add an indicator of the number of the dataset in case it's needed for analyzing data
    if Settings.values["file_num"]:
        line.append(file_num)

    # Run algorithms
    # Weight
    run_alg(algorithm, line, "weight", cost.weight, suitcase, products)
    run_alg(algorithm, line, "size_linear",
            cost.size_linear, suitcase, products)
    run_alg(algorithm, line, "size_quad", cost.size_quad, suitcase, products)
    run_alg(algorithm, line, "combined_linear",
            cost.combined_linear, suitcase, products)
    run_alg(algorithm, line, "combined_quad",
            cost.combined_quad, suitcase, products)

    # Write to file
    output_file.write(",".join(map(str, line)))
    output_file.write("\n")


def run_alg(algorithm, line, label, cost_fn, suitcase, products):
    if Settings.greedy[label]:
        t = time.time_ns()
        if algorithm == "greedy":
            res = greedy(suitcase.max_weight, suitcase.width,
                         suitcase.height, products, cost_fn)
        if algorithm == "GRASP":
            res = GRASP(suitcase.max_weight, suitcase.width,
                        suitcase.height, products, cost_fn, 0)
        dt = time.time_ns() - t
        print_result(line, res, dt)
        if Settings.greedy[label]:
            t = time.time_ns()
            (total_price, total_weight, selected, rest) = res
            res = local_search(total_weight, total_price,
                               suitcase.max_weight, selected, rest)
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


def product_list(data):
    data.p, data.w, data.s
    products = []
    for i in range(data.n):
        products.append(Product(data.p[i], data.w[i], data.s[i]))
    return products


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", type=str, choices=["greedy", "GRASP", "localsearch"],
                        help="Algorithm to run")
    parser.add_argument("--file_num", type=int,
                        required=True, help="Number of the file")
    parser.add_argument("--input_file_name", type=str,
                        required=True, help="Input file")
    parser.add_argument("--output_file_name", type=str,
                        required=True, help="Output file")
    args = parser.parse_args()
    input_file = os.path.join("input", args.input_file_name)

    output_file = open(os.path.join(
        "output_test", f"{args.output_file_name}_{args.file_num}.csv"), 'w')

    sys.exit(execute(args.algorithm, args.file_num,
             args.input_file_name, output_file))
