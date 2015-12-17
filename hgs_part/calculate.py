"""
This file is the calculating part.
It can be used to calculate the average and the standard derivation of the list.
"""


import math

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