# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 19:22:05 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

get_value_unit():           Get the values and units of the axis.
set_value_unit():           Set the values and units of the axis.

"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from technoteam import activex as ax
from variables import dicts as dic

def get_value_unit(image=dic.IMAGE_TYPES['Color']):
    """
    Get the values and units of the axis.|
    -------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :Image: int (default: IMAGE_TYPES['Color'])
            | Index of image
    Returns:
        :x_value: QString
            | Value of X axis
        :x_unit: QString
            | Unit of X axis
        :y_value: QString
            | Value of Y axis
        :y_unit: QString
            | Unit of Y axis
        :unit_area: QString
            | Unit of area
    """
    [err_code, x_value, x_unit, y_value, y_unit, unit_area] = ax.LMK.iCoordSystemGetValueUnit(image)
    ax.error_code(err_code) # Check for error

    return x_value, x_unit, y_value, y_unit, unit_area

def set_value_unit(image=dic.IMAGE_TYPES['Color'], x_value='x',
                   x_unit='pix', y_value='y', y_unit='pix', unit_area='pix^2'):
    """
    Set the values and units of the axis.|
    -------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Index of image
        :x_value: QString (default: 'x')
            | Value of X axis
        :x_unit: QString (default: 'pix')
            | Unit of X axis
        :y_value: QString (default: 'y')
            | Value of Y axis
        :y_unit: QString (default: 'pix')
            | Unit of Y axis
        :unit_area: QString (default: 'pix^2')
            | Unit of area
    """
    err_code = ax.LMK.iCoordSystemSetValueUnit(image, x_value, x_unit, y_value, y_unit, unit_area)
    ax.error_code(err_code) # Check for error
