# Cost functions for greedy algorithm

def price(item):
    return item.price


def weight(item):
    return item.price / item.weight


def side_linear(item):
    return item.price / item.side


def side_quad(item):
    return item.price / (item.side ** 2)


def combined_linear(item):
    return item.price / (item.weight * item.side)


def combined_quad(item):
    return item.price / (item.weight * item.side ** 2)
