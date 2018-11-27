import disk
import random

"""
Моделирование процесса разрушения поверхности диска.
Появляющиеся со временем на диске bad секторы приводят к повреждению файлов на носителе.
Данная программа предназначена для вычисления объемной и количественной доли файлов, которые
можно восстановить простым чтением.
На вход программе подаётся предполагаемое распределение файлов по размеру n(s), где
n - общее количество файлов на компьютере размера s
"""

# these are needed to using in the program
MAX_BAD_SECTORS = 13000
DISK_VOLUME = 0.05  # volume of disk (Gb)
DEDICATED_VOLUME = 0.04  # space with files in disk (Gb)
SECTOR_SIZE = 4  # size of a sector on a disk (Kb)
KIND_DISTRIBUTION = 'exp_decay'  # may be 'exp_decay', 'user_dist' (requires to define FILE_NAME, see next)

# these are optional (used if it requires, depends of your selection)
MAX_FILE_SIZE = 0.0005  # the greatest file size in the file system (Gb)
MAX_NUMBER = 500  # maximal number of files which have the same size
FILE_NAME = 'user_distribution'


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
    print('max bad sectors = ', MAX_BAD_SECTORS)
    my_disk = disk.Disk(SECTOR_SIZE, DISK_VOLUME)
    my_disk.write_files(DEDICATED_VOLUME, KIND_DISTRIBUTION, MAX_FILE_SIZE)
    print('num engaged sectors = ', my_disk.num_engaged_sectors, '; num sectors = ', my_disk.num_sectors, sep='')
    print('total number files = ', my_disk.get_number_files())
    for i in range(MAX_BAD_SECTORS):
        add_bad_sector(my_disk)
        my_disk.print_stats()


if __name__ == '__main__':
    main()
