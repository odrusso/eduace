import random
from time import time


def integer_coefficients(amount=1, number_range=(1, 10), seed=time()):

    random.seed(a=seed)
    ints = []

    for _ in range(amount):
        sign = random.choice([0, 1])
        ints += [(-1) ** sign * random.randint(*number_range)]

    return ints


def positive_integer_coefficients(amount=1, number_range=(1, 10), seed=time()):
    random.seed(a=seed)
    ints = []

    for _ in range(amount):
        ints += [random.randint(*number_range)]

    return ints
