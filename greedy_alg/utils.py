def build_input_list(price, weight, side):
    output = []
    for i in range(len(price)):
        output.append((price[i], weight[i], side[i]))
    return output


def print_results(width, height, result):
    for i in range(height):
        line = []
        for j in range(width):
            overlaps = False
            number = 0
            for (ri, res) in enumerate(result):
                number = ri
                (x, y, side, _, _) = res
                if x <= j < x + side and y <= i < y + side:
                    overlaps = True
                    break
            if overlaps:
                if number <= 9:
                    line.append(str(number))
                elif number <= 9 + 26:
                    line.append(str(chr(ord('A') + number - 10)))
                else:
                    line.append(str(chr(ord('a') + number - 10)))
            else:
                line.append(" ")
        print(''.join(line))