# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 19:19:29 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

single_pic():               SinglePic capture algorithm.
multi_pic():                MultiPic capture algorithm.
high_dyn_pic():             HighDyn capturing for luminance image.
color_high_dyn():           HighDyn capturing for color image.
get_last_info():            Determine information about the preceeding capture.


"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import operator
import datetime

from technoteam import activex as ax
from technoteam import camera as cam

def single_pic(autoscan=True, exposure_time=0.1):
    """
    SinglePic capture algorithm.|
    ----------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :exposure_time: float (default: 0.1)
            | Exposure time to use
    """

    if autoscan is True:
        exposure_times = cam.color_autoscan_time() # [REQUIRED if wanting best exposure times]
        err_code = ax.LMK.iSinglePic2(max(exposure_times.items(), key=operator.itemgetter(1))[1])
    else:
        err_code = ax.LMK.iSinglePic2(exposure_time)
    ax.error_code(err_code) # Check for error

def multi_pic(autoscan=True, exposure_time=0.1, pic_count=1):
    """
    MultiPic capture algorithm.|
    ---------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :exposure_time: float (default: 0.1)
            | Exposure time to use
        :pic_count: int (default: 1)
            | Number of camera images
    """

    if autoscan is True:
        exposure_times = cam.color_autoscan_time() # [REQUIRED if wanting best exposure times]
        err_code = ax.LMK.iMultiPic2(max(exposure_times.items(), \
                                      key=operator.itemgetter(1))[1], pic_count)
    else:
        err_code = ax.LMK.iMultiPic2(exposure_time, pic_count)
    ax.error_code(err_code) # Check for error

def high_dyn_pic(autoscan=True, exposure_time=0.1, start_ratio=10.0, time_ratio=3.0, pic_count=1):
    """
    HighDyn capturing for luminance image.|
    --------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :exposure_time: float (default 0.1)
            | Exposure time to use
        :start_ratio: float (default: 10.0)
            | Exposure time is  multiplied with this parameter to determine
                the longest exposure time.
        :time_ratio: float (default: 3.0)
            | The exposure time is decreased by this factor until there is
                no overdrive in the images captured
        :pic_count: int (default: 1)
            | Number of captures for every exposure time
    """

    if autoscan is True:
        exposure_times = cam.color_autoscan_time() # [REQUIRED if wanting best exposure times]
        err_code = ax.LMK.iHighDynPic3(max(exposure_times.items(),
                                        key=operator.itemgetter(1))[1],
                                    start_ratio, time_ratio, pic_count)
    else:
        err_code = ax.LMK.iHighDynPic3(exposure_time, start_ratio, time_ratio, pic_count)
    ax.error_code(err_code) # Check for error

def color_high_dyn(autoscan=True, max_time=15.0, min_time=0.0, time_ratio=3.0, pic_count=1):
    """
    HighDyn capturing for color image.|
    ----------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :max_time: float (defualt: 5.0)
            | Largest exposure time
        :min_time: float (default: 0.0)
            | Smallest exposure time. Proposal: 0.0
        :time_ratio: float (default: 3.0)
            | Factor between two times. Proposal: 3.0
        :pic_count: int (default: 1)
            | Number of shots per integration time
    """

    if autoscan is True:
        exposure_times = cam.color_autoscan_time() # [REQUIRED if wanting best exposure times]
        err_code = ax.LMK.iColorHighDynPic2(max(exposure_times.items(),
                                             key=operator.itemgetter(1))[1],
                                         min_time, time_ratio, pic_count)
    else:
        err_code = ax.LMK.iColorHighDynPic2(max_time, min_time, time_ratio, pic_count)
    ax.error_code(err_code) # Check for error

