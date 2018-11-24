# disk_surface_degradation

This project is aimed to simulate process of disk surface degradation.

Quite often, HDD breaks down due to the aging surface of a disk, that leads to appearing of so-called bad-sectors.
When a read head tries to obtain data from a bad sector, an read error arises, and the file containing the bad sector 
can't be red fully without using special resources.

My HDD have broken down recenly due to bad blocks. Fortunately, almost all of my files (96%) on it have been recovered successfully.
And it has become interesting to me, how many files could I recover, if I had started recovery a little bit earlier.
So I creates this program to simulate and to plot P(b), where:
  P - percent of whole files (files that did not damaged)
  b - number of bad blocks

SYSTEM REQUIREMENTS:
For the model, described in code, the more the disk volume, the more RAM are required.
It depends of set parameters such as volume of the disk (DISK_VOLUME), 
size of disk sector (SECTOR_SIZE), maximal number of bad sectors (MAX_BAD_SECTORS), 
and volume of the files (DEDICATED_VOLUME).
For example, it requires about 100 Mb RAM and two CPU cores to model 41 Mb HDD.
