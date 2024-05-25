import time
from base_algorithm import Solution


def local_search(solution, max_weight, initial_time) -> Solution:
    total_weight = solution.weight
    total_price = solution.price
    selected = solution.selected
    candidates = solution.discarded
    rest = []
    final = []
    while len(selected) > 0 and len(candidates) > 0:
        nochanges = True

        # Sort the selected items from lowest price first
        selected.sort(key=lambda x: x[2].price)

        # Sort the remaining items from highest price first
        candidates.sort(key=lambda x: x.price, reverse=True)

        min_price = selected[0][2].price

        # Remove candidates whose price is smaller than the minimum price in solution
        candidates = list(filter(lambda x: x.price > min_price, candidates))

        x, y, item = selected[0]

        # Find an item the same size
        for i, candidate in enumerate(candidates):
            # Only consider items with the same size
            if item.side != candidate.side:
                continue

            # If the price of the candidate is smaller there is no better candidate, skip
            if item.price >= candidate.price:
                break

            # If new item is to heavy skip it
            new_weight = total_weight - item.weight + candidate.weight
            if new_weight > max_weight:
                continue

            # Perform swap
            nochanges = False
            total_price = total_price - item.price + candidate.price
            total_weight = new_weight
            selected[0] = (x, y, candidate)
            del candidates[i]

            # Once an item has been swapped it'll have a smaller price than the rest of the elements in the solution
            # with the same size, so it can be discarded
            rest.append(item)

        # If no changes were made it's because the price of the best candidate was too small or because
        # no candidate with an appropriate weight was found
        # In either case there is no better candidate than the item in the solution so it can be removed and stored
        if nochanges:
            final.append(selected.pop(0))

    t = time.time_ns() - initial_time
    return Solution(total_price, total_weight, solution.space, selected + final, candidates + rest, t)
