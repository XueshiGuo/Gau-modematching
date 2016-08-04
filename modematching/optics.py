import math
import operator
import os
#
from . import opo
from . import abcd
import numpy as np
#
#            
class Optics(object):    
    '''
    All units are in mm
    --------
    An optics is defined by: 
        start_position: the position of entering surface, 
        stop_position: the position of exiting surface,
        abcd_matrix: abcd matrix of the otpics
        part_name: name of the optical part
    -------
    the function for abcm_matrix are defined in "abcd.py"
    '''
    def __init__(self, start_position=0, stop_position=0, 
                 abcd_matrix=np.matrix([[1, 0], [0, 1]]), 
                 part_name="Optics_Part"):
        self.start_position=start_position
        self.stop_position=stop_position
        self.abcd_matrix=abcd_matrix
        self.part_name=part_name
#
class Lens(Optics):
    '''
    Thin Lens:
    '''
    def __init__(self, f=50.0, position=0.0, lens_name='lens'):
        _MLens = abcd.Mlens(f)
        super().__init__(start_position=position, 
                         stop_position=position, 
                         abcd_matrix=_MLens, 
                         part_name=lens_name)
#
class Interface(Optics):
    '''
    optical slab:
    n_in: the RI of the optical slab
    n_out: the RI of optical path out of the slab
    '''
    def __init__(self, thickness=1.0, n_in=1.5, n_out=1, center_positon=0.0, slab_name='slab'):
        _M1=abcd.Minterface(n_out,n_in)
        _M2=abcd.Mprop(thickness)
        _M3=abcd.Minterface(n_in,n_out)
        _M_slab= _M3*_M2*_M1
        super().__init__(start_position = center_positon - thickness/2.0, 
                         stop_position  = center_positon + thickness/2.0, 
                         abcd_matrix=_M_slab, 
                         part_name=slab_name)
        
        
class Interface(Optics):
        
        
        
        
        
        
        
        
        
        
        