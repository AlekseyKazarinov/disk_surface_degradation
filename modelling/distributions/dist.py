from modelling.distributions import *

"""
It implements selection the distribution function
using 'form' parameter
"""


class DistException(Exception):
    pass


def get_distribution(vol, form, **kargs):
    """
    :param vol: volume dedicated to files, number of sectors (if you use 'user_distribution' as the form, input None)
    :param form: sets type of distribution function ('linear', 'exp_decay', 'user_distribution')
    :param kargs: you may set such parameters as max_number, max_size (number of sectors for a file)
    :return:
    """
    set_volume(vol)
    set_max_size(kargs.get('max_size'))
    set_max_number(kargs.get('max_number'))
    set_file_name(kargs.get('file_name'))

    #print('max_size in get_distribution = ', get_max_size())

    if form == 'linear_decay':
        from modelling.distributions import linear_decay
        return linear_decay.get_linear_decay()

    elif form == 'exp_decay':
        from modelling.distributions import exp_decay
        return exp_decay.get_exp_decay()

    elif form == 'user_distribution':
        from modelling.distributions import user_distribution
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
