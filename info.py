import sys
from os.path import dirname, join
import datetime as DT 
import regex as RE
sys.path.insert(0,join(dirname(__file__),'src'))

from dapi2._version import __version__, VERSION, __ver__, DATE

SHORTNAME = 'PyDapi2'
NAME = 'PyDapi2'
COMPACTNAME = 'pydapi2'
DESCRIPTION = 'Python implemantation of Dassym API verion 2'
COPYRIGHT = 'Dassym SA - 2021'
AUTHORS = ('F.Voillat', 'T. Marti')


def setReleaseDate(isodate):
    d = DT.datetime.strptime(isodate, '%Y-%m-%d')
    ds = '{0:d}, {1:d}, {2:d}'.format(*d.timetuple())
    fname = join('src', 'dapi2','_version.py')
    with open(fname, 'r+') as f:
        tmp = f.read() 
    tmp = RE.sub( r'^DATE\s*=\s*DT\.date\([^)]+\)\s*$',
            "DATE = DT.date({0:s})".format(ds),
            tmp, flags=RE.MULTILINE
            )
    with open(fname, 'w+') as f:
        f.write(tmp) 