# -*- coding: utf-8 -*-
# =============================================================================
# Created on Wed Jun 19 14:27:57 2019
# @author: Gareth V. Walkom (walkga04 at googlemail.com)
# 
# (-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)
# _(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_( ͡° ͜ʖ ͡°)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_
# (-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)
# (-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(TechnoPy)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)
# (-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)
# (-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(¯\_(ツ)_/¯)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)
# (-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_(-_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)_-)
# 
# Good afternoon and welcome to TechnoPy.
# 
# TechnoPy allows you to control your TechnoTeam LMK.
# 
# Initially created in Matlab by TechnoTeam and Jan Audenaert, it has now been
# created for use in Python by Gareth V. Walkom. Once connected to the ActiveX
# server, you can then open the LMK LabSoft4 Standard Color ActiveX (ActiveX 
# version of the software is needed to run this script), access the Calibration
# data, and control the camera to make measurements.
#
# Please listen to the TechnoPy playlist while making measurements for inspo:
# https://www.youtube.com/playlist?list=PLu3mtT1o6gSieYEqJEBHm5NX9lWljoED
# =============================================================================
"""

Structure:|
----------
ActiveX():
    Connect():                  Connect to LMK ActiveX Server.
    ErrorCode():                Prints error code if error occurs.

LabSoft():
    Open():                     Opens the LMK4 application.
    Close():                    Closes the LMK4 application.
    Save():                     Save the measurement as a .ttcs file.
    Load():                     Load a measurement from a .ttcs file.
    
Select():
    Lenses():                   Gets list of all lenses of selected camera.
    Lens():                     Gets ID of selected lens.
    FocusFactors():             Gets list of all focus factors of current lens.
    FocusFactor():              Gets ID of selected focus factor.

Camera():
    Lenses():                   Gets list of all lenses of selected camera.
    Lens():                     Gets ID of selected lens.
    FocusFactors():             Gets list of all focus factors of current lens.
    FocusFactor():              Gets ID of selected focus factor.
    Open():                     Set new camera calibration data.
    GetConvertingUnits():       Get converting information.
    SetConvertingUnits():       Set new converting values.
    GetFocusFactors():          List of available focus factors.
    SetFocusFactor():           Set a focus factor.
    GetModulationFrequency():   Get the modulation frequency.
    SetModulationFrequency():   Set the frequency of modulated light.
    GetScatteredLight():        Is scattered light correction switched on?
    SetScatteredLight():        Use of scattered light correction.
    GetIntegrationTime():       Determine current exposure time and other time parameters.
    SetIntegrationTime():       Set new exposure time.
    GetMaxCameraTime():         Determine the maximum possible exposure time.
    SetMaxCameraTime():         Set the maximum possible exposure time.
    GetAutoScan():              Get use of autoscan algorithm.
    SetAutoScan():              Set use of autoscan algorithm.
    GetFilterWheel():           Determine filter state.
    GetGreyFilterList():        List of available grey filters.
    SetGreyFilterList():        Set grey filters.
    SetGreyFilter():            Selection of a grey filter.
    ColorAutoScanTime():        Determine good exposure times for every color filter.
    GetColorCorrectionList():   List of available color correction factors.
    SetColorCorrection():       Selection of a color correction factor.
    GetSmear():                 Get the parameter for smear correction.
    SetSmear():                 Set the parameter for smear correction.
    GetAutomatic():             Get the state of Automatic-Flag for exposure times.
    SetAutomatic():             Set Automatic-Flag for all exposure times.
    
Coordinates():
    GetValueUnit():             Get the values and units of the axis.
    SetValueUnit():             Set the values and units of the axis.
    
Capture():
    SinglePic():                SinglePic capture algorithm.
    MultiPic():                 MultiPic capture algorithm.
    HighDynPic():               HighDyn capturing for luminance image.
    ColorHighDyn():             HighDyn capturing for color image.
    GetLastInfo():              Determine information about the preceeding capture.
    
Image():
    GetSize():                  Get image size and parameter.
    Save():                     Save image.
    Load():                     Load image from .pcf.
    Show():                     Show image.
    
Region():
    Create():                   Create a region.
    CreateRectImageSize():      Create a rectangular region the size of the whole image.
    CreateGrid():               Create a grid region within whole image with defined amount of squares.
    GetID():                    Get index of region given region name.
    Select():                   Selects or deselects a region.
    Delete():                   Delete a region.
    
Evaluation():
    CreateStatistic():          Create a new statistic.
    GetStandardStatistic():     Determine parameter of the standard statistic.
    DeleteStatistic():          Delete an existing statistic.
    GetImageMeanXYZ():          Create region size of image and get mean XYZ.
#    GetGridMeanXYZ():           Create regions as a grid in image and get mean XYZ.
#    GetColorHistogramValues():  Get the values of the histogram in a color image.
    GetPixelColor():            Get a pixel value of a color image.
    Convert_CIE_RGB():          Conversion of a color value from CIE-RGB to another color space.
    XYZ_To_xy():                Convert XYZ to x, y.
    XYZ_To_u_v_():              Convert XYZ to u', v'.
    Show_xy():                  Plot x, y color coordinates using Luxpy.
    Show_u_v_():                Plot u', v' color coordinates using Luxpy.
    
Table():
#    GetNumber():                Returns the number of tables in the result tab widget.
#    GetNameAndCaption():        Returns the name and the caption of an existing table.
#    GetIndex():                 Search for a table, given by name or caption.
#    GetNumberColumns():         Returns the number of columns of a table.
#    GetColumn():                Returns the column header of a column of a table.
#    GetCell():                  Returns the content of a cell of a table.
#    GetAllContent():            Returns all cells of a table as a list.
    
Characterize():
    VR_HMD():                   Characterize a Virtual Reality Head-Mounted-Display.

To-do:|
------
    * Check all docstrings have correct information
    * Change print statements depending on what parameters are chosen
    * Create 6 regions like a grid for Characterize.VR_HMD()
    * Update Structure
    * ColorHighDyn: Simple... Define multiple filter exposure times?
    * Fix messy code in some places
    * Call .self within classes instead of global if not needed elsewhere.
    * Change names to more logical names
    * Update __main__ example code so it works 
    * Change doctstrings to inlude 'Raises:' for ErrorCodes (https://docs.scipy.org/doc/numpy/reference/generated/numpy.interp.html)
    * Change docstring layout similar to Numpy (https://github.com/numpy/numpy/blob/v1.16.1/numpy/lib/function_base.py#L1282-L1412)
    * Space text with \n better
    * Create instructions/example code with Jupyter Notebook.
    * Move lens and focus factor functions for Camera() class to Select() class, and get the working
    * Error check statisticType{} for compatible images and regions
    * Test functions in table class
    * Sort out absolute mess
    * Give warning if focus factor needed, but no chosen
    * Delete old functions that are no longer needed
    * Add spectral responsitivities (in LMK book in box) for each lens
"""
from win32com.client import Dispatch
import os
from glob import glob
import datetime, time
import configparser
import operator
import smtplib
import numpy as np
import luxpy as lx
from matplotlib import pyplot as plt
from skimage import io

# Define the root to the calibration data
CalibrationDataRoot = 'F:/LMK/Calibration Data'

# Name of the TechnoTeam LMK Camera
cameraName = str(os.listdir(CalibrationDataRoot))[2:-2]

Camera_Names = {'Old':'ttf8847',
                'VR': 'tts20035'}

Old_Lenses = {'6.5': 'o13196f6_5',
              '12': 'o95653f12',
              '25': 'oB225463f25',
              '50': 'oC216813f50'}

VR_Lenses = {'50mm': 'oM00442f50',
             'Conoscopic': 'oTTC-163_D0224',
             'NED_2mm': 'oTTNED-12_50_2mmEP', 
             'NED_4mm': 'oTTNED-12_50_4mmEP'}

#Camera_Lens = {'Old':{
#        'Name':'ttf8847',
#        'Lenses':{
#                '6.5': 'o13196f6_5',
#                '12': 'o95653f12',
#                '25': 'oB225463f25',
#                '50': 'oC216813f50'}},
#    'VR':{
#            'Name': 'tts20035',
#            'Lenses':{
#                    '50mm': 'oM00442f50',
#                    'Conoscopic': 'oTTC-163_D0224',
#                    'NED_2mm': 'oTTNED-12_50_2mmEP', 
#                    'NED_4mm': 'oTTNED-12_50_4mmEP'}}}

## Access Color Spaces
# Dictionary containing all available color spaces.
# WARNING: All statistics are gathered in CIE-RGB. To use another color space,
# this must be converted using GetColor()
colorSpace = {
        'CIE-RGB': 1,
        'S-RGB': 2,
        'EBU-RGB': 4,
        'XYZ': 16,
        'Lxy': 32,
        'Luv': 64,
        'Lu_v_': 128,
        'L*u*v*': 256,
        'C*h*s*_uv': 512,
        'L*a*b*': 1024,
        'C*h*_ab': 2048,
        'HSV': 4096,
        'HSI': 8192,
        'WST': 16384,
        'Lrg': 32768,
        'LWS': 65536}

## Access Image
# Structure to access the images
imageType = {
        'Camera': -3,
        'Luminance': -2,
        'Color': -1}

## Access Available File Types
# Not really needed, but nice to have them all in one dict
fileType = {
        'ttcs': '.ttcs',
        'pus': '.pus',
        'pf': '.pf',
        'pcf': '.pcf',
        'txt': '.txt',
        'tix': '.tix',
        'bmp': '.bmp',
        'jpg': '.jpg',
        'png': '.png',
        'cos': '.cos',
        'csv': '.csv',
        'ini': '.ini'}

## Access Regions
# Structure to access region lists
regionType = {
        'Rectangle': {
                'identifier': 0,
                'points': 2},
        'Line': {
                'identifier': 1,
                'points': 2},
        'Circle': {
                'identifier': 2,
                'points': 2},
        'Polygon': {
                'identifier': 3,
                'points': 3},
        'Polyline': {
                'identifier': 4,
                'points': 3},
        'Ellipse': {
                'identifier': 5,
                'points': 3},
        'CircularRing': {
                'identifier': 6,
                'points': 3},
        'OR': {
                'identifier': 7,
                'points': 2},
        'XOR': {
                'identifier': 8,
                'points':2},
        'AND': {
                'identifier': 9,
                'points': 2}}
        
## Access Statistics
# Comments show which regionType and imageType the statistic types can be used with
statisticType = {
        'standardGrey': 0,            # Rectangle, Line   :: Camera, Luminance :: Standard statistic in grey images
        'standardColor': 1,           # Rectangle, Line   :: Color             :: Standard statistic in color images
        'sectionalGrey': 2,           # Rectangle, Line   :: Camera, Luminance :: Sectional view in grey images
        'sectionalColor': 3,          # Rectangle, Line   :: Color             :: Sectional view in color images
        'histogramGrey': 4,           #                   :: [ERROR]           :: Histogram in grey images
        'histogramColor': 5,          #                   :: [ERROR]           :: Histogram in color images
        'bitHistogramGrey': 6,        #                   :: [ERROR]           :: Bit histogram in grey images (only images of camera image type)
        'bitHistorgramColor': 7,      #                   :: [ERROR]           :: Bit histogram in color images (only images of color camera image type)
        'projectionGrey': 8,          #                   :: [ERROR]           :: Projection in grey images
        'projectionColor': 9,         #                   :: [ERROR]           :: Projection in color images
        'luminanceGrey': 20,          #                   :: [ERROR]           :: Luminance objects in grey images
        'integralGrey': 22,           #                   :: [ERROR]           :: Integral objects in grey images
        'integralColor': 23,          #                   :: [ERROR]           :: Integral objects in color images
        'symbolGrey': 24,             #                   :: [ERROR]           :: Symbol objects in grey images
        'symbolColor': 25,            #                   :: [ERROR]           :: Symbol objects in color images
        'lightArcGrey': 26,           #                   :: [ERROR]           :: Light arc objects in grey images
        'spiralWoundGrey': 28,        #                   :: [ERROR]           :: Spiralwoundfilaments in grey images
        'chromaticityLineColor': 31,  #                   :: [ERROR]           :: Chromaticity line diagrams in color images
        'chromaticityAreaColor': 33,  #                   :: [ERROR]           :: Chromaticity area diagrams in color images
        'threeDviewGrey': 34,         #                   :: [ERROR]           :: 3D view in grey images
        'integralNegativeGrey': 36,   #                   :: [ERROR]           :: Integral objects in grey images (negative contrast)
        'integralNegativeColor': 38,  #                   :: [EEROR]           :: Symbol objects in grey images (negative contrast)
        'symbolNegativeColor': 39,    #                   :: [ERROR]           :: Symbol objects in color images (negative contrast)
        'contrastGrey': 40}           #                   :: [ERROR]           :: Contrasts objects in grey images

