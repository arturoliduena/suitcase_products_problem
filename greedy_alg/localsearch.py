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

    (total_price, total_weight, selected, rest) = greedy(max_weight, data.caseWidth, data.caseHeight, l)

    print(f"Greedy picked: {len(selected)} items")
    print(f"Total price of selection: {total_price}")
    print(f"Total weight of selection: {total_weight}")
    print("-----------------------")

    # We assume the limit will always be no more space available, so the greedy algorithm needs to
    # prioritize low weight solutions
    # An algorithm that handles max weight reached could be implemented but it would be more complicated since
    # it would need to remove high weight items and then fill in multiple holes

    while total_weight < max_weight and len(rest) > 0:
        selected.sort(key=price_srt_res, reverse=True)
        rest.sort(key=price_srt)
        (nprice, nweight, nside) = rest.pop(0)

        i = 0
        while i < len(selected) and selected[i][2] != nside:
            i += 1

        if i == len(selected):
            continue

        (x, y, oside, oweight, oprice) = selected[i]
        if total_weight - oweight + nweight > max_weight:
            continue
        total_price = total_price - oprice + nprice
        total_weight = total_weight - oweight + nweight
        selected[i] = (x, y, nside, nweight, nprice)



    """
    TODO:
    pack results (?)
    if available weight and space:
        add more elements that fit
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
        (x, y, side, _, _) = s
        print(f"x: {x}, y: {y}, side: {side}")
    print("-----------------------")
    print_results(data.x, data.y, selected)


def pack():
    pass


def price_srt(item):
    return item[0]


def price_srt_res(item):
    (_, _, _, _, price) = item
    return price


if __name__ == '__main__':
    sys.exit(run())
