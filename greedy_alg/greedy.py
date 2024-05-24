from base_algorithm import BaseAlgorithm


class Greedy(BaseAlgorithm):
    def __init__(self) -> None:
        pass

    def select_candidate(self, candidates, cost_fn, total_price, total_weight, selected, discarded, alpha):
        # Sort candidates by value (price/side over weight)
        candidates.sort(key=cost_fn, reverse=True)
        # Get the first candidate
        candidate = candidates.pop(0)
        return candidate