# Define the Lens and focus factor in use.
lens = '12'
scale = 'infinite'

# Define Save Parameters
MeasRoot = 'E:/Measurements/' + str(datetime.date.today()) + '/'
MeasName = datetime.datetime.now().strftime('%H:%M:%S')
extension = fileType['png']

class ActiveX():
    
    def Connect():
        """
        Connect to LMK ActiveX Server.|
        ------------------------------
        After connecting, you can communicate with the LMK ActiveX Server.
        -----------------------------------------------------------------------
        Returns:
            :lmk:
                | lmk must now be referenced to access the LMK ActiveX Server.
        """
        lmk = Dispatch('lmk4.LMKAxServer')
        
        return lmk
    
    def ErrorCode(lmk, ErrorCode):
        """
        Prints error code if error occurs.|
        ----------------------------------
        Parameters:
            :ErrorCode: int
                | Error code from ActiveX server.
                | 0 = Continue with no error.
                | !0 = Error with function from ActiveX server.
        """
        if ErrorCode != 0:
            print ('Error code:', ErrorCode, '\n')
            _, ErrorInformation = lmk.iGetErrorInformation()
            print ('Error info:', ErrorInformation)
            
class LabSoft():
    
    def Open(lmk):
        """
        Opens the LMK4 application.|
        ---------------------------
        After opening, the main window is visible.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        """
        ErrorCode = lmk.iOpen()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def Close(lmk, Question = 0):
        """
        Closes the LMK4 application.|
        ----------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Question: int, optional
                | !0 = Opens a dialogue window in the application. The user can
                        choose whether they wish to save the current state or not
                        or cancel the closing of the program.
                | 0 = No dialogue window
        """
        ErrorCode = lmk.iClose(Question)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def Save(lmk, FileName = MeasRoot + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + fileType['ttcs']):
        """
        Save the measurement as a .ttcs file.|
        -------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :FileName: QString, optional (default: MeasRoot + datetime + .ttcs')
                | Change to adjust root to save measurement
                | Datetime is the exact datetime of the measurement, not datetime when saved.
        """
        if not os.path.exists(MeasRoot):
            os.makedirs(MeasRoot)
        ErrorCode = lmk.iSaveProtokoll(FileName)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def Load(lmk, FileName = 'Meas.ttcs'):
        """
        Load a measurement from a .ttcs file.|
        -------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :FileName: QString, optional (default: 'Meas.ttcs')
                | Change to adjust root to load measurement
        """
        ErrorCode = lmk.iLoadProtokoll(FileName)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
class Select():
    
    def Camera(CalibrationDataRoot = CalibrationDataRoot):
        
        cameras = []
        
        for camera in os.listdir(CalibrationDataRoot):
            
            cameras.append(camera)
            
        return cameras
    
    def Lenses(cameraName, CalibrationDataRoot = CalibrationDataRoot):
        """
        Gets list of all lenses of selected camera.|
        -------------------------------------------
        """
    
        global lenses
        
        lenses = []
        
        for lens in (glob(CalibrationDataRoot + '/' + cameraName + '/*/')):
            lenses.append(lens.split('\\')[1])
        
        return lenses
    
    def Lens(lenses, current_lens = '12'):
        """
        Gets ID of selected lens.|
        -------------------------
        """
        
        global lens_ID
        
        lens = []
        
        for l in range(len(lenses)):
            lens.append(lenses[l].split('f')[1])
            
        if current_lens in lens:
            lens_ID = (lens.index(current_lens))
            
        return lens_ID
    
    def FocusFactors():
        """
        Gets list of all focus factors of current lens.|
        -----------------------------------------------
        """
        
        lenses = Camera.Lenses()
        
        lens_ID = Camera.Lens(lenses)        
        lens = lenses[lens_ID]
        
        FocusFactors = []
                        
        config = configparser.ConfigParser()
        config.read(CalibrationDataRoot + '/' + cameraName + '/' + lens + '/' + 'FocusFactor' + fileType['ini'])
        FocusFactors_Size = config.get('GreyFactor', 'Size')
        FocusFactors_Size = int(FocusFactors_Size)
        for FocusFactor in range(FocusFactors_Size):
            FocusFactor = str(FocusFactor + 1)
            FocusFactors.append(config.get('GreyFactor/' + FocusFactor, 'Name'))
            
        return FocusFactors, FocusFactors_Size
    
    def FocusFactor(FocusFactors, scale = 'infinite'):
        """
        Gets ID of selected focus factor.|
        ---------------------------------
        """
        
        FocusFactor = []
        
        for f in range(len(FocusFactors)):
            FocusFactor.append(FocusFactors[f].split(' ')[2])
            
        if scale in FocusFactor:
            FocusFactor_ID = (FocusFactor.index(scale))
            
        return FocusFactor_ID
        
