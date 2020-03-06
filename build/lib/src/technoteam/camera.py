# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 19:08:19 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

get_cameras():
set_camera():
get_lenses():
set_lens():
lenses():                   Gets list of all lenses of selected camera.
lens():                     Gets ID of selected lens.
get_focus_factors():        Gets list of all focus factors of current lens.
get_focus_factors_old():    List of available focus factors
get_focus_factor_id():      Gets ID of selected focus factor.
set_focus_factor():         Set a focus factor.
open_camera():              Set new camera calibration data.
get_converting_units():     Get converting information.
set_converting_units():     Set new converting values.
get_modulation_frequency(): Get the modulation frequency.
set_modulation_frequency(): Set the frequency of modulated light.
get_scattered_light():      Is scattered light correction switched on?
set_scattered_light():      Use of scattered light correction.
get_integration_time():     Determine current exposure time and other time parameters.
set_integration_time():     Set new exposure time.
get_max_camera_time():      Determine the maximum possible exposure time.
set_max_camera_time():      Set the maximum possible exposure time.
get_autoscan():             Get use of autoscan algorithm.
set_autoscan():             Set use of autoscan algorithm.
get_filter_wheel():         Determine filter state.
get_grey_filter_list():     List of available grey filters.
set_grey_filter_list():     Set grey filters.
set_grey_filter():          Selection of a grey filter.
color_autoscan_time():      Determine good exposure times for every color filter.
get_color_correction_list():List of available color correction factors.
set_color_correction_list():Selection of a color correction factor.
get_smear():                Get the parameter for smear correction.
set_smear():                Set the parameter for smear correction.
get_automatic():            Get the state of Automatic-Flag for exposure times.
set_automatic():            Set Automatic-Flag for all exposure times.

