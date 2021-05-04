'''
Created on 8 févr. 2021

@author: fv
'''

from .base import BaseRegElement, DRegException
from .. import dreg

class DRegUndefinedError(DRegException):
    pass

class Register(BaseRegElement):
    '''Class for registers group in DAPI2 registers structure.
    
    :param parent: Registers parent element.
    :type parent: Regsisters
    
    :param name: Group name
    :type name: str

    :param addr: Group base address in registers array.
    :type addr: int

    :param size: Group size, number of registers slot in group (optional).
    :type size: int

    :param descr: Group  description (otional).
    :type descr: str

    :param shortname: Group short name (otional).
    :type shortname: str

    :param readonly: Group readonly status (otional, default:True).
    :type readonly: bool
    '''
    
    
    def __init__(self, name, parent=None, addr=None, size=1, descr=None, shortname=None, readonly=True):
        assert parent is None or isinstance(parent, (dreg.RegContainer, dreg.RegGroup, dreg.RegisterArray )), 'parent is '+type(parent).__name__
        super().__init__(name, parent, addr, size, descr, shortname)
        self.readonly = readonly  
        self._modified = False
        self._undefined = True
        self._callback_list = []
        
        
    def _stringData(self):
        try:
            return '0x{3:04x}({3:d}) ; addr:{0:02X} ×{1:d} {2!s} '.format(
                    self.addr, 
                    self.size, 
                    'R-' if self.readonly else 'RW',
                    self.value) 
        except Exception as e:
            return  "!!Group:" + str(e)+ "!!"
        
    def _valueChanged(self, old):
        if self.container.eventsEnabled:
            for callback in self._callback_list:
                callback(self, old, self.value)
        
    def isModified(self):
        return self._modified
    
    def isUndefined(self):
        return self._undefined
    
    def asString(self):
        return chr(self.value // 256) + chr( self.value & 0xff )  
    
    def alter(self, value):
        self.set(value, modified=True)
    
    def set(self, value, modified=False):
        self._undefined = False
        self._modified = modified
        if self.container.values[self.addr] != value:
            old = self.container.values[self.addr] 
            self.container.values[self.addr] = value
            self._valueChanged(old)
            
        
    def get(self):
        if self._undefined:
            raise DRegUndefinedError(self, 'get', 'Undefined value in register '+self.name)
        return self.container.values[self.addr]      
    
    def connect(self, callback):
        if all(x != callback for x in self._callback_list):
            self._callback_list.append(callback)            

    def disconnect(self, callback):
        self._callback_list.remove(callback) 
        

        
class ReservedRegister(Register):
    
        pass
#     def get(self):
#         raise  Exception('Get value of reserved register is not allowed!')     
        
class BitFieldRegister(Register):
    
    def __init__(self, name, parent=None, addr=None, size=1, descr=None, shortname=None, readonly=True):
        super().__init__(name, parent, addr, size, descr, shortname, readonly)
        self._bits = []
        self._index = {}
        
    def __getitem__(self, index):
        return self._bits[index]
    
    def __getattr__(self, name):
        return self.getBit(name)
    
    def __len__(self):
        return len(self._bits)
    
    def __iter__(self):
        for bit in self._bits:
            yield bit         
        
    def _getNextFreeAddr(self):
        if len(self._bits)==0:
            return 0
        else:
            return self._bits[-1].addr + self._bits[-1].size
        
    def _stringData(self):
        try:
            return super()._stringData() + " ; count:{}".format(len(self)) 
        except Exception as e:
            return  "!!BitFieldRegister:" + str(e)+ "!!"     
        
    def getBit(self, name):
        '''Returns the bit  according to its name.
        
        :param str name: the bit name to return
        
        :return: The bit found
        :rtype: RegBit
        '''
        return self._index[name]
        
        
    def toStringChildren(self, indent=1, prefix='', end='', depth=0):
        '''Returns a pretty listing of registers (children) of this group.
        
        :param indent: Indentation level (optional, default: 1)
        :type indent: int
        
        :param prefix: Prefix for the child's name (optional, default: null string)
        :type prefix: str
        
        :param end: String applied on the end of child's representation (optional, default: null string)
        :type end: str
        
        :param depth: The depth of exploration of children and grandchildren (optional, default: 0 = no exploration)
        :type depth: int
        
        :return: A string with the listing of groups and registers.
        :rtype: str
        '''        
        if len(self._bits)>=10:
            idx_fmt = '{0:02d} ‒ '
        else:
            idx_fmt = '{0:d} ‒ '
        return prefix + '\n'.join( [x.toString(indent,idx_fmt.format(i),depth=depth-1) for (i,x) in enumerate(self._bits)]  ) + end      
                   

    def add(self, *bits):
        '''Adds bits to this bits field register
        
        :param bit: One or more bits to be added to the bits field register
        :type bit: RegBit
        
        :return: The next address (position) after the last added bit
        :rtype: int
        '''
        for bit in bits:
            if bit.addr is None:
                bit.setAddress(self._getNextFreeAddr())
            self._bits.append(bit)
            self._index[bit.name] = bit
            
            self._bits.sort(key=lambda x: x.addr)
        return bit.addr+bit.size
    
    
    @property
    def bits(self):
        return self._bits 
        
class RegisterArray(Register):
    def __init__(self, name, parent=None, addr=None, size=1, descr=None, shortname=None, readonly=True):
        super().__init__(name, parent, addr, size, descr, shortname, readonly)
        self._regs = []
        
        for i in range(self.size):
            reg = Register(self.name+str(i), self, self.addr+i, size=1, shortname=self.shortname+str(i), readonly=readonly)
            self._regs.append(reg)

    def __getitem__(self, index):
        return self._regs[index]
    
    def __len__(self):
        return len(self._regs)
    
    def __iter__(self):
        for dreg in self._regs:
            yield dreg     
            
    def isUndefined(self):
        for r in self:
            if r.isUndefined():
                return True
        return False
    
    def setAddr(self, value):
        Register.setAddr(self, value)
        for i, r in enumerate(self):
            r.setAddr(self.addr+i)
    
    def alter(self, values):
        self.set(values, True)
    
    def set(self, values, modified=False):
        self._modified = modified
        for i, v in enumerate(values):
            self._regs[i].set(v, modified)
        self._undefined = False
        
    def get(self):
        return list([ self._regs[i].get() for i in range(self.size) ])

class RegBitChoice():
    def __init__(self, name, value, bit=None, descr=None, shortname=None ):
        self._bit = bit
        self.value = value
        self.name = name
        self.descr = descr
        if shortname is None:
            self.shortname = name[:3]
        else:
            self.shortname = shortname
            
    def __str__(self):
        return '{0:d}:{1:s}'.format(self.value,self.name)
            
    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value        


class RegBit(BaseRegElement):
    def __init__(self, name, parent=None, addr=None, size=1, descr=None, shortname=None, choices={}):
        super().__init__(name, parent, addr, size, descr, shortname)
        self.choices = choices
        if shortname is None:
            self.shortname = name[:3]
        else:
            self.shortname = shortname
        self._mask = ((1<<self._size)-1) << self._addr
        
#     def __str__(self):
#         try:
#             return '{p:2d}-{n:s}:{v!s}'.format(n=self.name, p=self.pos, v=self.choices[self.value])
#         except KeyError:
#             return ('{1:2d}-{0}:{2:0'+str(self._size)+'b} (0x{2:x})').format(self.name, self.pos, self.value)

    
    def __lt__(self, other):
        return self.name < other.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    def _stringData(self):
        return "{0:d}".format(self.get())
    
    def alter(self, value):
        self.set(value, True)
        
    def set(self, value=1, modified=False):
        assert value >= 0 and value < (1<<self._size), 'RegBit.set:{} is an invalid value for the flag {}.{}'.format(value,self._owner.reg.name,self.name)
        self._parent.set((self._parent.value & ~self._mask) | (value << self.addr),modified)
        return self._parent.value
    
    def toggle(self, modified=False):
        self._parent.set(self._parent.value ^ self._mask,modified)
        return self._parent.value
        
    def clear(self):
        self.set(0, False)
        return self._parent.value
        
    def get(self):
        return (self._parent.value & self._mask) >> self.addr  
    
class ReservedRegBit(RegBit):
    pass

    
        