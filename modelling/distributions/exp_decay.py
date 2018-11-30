import math
from random import random, randrange

from modelling.distributions import *


dist = dict()


def build_exp_decay_dist(alpha=0.01):
    """
    formula - f(x) = a*exp(-alpha*x) - c
    requires defined max_size parameter
    :param alpha: decay parameter, default value = 1
    :return:
    """
    max_size = get_max_size()
    volume = get_volume()
    assert max_size
    assert volume
    flag = (random() >= 0.5)
    tmp = math.exp(alpha * max_size)
    c = volume / (tmp / (alpha ** 2) - 1 / alpha * (1 / alpha + max_size) - max_size * max_size / 2)
    a = c*tmp

    for x in range(1, max_size+1):
        f = math.floor((a*math.exp(-alpha*(x-1))+a*math.exp(-alpha*x))/2 - c)
        if f:
            dist[x] = f

    fact_volume = 0
    for i in range(1, max_size + 1):
        fact_volume += dist.get(i, 0)*i
    delta_volume = volume - fact_volume
    #print('delta_volume=', delta_volume)
    if delta_volume > 0:
        xm = max_size
        while delta_volume:
            x = randrange(1, xm+1, 1)
            if x > delta_volume:
                xm = delta_volume
            else:
                dist[x] = dist.get(x, 0) + 1
                delta_volume -= x


def exp_decay(x):
    assert x >= 0
    return dist.get(x, 0)


def get_exp_decay(**alpha):
    build_exp_decay_dist(**alpha)
    return exp_decay


if __name__ == '__main__':
    pass
