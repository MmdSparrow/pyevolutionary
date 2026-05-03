import math


def constant_start_number_end_number_average(_, start_number, end_number):
    return start_number+end_number/2

def linear(time, start_number, end_number):
    return start_number + (end_number - start_number) / end_number * time

def exp(time, start_number, end_number):
    return start_number * pow(math.e, end_number/(time+1))