class Camera():
    
    def GetCameras(Camera_Names = Camera_Names):
        
        print ('Cameras:')
        for cameras in Camera_Names.keys():
            print (cameras)
        
        return cameras
    
    def SetCamera(camera = None):
        
        if camera is None:
            print ('Cameras:')
            for cameras in Camera_Names.keys():
                print (cameras)
                
            camera = input ('Input chosen camera: ')
            
        camera_no = Camera_Names[camera]
        
        return camera, camera_no
    
    def GetLenses(camera, Old_Lenses = Old_Lenses, VR_Lenses = VR_Lenses):
        
        print ('Lenses:')
        
        if camera == 'Old':
            for lenses in Old_Lenses.keys():
                print (lenses)
        elif camera == 'VR':
            for lenses in VR_Lenses.keys():
                print (lenses)
            
        return lenses
    
    def SetLens(camera, lens = None, Old_Lenses = Old_Lenses, VR_Lenses = VR_Lenses):
        
        if lens is None:
            print ('Lenses:')
            if camera == 'Old':
                for lenses in Old_Lenses.keys():
                    print (lenses)
            elif camera == 'VR':
                for lenses in VR_Lenses.keys():
                    print (lenses)
            
            lens = input ('Input chosen lens: ')
        
        if camera == 'Old':
            lens_no = Old_Lenses[lens]
        elif camera == 'VR':
            lens_no = VR_Lenses[lens]
        
                
        return lens, lens_no
    
    def Lenses(cameraName, CalibrationDataRoot = CalibrationDataRoot):
        """
        Gets list of all lenses of selected camera.|
        -------------------------------------------
        """
    
        global lenses
        
        lenses = []
        
        for lens in (glob(CalibrationDataRoot + '/' + cameraName + '/*/')):
            lenses.append(lens.split('\\')[1])
        
        return lenses
    
    def Lens(lenses, current_lens = '12'):
        """
        Gets ID of selected lens.|
        -------------------------
        """
        
        global lens_ID
        
        lens = []
        
        for l in range(len(lenses)):
            lens.append(lenses[l].split('f')[1])
            
        if current_lens in lens:
            lens_ID = (lens.index(current_lens))
            
        return lens_ID
    
    def FocusFactors():
        """
        Gets list of all focus factors of current lens.|
        -----------------------------------------------
        """
        
        lenses = Camera.Lenses()
        
        lens_ID = Camera.Lens(lenses)        
        lens = lenses[lens_ID]
        
        FocusFactors = []
                        
        config = configparser.ConfigParser()
        config.read(CalibrationDataRoot + '/' + cameraName + '/' + lens + '/' + 'FocusFactor' + fileType['ini'])
        FocusFactors_Size = config.get('GreyFactor', 'Size')
        FocusFactors_Size = int(FocusFactors_Size)
        for FocusFactor in range(FocusFactors_Size):
            FocusFactor = str(FocusFactor + 1)
            FocusFactors.append(config.get('GreyFactor/' + FocusFactor, 'Name'))
            
        return FocusFactors, FocusFactors_Size
    
    def FocusFactor(FocusFactors, scale = 'infinite'):
        """
        Gets ID of selected focus factor.|
        ---------------------------------
        """
        
        FocusFactor = []
        
        for f in range(len(FocusFactors)):
            FocusFactor.append(FocusFactors[f].split(' ')[2])
            
        if scale in FocusFactor:
            FocusFactor_ID = (FocusFactor.index(scale))
            
        return FocusFactor_ID
        
    
    def Open(lmk, camera_no, lens_no):
        """
        Set new camera calibration data.|
        --------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :CalibrationDataRoot: QString (default: CalibrationDataRoot)
                | Path to the camera calibration data. More exactly spoken path
                    to the lens sub directory. After calling this function the
                    camera is completely reinitialized.
                | If the string is empty a currently existing camera connection
                    is finished.
        """
        ErrorCode = lmk.iSetNewCamera(CalibrationDataRoot + '/' + camera_no + '/' + lens_no)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
    def GetConvertingUnits(lmk):
        """
        Get converting information.|
        ---------------------------
        See dialog "Camera|Recalibration" in LabSoft main menu.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :UnitsName: QString (default: 'L')
                | Units Name used
            :Units: QString (default: 'cd/m^2')
                | Units used
            :UnitsFactor: float (default: 1.0)
                | Units factor used
        """
        [ErrorCode, UnitsName, Units, UnitsFactor] = lmk.iGetConvertingUnits()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
        return UnitsName, Units, UnitsFactor
    
    def SetConvertingUnits(lmk, UnitsName = 'L', Units = 'cd/m^2', UnitsFactor = 1.0):
        """
        Set new converting values.|
        --------------------------
        See dialog "Camera|Recalibration" in LabSoft main menu.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :UnitsName: QString (default: 'L')
                | Wished units name
            :Units: QString (default: 'cd/m^2')
                | Wished units
            :UnitsFactor: float (default: 1.0)
                | Wished units factor
        """
        ErrorCode = lmk.iSetConvertingUnits(UnitsName, Units, UnitsFactor)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetFocusFactors(lmk):
        """
        List of available focus factors.|
        --------------------------------
        Parameters:
            :lmk: 
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :FocusFactors: QStringList
                | List of focus factors
            :FocusFactor: int
                | Index of current focus factor
        """
        [ErrorCode, FocusFactors, FocusFactor] = lmk.iGetFocusFactorList()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return FocusFactors, FocusFactor
    
    def SetFocusFactor(lmk, FocusFactor = scale):
        """
        Set a focus factor.|
        -------------------
        See dialog "Camera|Recalibration" in LabSoft main menu.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :FocusFactor: int
                | Index of focus factor
        """
        FocusFactors, FocusFactors_Size = Camera.FocusFactors()
        FocusFactor_ID = Camera.FocusFactor(FocusFactors, FocusFactor)
        ErrorCode = lmk.iSetFocusFactor(FocusFactor_ID)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetModulationFrequency(lmk):
        """
        Get the modulation frequency.|
        -----------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :ModulationFrequency: float
                | Frequency of light source
                | 0 = no modulation is to be concerned
        """
        [ErrorCode, ModulationFrequency] = lmk.iGetModulationFrequency()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return ModulationFrequency

    def SetModulationFrequency(lmk, ModulationFrequency = 90.0):
        """
        Set the frequency of modulated light.|
        -------------------------------------
        If the light source is driven by alternating current, there are some
        restriction for the exposure times. Please inform the program about
        the modulation frequency.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :ModulationFrequency: float (default: 90.0)
                | Frequency of light source
                | 0 = no modulation is to be concerned
        """
        ErrorCode = lmk.iSetModulationFrequency(ModulationFrequency)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetScatteredLight(lmk):
        """
        Is scattered light correction switched on?|
        ------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :ScatteredLight: int
                | 1 = scattered light correction is switched on
                | 0 = scattered light correction is switched off
        """
        [ErrorCode, ScatteredLight] = lmk.iGetScatteredLight()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return ScatteredLight
        
    def SetScatteredLight(lmk, ScatteredLight = 1):
        """
        Use of scattered light correction.|
        ----------------------------------
        Only usable if a parameter set is available in program.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :ScatteredLight: int (defualt: 1)
                | 1 = switch on scattered light correction
                | 0 = switch off scattered light correction
        """
        ErrorCode = lmk.iSetScatteredLight(ScatteredLight)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetIntegrationTime(lmk):
        """
        Determine current exposure time and other parameters.|
        -----------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :CurrentTime: float
                | Current integration time
            :PreviousTime: float
                | Next smaller (proposed) time
            :NextTime: float
                | Next larger (proposed) time
            :MinTime: float
                | Minimal possible time
            :MaxTime: float
                | Maximal possible time
        """
        [ErrorCode, CurrentTime, PreviousTime, NextTime, MinTime, MaxTime] = lmk.iGetIntegrationTime()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return CurrentTime, PreviousTime, NextTime, MinTime, MaxTime
        
    def SetIntegrationTime(lmk, WishedTime = 5.0):
        """
        Set new exposure time.|
        ----------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :WishedTime: float (default: 5.0)
                | Wished integration time
        Returns
            :IntegrationTime: float
                | Realized integration time
        """
        [ErrorCode, IntegrationTime] = lmk.iSetIntegrationTime(WishedTime)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return IntegrationTime
    
    def GetMaxCameraTime(lmk):
        """
        Determine the maximum possible exposure time.|
        ---------------------------------------------
        Normally this time is restricted by camera properties. In some cases it
        could be useful to use an even smaller maximum exposure time.
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns
            :MaxTime: float
                | Current maximum time
        """
        [ErrorCode, MaxTime] = lmk.iGetMaxCameraTime()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return MaxTime
    
    def SetMaxCameraTime(lmk, MaxTime = 5.0):
        """
        Set the maximum possible exposure time.|
        ---------------------------------------
        The maximum values is of course restricted by camera properties. But
        you can use an even smaller time to avoid to long meausrement times.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :MaxTime: float (default: 5.0)
                | Wished value
        """
        ErrorCode = lmk.iSetMaxCameraTime(MaxTime)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetAutoscan(lmk):
        """
        Get use of autoscan algorithm.|
        ------------------------------
        Is autoscan switched on?
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :Autoscan: int
                | 1 = autoscan is switched on
                | 0 = autoscan is switched off
        """
        [ErrorCode, Autoscan] = lmk.iGetAutoscan()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Autoscan
    
    def SetAutoscan(lmk, Autoscan = 1):
        """
        Set use of autoscan algorithm.|
        ------------------------------
        Determination of a good exposure time before the capturing algorithm.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Autoscan: int (default: 1)
                | 1 = Use autoscan
                  0 = Do not use autoscan
        """
        ErrorCode = lmk.iSetAutoscan(Autoscan)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetFilterWheel(lmk):
        """
        Determine filter state.|
        -----------------------
        If there is no filter wheel, the function returns an error code.
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :CurrentFilterPos: int
                | Position of filter wheel
            :CurrentFilterName: QString
                | Name of current filter
        """
        [ErrorCode, CurrentFilterPos, CurrentFilterName] = lmk.iGetFilterWheel()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return CurrentFilterPos, CurrentFilterName
    
    def GetGreyFilterList(lmk):
        """
        List of available grey filters.|
        ------------------------------
        See dialog "Camera|Recalibration" in LabSoft main menu.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :GreyFilterList: QStringList
                | List of filters
            :GreyFilterSelected: QStringList
                | 0 = none selected
                | 1 = selected
        """
        [ErrorCode, GreyFilterList, GreyFilterSelected] = lmk.iGetGreyFilterList()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return GreyFilterList, GreyFilterSelected
    
    def SetGreyFilterList(lmk, GreyFilterSelected = ('0', '0', '0')):
        """
        Set grey filters.|
        -----------------
        See GetGreyFilterList(). In this function, the program returns a list
        of the available grey filters and whether they are switched on or off.
        Use this function to get the appropriate list size.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :GreyFilterSelected: QStringList (default: ('0', '0', '0'))
                | 0 = none selected
                | 1 = selected
        Returns:
            :GreyFilterSelected: QStringList
                | 0 = none selected
                | 1 = selected
        """
        [ErrorCode, GreyFilterSelected] = lmk.iSetGreyFilterList(GreyFilterSelected)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
        return GreyFilterSelected
    
    def SetGreyFilter(lmk, GreyFilterIndex = 0, GreyFilterSelected = 0):
        """
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :GreyFilterIndex: int (default: 0)
                | Index of filter, indexes start from '0'
            :GreyFilterSelected: int (default: 0)
                | 0 = deselect
                | 1 = select
        """
        ErrorCode = lmk.iSetGreyFilter(GreyFilterIndex, GreyFilterSelected)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def ColorAutoScanTime(lmk):
        """
        Determine good exposure times for every color filter.|
        -----------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :ExposureTimes: QStringList
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
        
        All = {'All': []}
        ExposureTimes = {'G': [], 'X1': [], 'X2': [], 'Z': [], 'VL': [], 'IR': []}

        ErrorCode = lmk.iColorAutoScanTime()[0]
        
        if ErrorCode != 0:
            print ('Error code:', ErrorCode)
        else:
            All['All'].append(lmk.iColorAutoScanTime()[1])
            All['All'] = str(All['All'])[2:-2]
            temp = All['All'].split(" ", 6)
            
            ExposureTimes['G'].append(temp[0])
            ExposureTimes['G'] = str(ExposureTimes['G'])[3:-4]
            ExposureTimes['G'] = float(ExposureTimes['G'])
            
            ExposureTimes['X1'].append(temp[1])
            ExposureTimes['X1'] = str(ExposureTimes['X1'])[3:-4]
            ExposureTimes['X1'] = float(ExposureTimes['X1'])
            
            ExposureTimes['X2'].append(temp[2])
            ExposureTimes['X2'] = str(ExposureTimes['X2'])[3:-4]
            ExposureTimes['X2'] = float(ExposureTimes['X2'])
            
            ExposureTimes['Z'].append(temp[3])
            ExposureTimes['Z'] = str(ExposureTimes['Z'])[3:-4]
            ExposureTimes['Z'] = float(ExposureTimes['Z'])
            
            ExposureTimes['VL'].append(temp[4])
            ExposureTimes['VL'] = str(ExposureTimes['VL'])[3:-4]
            ExposureTimes['VL'] = float(ExposureTimes['VL'])
            
            ExposureTimes['IR'].append(temp[5])
            ExposureTimes['IR'] = str(ExposureTimes['IR'])[3:-3]
            ExposureTimes['IR'] = float(ExposureTimes['IR'])
            
        
        return ExposureTimes
    
    def GetColorCorrectionList(lmk):
        """
        List of available color correction factors.|
        -------------------------------------------
        See dialog 'Camera|Recalibration' in LabSoft main menu.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :ColCorrList: QStringList
                | List of factors
            :ColCorrSelected: QStringList
                | 0 = not selected
                | 1 = selected
        """
        [ErrorCode, ColCorrList, ColCorrSelected] = lmk.iGetColorCorrList()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
        return ColCorrList, ColCorrSelected
    
    def SetColorCorrection(lmk, ColCorrIndex = 0, ColCorrSelected = 1):
        """
        Selection of a color correction factor.|
        -------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :ColCorrIndex: int (default: 0)
                | List of factors
            :ColCorrSelected: int (default: 1)
                | 0 = deselect
                | 1 = select
        """
        ErrorCode = lmk.iSetColorCorr()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
    def GetSmear(lmk):
        """
        Get the parameter for smear correction.|
        ---------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :Smear: int
                | 0 = no smear
                | !0 = smear correction with at least 10 dark images captures
                | > 10 number of dark images
        """
        ErrorCode = lmk.iGetSmear()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
    def SetSmear(lmk, Smear = 0):
        """
        Set the parameter for smear correction.|
        ---------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Smear: int (default: 0)
                | 0 = no smear
                | !0 = smear correction with at least 10 dark images captures
                | > 10 number of dark images
        """
        ErrorCode = lmk.iGetSmear()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
                    
    def GetAutomatic(lmk):
        """
        Get the state of Automatic-Flag for exposure times.|
        ---------------------------------------------------
        If this flag is set, all exposure times will automatically adjusted if
        camera exposure time is reduced or enlarged.
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :Automatic: int
                | 1 = option is switched on
                | 0 = option is switched off
        """
        [ErrorCode, Automatic] = lmk.iGetAutomatic()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Automatic
        
    def SetAutomatic(lmk, Automatic = 1):
        """
        Set Automatic-Flag for all exposure times.|
        ------------------------------------------
        If this flag is set, all exposure times will automatically adjusted if
        camera exposure time is reduced or enlarged.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Automatic: int (default: 1)
                | 1 = use autoscan
                | 0 = do not use autoscan
        """
        ErrorCode = lmk.iSetAutomatic(Automatic)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
class Coordinates():
    
    def GetValueUnit(lmk, Image = imageType['Color']):
        """
        Get the values and units of the axis.|
        -------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Index of image
        Returns:
            :X_Value: QString
                | Value of X axis
            :X_Unit: QString
                | Unit of X axis
            :Y_Value: QString
                | Value of Y axis
            :Y_Unit: QString
                | Unit of Y axis
            :UnitArea: QString
                | Unit of area
        """
        [ErrorCode, X_Value, X_Unit, Y_Value, Y_Unit, UnitArea] = lmk.iCoordSystemGetValueUnit(Image)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
        return X_Value, X_Unit, Y_Value, Y_Unit, UnitArea
    
    def SetValueUnit(lmk, Image = imageType['Color'], X_Value = 'x',
                     X_Unit = 'pix', Y_Value = 'y', Y_Unit = 'pix', UnitArea = 'pix^2'):
        """
        Set the values and units of the axis.|
        -------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Index of image
            :X_Value: QString (default: 'x')
                | Value of X axis
            :X_Unit: QString (default: 'pix')
                | Unit of X axis
            :Y_Value: QString (default: 'y')
                | Value of Y axis
            :Y_Unit: QString (default: 'pix')
                | Unit of Y axis
            :UnitArea: QString (default: 'pix^2')
                | Unit of area
        """
        ErrorCode = lmk.iCoordSystemSetValueUnit(Image, X_Value, X_Unit, Y_Value, Y_Unit, UnitArea)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
    
class Capture():
    
    def SinglePic(lmk, AutoScan = True, ExposureTime = 0.1):
        """
        SinglePic capture algorithm.|
        ----------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :ExposureTime: float (default: 0.1)
                | Exposure time to use
        """
        
        if AutoScan is True:
            ExposureTimes = Camera.ColorAutoScanTime(lmk) # [REQUIRED if wanting best exposure times]
            ErrorCode = lmk.iSinglePic2(max(ExposureTimes.items(), key=operator.itemgetter(1))[1])
        else:
            ErrorCode = lmk.iSinglePic2(ExposureTime)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
    
    def MultiPic(lmk, AutoScan = True, ExposureTime = 0.1, PicCount = 1):
        """
        MultiPic capture algorithm.|
        ---------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :ExposureTime: float (default: 0.1)
                | Exposure time to use
            :PicCount: int (default: 1)
                | Number of camera images
        """
        
        if AutoScan is True:
            ExposureTimes = Camera.ColorAutoScanTime(lmk) # [REQUIRED if wanting best exposure times]
            ErrorCode = lmk.iMultiPic2(max(ExposureTimes.items(), key=operator.itemgetter(1))[1], PicCount)
        else:
            ErrorCode = lmk.iMultiPic2(ExposureTime, PicCount)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def HighDynPic(lmk, AutoScan = True, ExposureTime = 0.1, StartRatio = 10.0, TimeRatio = 3.0, PicCount = 1):
        """
        HighDyn capturing for luminance image.|
        --------------------------------------
        Parameters:
            :lmk:
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
            ExposureTimes = Camera.ColorAutoScanTime(lmk) # [REQUIRED if wanting best exposure times]
            ErrorCode = lmk.iHighDynPic3(max(ExposureTimes.items(), key=operator.itemgetter(1))[1],
                                         StartRatio, TimeRatio, PicCount)
        else:
            ErrorCode = lmk.iHighDynPic3(ExposureTime, StartRatio, TimeRatio, PicCount)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
    
    def ColorHighDyn(lmk, AutoScan = True, MaxTime = 15.0, MinTime = 0.0, TimeRatio = 3.0, PicCount = 1):
        """
        HighDyn capturing for color image.|
        ----------------------------------
        Parameters:
            :lmk:
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
            ExposureTimes = Camera.ColorAutoScanTime(lmk) # [REQUIRED if wanting best exposure times]
            ErrorCode = lmk.iColorHighDynPic2(max(ExposureTimes.items(), key=operator.itemgetter(1))[1],
                                          MinTime, TimeRatio, PicCount)
        else:
            ErrorCode = lmk.iColorHighDynPic2(MaxTime, MinTime, TimeRatio, PicCount)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetLastInfo(lmk):
        """
        Determine information about the preceeding capture.|
        ---------------------------------------------------
        Parameters:
            :lmk:
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
        ErrorCode = lmk.iCaptureGetLastInfo()[0]
        if ErrorCode != 0:
            print ('Error code:', ErrorCode)
        else:
            LastInfo['CaptureSuccess'].append(lmk.iCaptureGetLastInfo()[1])
            LastInfo['CaptureSuccess'] = str(LastInfo['CaptureSuccess'])[1:-1]
            LastInfo['CaptureSuccess'] = int(LastInfo['CaptureSuccess'])
            
            LastInfo['CaptureType'].append(lmk.iCaptureGetLastInfo()[2])
            LastInfo['CaptureType'] = str(LastInfo['CaptureType'])[1:-1]
            LastInfo['CaptureType'] = int(LastInfo['CaptureType'])
            
            LastInfo['GreyFilter'].append(lmk.iCaptureGetLastInfo()[3])
            LastInfo['GreyFilter'] = str(LastInfo['GreyFilter'])[1:-1]
            
            LastInfo['ColorFilters'].append(lmk.iCaptureGetLastInfo()[4])
            LastInfo['ColorFilters'] = str(LastInfo['ColorFilters'])[1:-1]
            
            LastInfo['PicCount'].append(lmk.iCaptureGetLastInfo()[5])
            LastInfo['PicCount'] = str(LastInfo['PicCount'])[1:-1]
            LastInfo['PicCount'] = int(LastInfo['PicCount'])
            
            LastInfo['MaxExposureTime'].append(lmk.iCaptureGetLastInfo()[6])
            LastInfo['MaxExposureTime'] = str(LastInfo['MaxExposureTime'])[1:-1]
            LastInfo['MaxExposureTime'] = float(LastInfo['MaxExposureTime'])
            
            LastInfo['MinExposureTime'].append(lmk.iCaptureGetLastInfo()[7])
            LastInfo['MinExposureTime'] = str(LastInfo['MinExposureTime'])[1:-1]
            LastInfo['MinExposureTime'] = float(LastInfo['MinExposureTime'])
            
            LastInfo['PercentageOverdrivenPixels'].append(lmk.iCaptureGetLastInfo()[8])
            LastInfo['PercentageOverdrivenPixels'] = str(LastInfo['PercentageOverdrivenPixels'])[1:-1]
            LastInfo['PercentageOverdrivenPixels'] = float(LastInfo['PercentageOverdrivenPixels'])
            
            LastInfo['PercentageOverdrive'].append(lmk.iCaptureGetLastInfo()[9])
            LastInfo['PercentageOverdrive'] = str(LastInfo['PercentageOverdrive'])[1:-1]
            LastInfo['PercentageOverdrive'] = float(LastInfo['PercentageOverdrive'])
            
            LastInfo['CaptureDateTime'].append(lmk.iCaptureGetLastInfo()[10])
            LastInfo['CaptureDateTime'] = str(LastInfo['CaptureDateTime'])[1:-1]
            LastInfo['CaptureDateTime'] = float(LastInfo['CaptureDateTime'])
            seconds = (LastInfo['CaptureDateTime'] - 25569) * 86400.0
            LastInfo['CaptureDateTime'] = datetime.datetime.utcfromtimestamp(seconds)
            
            LastInfo['SmearedImages'].append(lmk.iCaptureGetLastInfo()[11])
            LastInfo['SmearedImages'] = str(LastInfo['SmearedImages'])[1:-1]
            LastInfo['SmearedImages'] = int(LastInfo['SmearedImages'])
            
            LastInfo['ModulationFrequency'].append(lmk.iCaptureGetLastInfo()[12])
            LastInfo['ModulationFrequency'] = str(LastInfo['ModulationFrequency'])[1:-1]
            LastInfo['ModulationFrequency'] = float(LastInfo['ModulationFrequency'])
            
        return LastInfo
    
