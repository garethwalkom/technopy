# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:38:59 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

error_code():               Prints error code if error occurs.

"""
from win32com.client import Dispatch

LMK = Dispatch('lmk4.LMKAxServer')

def error_code(err_code):
    """
    Prints error code if error occurs.|
    ----------------------------------

    %timeit:
        563 µs ± 15.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

    Parameters:
        :err_code: int
            | Error code from ActiveX server.
            | 0 = Continue with no error.
            | !0 = Error with function from ActiveX server.
    """
    if err_code != 0:
        print('Error code:', err_code, '\n')
        _, error_info = LMK.iGetErrorInformation()
        print('Error info:', error_info)