"""
import sys
import os
import glob
import configparser
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import change_this.roots as root
import technoteam.activex as ax
import variables.dicts as dic

# Name of the TechnoTeam LMK Camera
CAMERA_NAME = str(os.listdir(root.DATA))[2:-2]

def get_cameras():
    """
    [ADD THIS]

    Returns
    -------
    cameras : TYPE
        DESCRIPTION.

    """

    print('Cameras:')
    for cameras in dic.CAMERA_NAMES.keys():
        print(cameras)

    return cameras

def set_camera(camera=None):
    """
    [ADD THIS]

    Parameters
    ----------
    camera : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    camera : TYPE
        DESCRIPTION.
    camera_no : TYPE
        DESCRIPTION.

    """

    if camera is None:
        print('Cameras:')
        for cameras in dic.CAMERA_NAMES.keys():
            print(cameras)

        camera = input('Input chosen camera: ')

    camera_no = dic.CAMERA_NAMES[camera]

    return camera, camera_no

def get_lenses(camera):
    """
    [ADD THIS]

    Parameters
    ----------
    camera : TYPE
        DESCRIPTION.

    Returns
    -------
    lenses : TYPE
        DESCRIPTION.

    """

    print('Lenses:')

    if camera == 'Old':
        for lenses in dic.OLD_LENSES.keys():
            print(lenses)
    elif camera == 'VR':
        for lenses in dic.VR_LENSES.keys():
            print(lenses)
    elif camera == 'Hyperspectral':
        for lenses in dic.HYPERSPECTRAL_LENSES.keys():
            print(lenses)

    return lenses

def set_lens(camera, lens=None):
    """
    [ADD THIS]

    Parameters
    ----------
    camera : TYPE
        DESCRIPTION.
    lens : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    lens : TYPE
        DESCRIPTION.
    lens_no : TYPE
        DESCRIPTION.

    """

    if lens is None:
        print('Lenses:')
        if camera == 'Old':
            for lenses in dic.OLD_LENSES.keys():
                print(lenses)
        elif camera == 'VR':
            for lenses in dic.VR_LENSES.keys():
                print(lenses)
        elif camera == 'Hyperspectral':
            for lenses in dic.HYPERSPECTRAL_LENSES.keys():
                print(lenses)

        lens = input('Input chosen lens: ')

    if camera == 'Old':
        lens_no = dic.OLD_LENSES[lens]
    elif camera == 'VR':
        lens_no = dic.VR_LENSES[lens]
    elif camera == 'Hyperspectral':
        lens_no = dic.HYPERSPECTRAL_LENSES[lens]


    return lens, lens_no

def lenses():
    """
    Gets list of all lenses of selected camera.|
    -------------------------------------------
    """

    global LENSES

    LENSES = []

    for lens in glob(root.DATA + '/' + CAMERA_NAME + '/*/'):
        LENSES.append(lens.split('\\')[1])

    return LENSES

def lens(current_lens='12'):
    """
    Gets ID of selected lens.|
    -------------------------
    """

    global LENS_ID

    lens = []

    for lenses in range(len(LENSES)):
        lens.append(LENSES[lenses].split('f')[1])

    if current_lens in lens:
        LENS_ID = (lens.index(current_lens))

    return LENS_ID

def get_focus_factors():
    """
    Gets list of all focus factors of current lens.|
    -----------------------------------------------
    """

    all_lenses = lenses()

    current_lens_id = lens(all_lenses)
    current_lens = all_lenses[current_lens_id]

    focus_factors = []

    config = configparser.ConfigParser()
    config.read(root.DATA + '/' + CAMERA_NAME + '/' +
                current_lens + '/' + 'FocusFactor' + dic.FILE_TYPES['ini'])
    focus_factors_size = config.get('GreyFactor', 'Size')
    focus_factors_size = int(focus_factors)
    for focus_factor in range(focus_factors_size):
        focus_factor = str(focus_factor + 1)
        focus_factors.append(config.get('GreyFactor/' + focus_factor, 'Name'))

    return focus_factors, focus_factors_size

def get_focus_factors_old():
    """
    List of available focus factors.|
    --------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :focus_factors: QStringList
            | List of focus factors
        :focus_factor: int
            | Index of current focus factor
    """
    err_code, focus_factors, focus_factor = ax.LMK.iGetFocusFactorList()
    ax.error_code(err_code) # Check for error

    return focus_factors, focus_factor

def get_focus_factor_id(focus_factors, scale='infinite'):
    """
    Gets ID of selected focus factor.|
    ---------------------------------
    """

    focus_factor = []

    for focus in range(len(focus_factors)):
        focus_factor.append(focus_factors[focus].split(' ')[2])

    if scale in focus_factor:
        focus_factor_id = (focus_factor.index(scale))

    return focus_factor_id

def set_focus_factor():
    """
    Set a focus factor.|
    -------------------
    See dialog "Camera|Recalibration" in LabSoft main menu.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :focus_factor: int
            | Index of focus factor
    """
    focus_factors, _ = get_focus_factors()
    focus_factor_id = get_focus_factor_id(focus_factors)
    err_code = ax.LMK.iSetFocusFactor(focus_factor_id)
    ax.error_code(err_code) # Check for error

def get_filter_wheels():
    """
    [ADD THIS]

    Returns
    -------
    filter_wheel_max : TYPE
        DESCRIPTION.
    filter_wheel_names : TYPE
        DESCRIPTION.

    """

    config = configparser.ConfigParser()
    config.read(root.DATA + '/' + dic.CAMERA_NAMES['Hyperspectral'] + '/' + \
                'camera' + dic.FILE_TYPES['ini'])
    filter_wheel_max = config.get('PropertyList', 'FILTER_WHEEL_MAX')
    filter_wheel_names = config.get('PropertyList', 'FILTER_WHEEL_NAMES')
    filter_wheel_names = filter_wheel_names.split(' ')
    filter_wheel_names = np.vstack(filter_wheel_names).astype(int)

    return filter_wheel_max, filter_wheel_names

def open_camera(camera_no, lens_no):
    """
    Set new camera calibration data.|
    --------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :root.DATA: QString (default: root.DATA)
            | Path to the camera calibration data. More exactly spoken path
                to the lens sub directory. After calling this function the
                camera is completely reinitialized.
            | If the string is empty a currently existing camera connection
                is finished.
    """
    err_code = ax.LMK.iSetNewCamera(root.DATA + '/' + camera_no + '/' + lens_no)
    ax.error_code(err_code) # Check for error

def get_converting_units():
    """
    Get converting information.|
    ---------------------------
    See dialog "Camera|Recalibration" in LabSoft main menu.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :units_name: QString (default: 'L')
            | Units Name used
        :units: QString (default: 'cd/m^2')
            | Units used
        :units_factor: float (default: 1.0)
            | Units factor used
    """
    err_code, units_name, units, units_factor = ax.LMK.iGetConvertingUnits()
    ax.error_code(err_code) # Check for error

    return units_name, units, units_factor

def set_converting_units(units_name='L', units='cd/m^2', units_factor=1.0):
    """
    Set new converting values.|
    --------------------------
    See dialog "Camera|Recalibration" in LabSoft main menu.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :units_name: QString (default: 'L')
            | Wished units name
        :units: QString (default: 'cd/m^2')
            | Wished units
        :units_factor: float (default: 1.0)
            | Wished units factor
    """
    err_code = ax.LMK.iSetConvertingUnits(units_name, units, units_factor)
    ax.error_code(err_code) # Check for error

def get_modulation_frequency():
    """
    Get the modulation frequency.|
    -----------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :modulation_frequency: float
            | Frequency of light source
            | 0 = no modulation is to be concerned
    """
    err_code, modulation_frequency = ax.LMK.iGetModulationFrequency()
    ax.error_code(err_code) # Check for error

    return modulation_frequency

def set_modulation_frequency(modulation_frequency=90.0):
    """
    Set the frequency of modulated light.|
    -------------------------------------
    If the light source is driven by alternating current, there are some
    restriction for the exposure times. Please inform the program about
    the modulation frequency.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :modulation_frequency: float (default: 90.0)
            | Frequency of light source
            | 0 = no modulation is to be concerned
    """
    err_code = ax.LMK.iSetModulationFrequency(modulation_frequency)
    ax.error_code(err_code) # Check for error

def get_scattered_light():
    """
    Is scattered light correction switched on?|
    ------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :ScatteredLight: int
            | 1 = scattered light correction is switched on
            | 0 = scattered light correction is switched off
    """
    err_code, scattered_light = ax.LMK.iGetScatteredLight()
    ax.error_code(err_code) # Check for error

    return scattered_light

def set_scattered_light(scattered_light=1):
    """
    Use of scattered light correction.|
    ----------------------------------
    Only usable if a parameter set is available in program.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :scattered_light: int (defualt: 1)
            | 1 = switch on scattered light correction
            | 0 = switch off scattered light correction
    """
    err_code = ax.LMK.iSetScatteredLight(scattered_light)
    ax.error_code(err_code) # Check for error

def get_integration_time():
    """
    Determine current exposure time and other parameters.|
    -----------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :current_time: float
            | Current integration time
        :previous_time: float
            | Next smaller (proposed) time
        :next_time: float
            | Next larger (proposed) time
        :min_time: float
            | Minimal possible time
        :max_time: float
            | Maximal possible time
    """
    err_code, current_time, previous_time, next_time, min_time, max_time = \
        ax.LMK.iGetIntegrationTime()
    ax.error_code(err_code) # Check for error

    return current_time, previous_time, next_time, min_time, max_time

def set_integration_time(wished_time=5.0):
    """
    Set new exposure time.|
    ----------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :wished_time: float (default: 5.0)
            | Wished integration time
    Returns
        :IntegrationTime: float
            | Realized integration time
    """
    err_code, integration_time = ax.LMK.iSetIntegrationTime(wished_time)
    ax.error_code(err_code) # Check for error

    return integration_time

def get_max_camera_time():
    """
    Determine the maximum possible exposure time.|
    ---------------------------------------------
    Normally this time is restricted by camera properties. In some cases it
    could be useful to use an even smaller maximum exposure time.
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns
        :max_time: float
            | Current maximum time
    """
    err_code, max_time = ax.LMK.iGetMaxCameraTime()
    ax.error_code(err_code) # Check for error

    return max_time

def set_max_camera_time(max_time=5.0):
    """
    Set the maximum possible exposure time.|
    ---------------------------------------
    The maximum values is of course restricted by camera properties. But
    you can use an even smaller time to avoid to long meausrement times.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :max_time: float (default: 5.0)
            | Wished value
    """
    err_code = ax.LMK.iSetMaxCameraTime(max_time)
    ax.error_code(err_code) # Check for error

def get_autoscan():
    """
    Get use of autoscan algorithm.|
    ------------------------------
    Is autoscan switched on?
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :autoscan: int
            | 1 = autoscan is switched on
            | 0 = autoscan is switched off
    """
    err_code, autoscan = ax.LMK.iGetAutoscan()
    ax.error_code(err_code) # Check for error

    return autoscan

def set_autoscan(autoscan=1):
    """
    Set use of autoscan algorithm.|
    ------------------------------
    Determination of a good exposure time before the capturing algorithm.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :autoscan: int (default: 1)
            | 1 = Use autoscan
              0 = Do not use autoscan
    """
    err_code = ax.LMK.iSetAutoscan(autoscan)
    ax.error_code(err_code) # Check for error

def get_filter_wheel():
    """
    Determine filter state.|
    -----------------------
    If there is no filter wheel, the function returns an error code.
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :current_filter_pos: int
            | Position of filter wheel
        :current_filter_name: QString
            | Name of current filter
    """
    err_code, current_filter_pos, current_filter_name = ax.LMK.iGetFilterWheel()
    ax.error_code(err_code) # Check for error

    return current_filter_pos, current_filter_name

def set_filter_wheel(filter_pos):
    """
    [ADD THIS]

    Parameters
    ----------
    filter_pos : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    err_code = ax.LMK.iSetFilterWheel(filter_pos)
    ax.error_code(err_code) # Check for error