class Image():
    
    def GetSize(lmk, Image = imageType['Color']):
        """
        Get image size and parameter.|
        -----------------------------
        These informations are needed for the other access functions.
        See also Image.SetSize()
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: -1)
                | Index of image to inform about
        Returns:
            | Number of lines is LastLine - FirstLine + 1.
            | Number of columns is LastColumn - FirstColumn + 1.
            :FirstLine: int
                | Gets the index of the first line
            :LastLine: int
                | Gets the index of the last line
            :FirstColumn: int
                | Gets the index of the first column
            :LastColumn: int
                | Gets the index of the last column
            :Dimensions: int
                | 1 = gray images
                | 3 = color images
        """
        [ErrorCode, Image_FirstLine, Image_LastLine, Image_FirstColumn, Image_LastColumn, Image_Dimensions] = lmk.iImageGetSize(Image)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Image_FirstLine, Image_LastLine, Image_FirstColumn, Image_LastColumn, Image_Dimensions
    
    def Save(lmk, Image = imageType['Color'], FileName = MeasRoot + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + fileType['png']):
        """
        Save image.|
        -----------
        The function overwrites an existing file.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default -1)
                | Index of image to save
            :FileName: QString (default: 'C:/Desktop/Image.png')
                | Destination file name  
                | Datetime is the exact datetime of the measurement, not datetime when saved.
        """
        if not os.path.exists(MeasRoot):
            os.makedirs(MeasRoot)
        ErrorCode = lmk.iSaveImage(Image, FileName)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
    def Load(lmk, Image = imageType['Color'], FileName = MeasRoot + 'Image' + fileType['pcf']):
        """
        Load image from .pcf.|
        ---------------------
        Loads a saved image from .pcf. Of course, the image needs to be saved
        first.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default -1)
                | Index of image to Load to
            :FileName: QString (default: MeasRoot + 'Image.pcf')
                | Source file name
                | .pus = Camera Image
                | .pf = Luminance Image
                | .pcf = Color Image
        """
        ErrorCode = lmk.iLoadImage(Image, FileName)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
            
    def Show(FileName = MeasRoot + 'Image' + fileType['png']):
        """
        Show image.|
        -----------
        Shows a saved image. Of course, the image needs to be saved first.
        -----------------------------------------------------------------------
        Parameters:
            :FileName: QString (default: MeasRoot + 'Image.png')
                | Source file name   
        Returns:
            :image: uint8
                | Stores image into a numpy array and show it
        """
        image = io.imread(FileName) 
        io.imshow(image)
        
        return image
    
class Region():
    
    def Create(lmk, Image = imageType['Color'],
               Type = regionType['Ellipse']['identifier'],
               NumPoints = regionType['Ellipse']['points'],
               X = [1226, 500, 500], Y = [1026, 500, 500]):
        """
        Create a region.|
        ----------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Index of region list (same as image index)
            :Type: int (default: regionType['Ellipse']['identifier'])
                | Type of region from regionType{}
            :NumPoints: int (default: regionType['Ellipse']['points'])
                | Number of points from regionType{}
        Returns:
            :X: QStringList
                | List of x-points
            :Y: QStringList
                | List of y-points
        """
        [ErrorCode, Region_X_Points, Region_Y_Points] = lmk.iCreateRegion(Image, Type, NumPoints, X, Y)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Region_X_Points, Region_Y_Points
    
    def CreateRectImageSize(lmk, Im = imageType['Color'],
               Type = regionType['Rectangle']['identifier'],
               NumPoints = regionType['Rectangle']['points']):
        """
        Create a rectangular region the size of the whole image.|
        --------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Im: int (default: imageType['Color'])
                | Index of region list (same as image index)
                | Im is usually defined as 'Image', but we needed to call in Image() here
            :Type: int (default: regionType['Rectangle']['identifier'])
                | Type of region from regionType{}
            :NumPoints: int (default: regionType['Rectangle']['points'])
                | Number of points from regionType{}
        Returns:
            :X: QStringList
                | List of x-points
            :Y: QStringList
                | List of y-points
        """
        [Image_FirstLine, Image_LastLine, Image_FirstColumn, Image_LastColumn, _] = Image.GetSize(lmk)
        X = [Image_FirstColumn, Image_LastColumn]
        Y = [Image_FirstLine, Image_LastLine]
        [ErrorCode, Region_X_Points, Region_Y_Points] = lmk.iCreateRegion(Im, Type, NumPoints, X, Y)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Region_X_Points, Region_Y_Points
    
    def CreateGrid(lmk, Im = imageType['Color'],
               Type = regionType['Rectangle']['identifier'],
               NumPoints = regionType['Rectangle']['points'],
               X_Squares = 3, Y_Squares = 3):
        """
        Create a grid region within whole image with defined amount of squares.|
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Im: int (default: imageType['Color'])
                | Index of region list (same as image index)
                | Im is usually defined as 'Image', but we needed to call in Image() here
            :Type: int (default: regionType['Rectangle']['identifier'])
                | Type of region from regionType{}
            :NumPoints: int (default: regionType['Rectangle']['points'])
                | Number of points from regionType{}
            :X_Squares: int (default: 3)
                | Number of squares in grid along X axis
            :Y_Squares: int (default: 3)
                | Number of squares in grid along Y axis
        Returns:
            :X: QStringList
                | List of x-points
            :Y: QStringList
                | List of y-points
        """
        [Image_FirstLine, Image_LastLine, Image_FirstColumn, Image_LastColumn, _] = Image.GetSize(lmk)
        Image_SecondColumn = int(Image_LastColumn/3)
        Image_ThirdColumn = int((Image_LastColumn/3)*2)
        Image_SecondLine = int(Image_LastLine/3)
        Image_ThirdLine = int((Image_LastLine/3)*2)
        