def get_last_info():
    """
    Determine information about the preceeding capture.|
    ---------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :capture_success: int
            | 1 = successful
            | 0 = unsuccessful
        :capture_type: int
            | 1 = SinglePic
            | 2 = MutliPic
            | 3 = HighDynPic
            | 4 = ColorHighDyn
        :grey_filter: QString
            | 1 = Unused
        :color_filters: QString
            | List of color filters
        :pic_count: int
            | Number of camera images (MultiPic)
        :max_exposure_time: float
            | Maximum exposure time
        :min_exposure_time: float
            | Minimum exposure time
        :percentage_overdriven_pixels: float
            | Percentage of overdriven pixels
        :percentage_overdrive: float
            | Percentage of overdrive
        :capture_date_time: float
            | Capture date and time as float number
        :smeared_images: int
            | Number of smear images
        :modulation_frequency: float
            | Modulation frequency
    """
    last_info = {'CaptureSuccess': [], 'CaptureType': [], 'GreyFilter': [],
                 'ColorFilters': [], 'PicCount': [], 'MaxExposureTime': [],
                 'MinExposureTime': [], 'PercentageOverdrivenPixels': [],
                 'PercentageOverdrive': [], 'CaptureDateTime': [],
                 'SmearedImages': [], 'ModulationFrequency': []}

    # Messy, sorts properly into a dictionary in correct types for now.
    err_code = ax.LMK.iCaptureGetlast_info()[0]
    ax.error_code(err_code) # Check for error

    last_info['CaptureSuccess'].append(ax.LMK.iCaptureGetlast_info()[1])
    last_info['CaptureSuccess'] = str(last_info['CaptureSuccess'])[1:-1]
    last_info['CaptureSuccess'] = int(last_info['CaptureSuccess'])

    last_info['CaptureType'].append(ax.LMK.iCaptureGetlast_info()[2])
    last_info['CaptureType'] = str(last_info['CaptureType'])[1:-1]
    last_info['CaptureType'] = int(last_info['CaptureType'])

    last_info['GreyFilter'].append(ax.LMK.iCaptureGetlast_info()[3])
    last_info['GreyFilter'] = str(last_info['GreyFilter'])[1:-1]

    last_info['ColorFilters'].append(ax.LMK.iCaptureGetlast_info()[4])
    last_info['ColorFilters'] = str(last_info['ColorFilters'])[1:-1]

    last_info['PicCount'].append(ax.LMK.iCaptureGetlast_info()[5])
    last_info['PicCount'] = str(last_info['PicCount'])[1:-1]
    last_info['PicCount'] = int(last_info['PicCount'])

    last_info['MaxExposureTime'].append(ax.LMK.iCaptureGetlast_info()[6])
    last_info['MaxExposureTime'] = str(last_info['MaxExposureTime'])[1:-1]
    last_info['MaxExposureTime'] = float(last_info['MaxExposureTime'])

    last_info['MinExposureTime'].append(ax.LMK.iCaptureGetlast_info()[7])
    last_info['MinExposureTime'] = str(last_info['MinExposureTime'])[1:-1]
    last_info['MinExposureTime'] = float(last_info['MinExposureTime'])

    last_info['PercentageOverdrivenPixels'].append(ax.LMK.iCaptureGetlast_info()[8])
    last_info['PercentageOverdrivenPixels'] = str(last_info['PercentageOverdrivenPixels'])[1:-1]
    last_info['PercentageOverdrivenPixels'] = float(last_info['PercentageOverdrivenPixels'])

    last_info['PercentageOverdrive'].append(ax.LMK.iCaptureGetlast_info()[9])
    last_info['PercentageOverdrive'] = str(last_info['PercentageOverdrive'])[1:-1]
    last_info['PercentageOverdrive'] = float(last_info['PercentageOverdrive'])

    last_info['CaptureDateTime'].append(ax.LMK.iCaptureGetlast_info()[10])
    last_info['CaptureDateTime'] = str(last_info['CaptureDateTime'])[1:-1]
    last_info['CaptureDateTime'] = float(last_info['CaptureDateTime'])
    seconds = (last_info['CaptureDateTime'] - 25569) * 86400.0
    last_info['CaptureDateTime'] = datetime.datetime.utcfromtimestamp(seconds)

    last_info['SmearedImages'].append(ax.LMK.iCaptureGetlast_info()[11])
    last_info['SmearedImages'] = str(last_info['SmearedImages'])[1:-1]
    last_info['SmearedImages'] = int(last_info['SmearedImages'])

    last_info['ModulationFrequency'].append(ax.LMK.iCaptureGetlast_info()[12])
    last_info['ModulationFrequency'] = str(last_info['ModulationFrequency'])[1:-1]
    last_info['ModulationFrequency'] = float(last_info['ModulationFrequency'])

    return last_info
