def build_input_list(price, weight, side):
    output = []
    for i in range(len(price)):
        output.append((price[i], weight[i], side[i]))
    return output