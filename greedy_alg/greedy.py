def greedy(max_weight, max_width, max_height, candidates, sort):
    max_space = max_width * max_height
    # Candidate: (price, weight, side)
    # Selected: (x, y, side)
    selected = []
    discarded = []
    total_weight = 0
    total_space = 0
    total_price = 0
    positions = [(0,0)]

    # Iterate indefinitely, end condition is checked inside the loop
    i = 0
    while True:
        # Remove candidates that exceed limits
        # Space filter isn't totally accurate but it can skip some work later
        candidates = filter(lambda x: x[1] <= max_weight - total_weight, candidates)
        candidates = list(filter(lambda x: x[2] ** 2 <= max_space - total_space, candidates))

        # If there are no more candidates (all are selected or discarded) end the algorithm
        if len(candidates) == 0:
            return (total_price, total_weight, selected, discarded)

        # Sort candidates by value (price/side over weight)
        candidates.sort(key=sort)

        # Get the first candidate
        # TODO: Change for grasp
        candidate = candidates.pop(0)
        # Find most appropriate position
        position = find_position(positions, candidate, max_width, max_height, selected.copy())

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
        #print(f"Found {len(selected)} items")


def find_position(positions, item, max_width, max_height, selected):
    (_, _, iside) = item
    checks = positions.copy()

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
            if ox + oside < cx or oy + oside < cy or ox > cx + iside or oy > cy + iside:
                continue

            # This check might be made redundant by the previous one but in that case it'll only run once so it's ok
            if check_overlap((cx, cy, iside), (ox, oy, oside)):
                overlaps = True
                break

        # If none of the other selected items overlap return this position, otherwise check next
        if not overlaps:
            if cx + iside > max_width or cy + iside > max_height:
                continue
            if cx + iside < max_width:
                positions.append((cx + iside, cy))
            if cy + iside < max_height:
                positions.append((cx, cy + iside))
            positions.remove((cx, cy))
            return (cx, cy)


def check_overlap(a, b):
    (ax, ay, aside) = a
    (bx, by, bside) = b
    return not (ax + aside <= bx
            or bx + bside <= ax
            or ay + aside <= by
            or by + bside <= ay)
