r"""
Used to configure the main parameters for each implemented model.

.. currentmodule:: compmech.stiffener.modelDB


"""
from __future__ import absolute_import

from . models import *
from compmech.panel.models import (cpanel_clt_donnell_bardell,
                                   cpanel_clt_donnell_bardell_field,
                                   plate_clt_donnell_bardell,
                                   plate_clt_donnell_bardell_field)
db = {
    'bladestiff1d_clt_donnell_bardell': {
                    'linear static': True,
                    'linear buckling': True,
                    'non-linear static': False,
                    'matrices': bladestiff1d_clt_donnell_bardell,
                    'dofs': 3,
                    'e_num': 6,
                    'num1': 3,
                    },
    'bladestiff2d_clt_donnell_bardell': {
                    'linear static': True,
                    'linear buckling': True,
                    'non-linear static': False,
                    'field_flange': plate_clt_donnell_bardell_field,
                    'matrices': bladestiff2d_clt_donnell_bardell,
                    'dofs': 3,
                    'e_num': 6,
                    'num1': 3,
                    },
    'tstiff2d_clt_donnell_bardell': {
                    'linear static': True,
                    'linear buckling': True,
                    'non-linear static': False,
                    #'field_base': None, # must be defined at runtime
                    'field_flange': plate_clt_donnell_bardell_field,
                    #'matrices_base': None, # must be defined at runtime
                    'matrices_flange': plate_clt_donnell_bardell,
                    'connections': tstiff2d_clt_donnell_bardell,
                    'dofs': 3,
                    'e_num': 6,
                    'num1': 3,
                    'num2': 3,
                    },
    }
