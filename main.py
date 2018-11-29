from modelling.simulation import *
import modelling.disk as disk
import cmd_out as cmd


stats = []


def set_parameter(name, value):
    if name in params:
        if value.isdigit():  # если число целое в строке
            value = int(value)
        elif value.lstrip('-').replace('.', '', 1).isdigit():  # если действительное, более общий случай
            value = float(value)
        params[name] = value


def load_parameters():
    with open('params', 'r') as f:
        for line in f:
            key, value, *trash = (i for i in line.rstrip().split())
            set_parameter(key, value)


def gather_stats(my_disk):
    stats.append([my_disk.num_bad_sectors,
                  float(100.0 * (my_disk.get_unbroken_number_files() / my_disk.get_number_files())),
                  float(100.0 * (my_disk.num_bad_sectors / my_disk.num_sectors))])


def save_parameters(params):
    with open('params', 'w') as fp:
        for name in params.keys():
            fp.write(name+'\t'+str(params[name])+'\n')


def save_dist(my_disk):
    with open('last_experimental_distribution.txt', 'w') as fout:
        for pair in my_disk.dist:
            fout.write(str(pair[0])+'\t'+str(pair[1])+'\n')


def save_results(stats):
    with open('stats.txt', 'w') as f:
        for stat in stats:
            f.write(str(stat[0])+'\t'+str(stat[1])+'\t'+str(stat[2])+'\n')


def save_data(params, my_disk, stats):
    save_parameters(params)
    save_dist(my_disk)
    save_results(stats)


def simulate():
    print('Set up parameters:')
    cmd.print_parameters(params)
    print('max bad sectors = ', params['MAX_BAD_SECTORS'])
    my_disk = disk.Disk(params['SECTOR_SIZE'], params['DISK_VOLUME'])
    my_disk.write_files(params['DEDICATED_VOLUME'], params['KIND_DISTRIBUTION'], params['MAX_FILE_SIZE'])
    cmd.print_disk_info(my_disk)
    for i in range(params['MAX_BAD_SECTORS']):
        add_bad_sector(my_disk)
        gather_stats(my_disk)
        my_disk.print_stats()
    cmd.output_finish_message()
    if cmd.offer_save_data():
        save_data(params, my_disk, stats)
        cmd.successfull_save()
    exit(0)


cmds = {'print --info': cmd.print_info,
        'print --param': (lambda: cmd.print_parameters(params)),
        'start': simulate,
        'simulate': simulate,
        'reset': (lambda: cmd.reset_parameter(params)),
        'help': (lambda: cmd.print_help(cmds)),
        'exit': (lambda: exit(0))}


def main():
    load_parameters()
    cmd.print_intro(cmds, params)
    while True:
        inp = input()
        if inp in cmds:
            cmds[inp]()
        else:
            cmd.print_help(cmds)


if __name__ == '__main__':
    main()