def get_grey_filter_list():
    """
    List of available grey filters.|
    ------------------------------
    See dialog "Camera|Recalibration" in LabSoft main menu.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :grey_filter_list: QStringList
            | List of filters
        :grey_filter_selected: QStringList
            | 0 = none selected
            | 1 = selected
    """
    err_code, grey_filter_list, grey_filter_selected = ax.LMK.iGetGreyFilterList()
    ax.error_code(err_code) # Check for error

    return grey_filter_list, grey_filter_selected

def set_grey_filter_list(grey_filter_selected=('0', '0', '0')):
    """
    Set grey filters.|
    -----------------
    See GetGreyFilterList(). In this function, the program returns a list
    of the available grey filters and whether they are switched on or off.
    Use this function to get the appropriate list size.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :grey_filter_selected: QStringList (default: ('0', '0', '0'))
            | 0 = none selected
            | 1 = selected
    Returns:
        :grey_filter_selected: QStringList
            | 0 = none selected
            | 1 = selected
    """
    err_code, grey_filter_selected = ax.LMK.iSetGreyFilterList(grey_filter_selected)
    ax.error_code(err_code) # Check for error

    return grey_filter_selected

def set_grey_filter(grey_filter_index=0, grey_filter_selected=0):
    """
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :grey_filter_index: int (default: 0)
            | Index of filter, indexes start from '0'
        :grey_filter_selected: int (default: 0)
            | 0 = deselect
            | 1 = select
    """
    err_code = ax.LMK.iSetGreyFilter(grey_filter_index, grey_filter_selected)
    ax.error_code(err_code) # Check for error

