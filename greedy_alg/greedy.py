import sys
from Heuristics.datParser import DATParser
from utils import build_input_list, print_results


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

    (total_price, total_weight, selected, _) = greedy(max_weight, data.caseWidth, data.caseHeight, l)

    print(f"Total price: {total_price}")
    print(f"Total weight: {total_weight}")
    print("-----------------------")
    print(f"Selected elements:")
    for s in selected:
        (x, y, side, _, _) = s
        print(f"x: {x}, y: {y}, side: {side}")
    print("-----------------------")
    print_results(data.x, data.y, selected)


def greedy(max_weight, max_width, max_height, candidates):
    max_space = max_width * max_height
    # Candidate: (price, weight, side)
    # Selected: (x, y, side)
    selected = []
    discarded = []
    total_weight = 0
    total_space = 0
    total_price = 0

    # Iterate indefinitely, end condition is checked inside the loop
    while True:
        # Remove candidates that exceed limits
        # Space filter isn't totally accurate but it can skip some work later
        candidates = filter(lambda x: x[1] <= max_weight - total_weight, candidates)
        candidates = list(filter(lambda x: x[2] ** 2 <= max_space - total_space, candidates))

        # If there are no more candidates (all are selected or discarded) end the algorithm
        if len(candidates) == 0:
            return (total_price, total_weight, selected, discarded)

        # Sort candidates by value (price/side over weight)
        candidates.sort(key=weight_cmp)

        # Get the first candidate
        # TODO: Change for grasp
        candidate = candidates.pop(0)
        # Find most appropriate position
        position = find_position(candidate, max_width, max_height, selected.copy())

        # If it doesn't fit skip it
        # It has already been removed from candidates list bc it doesn't fit and won't fit anymore
        if position is None:
            discarded.append(candidate)
            continue

        # Otherwise store all relevant data
        (x, y) = position
        (price, weight, side) = candidate
        total_price += price
        total_weight += weight
        total_space += side ** 2

        # Add it to selected items at given position
        selected.append((x, y, side, weight, price))


def weight_cmp(item):
    price = item[0]
    weight = item[1]
    return price / weight


def size_cmp(item):
    price = item[0]
    size = item[2]
    return price / size


def find_position(item, max_width, max_height, selected):
    # Start at top left corner
    checks = [(0, 0)]

    (_, _, iside) = item
    max_x = max_width - iside
    max_y = max_height - iside

    # Iterate over all possible positions
    while len(checks) > 0:
        (cx, cy) = checks.pop(0)
        overlaps = False

        # Iterate over all non yet collided selected items
        for other in selected:
            #print(f"iterating: {(cx,cy)}")
            # If it overlaps remove the colliding item, add new candidate positions and
            # start over again from new position (without the removed colliding items)
            (ox, oy, oside, _, _) = other
            if check_overlap((cx, cy, iside), (ox, oy, oside)):
                overlaps = True
                if cx + oside < max_x:
                    checks.append((cx + oside, cy))
                if cy + oside < max_y:
                    checks.append((cx, cy + oside))
                break

        # If none of the other selected items overlap return this position, otherwise check next
        if not overlaps:
            return (cx, cy)


def check_overlap(a, b):
    (ax, ay, aside) = a
    (bx, by, bside) = b
    return not (ax + aside <= bx
            or bx + bside <= ax
            or ay + aside <= by
            or by + bside <= ay)


if __name__ == '__main__':
    sys.exit(run())
