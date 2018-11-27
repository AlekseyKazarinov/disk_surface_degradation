import math

"""
In this package different distribution functions are described.
By this time there are two types of the functions: linear and exponential decay, user_dist
These functions are implemented inside get_distribution function, which can receive
additional parameters that may be required in calculations:
- max_number - most big number of files that have the same size
- max_size - the greatest size of file on a disk (sectors)
- file_name - file that has a distribution of files by size, must have for user_dist
It is recommended to set at least one parameter.
Each function in get_distribution might have its restricted set of required parameters.
"""

max_number = 0
max_size = 0
file_name = None
volume = 0


def set_max_number(value):
    global max_number
    max_number = value


def get_max_number():
    return max_number


def set_max_size(value):
    global max_size
    max_size = value


def get_max_size():
    return max_size


def set_file_name(value):
    global file_name
    file_name = value


def get_file_name():
    return file_name


def set_volume(value):
    global volume
    volume = value


def get_volume():
    return volume


def convert_to_sectors(vol, sector_size=4):
    """
    converts volume (Gb) to a number of sectors
    :param vol:
    :param sector_size: by default, equals 4 Kb
    :return:
    """
    return math.ceil(vol * (2 ** 20) / sector_size)


__all__ = ['get_max_number', 'set_max_number',
           'get_max_size', 'set_max_size',
           'get_file_name', 'set_file_name',
           'get_volume', 'set_volume',
           'convert_to_sectors']