def color_autoscan_time():
    """
    Determine good exposure times for every color filter.|
    -----------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :exposure_times: QStringList
            | Return value: List of exposure times. One time for every
                color filter.
                Attention: The list of exposure times contains one value
                for every filter in the filter wheel, independent of this
                filter is used in color capturing or not. In most cameras,
                there are at least 5 filters: Glass, X1, X2, Z, Y
                In some cases there is additionally a sixth filter available.
                The list of capture times therefore contains either 5 or 6
                entries. Color captures are mostly done with X1, X2, Z and Y
                filters. Therefore the first entry in the exposure time list
                is irrelevant for color captures. And in the case of 6
                filters,the last entry too.
                You can use the returned list of exposure times in the
                function ColorHighDyn()
    """

    color_filters = {'All': []}
    exposure_times = {'G': [], 'X1': [], 'X2': [], 'Z': [], 'VL': [], 'IR': []}

    err_code = ax.LMK.iColorAutoScanTime()[0]

    if err_code != 0:
        print('Error code:', err_code)
    else:
        color_filters['All'].append(ax.LMK.iColorAutoScanTime()[1])
        color_filters['All'] = str(color_filters['All'])[2:-2]
        temp = color_filters['All'].split(" ", 6)

        exposure_times['G'].append(temp[0])
        exposure_times['G'] = str(exposure_times['G'])[3:-4]
        exposure_times['G'] = float(exposure_times['G'])

        exposure_times['X1'].append(temp[1])
        exposure_times['X1'] = str(exposure_times['X1'])[3:-4]
        exposure_times['X1'] = float(exposure_times['X1'])

        exposure_times['X2'].append(temp[2])
        exposure_times['X2'] = str(exposure_times['X2'])[3:-4]
        exposure_times['X2'] = float(exposure_times['X2'])

        exposure_times['Z'].append(temp[3])
        exposure_times['Z'] = str(exposure_times['Z'])[3:-4]
        exposure_times['Z'] = float(exposure_times['Z'])

        exposure_times['VL'].append(temp[4])
        exposure_times['VL'] = str(exposure_times['VL'])[3:-4]
        exposure_times['VL'] = float(exposure_times['VL'])

        exposure_times['IR'].append(temp[5])
        exposure_times['IR'] = str(exposure_times['IR'])[3:-3]
        exposure_times['IR'] = float(exposure_times['IR'])


    return exposure_times

