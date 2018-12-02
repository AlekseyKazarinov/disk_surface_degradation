import math
from random import random

from modelling.distributions import *


dist = dict()   # Here will be saved values of distribution function


def build_linear_decay_dist():
    """
    Constructs a linear decay distribution according the parameters in __init__.py
    :return:
    """
    # max_number = get_max_number()
    volume = get_volume()
    max_size = get_max_size()
    '''
    if max_number:
        a = -max_number * max_number * x / (2 * volume)
        b = max_number
        max_size = int(-b/a)
    '''

    if max_size:
        b = 6 * volume / (max_size * max_size)
        a = -b / max_size
        for x in range(1, max_size + 1):
            flag = (random() >= 0.5)
            f = math.floor(a * x + b) if flag else math.ceil(a * x + b)
            if f > 0:
                dist[x] = f


def linear_decay(x):
    assert x >= 0
    return dist.get(x, 0)


def get_linear_decay():
    """
    Returns linear decay distribution function.
    """
    build_linear_decay_dist()
    return linear_decay
