import modelling


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


def print_intro(cmds, params):
    print('Welcome! This program can simulate a process of disk degradation due to bad blocks.')
    print('You may use the following commands:')
    for cmd in cmds:
        print(cmd)
    print('-'*20)
    print('Parameters are set:')
    print_parameters(params)
    print('-' * 20, end='\n')


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
    for name in params:
        print_param(params, name)


def set_parameter(param, value, params):
    if param not in params:
        print('Wrong name of the input parameter')
        print('Please, type in correct name from:')
        print_parameters(params)
    else:
        import main
        main.set_parameter(param, value)


def reset_parameter(params):
    name = input('Enter a name of a parameter: \n').upper()
    if name not in params:
        print('A mistake in name! Reset aborted.')
    else:
        print('Current value:')
        print_param(params, name)
        value = input('Enter a new value:\n')
        set_parameter(name, value, params)
        print('The new value has been accepted.')


# ++++++++++++++++++++++++++++++
# +++ Modelling: +++

def print_disk_info(my_disk):
    print('num engaged sectors = ', my_disk.num_engaged_sectors,
          '\nnum sectors = ', my_disk.num_sectors,
          '\ntotal number files = ', my_disk.get_number_files(), sep='')


def output_finish_message():
    print('The simulation has been successfully performed.')


def offer_save_data():
    print('Do you want to save your parameters and results? (Y/n)', end=' ')
    answer = input()
    if answer.lower() in ['', 'y', 'yes']:
        return True
    else:
        return False


def successfull_save():
    print('Data have been saved. Thank you for using this program :)')
