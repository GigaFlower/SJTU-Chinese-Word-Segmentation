


import math

def calculate_mean(num_list):
    num_list.sort()
    length = len(num_list)
    if length % 2 == 1:
        middle = int(length / 2 + 0.5)
        mean = num_list[middle]
    else:
        middle = int(length / 2)
        mean = num_list[middle] + num_list[middle + 1]
    return mean

def calculate_average(num_list):
    length = len(num_list)
    sum = 0
    for element in num_list:
        sum += element
    average = sum / length
    return average

def calculate_list_standard_derivation(num_list):
    length = len(num_list)
    average = calculate_average(num_list)
    variance = 0
    for element in num_list:
        variance += (element - average) ** 2 / length
    derivation = math.sqrt(variance)
    return derivation