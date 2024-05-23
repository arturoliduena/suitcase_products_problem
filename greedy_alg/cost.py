# Cost functions for greedy algorithm

def weight(item):
    price = item[0]
    weight = item[1]
    return price / weight


def size_linear(item):
    price = item[0]
    size = item[2]
    return price / size


def size_quad(item):
    price = item[0]
    size = item[2] ** 2
    return price / size


def combined_linear(item):
    (price, weight, side) = item
    return price / (weight * side)


def combined_quad(item):
    (price, weight, side) = item
    return price / (weight * side * side)