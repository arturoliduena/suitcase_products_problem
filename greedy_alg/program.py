import os
import sys
import time
from typing import IO, Any
import argparse
import cost
from greedy import Greedy
from GRASP import GRASP
from localsearch import local_search
from Heuristics.datParser import DATParser, DATAttributes


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


dict = {
    "weight": cost.weight,
    "size_linear": cost.size_linear,
    "size_quad": cost.size_quad,
    "combined_linear": cost.combined_linear,
    "combined_quad": cost.combined_quad
}


def execute(algorithm: str, data: DATAttributes, cost_fn_name: str):
    products = product_list(data)
    suitcase = Suitcase(data.c, data.x, data.y)

    # Run algorithms
    cost_fn = dict[cost_fn_name]
    t = time.time_ns()
    if algorithm == "greedy":
        greedy = Greedy()
        res = greedy.solve(suitcase.max_weight, suitcase.width,
                           suitcase.height, products, cost_fn)
    if algorithm == "GRASP":
        grasp = GRASP()
        res = grasp.solve(suitcase.max_weight, suitcase.width,
                          suitcase.height, products, cost_fn, 0)
    (total_price, total_weight, selected, rest) = res

    res = local_search(total_weight, total_price,
                       suitcase.max_weight, selected, rest)
    dt = time.time_ns() - t
    return res, dt


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
    parser.add_argument("--input_file_name", type=str,
                        required=True, help="Input file")
    args = parser.parse_args()

    data = DATParser.parse(args.input_file_name)
    sys.exit(execute(args.algorithm, data, "weight"))
