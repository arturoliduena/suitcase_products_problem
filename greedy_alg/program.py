import os
import sys
import time
from typing import IO, Any
import argparse
import cost
from base_algorithm import Solution
from greedy import Greedy
from GRASP import GRASP
from localsearch import local_search
from Heuristics.datParser import DATParser, DATAttributes
import pandas as pd
import numpy as np


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


cost_fn_dict = {
    "price": cost.price,
    "weight": cost.weight,
    "side_linear": cost.side_linear,
    "side_quad": cost.side_quad,
    "combined_linear": cost.combined_linear,
    "combined_quad": cost.combined_quad
}


def execute(algorithm: str, data: DATAttributes, cost_fn_name: str):
    products = product_list(data)
    suitcase = Suitcase(data.c, data.x, data.y)

    # Run algorithms
    cost_fn = cost_fn_dict[cost_fn_name]
    initial_time = time.time_ns()
    if algorithm == "greedy":
        greedy = Greedy()
        solution: Solution = greedy.solve(suitcase.max_weight, suitcase.width,
                                          suitcase.height, products, initial_time, cost_fn)
    if algorithm == "GRASP":
        grasp = GRASP()
        solution: Solution = grasp.solve(suitcase.max_weight, suitcase.width,
                                         suitcase.height, products, initial_time, cost_fn, 0)

    res_search: Solution = local_search(
        solution, suitcase.max_weight, initial_time)
    return solution, res_search


def product_list(data):
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

    solution, res_search = execute(
        args.algorithm, data, "price")

    df = pd.DataFrame(np.array([[args.input_file_name, 100, 100, 10000, 1000, solution.price, solution.weight, solution.space, len(solution.selected), solution.time, res_search.price, res_search.time]]),
                      columns=['file_name', 'x', 'y', 'c', 'n', 'price', "weight", "space", "selected", 'time', 'price_search', 'time_search'])
    df.to_csv('results.csv', mode='a', index=False)
    print(df)