#        X_Size = int(Image_LastColumn/X_Squares)
#        Y_Size = int(Image_LastLine/Y_Squares)
#        
#        for Y in range(Image_FirstLine, Image_LastLine, Y_Size):
#            Y_Pos = ((Image_FirstColumn, Y - Image_FirstLine), (Image_LastColumn, Y - Image_FirstLine))
            
        Xa = [Image_FirstColumn, Image_SecondColumn]
        Ya = [Image_FirstLine, Image_SecondLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xa, Ya)
        
        Xb = [Image_SecondColumn, Image_ThirdColumn]
        Yb = [Image_FirstLine, Image_SecondLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xb, Yb)
        
        Xc = [Image_ThirdColumn, Image_LastColumn]
        Yc = [Image_FirstLine, Image_SecondLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xc, Yc)
        
        Xd = [Image_FirstColumn, Image_SecondColumn]
        Yd = [Image_SecondLine, Image_ThirdLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xd, Yd)
        
        Xe = [Image_SecondColumn, Image_ThirdColumn]
        Ye = [Image_SecondLine, Image_ThirdLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xe, Ye)
        
        Xf = [Image_ThirdColumn, Image_LastColumn]
        Yf = [Image_SecondLine, Image_ThirdLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xf, Yf)
        
        Xg = [Image_FirstColumn, Image_SecondColumn]
        Yg = [Image_ThirdLine, Image_LastLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xg, Yg)
        
        Xh = [Image_SecondColumn, Image_ThirdColumn]
        Yh = [Image_ThirdLine, Image_LastLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xh, Yh)
        
        Xi = [Image_ThirdColumn, Image_LastColumn]
        Yi = [Image_ThirdLine, Image_LastLine]
        lmk.iCreateRegion(Im, Type, NumPoints, Xi, Yi)

#        X = [Image_FirstColumn, Image_LastColumn]
#        Y = [Image_FirstLine, Image_LastLine]
#        [ErrorCode, Region_X_Points, Region_Y_Points] = lmk.iCreateRegion(Im, Type, NumPoints, X, Y)        

        
    def GetID(lmk, Image = imageType['Color'], Name = '1'):
        """
        Get index of region given region name.|
        --------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Input: Index of region list (same as image index)
            :Name: QString (default: '1')
                | InputL Name of region
        Returns:
            :Index_Out: int
                | Output: Index of this region
        """
        [ErrorCode, Index_Out] = lmk.iGetIndexOfRegion(Image, Name)
#        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return ErrorCode, Index_Out
    
    def Select(lmk, Image = imageType['Color'], Index = 0, Select = 1):
        """
        Selects or deselects a region.|
        ------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Input: Index of region list (same as image index)
            :Index: int (default: 0)
                | Index of region
            :Select: int (default: 1)
                | 1= select region, 0= deselect region
        """
        ErrorCode = lmk.iSelectRegion(Image, Index, Select)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
                
    def Delete(lmk, Image = imageType['Color'], Index = 0):
        """
        Delete a region.|
        ----------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Input: Index of region list (same as image index)
            :Index: int (default: 0)
                | Index of region to delete
        """
        ErrorCode = lmk.iDeleteRegion(Image, Index)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
