def invert_value_signs(dictionary):
    for key in dictionary:
        dictionary[key] *= -1


def sum_dict_values(dictionary):
    sum = 0
    for key in dictionary:
        sum += dictionary[key]
    return sum


def safe_dict_increment(dictionary, key, value):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value
