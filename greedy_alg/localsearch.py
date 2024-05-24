def local_search(total_weight, total_price, max_weight, selected, candidates):
    rest = []
    while total_weight < max_weight and len(candidates) > 0:

        # Sort the selected items from lowest price first
        selected.sort(reverse=True, key=lambda x: x[2].price)

        # Sort the remaining items from highest price first
        candidates.sort(key=lambda x: x.price)
        candidate = candidates.pop(0)

        # Find an item with same size
        i = 0
        while i < len(selected) and selected[i][2] != candidate.side:
            i += 1

        if i == len(selected):
            continue

        # Swap items
        (x, y, item) = selected[i]
        if total_weight - item.weight + candidate.weight > max_weight:
            rest.append(candidate)
            continue
        total_price = total_price - item.price + candidate.price
        total_weight = total_weight - item.weight + candidate.weight
        selected[i] = (x, y, candidate)
        rest.append(item)

    return total_price, total_weight, selected, candidates
