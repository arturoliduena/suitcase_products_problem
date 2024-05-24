# Cost functions for greedy algorithm

def weight(item):
    return item.price / item.weight


def size_linear(item):
    return item.price / item.side


def size_quad(item):
    size = item.side ** 2
    return item.price / size


def combined_linear(item):
    return item.price / (item.weight * item.side)


def combined_quad(item):
    return item.price / (item.weight * item.side * item.side)
