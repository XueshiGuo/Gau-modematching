import math
import operator
import os
#
from .memory import MemoryTree
from .optics import *
from . import abcd
import numpy as np
#
from numpy import pi, conj
from collections import OrderedDict as OD
#
def mode_overlap_q(q1, q2, lam=0.001552):
    """
    Mode overlap (power transmission) between two coaxial Gaussian beams.
    see: Applied Opitcs Volume 23 Page 4187: Alignment of Gaussian beams
    Parameters
    ----------
    q1, q1 : complex
        q parameters of the two beams in the same positon.

    Returns
    -------
    float
    """
    w0_1 = abcd.q2w0(q1)
    w0_2 = abcd.q2w0(q2)
    _s  = np.real(q1)-np.real(q2)
    return 4 / ((w0_1/w0_2 + w0_2/w0_1)**2 + (_s*lam/np.pi)**2/(w0_1**2 * w0_2**2))
#
#
class Gaussian_Beam(object):
    '''
    All units are in mm
    --------
    A Gaussian Beam is defined by: 
        w0: waist radius, 
        z0: waist position,
        lam: wavelength
        n: refrective index out of optics
        beam_name: name of the beam
    -------
    class methods are defined to init. a Gau. in a diff. way
    '''
    def __init__(self, w0=1, z0=0, lam=0.001552, n=1.0, beam_name="beam"):
        self.w0 = w0
        self.z0 = z0
        self.lam = lam
        self.n = n # here n is the RI of the media out of optics
        self.q0 = abcd.w02q(w0=self.w0, n=self.n)
        self.zR = w0**2*pi*n/lam
        self.div = abcd.q2div(q=self.q0, n=self.n)
        self.beam_name=beam_name
    #
    @classmethod
    def from_q(cls, q, z , lam=0.001552, n=1.0, beam_name="beam"):
        w0_ = abcd.q2w0(q)
        z0_ = z-np.real(q)
        return cls(w0_, z0_, lam, n, beam_name)
    #
    @classmethod
    def from_w_div(cls, w, z, div, lam=0.001552, n=1.0, beam_name="beam"):
        '''
        div: divergance in the unit of degree, positive sign denotes diverging z
        w, z: beam radius "w" at a position "z" in the unit of millimeter
        '''
        w0_ = lam/np.tan(div*np.pi/180)/n/pi
        zR_ = w0_**2*pi*n/lam
        z0_ = z-np.sqrt((w/w0_)**2-1.0) * zR_
        return cls(w0_, z0_, lam, n, beam_name)
    #
    def get_w(self,z):
        p_= abs(self.z0-z)
        return self.w0*np.sqrt(1.0 + (p_ / self.zR)**2 )
    #
    def get_R(self,z):
        p_= abs(self.z0-z)
        return p_*(1.0 + (self.zR / p_)**2 )
