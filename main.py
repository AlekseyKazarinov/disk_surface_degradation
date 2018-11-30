from modelling import simulation
import cmd_out as cmd
import os


def load_parameters():
    params = []
    with open('params', 'r') as f:
        for line in f:
            key, value, *trash = (i for i in line.rstrip().split())
            params.append([key, value])
    return params


def reset_parameter(sim):
    name = cmd.get_input_name()
    if name not in sim.params:
        cmd.error_message('A mistake in name! Reset aborted.')
    else:
        new_value = cmd.get_input_value(name, sim.get_param(name))
        sim.set_param(name, new_value)
        print('The new value has been accepted.')


def save_parameters(params):
    with open('params', 'w') as fp:
        for name in params.keys():
            fp.write(name+'\t'+str(params[name])+'\n')


def save_dist(dist):  # слишком сильная связь с чужими модулями
    path = 'results'
    name = 'last_experimental_distribution.txt'
    with open(os.path.join(path, name), 'w') as fout:
        for pair in dist:
            fout.write(str(pair[0])+'\t'+str(pair[1])+'\n')


def save_stats(stats):  # слишком сильная связь :(
    path = 'results'
    name = 'stats.txt'
    with open(os.path.join(path, name), 'w') as f:
        for stat in stats:
            f.write(str(stat[0])+'\t'+str(stat[1])+'\t'+str(stat[2])+'\n')


def save_data(sim):
    save_parameters(sim.get_params())
    save_dist(sim.get_dist())
    save_stats(sim.get_stats())


def simulate(sim):
    cmd.print_parameters(sim.params)
    sim.simulate()
    cmd.print_simulation_info(sim.get_info())
    cmd.output_finish_message()
    if cmd.offer_save_data():
        save_data(sim)
        cmd.successful_save()
    exit(0)

# сделать процедуру do command, в которую передаются агрументы для команд


def menu(cmds):
    while True:
        inp = input()
        if inp in cmds:
            cmds[inp]()
        else:
            cmd.print_help(cmds)


def main():
    params = load_parameters()
    model = simulation.Simulation(params)
    cmds = {'print --info': cmd.print_info,
            'print --param': (lambda: cmd.print_parameters(simulation.params)),
            'start': (lambda: simulate(model)),
            'simulate': (lambda: simulate(model)),
            'reset': (lambda: reset_parameter(model)),
            'help': (lambda: cmd.print_help(cmds)),
            'exit': (lambda: exit(0))}
    cmd.print_intro(cmds)
    menu(cmds)


if __name__ == '__main__':
    main()
