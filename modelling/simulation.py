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


def add_bad_sector(d):
    """
    Adds one bad sector to the disk by random
    :param d: selected disk
    :return:
    """
    if d.num_bad_sectors == d.num_sectors:
        return
    damaged = False
    while not damaged:
        num_bad_sector = int(random.random()*d.num_sectors)
        #print('num_bad_sector = ', num_bad_sector)
        if d.num_engaged_sectors <= num_bad_sector < d.num_sectors:  # если попадаем в незанятую область
            if not d.free[num_bad_sector-d.num_engaged_sectors]:
                d.free[num_bad_sector - d.num_engaged_sectors] = True  # помечаем сектор незанят. части поврежденным
                damaged = True
                d.num_bad_sectors += 1
        else:
            address = num_bad_sector
            for file in d:
                if address >= file.size:
                    address -= file.size
                    continue
                else:
                    success = file.damage(address)
                    if success:
                        damaged = True
                        d.num_bad_sectors += 1
                    break


def main():
    print('max bad sectors = ', params['MAX_BAD_SECTORS'])
    my_disk = disk.Disk(params['SECTOR_SIZE'], params['DISK_VOLUME'])
    my_disk.write_files(params['DEDICATED_VOLUME'], params['KIND_DISTRIBUTION'], params['MAX_FILE_SIZE'])
    # my_disk = disk.Disk(sector_size=4, volume=100)
    #my_disk.write_files(70, 'exp_decay', 0.05)
    print('num engaged sectors = ', my_disk.num_engaged_sectors, '; num sectors = ', my_disk.num_sectors, sep='')
    print('total number files = ', my_disk.get_number_files())
    for i in range(params['MAX_BAD_SECTORS']):
        add_bad_sector(my_disk)
        my_disk.print_stats()


#__all__ = ['params', 'add_bad_sector']


if __name__ == '__main__':
    main()