class Evaluation():
    
    def StatisticExists(lmk, Image = imageType['Color'], Region = 0):
        """
        Proof, if a statistic exists for a image / region / statistic type.|
        -------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: Image = imageType['Color'])
                | Image
            :Region: int (default: 0)
                | Index of region in this image
        Returns:
            :Exists: int
                | 1 = statistic exists
                | 0 = statistic does not exist
            :Type: int
                | Index of statistic type
            :Index: int
                | Index in statistic list?
        """
        [ErrorCode, Exists, StatisticType, StatisticIndex] = lmk.iHaveStatistic(Image, Region)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Exists, StatisticType, StatisticIndex
    
    def CreateStatistic(lmk, Type = statisticType['standardColor'],
                        Image = imageType['Color'], Region = 0,
                        NumParam = 1, ParamList = [1]):
        """
        Create a new statistic.|
        -----------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Type: int (default: statisticType['standardColor'])
                | Index of statistic type
            :Image: int (default: Image = imageType['Color'])
                | Image
            :Region: int (default: 0)
                | Index of region in this image
            :NumParam: int (default: 1)
                | Number of parameters for this statistic
            :ParamList: QStringList
        """
        [ErrorCode, Statistic] = lmk.iCreateStatistic(Type, Image, Region, NumParam, ParamList)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Statistic
    
    def GetStandardStatistic(lmk, Type = statisticType['standardColor'],
                             Region = 0, Class = 0):
        """
        Determine parameter of the standard statistic.|
        ----------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Type: int (default: statisticType['standardColor'])
                | Index of statistic type
            :Region: int (default: 0)
                | Index of region in this image
            :Class: int (default: 0)
                | Index of class or color:
                    0 = blue
                    1 = green
                    2 = red
        Returns:
            :Area: float
                | Amount of pixels in area of statistic
            :Min: float
                | Minimum value
            :Max: float
                | Maximum value
            :Mean: float
                | Mean value
            :Variance: float
                | Variance (...SD?) in values
        """
        
        Stats = {'Area': [], 'Min': [], 'Max': [], 'Mean': [], 'Variance': []}
        
        [ErrorCode, Area, Min, Max, Mean, Variance] = lmk.iGetStandardStatistic2(Type, Region, Class)
        if ErrorCode != 0:
            print ('Error code:', ErrorCode)
        else:
            Stats['Area'].append(lmk.iGetStandardStatistic2(Type, Region, Class)[1])
            Stats['Min'].append(lmk.iGetStandardStatistic2(Type, Region, Class)[2])
            Stats['Max'].append(lmk.iGetStandardStatistic2(Type, Region, Class)[3])
            Stats['Mean'].append(lmk.iGetStandardStatistic2(Type, Region, Class)[4])
            Stats['Variance'].append(lmk.iGetStandardStatistic2(Type, Region, Class)[5])
                                
        return Stats
    
    def DeleteStatistic(lmk, Type = statisticType['standardColor'], Stat_No = 0):
        """
        Delete an existing statistic.|
        -----------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Type: int (default: statisticType['standardColor'])
                | Index of statistic type
            :Stat_No: int (default: 0)
                | Index of statistic number
        """
        ErrorCode = lmk.iDeleteStatistic(Type, Stat_No)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
    
    def GetImageMeanXYZ(lmk):
        """
        Create region size of image and get mean XYZ.|
        ----------------------------------------------
        """
            
        # Create a region the size of the whole image
        Region_X_Points, Region_Y_Points = Region.CreateRectImageSize(lmk)
        # Get ID of region
        ErrorCode, Index_Out = Region.GetID(lmk, imageType['Color'], Name = '1')
        # Select region from index of region
        Region.Select(lmk, Index = Index_Out)
        
        ### Evaluate Region
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Out, ParamList = [1])
        
        Blue_Stats = Evaluation.GetStandardStatistic(lmk, Class = 0)
        B_Mean = str(Blue_Stats['Mean'])[1:-1]
        B_Mean = float(B_Mean)
        Green_Stats = Evaluation.GetStandardStatistic(lmk, Class = 1)
        G_Mean = str(Green_Stats['Mean'])[1:-1]
        G_Mean = float(G_Mean)
        Red_Stats = Evaluation.GetStandardStatistic(lmk, Class = 2)
        R_Mean = str(Red_Stats['Mean'])[1:-1]
        R_Mean = float(R_Mean)
                
        Output_Color = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean, CIE_G = G_Mean, CIE_B = B_Mean)
                
        return Output_Color
    
    def GetCircleMeanXYZ(lmk):
        """
        Get size of image, create eclipse in center, get mean XYZ from circle.|
        ----------------------------------------------------------------------
        """
        
        # Get size of image
        Image_FirstLine, Image_LastLine, Image_FirstColumn, Image_LastColumn, Image_Dimensions = Image.GetSize(lmk)
        
        # If region already exists, delete it
        ErrorCode, Index_Out = Region.GetID(lmk)
        if ErrorCode == 0:
            Region.Delete(lmk)
        
        # If statistic already exists, delete it
        Exists, StatisticType, StatisticIndex = Evaluation.StatisticExists(lmk)
        if Exists == 1:
            Evaluation.DeleteStatistic(lmk)
        
        # Create a region the size of the whole image
        Region_X_Points, Region_Y_Points = Region.Create(lmk,
                                                         X = [Image_LastColumn/2, 1700, 1700],
                                                         Y = [Image_LastLine/2, 1700, 1700])
        # Get ID of region
        ErrorCode, Index_Out = Region.GetID(lmk, imageType['Color'], Name = '1')
        # Select region from index of region
        Region.Select(lmk, Index = Index_Out)
        
        ### Evaluate Region
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Out, ParamList = [1])
        
        Blue_Stats = Evaluation.GetStandardStatistic(lmk, Class = 0)
        B_Mean = str(Blue_Stats['Mean'])[1:-1]
        B_Mean = float(B_Mean)
        Green_Stats = Evaluation.GetStandardStatistic(lmk, Class = 1)
        G_Mean = str(Green_Stats['Mean'])[1:-1]
        G_Mean = float(G_Mean)
        Red_Stats = Evaluation.GetStandardStatistic(lmk, Class = 2)
        R_Mean = str(Red_Stats['Mean'])[1:-1]
        R_Mean = float(R_Mean)
                
        Output_Color = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean, CIE_G = G_Mean, CIE_B = B_Mean)
                
        return Output_Color
        
    
    def GetGridMeanXYZ(lmk):
        """
        Create regions as a grid in image and get mean XYZ.|
        ---------------------------------------------------
        """
            
        # Create a region the size of the whole image
        Region.CreateGrid(lmk)
        # Get ID of region
        ErrorCode, Index_Zero = Region.GetID(lmk, imageType['Color'], Name = '1')
        ErrorCode, Index_One = Region.GetID(lmk, imageType['Color'], Name = '2')
        ErrorCode, Index_Two = Region.GetID(lmk, imageType['Color'], Name = '3')
        ErrorCode, Index_Three = Region.GetID(lmk, imageType['Color'], Name = '4')
        ErrorCode, Index_Four = Region.GetID(lmk, imageType['Color'], Name = '5')
        ErrorCode, Index_Five = Region.GetID(lmk, imageType['Color'], Name = '6')
        ErrorCode, Index_Six = Region.GetID(lmk, imageType['Color'], Name = '7')
        ErrorCode, Index_Seven = Region.GetID(lmk, imageType['Color'], Name = '8')
        ErrorCode, Index_Eight = Region.GetID(lmk, imageType['Color'], Name = '9')
        # Select region from index of region
        Region.Select(lmk, Index = Index_Zero)
        Region.Select(lmk, Index = Index_One)
        Region.Select(lmk, Index = Index_Two)
        Region.Select(lmk, Index = Index_Three)
        Region.Select(lmk, Index = Index_Four)
        Region.Select(lmk, Index = Index_Five)
        Region.Select(lmk, Index = Index_Six)
        Region.Select(lmk, Index = Index_Seven)
        Region.Select(lmk, Index = Index_Eight)
        
        ### Evaluate Region
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Zero, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_One, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Two, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Three, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Four, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Five, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Six, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Seven, ParamList = [1])
        Evaluation.CreateStatistic(lmk, statisticType['standardColor'], imageType['Color'], Index_Eight, ParamList = [1])
        
        Blue_Stats_Zero = Evaluation.GetStandardStatistic(lmk, Region = 0, Class = 0)
        B_Mean_Zero = str(Blue_Stats_Zero['Mean'])[1:-1]
        B_Mean_Zero = float(B_Mean_Zero)
        Green_Stats_Zero = Evaluation.GetStandardStatistic(lmk, Region = 0, Class = 1)
        G_Mean_Zero = str(Green_Stats_Zero['Mean'])[1:-1]
        G_Mean_Zero = float(G_Mean_Zero)
        Red_Stats_Zero = Evaluation.GetStandardStatistic(lmk, Region = 0, Class = 2)
        R_Mean_Zero = str(Red_Stats_Zero['Mean'])[1:-1]
        R_Mean_Zero = float(R_Mean_Zero)
        
        Blue_Stats_One = Evaluation.GetStandardStatistic(lmk, Region = 1, Class = 0)
        B_Mean_One = str(Blue_Stats_One['Mean'])[1:-1]
        B_Mean_One = float(B_Mean_One)
        Green_Stats_One = Evaluation.GetStandardStatistic(lmk, Region = 1, Class = 1)
        G_Mean_One = str(Green_Stats_One['Mean'])[1:-1]
        G_Mean_One = float(G_Mean_One)
        Red_Stats_One = Evaluation.GetStandardStatistic(lmk, Region = 1, Class = 2)
        R_Mean_One = str(Red_Stats_One['Mean'])[1:-1]
        R_Mean_One = float(R_Mean_One)
        
        Blue_Stats_Two = Evaluation.GetStandardStatistic(lmk, Region = 2, Class = 0)
        B_Mean_Two = str(Blue_Stats_Two['Mean'])[1:-1]
        B_Mean_Two = float(B_Mean_Two)
        Green_Stats_Two = Evaluation.GetStandardStatistic(lmk, Region = 2, Class = 1)
        G_Mean_Two = str(Green_Stats_Two['Mean'])[1:-1]
        G_Mean_Two = float(G_Mean_Two)
        Red_Stats_Two = Evaluation.GetStandardStatistic(lmk, Region = 2, Class = 2)
        R_Mean_Two = str(Red_Stats_Two['Mean'])[1:-1]
        R_Mean_Two = float(R_Mean_Two)
        
        Blue_Stats_Three = Evaluation.GetStandardStatistic(lmk, Region = 3, Class = 0)
        B_Mean_Three = str(Blue_Stats_Three['Mean'])[1:-1]
        B_Mean_Three = float(B_Mean_Three)
        Green_Stats_Three = Evaluation.GetStandardStatistic(lmk, Region = 3, Class = 1)
        G_Mean_Three = str(Green_Stats_Three['Mean'])[1:-1]
        G_Mean_Three = float(G_Mean_Three)
        Red_Stats_Three = Evaluation.GetStandardStatistic(lmk, Region = 3, Class = 2)
        R_Mean_Three = str(Red_Stats_Three['Mean'])[1:-1]
        R_Mean_Three = float(R_Mean_Three)
        
        Blue_Stats_Four = Evaluation.GetStandardStatistic(lmk, Region = 4, Class = 0)
        B_Mean_Four = str(Blue_Stats_Four['Mean'])[1:-1]
        B_Mean_Four = float(B_Mean_Four)
        Green_Stats_Four = Evaluation.GetStandardStatistic(lmk, Region = 4, Class = 1)
        G_Mean_Four = str(Green_Stats_Four['Mean'])[1:-1]
        G_Mean_Four = float(G_Mean_Four)
        Red_Stats_Four = Evaluation.GetStandardStatistic(lmk, Region = 4, Class = 2)
        R_Mean_Four = str(Red_Stats_Four['Mean'])[1:-1]
        R_Mean_Four = float(R_Mean_Four)
        
        Blue_Stats_Five = Evaluation.GetStandardStatistic(lmk, Region = 5, Class = 0)
        B_Mean_Five = str(Blue_Stats_Five['Mean'])[1:-1]
        B_Mean_Five = float(B_Mean_Five)
        Green_Stats_Five = Evaluation.GetStandardStatistic(lmk, Region = 5, Class = 1)
        G_Mean_Five = str(Green_Stats_Five['Mean'])[1:-1]
        G_Mean_Five = float(G_Mean_Five)
        Red_Stats_Five = Evaluation.GetStandardStatistic(lmk, Region = 5, Class = 2)
        R_Mean_Five = str(Red_Stats_Five['Mean'])[1:-1]
        R_Mean_Five = float(R_Mean_Five)
        
        Blue_Stats_Six = Evaluation.GetStandardStatistic(lmk, Region = 6, Class = 0)
        B_Mean_Six = str(Blue_Stats_Six['Mean'])[1:-1]
        B_Mean_Six = float(B_Mean_Six)
        Green_Stats_Six = Evaluation.GetStandardStatistic(lmk, Region = 6, Class = 1)
        G_Mean_Six = str(Green_Stats_Six['Mean'])[1:-1]
        G_Mean_Six = float(G_Mean_Six)
        Red_Stats_Six = Evaluation.GetStandardStatistic(lmk, Region = 6, Class = 2)
        R_Mean_Six = str(Red_Stats_Six['Mean'])[1:-1]
        R_Mean_Six = float(R_Mean_Six)
        
        Blue_Stats_Seven = Evaluation.GetStandardStatistic(lmk, Region = 7, Class = 0)
        B_Mean_Seven = str(Blue_Stats_Seven['Mean'])[1:-1]
        B_Mean_Seven = float(B_Mean_Seven)
        Green_Stats_Seven = Evaluation.GetStandardStatistic(lmk, Region = 7, Class = 1)
        G_Mean_Seven = str(Green_Stats_Seven['Mean'])[1:-1]
        G_Mean_Seven = float(G_Mean_Seven)
        Red_Stats_Seven = Evaluation.GetStandardStatistic(lmk, Region = 7, Class = 2)
        R_Mean_Seven = str(Red_Stats_Seven['Mean'])[1:-1]
        R_Mean_Seven = float(R_Mean_Seven)
        
        Blue_Stats_Eight = Evaluation.GetStandardStatistic(lmk, Region = 8, Class = 0)
        B_Mean_Eight = str(Blue_Stats_Eight['Mean'])[1:-1]
        B_Mean_Eight = float(B_Mean_Eight)
        Green_Stats_Eight = Evaluation.GetStandardStatistic(lmk, Region = 8, Class = 1)
        G_Mean_Eight = str(Green_Stats_Eight['Mean'])[1:-1]
        G_Mean_Eight = float(G_Mean_Eight)
        Red_Stats_Eight = Evaluation.GetStandardStatistic(lmk, Region = 8, Class = 2)
        R_Mean_Eight = str(Red_Stats_Eight['Mean'])[1:-1]
        R_Mean_Eight = float(R_Mean_Eight)
                
        Output_Color_Zero = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Zero, CIE_G = G_Mean_Zero, CIE_B = B_Mean_Zero)
        Output_Color_One = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_One, CIE_G = G_Mean_One, CIE_B = B_Mean_One)
        Output_Color_Two = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Two, CIE_G = G_Mean_Two, CIE_B = B_Mean_Two)
        Output_Color_Three = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Three, CIE_G = G_Mean_Three, CIE_B = B_Mean_Three)
        Output_Color_Four = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Four, CIE_G = G_Mean_Four, CIE_B = B_Mean_Four)
        Output_Color_Five = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Five, CIE_G = G_Mean_Five, CIE_B = B_Mean_Five)
        Output_Color_Six = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Six, CIE_G = G_Mean_Six, CIE_B = B_Mean_Six)
        Output_Color_Seven = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Seven, CIE_G = G_Mean_Seven, CIE_B = B_Mean_Seven)
        Output_Color_Eight = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R_Mean_Eight, CIE_G = G_Mean_Eight, CIE_B = B_Mean_Eight)
                
        return Output_Color_Zero, Output_Color_One, Output_Color_Two, Output_Color_Three, Output_Color_Four, Output_Color_Five, Output_Color_Six, Output_Color_Seven, Output_Color_Eight
        
    def GetColorHistogramValues(lmk, Image = imageType['Color'],
                                Color = colorSpace['XYZ']):
        """
        Get the values of the histogram in a color image.|
        -------------------------------------------------
        The color space is always RGB.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Index of object
            :Color: int (default: colorSpace['XYZ'])
                | Wished color space from colorSpace{}
        Returns:
            :NumParam: int
                | Number of values
            :X_Coords: QStringList
                | x-coordinates
            :HistValues: QStringList
                | Histogram values
        """
        [ErrorCode, NumParam, X_Coords, HistValues] = lmk.iGetColorHistogramValues(Image, Color)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return NumParam, X_Coords, HistValues
    
    def GetPixelColor(lmk, Image = imageType['Color'], Line = 500, Column = 500):
        """
        Get a pixel value of a color image.|
        -----------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Image: int (default: imageType['Color'])
                | Index of image
            :Line: int (default: 500)
                | Line index
            :Column: int (default: 500)
                | Column index
        Returns:
            | The function returns an error if the pixel position is
                outside or the image is a color image.
            :CIE_R: float
                | Gets the red component of the pixel value
            :CIE_G: float
                | Gets the green component of the pixel value
            :CIE_B: float
                | Gets the blue component of the pixel value
        """
        [ErrorCode, CIE_R, CIE_G, CIE_B] = lmk.iImageGetPixelColor(Image, Line, Column)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return CIE_R, CIE_G, CIE_B
        
    def Convert_CIE_RGB(lmk, CIE_R = 255.0, CIE_G = 0.0, CIE_B = 0.0, R_Ref = 0.0,
                     G_Ref = 0.0, B_Ref = 0.0, ColorSpace = colorSpace['XYZ']):
        """
        Conversion of a color value from CIE-RGB to another color space.|
        ----------------------------------------------------------------
        The color value is given in CIE-RGB and is converted into a color value
        in the target color space. If there is a reference color needed for this
        color space, the reference color is also in CIE-RGB. If there is no
        reference color needed, the three variables can be set to zero.
        The destination color space is given by the value of colorSpace{}.
        The three components of the destionation color are available
        in '_Out' after the function call returned.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :CIE_R: float (default: 255.0)
                | 	Red component of input color
            :CIE_G: float (default: 0.0)
                | 	Green component of input color
            :CIE_B: float (default: 0.0)
                | 	Blue component of input color
            :R_Ref: float (default: 0.0)
                | Red component of reference color
            :G_Ref: float (default: 0.0)
                | Green component of reference color
            :B_Ref: float (default: 0.0)
                | Blue component of reference color
            :ColorSpace: int (default: colorSpace['XYZ'])
                | 	Wished destination color space
        Returns:
            :Output_Color: array
                | Calculated color in an array shape of (1, 3)
        """
        [ErrorCode, Out_I, Out_II, Out_III] = lmk.iGetColor(CIE_R, CIE_G, CIE_B, R_Ref, G_Ref, 
                                               B_Ref, ColorSpace)
        if ErrorCode != 0:
            print ('Error code:', ErrorCode)
        else:
            # Place new values into an array
            Output_Color = np.array([[Out_I], [Out_II], [Out_III]])
            # Transpose array into (1, 3) shape
            Output_Color = Output_Color.T
        
        return Output_Color
    
    def XYZ_To_xy(XYZ):
        """
        Convert XYZ to x, y.|
        ---------------
        Parameters:
            :xyz: array (shape: (1, 3))
        Returns:
            :xy: array (shape: (1, 2))
        """
        Yxy = lx.xyz_to_Yxy(XYZ)
        Yxy_mean = np.array([[Yxy[:,0].mean(), Yxy[:,1].mean(), Yxy[:,2].mean()]])
        
        Yxy_Mean = np.around(Yxy_mean, decimals=3)
        
        x = Yxy_Mean[:,1]
        x = str(x)[1:-1]
        y = Yxy_Mean[:,2]
        y = str(y)[1:-1]
        
        xy = np.array([[x], [y]])
        xy = xy.T
        
        return xy
    
    def XYZ_To_u_v_(XYZ):
        """
        Conver XYZ to u', v'.|
        ---------------
        Parameters:
            :XYZ: array (shape: (1, 3))
        Returns:
            :u_v_: array (shape: (1, 2))
        """
        Yuv = lx.xyz_to_Yuv(XYZ)
        Yuv_mean = np.array([[Yuv[:,0].mean(), Yuv[:,1].mean(), Yuv[:,2].mean()]])
        
        Yuv_Mean = np.around(Yuv_mean, decimals=3)
        
        u_ = Yuv_Mean[:,1]
        u_ = str(u_)[1:-1]
        v_ = Yuv_Mean[:,2]
        v_ = str(v_)[1:-1]
                
        u_v_ = np.array([[u_], [v_]])
        u_v_ = u_v_.T
        
        return u_v_
        
    def Show_xy(x, y, label='x, y', facecolors='none', color='k', linestyle='--',
                title='x, y', grid=True, **kwargs):
        """
        Plot x, y color coordinates using Luxpy.
        
        Parameters:
            :x: float, int, or array
                | x coordinate(s)
            :y: float, int, or array
                | y coordinate(s)
            :label: string (default: 'x, y')
                | Change to adjust label within diagram of the input.
            :facecolors: string (default: 'none')
                | Change to adjust face color of value within diagram. Only if
                    gamut=None
            :color: string (default: 'k')
                | Change to adjust color of either edge color or line color,
                    depending on if 'gamut' is chosen.
            :linestyle: string (default: '--')
                | Change to adjust style of line if gamut is not None.
            :title: string (default: 'x, y')
                | Change to adjust title of figure.
            :grid: True of None (default: True)
                | Change to 'None' for no grid in diagram.
            :kwargs:
                | Additional keyword arguments for use with matplotlib.pyplot
                
        Returns:
            
        """
        plt.figure()
        ax_xy = plt.axes()
        lx.plot_chromaticity_diagram_colors(256,0.3,1,lx._CIEOBS,'Yxy',{},True,ax_xy,
                                            grid,'Times New Roman',12)
        plt.scatter(float(x), float(y), label = label, facecolors = facecolors, edgecolors = color)
        ax_xy.set_title(title)
        ax_xy.set_xlim([-0.1, 0.8])
        ax_xy.set_ylim([-0.1, 0.9])
        ax_xy.legend()
        
    def Show_u_v_(u_, v_, label='u_, v_', facecolors='none', color='k',
           linestyle='--', title='u_, v_', grid=True, **kwargs):
        """
        Plot u', v' color coordinates using Luxpy.
        
        Parameters:
            :u_: float, int, or array
                | u' coordinate(s)
            :v_: float, int, or array
                | v' coordinate(s)
            :label: string (default: 'u_, v_')
                | Change to adjust label within diagram of the input.
            :facecolors: string (default: 'none')
                | Change to adjust face color of value within diagram. Only if
                    gamut=None
            :color: string (default: 'k')
                | Change to adjust color of either edge color or line color,
                    depending on if 'gamut' is chosen.
            :linestyle: string (default: '--')
                | Change to adjust style of line if gamut is not None.
            :title: string (default: 'u_, v_')
                | Change to adjust title of figure.
            :grid: True of None (default: True)
                | Change to 'None' for no grid in diagram.
            :kwargs:
                | Additional keyword arguments for use with matplotlib.pyplot
                
        Returns:
            
        """
        plt.figure()
        ax_uv = plt.axes()
        lx.plot_chromaticity_diagram_colors(256,0.3,1,lx._CIEOBS,'Yuv',{},True,ax_uv,
                                            grid,'Times New Roman',12)
        plt.scatter(float(u_), float(v_), label = label, facecolors = facecolors, edgecolors = color)
        ax_uv.set_title(title)
        ax_uv.set_xlim([-0.1, 0.7])
        ax_uv.set_ylim([-0.1, 0.7])
        ax_uv.legend()
        
