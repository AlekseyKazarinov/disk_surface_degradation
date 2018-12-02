
"""
That module is aimed to represent command line user interface.
"""

info = dict()


# ++++++++++++++++++++++++++
# +++ Basic information: +++

def read_info():
    global info
    with open('program_info.txt', 'r') as f:
        for line in f:
            key, value = line.rstrip().split()
            info[key] = value


def print_info():
    read_info()
    for key in info.keys():
        print(str(key)+':', info[key])


def print_intro(cmds):
    print('Welcome! This program can simulate a process of disk degradation due to bad blocks.')
    print('You may use the following commands:')
    for cmd in cmds:
        print(cmd)
    print('-'*20)


def print_help(cmds):
    print('You can use this commands:')
    for cmd in cmds:
        print(cmd)


# +++++++++++++++++++++++++++++++++++++++
# +++ Operations with the parameters: +++

def print_param(params, name):
    offset = 30  # ширина первого столбца
    print(('{0}:' + ' ' * (offset - len(name)) + '{1}').format(name, params[name]))


def print_parameters(params):
    print('Set up parameters:')
    for name in params:
        print_param(params, name)


def get_input_name():
    return input('Enter a name of a parameter: \n').upper().replace(' ', '_')


def output_message(msg):
    print(msg)


def get_input_value(name, cur_val):
    print('Current value:')
    print(name, ': ', cur_val, sep='')
    return input('Enter a new value:\n')


# ++++++++++++++++++++++++++++++
# +++ Modelling: +++


def print_simulation_info(info):
    for key in info.keys():
        print(key, '=', info[key])


def output_finish_message():
    print('The simulation has been successfully performed.')


def offer_save_data():
    print('Do you want to save your parameters and results? (Y/n)', end=' ')
    answer = input()
    if answer.lower() in ['', 'y', 'yes']:
        return True
    else:
        return False


def successful_save():
    print('Data have been saved. Thank you for using this program :)')