#
class Optical_Path(object):
    '''
    All the lengths are in the unit of millimeter
    optics_list: list of optics sorted by start position
    beam_list: list of Gaussian beam sorted by waist position
    path_length: the range of the date for beam ploting is from 0 to path_length
    MemTree: A MemoryTree object that is used to create the optical path.
    OP_name: the name of the optical path
    '''
    def __init__(self, optics_dict=OD(), beam_dict=OD(),
                 path_length=500.0, MemTree = None, OP_name="Path"):
        self.optics_dict= optics_dict
        self.beam_dict= beam_dict
        self.path_length=path_length
        if MemTree == None or type(MemTree) == MemoryTree:
            self.in_MemTree = MemTree # read from .yml
        else:
            raise TypeError('MemTree should be a MemoryTree object from .yml file')
    #
    @classmethod
    def load_yml(cls, filename='default'):
        '''
        create optical path from .yml file (file name should not contain .yml)
        '''
        _configdir = os.path.join(os.path.dirname(__file__), "optical_path_config")
        _file = os.path.join(_configdir, filename+'.yml')
        _c = MemoryTree(_file)
        return cls.from_MemTree(_c)
    #
    @classmethod
    def from_MemTree(cls,MemTree):
        if not type(MemTree) == MemoryTree:
            raise TypeError("a MemTree for optical path is needed")
        _beam = MemTree.beam
        _optics = MemTree.optics
        # add lens
        _optics_dict={}
        for x in _optics._dict.keys():
            if x.split('_')[0] == 'lens':
                _position = float(_optics[x]['position'])
                _focal = float(_optics[x]['focal_length'])
                _lens=Optics(start_position=_position,stop_position=_position, 
                             abcd_matrix=abcd.Mlens(_focal), part_name=x)
                _optics_dict[_lens.part_name]=_lens
        _OD_optics_dict=OD(sorted(_optics_dict.items(), key=lambda x: x[1].start_position))
        # add beam
        _beam_dict={}
        for x in _beam._dict.keys():
            if _beam[x]['initialize_method']=='w_z_div':
                #
                _Gau1 = Gaussian_Beam.from_w_div(w = _beam[x]['w_z'][0],
                                                 z = _beam[x]['w_z'][1],
                                                 div = _beam[x]['div'],
                                                 lam = _beam[x]['wavelength'],
                                                 n = _beam[x]['refrective_n'],
                                                 beam_name = x)
                #
                _beam_dict[_Gau1.beam_name]=_Gau1
            #
            elif _beam[x]['initialize_method']=='w0_z0':
                #
                _Gau2 = Gaussian_Beam(w0=_beam[x]['w0_z0'][0],
                                      z0=_beam[x]['w0_z0'][1], 
                                      lam=_beam[x]['wavelength'],
                                      n=_beam[x]['refrective_n'],
                                      beam_name=x)
                #
                _beam_dict[_Gau2.beam_name]=_Gau2
        _OD_beam_dict=OD(sorted(_beam_dict.items(), key=lambda x: x[1].z0))
        #
        _path_length = MemTree.general.path_length
        #
        return cls(_OD_optics_dict, _OD_beam_dict, _path_length, MemTree)      
    #
    def show_path(self):
        p1="Optics --- "
        print(p1)
        for x in self.optics_dict.values():
            print( '\t'+x.part_name +": @" + str(x.start_position) )
        p2="Beams --- "
        print(p2)
        for x in self.beam_dict.values():
            print( '\t'+x.beam_name +": z0 " + str(x.z0) + " w0 "+ str(x.w0))
    #
    def plotdata_OP(self, points=500):
        '''
        # return the data for plot the optical path
        '''
        '''
        # generate the list for optics elements
        _Olist=[]
        for o in self.optics_list:
            if o.start_position == o.stop_position:
                _o_conponent=[o.start_position, o.abcd_matrix]
            _Olist.append(_o_conponent)
        '''
        # generate x to plot
        zs_to_plot = np.linspace(0, self.path_length+10, points)
        # generate y to plot from each Gaussian beam
        _Bplot=[]
        for b in self.beam_dict.values():
            w_to_plot=[abcd.q2w(abcd.qpropagate(b.z0, b.q0, self.Olist_qp, z)) for z in zs_to_plot]
            _Bplot.append(w_to_plot)
        return [zs_to_plot,_Bplot]
    #
    @property
    def Olist_qp(self):
        # generate the list that can be sent to abcd.qpropagate
        _Olist=[]
        for o in self.optics_dict.values():
            if o.start_position == o.stop_position:
                _o_conponent=[o.start_position, o.abcd_matrix]
            _Olist.append(_o_conponent)
        return _Olist
    #
    @property
    def modematching(self):
        _q_list_at_OP_end=[]
        _matching_list=[]
        # ulgy work around, lam should be alsways the same for each beam
        #----------------------------------------------#
        for _index, b in enumerate(self.beam_dict.values()):
            _q_m = abcd.qpropagate(b.z0, b.q0, self.Olist_qp, self.path_length)
            _q_list_at_OP_end.append(_q_m)
            if _index>0:
                _m = mode_overlap_q(_q_list_at_OP_end[_index],
                                _q_list_at_OP_end[_index-1],
                                b.lam)
                _matching_list.append(_m)
        #----------------------------------------------#    
        return _matching_list
    #
    def move_beam(self, beamname='', dz=0.0):
        try:
            self.beam_dict[beamname].z0 += dz
        except:
            raise KeyError('KeyError: Beam Name is not found')
    #
    def move_optics(self, opticsname='', dz=0.0):
        try:
            self.optics_dict[opticsname].start_position += dz
            self.optics_dict[opticsname].stop_position += dz
        except:
            raise KeyError('KeyError: Optics Name is not found')