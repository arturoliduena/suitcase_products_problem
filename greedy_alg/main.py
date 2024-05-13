import sys
from Heuristics.datParser import DATParser


def run():
    # Read input
    input_file = "input/suitcase_0.dat"

    print("Greedy Algorithm")
    print("-----------------------")
    print(f"Reading input file {input_file}...")

    # 1: Prepare input data
    data = DATParser.parse(input_file)
    l = build_input_list(data.price, data.weight, data.side)

    max_weight = data.caseCapacity

    print(f"Max suitcase weight: {max_weight}")
    print(f"Max suitcase space: {data.caseWidth * data.caseHeight}")
    print(f"Total candidates: {len(list(l))}")
    print("-----------------------")

    (total_price, total_weight, selected) = greedy(max_weight, data.caseWidth, data.caseHeight, l)

    print(f"Total price: {total_price}")
    print(f"Total weight: {total_weight}")
    print("-----------------------")
    print(f"Selected elements:")
    for s in selected:
        (x, y, side) = s
        print(f"x: {x}, y: {y}, side: {side}")
    print("-----------------------")
    print_results(data.caseWidth, data.caseHeight, selected)


def greedy(max_weight, max_width, max_height, candidates):
    max_space = max_width * max_height
    # Candidate: (price, weight, side)
    # Selected: (x, y, side)
    selected = []
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
            return (total_price, total_weight, selected)

        # Sort candidates by value (price/side over weight)
        candidates.sort(key=weight_cmp)

        # Get the first candidate
        candidate = candidates.pop(0)
        # Find most appropriate position
        position = find_position(candidate, max_width, max_height, selected.copy())

        # If it doesn't fit skip it
        # It has already been removed from candidates list bc it doesn't fit and won't fit anymore
        if position is None:
            continue

        # Otherwise store all relevant data
        (x, y) = position
        (price, weight, side) = candidate
        total_price += price
        total_weight += weight
        total_space += side ** 2

        # Add it to selected items at given position
        selected.append((x, y, side))


def build_input_list(price, weight, side):
    output = []
    for i in range(len(price)):
        output.append((price[i], weight[i], side[i]))
    return output


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
            (_, _, oside) = other
            if check_overlap((cx, cy, iside), other):
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

def print_results(width, height, result):
    for i in range(height):
        line = []
        for j in range(width):
            overlaps = False
            number = 0
            for (ri, res) in enumerate(result):
                number = ri
                (x, y, side) = res
                if x <= j < x + side and y <= i < y + side:
                    overlaps = True
                    break
            if overlaps:
                if number <= 9:
                    line.append(str(number))
                elif number <= 9 + 26:
                    line.append(str(chr(ord('A') + number - 10)))
                else:
                    line.append(str(chr(ord('a') + number - 10)))
            else:
                line.append(" ")
        print(''.join(line))

if __name__ == '__main__':
    sys.exit(run())
