# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 19:19:29 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
import ActiveX as ax
import Camera as cam

from win32com.client import Dispatch
import operator
import datetime

LMK = Dispatch('lmk4.LMKAxServer')

def SinglePic(AutoScan=True, ExposureTime=0.1):
    """
    SinglePic capture algorithm.|
    ----------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :ExposureTime: float (default: 0.1)
            | Exposure time to use
    """

    if AutoScan is True:
        ExposureTimes = cam.ColorAutoScanTime() # [REQUIRED if wanting best exposure times]
        err_code = LMK.iSinglePic2(max(ExposureTimes.items(), key=operator.itemgetter(1))[1])
    else:
        err_code = LMK.iSinglePic2(ExposureTime)
    ax.error_code(err_code) # Check for error

def MultiPic(AutoScan=True, ExposureTime=0.1, PicCount=1):
    """
    MultiPic capture algorithm.|
    ---------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :ExposureTime: float (default: 0.1)
            | Exposure time to use
        :PicCount: int (default: 1)
            | Number of camera images
    """

    if AutoScan is True:
        ExposureTimes = cam.ColorAutoScanTime() # [REQUIRED if wanting best exposure times]
        err_code = LMK.iMultiPic2(max(ExposureTimes.items(), key=operator.itemgetter(1))[1], PicCount)
    else:
        err_code = LMK.iMultiPic2(ExposureTime, PicCount)
    ax.error_code(err_code) # Check for error

def HighDynPic(AutoScan=True, ExposureTime=0.1, StartRatio=10.0, TimeRatio=3.0, PicCount=1):
    """
    HighDyn capturing for luminance image.|
    --------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :ExposureTime: float (default 0.1)
            | Exposure time to use
        :StartRatio: float (default: 10.0)
            | Exposure time is  multiplied with this parameter to determine
                the longest exposure time.
        :TimeRatio: float (default: 3.0)
            | The exposure time is decreased by this factor until there is
                no overdrive in the images captured
        :PicCount: int (default: 1)
            | Number of captures for every exposure time
    """

    if AutoScan is True:
        ExposureTimes = cam.ColorAutoScanTime() # [REQUIRED if wanting best exposure times]
        err_code = LMK.iHighDynPic3(max(ExposureTimes.items(),
                                        key=operator.itemgetter(1))[1],
                                    StartRatio, TimeRatio, PicCount)
    else:
        err_code = LMK.iHighDynPic3(ExposureTime, StartRatio, TimeRatio, PicCount)
    ax.error_code(err_code) # Check for error

def ColorHighDyn(AutoScan=True, MaxTime=15.0, MinTime=0.0, TimeRatio=3.0, PicCount=1):
    """
    HighDyn capturing for color image.|
    ----------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :MaxTime: float (defualt: 5.0)
            | Largest exposure time
        :MinTime: float (default: 0.0)
            | Smallest exposure time. Proposal: 0.0
        :TimeRatio: float (default: 3.0)
            | Factor between two times. Proposal: 3.0
        :PicCount: int (default: 1)
            | Number of shots per integration time
    """

    if AutoScan is True:
        ExposureTimes = cam.ColorAutoScanTime() # [REQUIRED if wanting best exposure times]
        err_code = LMK.iColorHighDynPic2(max(ExposureTimes.items(),
                                              key=operator.itemgetter(1))[1],
                                          MinTime, TimeRatio, PicCount)
    else:
        err_code = LMK.iColorHighDynPic2(MaxTime, MinTime, TimeRatio, PicCount)
    ax.error_code(err_code) # Check for error

