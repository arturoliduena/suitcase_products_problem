import random
import time


class Solution:
    def __init__(self, price, weight, space, selected, discarded, time):
        self.price = price
        self.weight = weight
        self.space = space
        self.selected = selected
        self.discarded = discarded
        self.time = time / 1000000


class BaseAlgorithm:
    def __init__(self) -> None:
        pass

    def solve(self, max_weight, max_width, max_height, candidates, initial_time, cost_fn, alpha=0) -> Solution:
        max_space = max_width * max_height
        selected = []
        discarded = []
        total_weight = 0
        total_space = 0
        total_price = 0
        positions = [(0, 0)]

        # Iterate indefinitely, end condition is checked inside the loop
        i = 0
        while True:
            # Remove candidates that exceed limits
            # Space filter isn't totally accurate but it can skip some work later
            candidates = filter(lambda x: x.weight <=
                                max_weight - total_weight, candidates)
            candidates = list(filter(lambda x: x.side ** 2 <=
                                     max_space - total_space, candidates))

            # If there are no more candidates (all are selected or discarded) end the algorithm
            if len(candidates) == 0:
                t = time.time_ns() - initial_time
                return Solution(total_price, total_weight, total_space, selected, discarded, t)

            candidate = self.select_candidate(
                candidates, cost_fn, total_price, total_weight, selected, discarded, alpha)
            # Find most appropriate position
            position = self.find_position(positions, candidate,
                                          max_width, max_height, selected.copy())

            # If it doesn't fit skip it
            # It has already been removed from candidates list bc it doesn't fit and won't fit anymore
            if position is None:
                discarded.append(candidate)
                continue

            # Otherwise store all relevant data
            (x, y) = position
            (x, y) = position
            total_price += candidate.price
            total_weight += candidate.weight
            total_space += candidate.side ** 2

            # Add it to selected items at given position
            selected.append((x, y, candidate))

    def find_position(self, positions, item, max_width, max_height, selected):
        checks = positions.copy()

        # Iterate over all possible positions
        while len(checks) > 0:
            (cx, cy) = checks.pop(0)
            overlaps = False

            # Iterate over all non yet collided selected items
            for other in selected:
                # If it overlaps remove the colliding item, add new candidate positions and
                # start over again from new position (without the removed colliding items)
                (ox, oy, oitem) = other
                if ox + oitem.side < cx or oy + oitem.side < cy or ox > cx + item.side or oy > cy + item.side:
                    continue

                # This check might be made redundant by the previous one but in that case it'll only run once so it's ok
                if self.check_overlap((cx, cy, item.side), (ox, oy, oitem.side)):
                    overlaps = True
                    break

            # If none of the other selected items overlap return this position, otherwise check next
            if not overlaps:
                if cx + item.side > max_width or cy + item.side > max_height:
                    continue
                if cx + item.side < max_width:
                    positions.append((cx + item.side, cy))
                if cy + item.side < max_height:
                    positions.append((cx, cy + item.side))
                positions.remove((cx, cy))
                return (cx, cy)

    def check_overlap(self, a, b):
        (ax, ay, aside) = a
        (bx, by, bside) = b
        return not (ax + aside <= bx
                    or bx + bside <= ax
                    or ay + aside <= by
                    or by + bside <= ay)
