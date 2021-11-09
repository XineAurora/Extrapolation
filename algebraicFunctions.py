import math


def linear(a, b, x):
    return a * x + b


def quadratic(a, b, c, x):
    return a * x ** 2 + b * x + c


def logarithmic(a, b, x):
    return a * math.log(x) + b


def exponential(a, b, x):
    return a * math.exp(x) + b