def GetLastInfo():
    """
    Determine information about the preceeding capture.|
    ---------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :CaptureSuccess: int
            | 1 = successful
            | 0 = unsuccessful
        :CaptureType: int
            | 1 = SinglePic
            | 2 = MutliPic
            | 3 = HighDynPic
            | 4 = ColorHighDyn
        :GreyFilter: QString
            | 1 = Unused
        :ColorFilters: QString
            | List of color filters
        :PicCount: int
            | Number of camera images (MultiPic)
        :MaxExposureTime: float
            | Maximum exposure time
        :MinExposureTime: float
            | Minimum exposure time
        :PercentageOverdrivenPixels: float
            | Percentage of overdriven pixels
        :PercentageOverdrive: float
            | Percentage of overdrive
        :CaptureDateTime: float
            | Capture date and time as float number
        :SmearedImages: int
            | Number of smear images
        :ModulationFrequency: float
            | Modulation frequency
    """
    LastInfo = {'CaptureSuccess': [], 'CaptureType': [], 'GreyFilter': [],
                'ColorFilters': [], 'PicCount': [], 'MaxExposureTime': [],
                'MinExposureTime': [], 'PercentageOverdrivenPixels': [],
                'PercentageOverdrive': [], 'CaptureDateTime': [],
                'SmearedImages': [], 'ModulationFrequency': []}

    # Messy, sorts properly into a dictionary in correct types for now.
    err_code = LMK.iCaptureGetLastInfo()[0]
    ax.error_code(err_code) # Check for error

    LastInfo['CaptureSuccess'].append(LMK.iCaptureGetLastInfo()[1])
    LastInfo['CaptureSuccess'] = str(LastInfo['CaptureSuccess'])[1:-1]
    LastInfo['CaptureSuccess'] = int(LastInfo['CaptureSuccess'])

    LastInfo['CaptureType'].append(LMK.iCaptureGetLastInfo()[2])
    LastInfo['CaptureType'] = str(LastInfo['CaptureType'])[1:-1]
    LastInfo['CaptureType'] = int(LastInfo['CaptureType'])

    LastInfo['GreyFilter'].append(LMK.iCaptureGetLastInfo()[3])
    LastInfo['GreyFilter'] = str(LastInfo['GreyFilter'])[1:-1]

    LastInfo['ColorFilters'].append(LMK.iCaptureGetLastInfo()[4])
    LastInfo['ColorFilters'] = str(LastInfo['ColorFilters'])[1:-1]

    LastInfo['PicCount'].append(LMK.iCaptureGetLastInfo()[5])
    LastInfo['PicCount'] = str(LastInfo['PicCount'])[1:-1]
    LastInfo['PicCount'] = int(LastInfo['PicCount'])

    LastInfo['MaxExposureTime'].append(LMK.iCaptureGetLastInfo()[6])
    LastInfo['MaxExposureTime'] = str(LastInfo['MaxExposureTime'])[1:-1]
    LastInfo['MaxExposureTime'] = float(LastInfo['MaxExposureTime'])

    LastInfo['MinExposureTime'].append(LMK.iCaptureGetLastInfo()[7])
    LastInfo['MinExposureTime'] = str(LastInfo['MinExposureTime'])[1:-1]
    LastInfo['MinExposureTime'] = float(LastInfo['MinExposureTime'])

    LastInfo['PercentageOverdrivenPixels'].append(LMK.iCaptureGetLastInfo()[8])
    LastInfo['PercentageOverdrivenPixels'] = str(LastInfo['PercentageOverdrivenPixels'])[1:-1]
    LastInfo['PercentageOverdrivenPixels'] = float(LastInfo['PercentageOverdrivenPixels'])

    LastInfo['PercentageOverdrive'].append(LMK.iCaptureGetLastInfo()[9])
    LastInfo['PercentageOverdrive'] = str(LastInfo['PercentageOverdrive'])[1:-1]
    LastInfo['PercentageOverdrive'] = float(LastInfo['PercentageOverdrive'])

    LastInfo['CaptureDateTime'].append(LMK.iCaptureGetLastInfo()[10])
    LastInfo['CaptureDateTime'] = str(LastInfo['CaptureDateTime'])[1:-1]
    LastInfo['CaptureDateTime'] = float(LastInfo['CaptureDateTime'])
    seconds = (LastInfo['CaptureDateTime'] - 25569) * 86400.0
    LastInfo['CaptureDateTime'] = datetime.datetime.utcfromtimestamp(seconds)

    LastInfo['SmearedImages'].append(LMK.iCaptureGetLastInfo()[11])
    LastInfo['SmearedImages'] = str(LastInfo['SmearedImages'])[1:-1]
    LastInfo['SmearedImages'] = int(LastInfo['SmearedImages'])

    LastInfo['ModulationFrequency'].append(LMK.iCaptureGetLastInfo()[12])
    LastInfo['ModulationFrequency'] = str(LastInfo['ModulationFrequency'])[1:-1]
    LastInfo['ModulationFrequency'] = float(LastInfo['ModulationFrequency'])

    return LastInfo