class Table():
    
    def GetNumber(lmk):
        """
        Returns the number of tables in the result tab widget.|
        ------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :Tables_No: int
                | Returns the number of tables
        """
        [ErrorCode, Tables_No] = lmk.iTableGetNumber()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Tables_No
    
    def TableGetNameAndCaption(lmk, Table_ID = 2):
        """
        Returns the name and the caption of an existing table.|
        ------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Table_ID: int (default: 2)
                | Index of wished table
        Returns:
            :Table_Name: QStringList
                | Returns the name of the table
            :Table_Caption: QStringList
                | Returns the caption of the table
        """
        [ErrorCode, Table_Name, Table_Caption] = lmk.iTableGetNameAndCaption(Table_ID)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Table_Name, Table_Caption
    
    def GetIndex(lmk, Table_NameOrCaption = 'Last capture'):
        """
        Search for a table, given by name or caption.|
        ---------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Table_NameOrCaption: QString (default: 'Last capture')
                | Searched name or caption of table
        Returns:
            :Table_ID: int (default: 2)
                | Index of table
                | -1 = not found
        """
        [ErrorCode, Table_ID] = lmk.iTableGetIndex(Table_NameOrCaption)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Table_ID
    
    def GetNumberColumns(lmk, Table_ID = 2):
        """
        Returns the number of columns of a table.|
        -----------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Table_ID: int (default: 2)
                | Index of wished table
        Returns:
            :Table_NumberColumns: int
                | Returns the number of columns in table
        """
        [ErrorCode, Table_NumberColumns] = lmk.iTableGetNumberColumns(Table_ID)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Table_NumberColumns
    
    def GetNumberLines(lmk, Table_ID = 2):
        """
        Returns the number of lines of a table.|
        ---------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Table_ID: int (default: 2)
                | Index of wished table
        Returns:
            :Table_NumberLines: int
                | Returns the number of lines in table
        """
        [ErrorCode, Table_NumberLines] = lmk.iTableGetNumberLines(Table_ID)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Table_NumberLines
    
    def GetColumn(lmk, Table_ID = 2, Table_ColumnID = 0):
        """
        Returns the column header of a column of a table.|
        -------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Table_ID: int (default: 2)
                | Index of wished table
            :Table_ColumnID: int (default: 0)
                | Index of wished column
        Returns:
            :Table_ColumnName: QString
                | Returns the name of the column
            :Table_ColumnCaption: QString
                | Returns the caption of the column
            :Table_ColumnUnit: QString
                | Returns the unit of the column
        """
        [ErrorCode, Table_ColumnName, Table_ColumnCaption, Table_ColumnUnit] = lmk.iTableGetColumn(Table_ID, Table_ColumnID)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Table_ColumnName, Table_ColumnCaption, Table_ColumnUnit
    
    def GetCell(lmk, Table_ID = 2, Table_LineID = 1, Table_ColumnID = 8):
        """
        Returns the content of a cell of a table.|
        -----------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Table_ID: int (default: 2)
                | Index of wished table
            :Table_LineID: int (default: 1)
                | Index of wished table line
            :Table_ColumnID: int (default: 8)
                | Index of wished table column
        Returns:
            :Table_Cell: QString
                | Returns the content of table cell
        """
        [ErrorCode, Table_Cell] = lmk.iTableGetCell(Table_ID, Table_LineID, Table_ColumnID)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Table_Cell
    
    def GetAllContent(lmk, Table_ID = 2):
        """
        Returns all cells of a table as a list.|
        ---------------------------------------
        The entries are sorted line by line.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Table_ID: int (default: 2)
                | Index of wished table
        Returns:
            :Table_Content: QStringList
                | List with content of all cells
        """
        [ErrorCode, Table_Content] = lmk.iGetAllContent(Table_ID)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Table_Content
    
class TIG():
    """
    Target Image Generator (TIG)|
    ----------------------------
    """
    
    def GetNoDisplays(lmk):
        """
        Number of connected displays.|
        -----------------------------
        At lease there is one - on which the program is shown.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :NoDisplays: int
                | Get number of available displays, at least one.
        """
        [ErrorCode, NoDisplays] = lmk.iTIG_GetNumberTargetDisplays()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return NoDisplays
    
    def GetTarget(lmk):
        """
        Get current target for template image generation.|
        -------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :DisplayID: int
                | -1 = Use given image name
                | 0...N-1 = One of the connected displays
            :DisplayName: QString
                | Image name is only returned if 'DisplayID' == -1
        """
        [ErrorCode, DisplayID, DisplayName] = lmk.iTIG_GetTarget()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return DisplayID, DisplayName
    
    def SetTarget(lmk, DisplayName, DisplayID):
        """
        Get current target for template image generation.|
        -------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :DisplayID: int
                | -1 = Use given image name
                | 0...N-1 = One of the connected displays
            :DisplayName: QString
                | Image name is only necessary if 'DisplayID' == -1
        """
        ErrorCode = lmk.iTIG_SetTarget(DisplayID, DisplayName)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetTargetProperties(lmk):
        """
        Get properties of current target.|
        ---------------------------------
        The size of the target image is fixed.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :TargetType: int
                | 1 = Monochrome image
                | 2 = Color image
                | 3 = Display
                |       in this case the type (monochrome or color)
                |       is chosen automatically
            :TargetHeight: int
                | Height in millimeters
            :TargetWidth: int
                | Width in millimeters
            :TargetLines: int
                | Number of image lines
            :TargetColumns: int
                | Number of image columns
        """
        [ErrorCode, TargetType, TargetHeight, TargetWidth, TargetLines, TargetColumns] = lmk.iTIG_GetTargetProperties()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return TargetType, TargetHeight, TargetWidth, TargetLines, TargetColumns
    
    def GetListOfCategories(lmk):
        """
        Get list of categories of template images.|
        ------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :Categories: QStringList
                | Shows list of categories for TIG
        """
        [ErrorCode, Categories] = lmk.iTIG_GetListOfCategories()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Categories
    
    def GetListOfOperations(lmk, Category):
        """
        Get list of types of template images for the given category.|
        ------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Category: QString
                | Chosen category
        Returns:
            :Operations: QStringList
                | Shows list of template image types for given category
        """
        [ErrorCode, Operations] = lmk.iTIG_GetListOfOperations(Category)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Operations
    
    def SetOperation(lmk, Category, Operation, Set = 1):
        """
        Set a type of template image or an option.|
        ------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Category: QString
                | Name of category
            :Operation: QString
                | Name of operation or option
            :Set: int
                | Set or unset.
                | This parameter is only valied if this is an option.
                |   (checkbox, not a radio button)
        """
        ErrorCode = lmk.iTIG_SetOperation(Category, Operation, Set)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def GetListOfParameterNames(lmk):
        """
        Get a parameter name list for the given template image type.|
        ------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        Returns:
            :Parameters: QStringList
                | Show parameter names in a list
        """
        [ErrorCode, Parameters] = lmk.iTIG_GetListOfParameterNames()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Parameters
    
    def GetParameterValue(lmk, Parameter):
        """
        Get a certain parameter value.|
        ------------------------------
        Parameters:
            :lmk: 
                | Dispatch('lmk4.LMKAxServer')
            :Parameter: QString
                | Name of parameter
        Returns:
            :Parameter_Value: float
                | Value of parameter (if bool, then 0 or 1)
        """
        [ErrorCode, Parameter_Value] = lmk.iTIG_GetParameterValue(Parameter)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
        return Parameter_Value
    
    def SetParameterValue(lmk, Parameter, Parameter_Value):
        """
        Set a certain parameter value.|
        ------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :Parameter: QString
                | Name of parameter
            :Parameter_Value: float
                | Value of parameter (if bool, then 0 or 1)                
        """
        ErrorCode = lmk.iTIG_SetParameterValue(Parameter, Parameter_Value)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
    
    def ShowDialog(lmk):
        """
        Make template image dialog visible.|
        -----------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        """
        ErrorCode = lmk.iTIG_ShowDialog()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def HideDialog(lmk):
        """
        Make template image dialog invisible.|
        -------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        """
        ErrorCode = lmk.iTIG_HideDialog()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def CreateImage(lmk):
        """
        Create template image with the adjusted parameters.|
        ---------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        """
        ErrorCode = lmk.iTIG_CreateImage()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def DeleteImage(lmk):
        """
        Remove template image from the display.|
        ---------------------------------------
        Template images can only be deleted from a display. If the target is an
        evaluation image, deletion is not possible.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
        """
        ErrorCode = lmk.iTIG_DeleteImage()
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
    def LoadImage(lmk, FileName):
        """
        Load template image file to the target.|
        ---------------------------------------
        This operation is only allowed for category 'User Defined'.
        -----------------------------------------------------------------------
        Parameters:
            :lmk:
                | Dispatch('lmk4.LMKAxServer')
            :FileName: QString
                | Name of an image file.
                | Allowed file extensions:
                |   .puc, .pus, .pf, .pco, .pcf, .bmp, .png, .jpg
        """
        ErrorCode = lmk.iTIG_LoadImage(FileName)
        ActiveX.ErrorCode(lmk, ErrorCode) # Check for error
        
