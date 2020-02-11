# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:44:49 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

open_labsoft():             Opens the LMK4 application.
close_labsoft():            Closes the LMK4 application.
save():                     Save the measurement as a .ttcs file.
load():                     Load a measurement from a .ttcs file.
get_program_info():         Get some information about program version and
                                camera current used.

"""
from win32com.client import Dispatch
import os
import datetime

import activex as ax
import dicts as dic

MEAS_ROOT = 'E:/Measurements/' + str(datetime.date.today()) + '/'

def open_labsoft():
    """
    Opens the LMK4 application.|
    ---------------------------
    After opening, the main window is visible.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    """
    ax.LMK = Dispatch('lmk4.LMKAxServer')
    err_code = ax.LMK.iOpen()
    ax.error_code(err_code) # Check for error

def close_labsoft(question=0):
    """
    Closes the LMK4 application.|
    ----------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :question: int, optional
            | !0 = Opens a dialogue window in the application. The user can
                    choose whether they wish to save the current state or not
                    or cancel the closing of the program.
            | 0 = No dialogue window
    """
    err_code = ax.LMK.iClose(question)
    ax.error_code(err_code) # Check for error

def save(file_name=MEAS_ROOT + \
         datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
         dic.FILE_TYPES['ttcs']):
    """
    Save the measurement as a .ttcs file.|
    -------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :file_name: QString, optional (default: MEAS_ROOT + datetime + .ttcs')
            | Change to adjust root to save measurement
            | Datetime is the exact datetime of the measurement, not datetime when saved.
    """
    if not os.path.exists(MEAS_ROOT):
        os.makedirs(MEAS_ROOT)
    err_code = ax.LMK.iSaveProtokoll(file_name)
    ax.error_code(err_code) # Check for error

def load(file_name='Meas.ttcs'):
    """
    Load a measurement from a .ttcs file.|
    -------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :file_name: QString, optional (default: 'Meas.ttcs')
            | Change to adjust root to load measurement
    """
    err_code = ax.LMK.iLoadProtokoll(file_name)
    ax.error_code(err_code) # Check for error

def get_program_info():
    """

    Get some information about program version and camera current used.|
    -------------------------------------------------------------------

    Parameters
    ----------
    LMK :
        Dispatch('lmk4.LMKAxServer')

    Returns
    -------
    program_type : QString
        Type of program version
    program_version : QString
        Number of program version
    camera_type : QString
        Type of camera
    camera_no : QString
        Number of camera
    lens_no : QString
        Number of lens

    """

    err_code, program_type, program_version, camera_type, camera_no, lens_no = ax.LMK.iGetProgramInfo()
    ax.error_code(err_code) # Check for error

    return program_type, program_version, camera_type, camera_no, lens_no
