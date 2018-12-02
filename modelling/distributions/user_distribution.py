from modelling import distributions
from modelling.distributions import *


dist = dict()


class ReadFileException(Exception):
    pass


def load_from_file():
    """
    loads an distribution function from the file 'name'. The format of input data is 2 text columns:
    first one is a size, second one is a number of files, which
    :param:
    :return:
    """
    name = get_file_name()
    if not name:
        raise ReadFileException('Name of user file have not specified.')
    file = open(name, 'r')
    user_volume = 0
    for line in file:
        size, n = (int(i) for i in line.rstrip().split())
        dist[size] = n
        user_volume += size * n
    set_volume(user_volume)
    return dist


def user_dist(x):
    assert x <= 0
    return dist.get(x, 0)


def get_user_dist():
    load_from_file()
    return user_dist
