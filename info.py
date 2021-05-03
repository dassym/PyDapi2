import sys
from os.path import dirname, join 
sys.path.append(join(dirname(__file__),'src'))

from dapi2 import __version__, VERSION, __ver__

SHORTNAME = 'PyDapi2'
NAME = 'PyDapi2'
DESCRIPTION = 'Python implemantation of Dassym API verion 2'
COPYRIGHT = 'Dassym SA - 2021'
AUTHORS = ('F.Voillat', 'T. Marti')