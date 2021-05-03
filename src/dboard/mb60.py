'''
Created on 24 févr. 2021

@author: fv
'''
from .base import DBoard
from dboard.base import DBoardPreferedDapiMode

class Board60(DBoard):
    '''
    classdocs
    '''
    number = '60'

    def __init__(self, dapi, dmode=DBoardPreferedDapiMode.REGISTER):
        '''Constructor'''
        super().__init__(dapi, dmode)
        self.speed_range.set(0,40000)         