from modelling.distributions.dist import *
"""
Describes a disk with files in it
"""


class DiskException(Exception):
    pass


def print_log(func):
    print(func.__name__, 'called')


class Sequence:
    def __init__(self, size):
        self.size = size
        self.sequence = [False for _ in range(self.size)]  # все сектора исправны

    def __getitem__(self, item):
        return self.sequence[item]

    def __setitem__(self, key, value):
        self.sequence[key] = value


class File(Sequence):
    """
    used as data structure only.
    Represents the file with the following attributes:
    size - size of the file (number of sectors for the file)
    id - unique number of the file, is set while the file is being written
    sequence - is an array of segments of the file in direct order
    is_broken - replies if any segment is broken (At least, one bad segment exists)
    """
    id = 0
    counter = 0

    def __init__(self, size):
        Sequence.__init__(self, size)
        self.id = File.id
        File.id += 1
        self.is_broken = False  # изначально все файлы в целостности
        #if File.id / 10000 == 0:
        #    print('current id', File.id)

    def damage(self, address):
        """
        Разрушает сектор файла по адресу
        :param address: адрес разрушаемого сектора
        :return: True, if the sector by the address has not been broken earlier
        """
        success = False
        #print('file s = ', self.sequence, ' broken: ', self.is_broken)
        if not self.sequence[address]:
            self.sequence[address] = True
            self.is_broken = True
            success = True
        #print('file s = ', self.sequence, ' broken: ', self.is_broken)
        return success


class DiskIterator:
    def __init__(self, d):
        self.files = d.files
        self.counter = 0
        self.limit = d.get_number_files()

    def __next__(self):
        if self.counter < self.limit:
            file = self.files[self.counter]
            self.counter += 1
            return file
        else:
            raise StopIteration


class Disk:
    def __init__(self, sector_size=4, volume=0.1):
        self.sector_size = sector_size  # размер сегмента диска, Кб
        self.volume = volume  # объём диска, Гб
        self.num_sectors = convert_to_sectors(volume, sector_size)  # всего сегментов на диске
        self.files = []  # файлы, хранящиеся на диске
        self.num_engaged_sectors = 0  # Занято секторов файлами
        self.num_bad_sectors = 0
        #print(self.num_sectors, self.num_engaged_sectors)
        self.free = []  # Sequence(self.num_sectors - self.num_engaged_sectors) - убрано, чтобы работало быстрее
        self.dist = None  # Distribution of files by their size on the disk
        self.stats = []

    def __iter__(self):
        return DiskIterator(self)

    def get_number_files(self):
        """
        total number of files in the disk
        :return integer:
        """
        return len(self.files)

    def write_files(self, engaged_space, form, max_size):
        """
        Заполняет диск файлами из заданного распределения
        :param engaged_space: размер занятого пространства на диске, Гб
        :param form: тип распределения файлов по размеру
        :param max_size: самый большой размер файла, который может встретиться на диске, Гб
        :return:
        """
        if engaged_space >= self.volume:
            take = engaged_space
            have = self.volume
            raise DiskException(f'Диск не резиновый! Требуется {take} Гб, имеется {have} Гб')
        engaged_sectors = convert_to_sectors(engaged_space, 4)
        self.num_engaged_sectors = 0
        self.free = Sequence(self.num_sectors - self.num_engaged_sectors)
        max_size = convert_to_sectors(max_size)
        #print('engaged_sectors = ', engaged_sectors)
        #print('max_size', max_size)
        distribution = get_distribution(engaged_sectors, form, max_size=max_size)
        self.dist = []
        for size in range(1, max_size+1):  # writes in the disk according our distribution function
            #print('size = ', size, 'dist(size) = ', distribution(size))
            d_size = distribution(size)
            self.dist.append([size, d_size])
            for file in range(d_size):
                self.files.append(File(size))
                self.num_engaged_sectors += size

    def get_unbroken_number_files(self):
        """
        Let's our disk has a special S.M.A.R.T. system, that tells us about the number of bad sectors
        :return: Integer
        """
        cnt = 0
        for f in self:
            if not f.is_broken:
                cnt += 1
        return cnt

    def get_stat(self):
        stat = dict()
        stat['num_bad_sectors'] = self.num_bad_sectors
        stat['percent of unbroken files'] = float(100.0 * (self.get_unbroken_number_files()/self.get_number_files()))
        stat['percent of bad blocks'] = float(100.0 * (self.num_bad_sectors/self.num_sectors))
        return stat

    def print_stats(self):
        """
        Outputs to stdout statistics, including number of bad sectors and percent of unbroken files
        :return: None
        """
        s = self.get_stat()
        print('{0}\t{1:.2f}\t{2:.2f}'.format((s[key] for key in s.keys())))

    def get_info(self):
        info = dict()
        info['num_engaged_sectors'] = self.num_engaged_sectors
        info['num_bad_sectors'] = self.num_bad_sectors
        info['number_files'] = self.get_number_files()
        return info


if __name__ == '__main__':
    d = Disk(sector_size=4, volume=0.05)
    print(d.num_sectors)
    d.write_files(0.04, 'linear', 0.00005)
    print('-> ', d.get_number_files())
    d.print_stats()
    print('from', d.num_sectors, ' engaged = ', d.num_engaged_sectors)