def get_color_correction_list():
    """
    List of available color correction factors.|
    -------------------------------------------
    See dialog 'Camera|Recalibration' in LabSoft main menu.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :col_corr_list: QStringList
            | List of factors
        :col_corr_selected: QStringList
            | 0 = not selected
            | 1 = selected
    """
    [err_code, col_corr_list, col_corr_selected] = ax.LMK.iGetColorCorrList()
    ax.error_code(err_code) # Check for error

    return col_corr_list, col_corr_selected

def set_color_correction(col_corr_index=0, col_corr_selected=1):
    """
    Selection of a color correction factor.|
    -------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :col_corr_index: int (default: 0)
            | List of factors
        :col_corr_selected: int (default: 1)
            | 0 = deselect
            | 1 = select
    """
    err_code = ax.LMK.iSetColorCorr(col_corr_index, col_corr_selected)
    ax.error_code(err_code) # Check for error

def get_smear():
    """
    Get the parameter for smear correction.|
    ---------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :Smear: int
            | 0 = no smear
            | !0 = smear correction with at least 10 dark images captures
            | > 10 number of dark images
    """
    err_code, smear = ax.LMK.iGetSmear()
    ax.error_code(err_code) # Check for error

    return smear

def set_smear(smear=0):
    """
    Set the parameter for smear correction.|
    ---------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :smear: int (default: 0)
            | 0 = no smear
            | !0 = smear correction with at least 10 dark images captures
            | > 10 number of dark images
    """
    err_code = ax.LMK.iSetSmear(smear)
    ax.error_code(err_code) # Check for error

def get_automatic():
    """
    Get the state of Automatic-Flag for exposure times.|
    ---------------------------------------------------
    If this flag is set, all exposure times will automatically adjusted if
    camera exposure time is reduced or enlarged.
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :automatic: int
            | 1 = option is switched on
            | 0 = option is switched off
    """
    err_code, automatic = ax.LMK.iGetAutomatic()
    ax.error_code(err_code) # Check for error

    return automatic

def set_automatic(automatic=1):
    """
    Set Automatic-Flag for all exposure times.|
    ------------------------------------------
    If this flag is set, all exposure times will automatically adjusted if
    camera exposure time is reduced or enlarged.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :automatic: int (default: 1)
            | 1 = use autoscan
            | 0 = do not use autoscan
    """
    err_code = ax.LMK.iSetAutomatic(automatic)
    ax.error_code(err_code) # Check for error

# class Select():

#     def Camera():

#         cameras = []

#         for camera in os.listdir(root.DATA):

#             cameras.append(camera)

#         return cameras

#     def Lenses():
#         """
#         Gets list of all lenses of selected camera.|
#         -------------------------------------------
#         """

#         global lenses

#         lenses = []

#         for lens in glob(root.DATA + '/' + CAMERA_NAME + '/*/'):
#             lenses.append(lens.split('\\')[1])

#         return lenses

#     def Lens(lenses, current_lens='12'):
#         """
#         Gets ID of selected lens.|
#         -------------------------
#         """

#         global lens_ID

#         lens = []

#         for l in range(len(lenses)):
#             lens.append(lenses[l].split('f')[1])

#         if current_lens in lens:
#             lens_ID = (lens.index(current_lens))

#         return lens_ID

#     def FocusFactors():
#         """
#         Gets list of all focus factors of current lens.|
#         -----------------------------------------------
#         """

#         lenses = Camera.Lenses()

#         lens_ID = Camera.Lens(lenses)
#         lens = lenses[lens_ID]

#         FocusFactors = []

#         config = configparser.ConfigParser()
#         config.read(root.DATA + '/' + CAMERA_NAME + '/' +
#                     lens + '/' + 'FocusFactor' + FILE_TYPES['ini'])
#         FocusFactors_Size = config.get('GreyFactor', 'Size')
#         FocusFactors_Size = int(FocusFactors_Size)
#         for FocusFactor in range(FocusFactors_Size):
#             FocusFactor = str(FocusFactor + 1)
#             FocusFactors.append(config.get('GreyFactor/' + FocusFactor, 'Name'))

#         return FocusFactors, FocusFactors_Size

#     def FocusFactor(FocusFactors):
#         """
#         Gets ID of selected focus factor.|
#         ---------------------------------
#         """

#         FocusFactor = []

#         for f in range(len(FocusFactors)):
#             FocusFactor.append(FocusFactors[f].split(' ')[2])

#         if SCALE in FocusFactor:
#             FocusFactor_ID = (FocusFactor.index(SCALE))

#         return FocusFactor_ID