def Setup(ModulationFrequency = 90.0):
            
        ### Initialize
        # Connect to ActiveX device
        lmk = ActiveX.Connect()
        # Open LMK LabSoft4 Standard Color ActiveX
        LabSoft.Open(lmk)
        camera, camera_no = Camera.SetCamera(camera = 'VR')
        lens, lens_no = Camera.SetLens(camera, lens = 'Conoscopic')
        Camera.Open(lmk, camera_no, lens_no)
        
        ### Adjust Camera
        # Set Modulation Frequency
        Camera.SetModulationFrequency(lmk, ModulationFrequency)
        # Change converting units so it doesn't multiply by two
        Camera.SetConvertingUnits(lmk)
                
        return lmk
    
def Max_Luminance(lmk, MinTime = 0.0, TimeRatio = 3.0, PicCount = 1):
        
    ### Capture Image
    # Capture a ColorHighDyn Image with Max Exposure Time of all Filters
    Capture.ColorHighDyn(lmk, AutoScan = False, MaxTime = 0.33, MinTime = MinTime,
                         TimeRatio = TimeRatio, PicCount = PicCount)
    
    ### Evaluate
    # Create a region the size of the whole image
    Region_X_Points, Region_Y_Points = Region.CreateRectImageSize(lmk)
    # Get ID of region
    ErrorCode, Index_Out = Region.GetID(lmk, imageType['Luminance'], Name = '1')
    # Select region from index of region
    Region.Select(lmk, Index = Index_Out)
        
    # Create statistic
    Evaluation.CreateStatistic(lmk, statisticType['standardGrey'], imageType['Luminance'], Index_Out, ParamList = [1])
    # Get max luminance of region
    Max_Lum = Table.GetCell(lmk, Table_ID = 2, Table_LineID = 0, Table_ColumnID = 6)
        
    Max_Lum = np.float64(Max_Lum)
    
    ### Save Measurement
    LabSoft.Save(lmk, FileName = MeasRoot + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + fileType['ttcs'])
        
    return Max_Lum
        
def Characterize(lmk, MinTime = 0.0, TimeRatio = 3.0, PicCount = 1):
    
    Char_Start = datetime.datetime.now()
    
    ### Capture Image
    # Capture a ColorHighDyn Image with Max Exposure Time of all Filters
    Capture.ColorHighDyn(lmk, AutoScan = False, MinTime = MinTime, TimeRatio = TimeRatio, PicCount = PicCount)
            
    ### Save Measurement
    LabSoft.Save(lmk, FileName = MeasRoot + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + fileType['ttcs'])
    
    Char_Fin = datetime.datetime.now()
    print ('Measured Image in: {}\n'.format(Char_Fin - Char_Start))
    
def Measure_WarmUp(warm_up = True, time_total = 120):
    
    time_warm = 0
    Output = []
    
    while time_warm < time_total:
        start = time.time()
        if datetime.datetime.now().minute % 1 == 0: 
            lmk = Setup()
            Max_Lum = Max_Luminance(lmk)
            LabSoft.Close(lmk)
            print (time_warm + 1, '(of', time_total, 'minutes)', '|', datetime.datetime.now().time(),
                   '|', Max_Lum, 'cd/m^2 (max)')
        time_warm = time_warm + 1
        Output.append([time_warm, Max_Lum])
        overlay = time.time() - start
        time.sleep(60 - overlay)
    
    if Output != []:
        Output = np.vstack((Output))
        
    return Output

def Get_Result_From_Folder(MeasRoot = 'E:/Measurements/2019-09-13-Char/', target = 'XYZ', region = 'Center Circle'):
    
    lmk = ActiveX.Connect()
    LabSoft.Open(lmk)
    
    Results = []
    
    for measurement in os.listdir(MeasRoot):
        if measurement.endswith('.ttcs'):
            LabSoft.Load(lmk, MeasRoot + '/' + measurement)
            if target == 'XYZ':
                if region == 'Whole Image':
                    Output = Evaluation.GetImageMeanXYZ(lmk)
                elif region == 'Center Circle':
                    Output = Evaluation.GetCircleMeanXYZ(lmk)
            elif target =='Y':
                if region == 'Whole Image':
                    Output = Max_Luminance(lmk)
            Results.append(Output)
        
    if Results != []:
        Results = np.vstack((Results))
        
    return Results
        
class VR_HMD():
    
    def __init__(self, ModulationFrequency = 90.0):
        
        
        ### Initialize
        # Connect to ActiveX device
        self.lmk = ActiveX.Connect()
        # Open LMK LabSoft4 Standard Color ActiveX
        LabSoft.Open(self.lmk)
        self.camera, self.camera_no = Camera.SetCamera(camera = 'VR')
        self.lens, self.lens_no = Camera.SetLens(self.camera, lens = 'Conoscopic')
        Camera.Open(self.lmk, self.camera_no, self.lens_no)
        
        ### Adjust Camera
        # Set Modulation Frequency
        Camera.SetModulationFrequency(self.lmk, ModulationFrequency)
        # Change converting units so it doesn't multiply by two
        Camera.SetConvertingUnits(self.lmk)
        
    
    def Characterize(self, MinTime = 0.0, TimeRatio = 3.0, PicCount = 1):
        """
        Characterize a Virtual Reality Head-Mounted-Display.|
        ----------------------------------------------------
        """
        Char_Start = datetime.datetime.now()
        
        ### Capture Image
        # Capture a ColorHighDyn Image with Max Exposure Time of all Filters
        Capture.ColorHighDyn(self.lmk, AutoScan = False, MinTime = MinTime, TimeRatio = TimeRatio, PicCount = PicCount)
#        # Pre-defined exposure time
#        MaxTime = Camera.SetIntegrationTime(lmk) # [REQUIRED for pre-defined exposure time]
#        Capture.ColorHighDyn(lmk, AutScan = False, MaxTime = MaxTime, MinTime = MinTime,
#                             TimeRatio = TimeRatio, PicCount = PicCount)
        
        ### Get Image Mean XYZ
        Output_Color = Evaluation.GetImageMeanXYZ(self.lmk)
#        Output_Color_Zero, Output_Color_One, Output_Color_Two, Output_Color_Three, Output_Color_Four, Output_Color_Five, Output_Color_Six, Output_Color_Seven, Output_Color_Eight = Evaluation.GetGridMeanXYZ(lmk)
        
        ### Save Measurement
        LabSoft.Save(self.lmk, FileName = MeasRoot + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + fileType['ttcs'])
        
        Char_Fin = datetime.datetime.now()
        print ('Measured Image in: {}\n'.format(Char_Fin - Char_Start))
        
        return Output_Color
    
class Email():
    # Setup an email address to email from and to
    # https://automatetheboringstuff.com/chapter16/
    def Connect(email, password, SMTP = 'smtp.gmail.com', gate = 587):
        
        # Connect to an SMTP server
        smtpObj = smtplib.SMTP(SMTP, gate)
        # Establish a connection to the SMTP server
        smtpObj.ehlo()
        # Enable encryption for connection
        smtpObj.starttls()
        # Enter login details
        smtpObj.login(email, password)
        
        return smtpObj
    
    # Send email to given email address    
    def Send(smtpObj, email):
        # Send mail with text to email
        smtpObj.sendmail(email, email, 'Subject: Measurement\nMeasurement finished.')
        
    def Disconnect(smtpObj):
        # Close email connection
        smtpObj.quit()


#if __name__ == '__main__':
#    # Define Camera Parameters
#    ModulationFrequency = 90.0   # Modulation Frequency
#    MinTime = 0.0                # Smallest Exposure Time (proposal: 0.0)
#    TimeRatio = 3.0              # TimeRatio between two times (proposal: 3.0)
#    PicCount = 1                 # Number of shots per integration time
#    
#    ### Initialize [REQUIRED]
#    # Connect to ActiveX device [REQUIRED]
#    lmk = ActiveX.Connect()
#    # Open LMK LabSoft4 Standard Color ActiveX [REQUIRED]
#    LabSoft.Open(lmk)
#    # Connect to Camera [REQUIRED] 
#    Camera.Open(lmk, CalibrationDataRoot)
#    
#    ### Adjust Camera
#    # Set Modulation Frequency
#    Camera.SetModulationFrequency(lmk, ModulationFrequency)
#    # Calculate Max Exposure Times for all filters
#    ExposureTimes = Camera.ColorAutoScanTime(lmk)
#    
#    ### Capture Image
#    # Capture a ColorHighDyn Image with Max Exposure Time of all Filters
#    Capture.ColorHighDyn(lmk, MaxTime = max(ExposureTimes.items(),
#                                            key=operator.itemgetter(1))[1],
#        MinTime = MinTime, TimeRatio = TimeRatio, PicCount = PicCount)
#    
#    ### Create Region on Image
#    # Create an ellipse region on image
#    Region.Create(lmk, imageType['Color'],
#                          regionType['Ellipse']['identifier'],
#                          regionType['Ellipse']['points'],
#                          X = [1226, 500, 500], Y = [1026, 500, 500])
#    # Create a region the size of the whole image
#    Region_X_Points, Region_Y_Points = Region.CreateRectImageSize(lmk)
#    # Get ID of region
#    ErrorCode, Index_Out = Region.GetID(lmk, imageType['Color'], Name = '1')
#    # Select region from index of region
#    Region.Select(lmk, Index = Index_Out)    
#    
#    ### Evaluate Image
#    # Create a standard color statistic
#    Evaluation.CreateStatistic(lmk, statisticType['standardColor'],
#                               imageType['Color'], Index_Out, ParamList = [1])
    
#    Blue_Stats = Evaluation.GetStandardStatistic(lmk, Class = 0)
#    Green_Stats = Evaluation.GetStandardStatistic(lmk, Class = 1)
#    Red_Stats = Evaluation.GetStandardStatistic(lmk, Class = 2)
    
    # Get Pixel Color
#    R, G, B = Evaluation.GetPixelColor(lmk, Line = 800, Column = 1300)
##    Convert CIE-RGB to XYZ
#    Output_Color = Evaluation.Convert_CIE_RGB(lmk, CIE_R = R, CIE_G = G, CIE_B = B)
#    # Convert XYZ into Yuv
#    u_v_ = Evaluation.XYZ_To_u_v_(Output_Color)
#    # Show u'v' in diagram
#    Evaluation.Show_u_v_(u_ = u_v_[:,0], v_ = u_v_[:,1])
    
#    ### Save
#    # Save measurement as an image
#    Image.Save(lmk, imageType['Color'], MeasRoot + MeasName + extension)
#    # Save measurement as .ttcs file. Can be reopened again.
#    LabSoft.Save(lmk, PathName = MeasRoot + 'Meas' + fileType['ttcs'])