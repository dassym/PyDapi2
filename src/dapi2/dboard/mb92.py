'''Module to define the class of MB-92 Dassym's electronic board representation.

:author: F. Voillat
:date: 2021-02-24 Creation
'''
from .base import DBoard, DBoardPreferredDapiMode


class Board92(DBoard):
    '''Class for MB-92 Dassym's board.

    .. inheritance-diagram:: Board92
        :parts: 1
    
    '''
    
    number = '92'
    '''Board type number (str)'''
    
    

    def __init__(self, dapi, dmode=DBoardPreferredDapiMode.REGISTER):
        '''Constructor'''
        super().__init__(dapi, dmode)
        self.speed_range.set(100,40000)         
        
class Board92B(Board92):
    ext = 'B'
        