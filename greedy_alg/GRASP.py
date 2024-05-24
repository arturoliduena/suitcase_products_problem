import random
from base_algorithm import BaseAlgorithm


class GRASP(BaseAlgorithm):
    def __init__(self) -> None:
        pass

    def select_candidate(self, candidates, sort, total_price, total_weight, selected, discarded, alpha):
        # Sort candidates by value price
        candidates = sorted(candidates, key=lambda x: x.price)

        # compute boundary highest price as a function of the minimum and maximum highest price and the alpha parameter
        minPrice = candidates[0].price
        maxPrice = candidates[-1].price
        boundaryPrice = minPrice + (maxPrice - minPrice) * alpha

        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in candidates:
            if candidate.price <= boundaryPrice:
                maxIndex += 1

        # create RCL and pick an element randomly
        # pick first maxIndex elements starting from element 0
        rcl = candidates[0:maxIndex]
        if not rcl:
            return (total_price, total_weight, selected, discarded)
        # pick a candidate from rcl at random
        candidate = random.choice(rcl)
        return candidate
