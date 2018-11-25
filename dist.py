import math
from random import random

"""
In this module different distribution functions are described.
By this time there are two types of the functions: linear and exponential decay, user_dist
These functions are implemented inside get_distribution function, which can receive
additional parameters that may be required in calculations:
- max_number - most big number of files that have the same size
- max_size - the greatest size of file on a disk (sectors)
- file_name - file that has a distribution of files by size, must have for user_dist
It is recommended to set at least one parameter.
Each function in get_distribution might have its restricted set of required parameters.
"""


class ReadFileException(Exception):
    pass


def convert_to_sectors(volume, sector_size=4):
    """
    converts volume (Gb) to a number of sectors
    :param volume:
    :param sector_size: by default, equals 4 Kb
    :return:
    """
    return math.ceil(volume * (2 ** 20) / sector_size)


def load_from_file(name):
    """
    loads an distribution function from the file 'name'. The format of input data is 2 text columns:
    first one is a size, second one is a number of files, which
    :param name:
    :return:
    """
    file = open(name, 'r')
    dist = dict()
    for line in file:
        size, n = line.rstrip().split()
        dist[size] = n
    return dist


def get_distribution(volume, form, **kargs):
    """
    :param volume: volume dedicated to files, number of sectors
    :param form: sets type of distribution function ('linear', 'exp_decay')
    :param kargs: you may set such parameters as max_number, max_size (number of sectors for a file)
    :return:
    """
    max_number = kargs.get('max_number')
    max_size = kargs.get('max_size')
    file_name = kargs.get('file_name')

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

    def user_dist(x):
        if not file_name:
            raise ReadFileException('Name of user file have not specified.')
        dist = load_from_file(file_name)
        assert x > 0
        return dist.get(x, 0)

    functions = {'linear': line,
                 'exp_decay': exp_decay,
                 'user_dist': user_dist}

    return functions[form]


if __name__ == '__main__':
    s = convert_to_sectors(0.00005)
    v = convert_to_sectors(0.04)
    f = get_distribution(v, form='exp_decay', max_size=s)
    for x in range(0, 1000, 1):
        print(x, '{0}'.format(f(x)))
