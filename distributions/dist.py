from distributions import *

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


class DistException(Exception):
    pass


def get_distribution(vol, form, **kargs):
    """
    :param vol: volume dedicated to files, number of sectors
    :param form: sets type of distribution function ('linear', 'exp_decay')
    :param kargs: you may set such parameters as max_number, max_size (number of sectors for a file)
    :return:
    """
    set_volume(vol)
    set_max_size(kargs.get('max_size'))
    set_max_number(kargs.get('max_number'))
    set_file_name(kargs.get('file_name'))

    #print('max_size in get_distribution = ', get_max_size())

    if form == 'linear_decay':
        from distributions import linear_decay
        return linear_decay.get_linear_decay()

    elif form == 'exp_decay':
        from distributions import exp_decay
        return exp_decay.get_exp_decay()

    elif form == 'user_distribution':
        from distributions import user_distribution
        user_distribution.get_user_dist()

    else:
        raise DistException('Incorrect name of distribution!')


if __name__ == '__main__':
    s = convert_to_sectors(0.0005)
    print('s = ', s)
    v = convert_to_sectors(0.04)
    print('v = ', v)
    f = get_distribution(v, form='exp_decay', max_size=s)
    print('max_size = ', get_max_size())
    for x in range(1, 200, 1):
        print(x, '{0}'.format(f(x)))
