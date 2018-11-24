import math
from random import random

"""
In this module different distribution functions are described.
By this time there are two types of the functions: linear and exponential decay.
These functions are implemented inside get_distribution function, which can receive
additional parameters that may be required in calculations:
- max_number - most big number of files that have the same size
- max_size - the greatest size of file on a disk (sectors)
It is recommended to set at least one parameter.
Each function in get_distribution might have its restricted set of required parameters.
"""


def convert_to_sectors(volume, sector_size=4):
    """
    converts volume (Gb) to a number of sectors
    :param volume:
    :param sector_size: by default, equals 4 Kb
    :return:
    """
    return math.ceil(volume * (2 ** 20) / sector_size)


def get_distribution(volume, form, **kargs):
    """
    :param volume: volume dedicated to files, number of sectors
    :param form: sets type of distribution function ('linear', 'exp_decay')
    :param kargs: you may set such parameters as max_number, max_size (number of sectors for a file)
    :return:
    """
    max_number = kargs.get('max_number')
    max_size = kargs.get('max_size')

    print('max_size in get_distribution = ', max_size)


    def line(x):
        """
        Функция вида y = a*x + b (a<0)
        :param x: input argument
        :return: y(x)
        """
        if x < 0:
            raise Exception
        flag = (random() >= 0.5)
        if max_number:
            a = -max_number*max_number*x/(2*volume)
            b = max_number
            m_size = -b/a
            if x >= m_size:
                return 0
            else:
                return math.floor(a * x + b) if flag else math.ceil(a * x + b)

        if max_size:
            if x >= max_size:
                return 0
            else:
                b = 6*volume/(max_size*max_size)
                #a = -2 * volume / (max_size * max_size)
                a = -b/max_size
                if flag:
                    return math.floor(a * x + b)
                else:
                    return math.ceil(a * x + b)

    def exp_decay(x, alpha=0.01):
        """
        formula - f(x) = a*exp(-alpha*x) - c
        requires defined max_size parameter
        :param x: input argument
        :param alpha: decay parameter, default value = 1
        :return: f(x)
        """
        assert x >= 0
        assert max_size
        flag = (random() >= 0.5)
        tmp = math.exp(alpha*max_size)
        c = volume / (tmp/(alpha**2) - 1/alpha*(1/alpha+max_size) - max_size*max_size/2)
        a = c*tmp
        #print(a, c)
        if x >= max_size:
            return 0
        else:
            return math.floor(a*math.exp(-alpha*x) - c) if flag else math.ceil(a*math.exp(-alpha*x) - c)

    functions = {'linear': line,
                 'exp_decay': exp_decay}

    return functions[form]


if __name__ == '__main__':
    s = convert_to_sectors(0.00005)
    v = convert_to_sectors(0.04)
    f = get_distribution(v, form='exp_decay', max_size=s)
    for x in range(0, 1000, 1):
        print(x, ' {0}'.format(f(x)))
