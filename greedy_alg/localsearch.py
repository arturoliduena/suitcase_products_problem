import sys
from Heuristics.datParser import DATParser
from utils import build_input_list, print_results
from greedy import greedy

def run():
    # Read input
    input_file = "input/suitcase_0.dat"

    print("Greedy Algorithm")
    print("-----------------------")
    print(f"Reading input file {input_file}...")

    # 1: Prepare input data
    data = DATParser.parse(input_file)
    l = build_input_list(data.p, data.w, data.s)

    max_weight = data.c

    print(f"Max suitcase weight: {max_weight}")
    print(f"Max suitcase space: {data.x * data.y}")
    print(f"Total candidates: {len(list(l))}")
    print("-----------------------")

    (total_price, total_weight, selected) = greedy(max_weight, data.x, data.y, l)

    """
    TODO:
    pack results
    if available weight and space:
        add more
    if available weight only:
        find elements with better price that can still fit in weight
        replace lowest price existing element with it (larges diff of same size)
    if available space only (harder):
       replace element with highest weight with a combination of 2 elements with highest price that fit
    
    since max weight is harder to handle we should prioritize the greedy algorithm for picking low weight elements
    """

    print(f"Total price: {total_price}")
    print(f"Total weight: {total_weight}")
    print("-----------------------")
    print(f"Selected elements:")
    for s in selected:
        (x, y, side) = s
        print(f"x: {x}, y: {y}, side: {side}")
    print("-----------------------")
    print_results(data.x, data.y, selected)

def pack():
    pass