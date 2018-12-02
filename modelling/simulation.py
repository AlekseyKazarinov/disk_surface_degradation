from modelling import disk
import random

"""
Моделирование процесса разрушения поверхности диска.
Появляющиеся со временем на диске bad секторы приводят к повреждению файлов на носителе.
Данная программа предназначена для вычисления объемной и количественной доли файлов, которые
можно восстановить простым чтением.
На вход программе подаётся предполагаемое распределение файлов по размеру n(s), где
n - общее количество файлов на компьютере размера s
"""

# These are needed to using in the program:

params = dict(MAX_BAD_SECTORS=13000,
              DISK_VOLUME=0.05,  # volume of disk (Gb)
              DEDICATED_VOLUME=0.04,  # space with files in disk (Gb)
              SECTOR_SIZE=4,  # size of a sector on a disk (Kb)
              KIND_DISTRIBUTION='exp_decay',  # may be 'linear_decay', 'user_dist' (requires to define FILE_NAME, see next)
# These are optional (used if it requires; it depends of your selection):
              MAX_FILE_SIZE=0.0005,  # the greatest file size in the file system (Gb)
              MAX_NUMBER=500,  # maximal number of files which have the same size
              FILE_NAME='user_distribution_example')  # first of all you need to add this file into distributions package


class Simulation:
    def __init__(self, parameters=None):
        self.params = params
        if parameters:
            self.set_params(parameters)
        self.disk = disk.Disk(self.params['SECTOR_SIZE'], self.params['DISK_VOLUME'])
        self.stats = list()

    def prepare(self):
        """
        Configures the system according their parameters
        :return:
        """
        self.disk.write_files(self.params['DEDICATED_VOLUME'],
                              self.params['KIND_DISTRIBUTION'],
                              self.params['MAX_FILE_SIZE'])

    def add_bad_sector(self):
        """
        Adds one bad sector to the disk by random
        :return:
        """
        if self.disk.num_bad_sectors == self.disk.num_sectors:
            return
        damaged = False
        while not damaged:
            num_bad_sector = int(random.random()*self.disk.num_sectors)
            if self.disk.num_engaged_sectors <= num_bad_sector < self.disk.num_sectors:  # если попадаем в незанятую область
                if not self.disk.free[num_bad_sector-self.disk.num_engaged_sectors]:
                    self.disk.free[num_bad_sector - self.disk.num_engaged_sectors] = True  # помечаем сектор незанят. части поврежденным
                    damaged = True
                    self.disk.num_bad_sectors += 1
            else:
                address = num_bad_sector
                for file in self.disk:
                    if address >= file.size:
                        address -= file.size
                        continue
                    else:
                        success = file.damage(address)
                        if success:
                            damaged = True
                            self.disk.num_bad_sectors += 1
                        break

    def gather_stats(self):
        stat = self.disk.get_stat()
        lst = [stat['num_bad_sectors'], stat['percent of unbroken files'], stat['percent of bad blocks']]
        self.stats.append(lst)

    def simulate(self, logging=False):
        for i in range(self.params['MAX_BAD_SECTORS']):
            self.add_bad_sector()
            self.gather_stats()
            if logging:
                print('{0} bad sectors from {1} calculated'.format(i, self.params['MAX_BAD_SECTORS']))

    def get_info(self):
        info = self.disk.get_info()
        # may collect more info also (in the future)
        return info

    def set_param(self, name, value):
        if name in self.params:
            if value.isdigit():  # если число целое в строке
                value = int(value)
            elif value.lstrip('-').replace('.', '', 1).isdigit():  # если действительное, более общий случай
                value = float(value)
            self.params[name] = value

    def set_params(self, params):
        for (name, value) in params:
            self.set_param(name, value)

    def get_params(self):
        return self.params

    def get_param(self, name):
        if name in self.params.keys():
            return self.params[name]
        else:
            return None

    def get_stats(self):
        return self.stats

    def get_dist(self):
        return self.disk.dist


def main():
    print('max bad sectors = ', params['MAX_BAD_SECTORS'])
    # my_disk = disk.Disk(params['SECTOR_SIZE'], params['DISK_VOLUME'])
    # my_disk.write_files(params['DEDICATED_VOLUME'], params['KIND_DISTRIBUTION'], params['MAX_FILE_SIZE'])
    my_simulation = Simulation()
    my_simulation.prepare()
    my_simulation.simulate()
    # my_disk = disk.Disk(sector_size=4, volume=100)
    # my_disk.write_files(70, 'exp_decay', 0.05)
    # print('num engaged sectors = ', my_disk.num_engaged_sectors, '; num sectors = ', my_disk.num_sectors, sep='')
    # print('total number files = ', my_disk.get_number_files())
    # for i in range(params['MAX_BAD_SECTORS']):
    #    my_simulation.add_bad_sector()
    #    my_disk.print_stats()


if __name__ == '__main__':
    main()
