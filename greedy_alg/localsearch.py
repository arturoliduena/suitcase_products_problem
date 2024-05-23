def local_search(total_weight, total_price, max_weight, selected, candidates):
    rest = []
    while total_weight < max_weight and len(candidates) > 0:

        # Sort the selected items from lowest price first
        selected.sort(reverse=True, key=lambda x: x[4])

        # Sort the remaining items from highest price first
        candidates.sort(key=lambda x: x[0])
        (nprice, nweight, nside) = candidates.pop(0)

        # Find an item with same size
        i = 0
        while i < len(selected) and selected[i][2] != nside:
            i += 1

        if i == len(selected):
            continue

        # Swap items
        (x, y, oside, oweight, oprice) = selected[i]
        if total_weight - oweight + nweight > max_weight:
            rest.append((nprice, nweight, nside))
            continue
        total_price = total_price - oprice + nprice
        total_weight = total_weight - oweight + nweight
        selected[i] = (x, y, nside, nweight, nprice)
        rest.append((oprice, oweight, oside))

    return total_price, total_weight, selected, candidates
