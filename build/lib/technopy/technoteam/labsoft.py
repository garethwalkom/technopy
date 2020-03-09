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
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import variables.dicts as dic
import technoteam.activex as ax

def open_labsoft():
    """
    Opens the LMK4 application.|
    ---------------------------
    After opening, the main window is visible.
    -----------------------------------------------------------------------

    %timeit:
        2.41 s ± 75.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    Returns
    -------
    None.

    """
    err_code = ax.LMK.iOpen()
    ax.error_code(err_code) # Check for error

def close_labsoft(question=0):
    """
    Closes the LMK4 application.|
    ----------------------------

    Parameters
    ----------
    question : int, optional
        The default is 0.
        !0 = Opens a dialogue window in the application. The user can
                    choose whether they wish to save the current state or not
                    or cancel the closing of the program.
        0 = No dialogue window.

    Returns
    -------
    None.

    """

    err_code = ax.LMK.iClose(question)
    ax.error_code(err_code) # Check for error

def save(save_root, file_name):
    """
    Save the measurement as a .ttcs file.|
    -------------------------------------

    Parameters
    ----------
    save_root : QString
        Change to adjust root to save measurement.
    file_name : QString
        Change to adjust name of measurement.

    Returns
    -------
    None.

    """

    if not os.path.exists(save_root):
        os.makedirs(save_root)
    err_code = ax.LMK.iSaveProtokoll(save_root + file_name + \
                                     dic.FILE_TYPES['ttcs'])
    ax.error_code(err_code) # Check for error

def load(load_root, file_name):
    """
    Load a measurement from a .ttcs file.|
    -------------------------------------

    Parameters
    ----------
    load_root : TYPE
        Change to adjust root to load measurement.
    file_name : TYPE
        Change to adjust name of measurement.

    Returns
    -------
    None.

    """

    err_code = ax.LMK.iLoadProtokoll(load_root + file_name)
    ax.error_code(err_code) # Check for error

def get_program_info():
    """

    Get some information about program version and camera current used.|
    -------------------------------------------------------------------

    %timeit:
        144 µs ± 5.82 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

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

    err_code, program_type, program_version, camera_type, camera_no, lens_no = \
        ax.LMK.iGetProgramInfo()
    ax.error_code(err_code) # Check for error

    return program_type, program_version, camera_type, camera_no, lens_no
