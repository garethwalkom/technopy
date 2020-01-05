# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:00:11 2019
@author: Gareth V. Walkom (walkga04 at googlemail.com)

To-do:|
------
    * Compare on one figure (multiple figures are opening)
    * Add measurements from Perez
    * Add all previous measurements
    * Get measurements from file
    * Get RGB values from calibration file
    * Get RGBs from file and use as key/name/seperate array
    * Analyze calibration data into graphs
    * Analyze calibration data into statistics
    * Write look-up tables
    * Fix messy functions

"""
import numpy as np
import luxpy as lx

import Analyze as anal

## Define Gamuts
# Each array should be ordered depending on what data you want to use (e.g.: x, y, u_ (u'), v_, (v'))
# Then, to draw array as a gamut, the rows must be ordered correctly to follow
# the line of the gamut and then closed back to the starting point
# (e.g.: R, G, B, R or R, Y, G, C, B, M, R)
# Split each column into seperate variables, so they can be called individually later

class MonitorAssetManager():
    
    def Oculus(new = True, color ='k'):
        x, y = np.array([[0.665, 0.250, 0.139, 0.665],
                           [0.334, 0.711, 0.050, 0.334]])
        anal.Show.xy(x, y, gamut = True, label = 'MonInfo: Oculus', title = None, color = color, new = new)
        Area = Find.Area(x, y)
        
        return Area
    
    def DELL_P2217H(new = True, color ='r'):
        x, y = np.array([[0.655, 0.325, 0.154, 0.655],
                           [0.336, 0.612, 0.065, 0.336]])
        anal.Show.xy(x, y, gamut = True, label = 'MonInfo: DELL P2217H', title = None, color = color, new = new)
        Area = Find.Area(x, y)
        
        return Area
    
    def DELL_SP2208WFP(new = True, color ='g'):
        x, y = np.array([[0.660, 0.217, 0.146, 0.660],
                           [0.325, 0.676, 0.075, 0.325]])
        anal.Show.xy(x, y, gamut = True, label = 'MonInfo: DELL SP2208WFP', title = None, color = color, new = new)
        Area = Find.Area(x, y)
        
        return Area

class Meas_2019_09_26():
    # Measurements from 2019/09/26
    # ++++++++++++++++ NEW LMK LENS ++++++++++++++++
    def __init__(self):
        self.root = 'E:/Github/VR-HMDs/VR-HMDs/Oculus Rift CV1/Measurements/'
        self.date = '2019-09-26'
    
        CapOn = self.root + self.date + '/' + 'CapOn.txt'
        XYZs, Yuvs, count = Convert.XYZ_to_space(input_type = 'file', file = CapOn)
#        CapOn = np.array([[2.12e-09, 6.16e-10, 1.08e-08]])
    
    def All(self):
        self.OpenVR(new = True)
        self.Matlab(new = False)
        self.Unity(new = False)
        self.Unreal(new = False)
        self.VirtualDesktop(new = False)
        self.Unity_Python(new = False)
        self.OpenVR_Left(new = False)
        
    def OpenVR(self, space = 'uv', new = True, color='k', input_type = 'file',
               label = 'OpenVR'):
        meas = self.root + self.date + '/' + 'OpenVR.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
        
#        white = np.array([[74.94, 74.65, 92.39]])
        
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)               
    
    def Matlab(self, space = 'uv', new = True, color='r', input_type = 'file',
               label = 'Matlab'):
        meas = self.root + self.date + '/' + 'Matlab.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
#        white = np.array([[74.57, 74.24, 91.98]])
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label) 
    
    def Unity(self, space = 'uv', new = True, color='g', input_type = 'file',
              label = 'Unity'):
        meas = self.root + self.date + '/' + 'Unity.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
#        white = np.array([[74.59, 74.22, 91.92]])
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label) 
    
    def Unreal(self, space = 'uv', new = True, color='b', input_type = 'file',
               label = 'Unreal'):
        meas = self.root + self.date + '/' + 'Unreal.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
#        white = np.array([[59.29, 59.33, 73.97]])
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)
    
    def VirtualDesktop(self, space = 'uv', new = True, color='c', input_type = 'file',
                       label = 'Virtual Desktop'):
        meas = self.root + self.date + '/' + 'Virtual Desktop.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
#        white = np.array([[74.57, 74.04, 91.9]])
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)
    
    def Unity_Python(self, space = 'uv', new = True, color='m', input_type = 'file',
                     label = 'Unity - Python'):
        meas = self.root + self.date + '/' + 'Unity-Python.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
#        white = np.array([[75.14, 74.83, 92.68]])
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)
    
    def OpenVR_Left(self, space = 'uv', new = True, color='y', input_type = 'file',
                    label = 'OpenVR - Left Eye'):
        meas = self.root + self.date + '/' + 'OpenVR Left_Eye.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
#        white = np.array([[68.49, 70.3, 86.61]])
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)

class Meas_2019_09_13():
    # Measurements from 2019/09/13
    # ++++++++++++++++ NEW LMK LENS ++++++++++++++++
    def __init__(self):
        self.root = 'E:/Github/VR-HMDs/VR-HMDs/Oculus Rift CV1/Measurements/'
        self.date = '2019-09-13'
        
    def All(self):
        self.OpenVR(new = True)
        self.OpenVR_Spot(new = False)
        
        
    def OpenVR(self, space = 'uv', new = True, color='k', input_type = 'file',
               label = 'OpenVR'):
        meas = self.root + self.date + '/' + 'OpenVR.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
        
#        white = np.array([[74.79, 74.2, 92.65]])
        
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)
        
    def OpenVR_Spot(self, space = 'uv', new = True, color='r', input_type = 'file',
               label = 'OpenVR - Spot'):
        meas = self.root + self.date + '/' + 'OpenVR_Spot.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
        
#        white = np.array([[81.0408, 81.6936, 89.5038]])
        
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label) 

class Meas_2019_04_13():
    # Measurements from 2019/09/26
    # ++++++++++++++++ OLD LMK LENS ++++++++++++++++
    def __init__(self):
        self.root = 'E:/Github/VR-HMDs/VR-HMDs/Oculus Rift CV1/Measurements/'
        self.date = '2019-04-13'
        
    def All(self):
        self.Matlab(new = True)
        self.Unreal(new = False)
        self.Unity(new = False)
    
    def Matlab(self, space = 'uv', new = True, color = 'k', input_type = 'file',
               label = 'Matlab'):
        meas = self.root + self.date + '/' + 'Matlab.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)
    
    def Unreal(self, space = 'uv', new = True, color = 'r', input_type = 'file',
               label = 'Unreal'):
        meas = self.root + self.date + '/' + 'Unreal.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)  
        
#        white = np.array([[61.33, 61.97, 75.46]])
        
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)
        
    def Unity(self, space = 'uv', new = True, color = 'g', input_type = 'file',
               label = 'Unity'):
        meas = self.root + self.date + '/' + 'Unity.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)  
        
#        white = np.array([[81.38, 81.33, 98.69]])
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.date + ': ' + label)
    
class Literature():
    
    def __init__(self):
        self.root = 'E:/Github/VR-HMDs/VR-HMDs/Oculus Rift CV1/Literature'
        self.type = 'Literature'
    
    def Perez2018(self, space = 'uv', new = True, color = 'k', input_type = 'file',
                  label = 'Perez 2018'):
        # Perez2018_Is it possible to apply colour management techniques in Virtual Reality devices
        meas = self.root + '/' + 'Perez2018.txt'
        
        XYZs, output, count = Convert.XYZ_to_space(input_type = input_type,
                                                 file = meas, space = space)        
                
        show(input_type = input_type, space = space, count = count,
             output = output, new = new, color = color, label = self.type + ': ' + label)
        
## Color Spaces
class ColorSpace():
    
    def Show(Diagram, space, x, y, u_, v_, title = 'Color Space', color = 'k', new = False):
    
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_, gamut = True, title = title, label = space, color = color, new = new)
            Area = Find.Area(u_, v_)
        else:
            anal.Show.xy(x, y, gamut=True, title = title, label = space)
            Area = Find.Area(x, y)
            
        return Area
    
    def All():
        ColorSpace.sRGB(new = True)
        ColorSpace.AdobeRGB(new = False)
        ColorSpace.AdobeWide(new = False)
        ColorSpace.DCI_P3(new = False)
        ColorSpace.NTSC1953(new = False)
        ColorSpace.Rec2020(new = False)
        ColorSpace.Rec2100(new = False)
        
    # sRGB Gamut (Rec.709 is the same)
    def sRGB(Diagram = 'u_v_', space = 'sRGB', color = 'k', new = True):      
        x, y, u_, v_ = np.array([[0.64000, 0.30000, 0.15000, 0.64000],
                                 [0.33000, 0.60000, 0.06000, 0.33000],
                                 [0.45070, 0.12500, 0.17544, 0.45070],
                                 [0.52289, 0.56250, 0.15789, 0.52289]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
        
        return Area
    
    # Adobe sRGB Gamut
    def AdobeRGB(Diagram = 'u_v_', space = 'AdobeRGB', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.64000, 0.21000, 0.15000, 0.64000],
                                 [0.33000, 0.71000, 0.06000, 0.33000],
                                 [0.45070, 0.07568, 0.17544, 0.45070],
                                 [0.52289, 0.57568, 0.15789, 0.52289]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area
    
    # Adobe Wide Gamut RGB
    def AdobeWide(Diagram = 'u_v_', space = 'Adobe Wide', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.73469, 0.11416, 0.15664, 0.73469],
                                 [0.26531, 0.82621, 0.01770, 0.26531],
                                 [0.62337, 0.03600, 0.21612, 0.62337],
                                 [0.50650, 0.58614, 0.05495, 0.50650]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area
    
    # DCI P3 Gamut
    def DCI_P3(Diagram = 'u_v_', space = 'DCI P3', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.68000, 0.26500, 0.15000, 0.68000],
                                 [0.32000, 0.69000, 0.06000, 0.32000],
                                 [0.49635, 0.09860, 0.17544, 0.49635],
                                 [0.52555, 0.57767, 0.15789, 0.52555]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area
    
    # NTSC 1953 Gamut
    def NTSC1953(Diagram = 'u_v_', space = 'NTSC 1953', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.67000, 0.21000, 0.14000, 0.67000],
                                 [0.33000, 0.71000, 0.08000, 0.33000],
                                 [0.47687, 0.07568, 0.15217, 0.47687],
                                 [0.52847, 0.57568, 0.19565, 0.52847]])

        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area
    
    # Rec. 2020 Gamut
    def Rec2020(Diagram = 'u_v_', space = 'Rec. 2020', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.70792, 0.17024, 0.13137, 0.70792],
                                 [0.29203, 0.79652, 0.04588, 0.29203],
                                 [0.55648, 0.05574, 0.15983, 0.55648],
                                 [0.51651, 0.58674, 0.12558, 0.51651]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area
    
    # Rec. 2100 Gamut
    def Rec2100(Diagram = 'u_v_', space = 'Rec. 2100', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.70800, 0.17000, 0.13100, 0.70800],
                                 [0.29220, 0.79700, 0.04600, 0.29220],
                                 [0.55634, 0.05563, 0.15927, 0.55634],
                                 [0.51662, 0.58680, 0.12584, 0.51662]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area
    
    ## ACES Gamut
    def ACES(Diagram = 'u_v_', space = 'ACES', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.73470, 0.00000, 0.00010, 0.73470],
                                 [0.26530, 1.00000, -0.07700, 0.26530],
                                 [0.62339, 0.00000, 0.00019, 0.62339],
                                 [0.50649, 0.60000, -0.33385, 0.50649]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area
    
    # ProPhoto RGB Gamut
    def ProPhotoRGB(Diagram = 'u_v_', space = 'Pro Photo RGB', color = 'k', new = True):
        x, y, u_, v_ = np.array([[0.73470, 0.15960, 0.03660, 0.73470],
                                 [0.00010, 0.84040, 0.26530, 0.00010],
                                 [0.62340, 0.05000, 0.05000, 0.62340],
                                 [0.50650, 0.59250, 0.00030, 0.50650]])
        
        Area = ColorSpace.Show(Diagram, space, x, y, u_, v_, color = color, new = new)
            
        return Area

## Define White Points
# This needs to be seperate from the previous imported data, as we don't want
# the gamut line being drawn to the white point
# Same structure as columns from data [x, y, u_ (u'), v_ (v')] 
class WhitePoint():
    
    def A(self, Diagram = 'u_v_'):
        
        x, y, u_, v_ = np.array([[0.44758], [0.40745], [0.25597], [0.52430]])
        
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)
            
    def B(self, Diagram = 'u_v_'):
        
        x, y, u_, v_ = np.array([[0.34842], [0.35161], [0.21367], [0.48517]])
        
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)
            
    def C(self, Diagram = 'u_v_'):
        
        x, y, u_, v_ = np.array([[0.31006], [0.31616], [0.20089], [0.46089]])
        
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)
            
    def D50(self, Diagram = 'u_v_'):
        
        x, y, u_, v_ = np.array([[0.34567], [0.35850], [0.20916], [0.48808]])
        
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)

    def D65(self, Diagram = 'u_v_'):
        
        x, y, u_, v_ = np.array([[0.31270], [0.32900], [0.19783], [0.46832]])
        
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)

## Monitors       
class Monitor:
    
    def __init__(self):
    
        self.title = 'Monitor'
    
    # AU Optronics M270DAN01.1 Gamut
    def AUM270(self, Diagram = 'u_v_', target = 'AU Optronics M270DAN01.1'):
        
        x, y, u_, v_ = np.array([[0.68900, 0.20800, 0.14900, 0.68900],
                                 [0.29900, 0.71400, 0.05000, 0.29900],
                                 [0.528983, 0.074605, 0.180497, 0.528983],
                                 [0.51651, 0.57622, 0.13628, 0.51651]])
        
        Area = Draw.Gamut(Diagram, target, x, y, u_, v_, self.title)
            
        return Area
                
    # LG Display LM240WU4 Gamut
    def LGLMWU4(self, Diagram = 'u_v_', target = 'LG Display LM240WU4'):
        
        x, y, u_, v_ = np.array([[0.68000, 0.20600, 0.15100, 0.68000],
                                 [0.31000, 0.69300, 0.05500, 0.31000],
                                 [0.507463, 0.075569, 0.179869, 0.507463],
                                 [0.52052, 0.57199, 0.14741, 0.52052]])
        
        Area = Monitor.Show(Diagram, target, x, y, u_, v_)
            
        return Area
    
    # LG Display LM240WU5-SLA1 Gamut
    def LGLMWU5(self, Diagram = 'u_v_', target = 'LG Display LM240WU5-SLA1'):    
        
        x, y, u_, v_ = np.array([[0.69000, 0.20500, 0.15000, 0.69000],
                                 [0.30000, 0.71500, 0.04500, 0.30000],
                                 [0.528736, 0.073411, 0.185185, 0.528736],
                                 [0.51724, 0.57610, 0.12500, 0.51724]])
        
        Area = Monitor.Show(Diagram, target, x, y, u_, v_)
            
        return Area
    
    # LG Displays: LM240WU9-SLA1 / LM270WQ3-SLA1 / LM300WQ6-SLA1 Gamut
    def LGLMWU9(self, Diagram = 'u_v_', target = 'LG Displays: LM240WU9-SLA1 / LM270WQ3-SLA1 / LM300WQ6-SLA1'):
        
        x, y, u_, v_ = np.array([[0.68000, 0.21000, 0.14700, 0.68000],
                                 [0.31000, 0.70000, 0.05400, 0.31000],
                                 [0.507463, 0.076503, 0.175313, 0.507463],
                                 [0.52052, 0.57377, 0.14490, 0.52052]])
        
        Area = Monitor.Show(Diagram, target, x, y, u_, v_)
            
        return Area
    
    # LG Display LM270WQ2-SLA1 Gamut
    def LGLMWQ2(self, Diagram = 'u_v_', target = 'LG Display LM270WQ2-SLA1'):
        
        x, y, u_, v_ = np.array([[0.67800, 0.20200, 0.14800, 0.67800],
                                 [0.30900, 0.68900, 0.05100, 0.30900],
                                 [0.506726, 0.074374, 0.178528, 0.506726],
                                 [0.51962, 0.57078, 0.13842, 0.51962]])

        Area = Monitor.Show(Diagram, target, x, y, u_, v_)
            
        return Area
    
    # LG Display LM300WQ5 Gamut
    def LGLMWQ5(self, Diagram = 'u_v_', target = 'LG Display LM300WQ5'):
        
        x, y, u_, v_ = np.array([[0.67800, 0.21000, 0.14600, 0.67800],
                                 [0.30900, 0.69200, 0.05500, 0.30900],
                                 [0.506726, 0.077178, 0.173397, 0.506726],
                                 [0.51962, 0.57222, 0.14697, 0.51962]])
        
        Area = Monitor.Show(Diagram, target, x, y, u_, v_)
            
        return Area
    
    # Samsung LTM240CS02
    def SAMLTM(self, Diagram = 'u_v_', target = 'Samsung LTM240CS02'):
        
        x, y, u_, v_ = np.array([[0.69200, 0.20500, 0.14800, 0.69200],
                                 [0.29500, 0.71700, 0.06500, 0.29500],
                                 [0.53685, 0.073254, 0.16992, 0.53685],
                                 [0.51493, 0.57647, 0.16791, 0.51493]])
        
        Area = Monitor.Show(Diagram, target, x, y, u_, v_)
            
        return Area
    
    # Mitsubishi LaserVue
    def MITSLV(self, Diagram = 'u_v_', target = 'Mitsubishi LaserVue'):
        x, y, u_, v_ = np.array([[0.71903, 0.17024, 0.15947, 0.71903],
                                 [0.28093, 0.79652, 0.01523, 0.28093],
                                 [0.583025, 0.055735, 0.222737, 0.583025],
                                 [0.51253, 0.58674, 0.04786, 0.51253]])
        
        Area = Monitor.Show(Diagram, target, x, y, u_, v_)
            
        return Area

## Laptops
class Laptop():
    
    # AU Optronics B156HW01: V0 / V1 / V2 / V3 / V5 / V6
    def AUOW01(self, Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.62300, 0.33600, 0.14800, 0.62300],
                                 [0.35100, 0.57400, 0.05300, 0.35100],
                                 [0.41770, 0.14583, 0.17725, 0.41770],
                                 [0.52950, 0.56055, 0.14281, 0.52950]])
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)
    
    # AU Optronics B156XW04 V5
    def AUOW04(self, Diagram = 'u_v_'):    
        x, y, u_, v_ = np.array([[0.59000, 0.33000, 0.15000, 0.59000],
                                 [0.34000, 0.55000, 0.14000, 0.34000],
                                 [0.40000, 0.14765, 0.13699, 0.40000],
                                 [0.51864, 0.55369, 0.28767, 0.51864]])
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)
    
    # LG Displays: LP156WF3 / LP171WU8-SLB1
    def LGLP15(self, Diagram = 'u_v_'):    
        x, y, u_, v_ = np.array([[0.68600, 0.20600, 0.14500, 0.68600],
                                 [0.30800, 0.71500, 0.04500, 0.30800],
                                 [0.51540, 0.07378, 0.17846, 0.51540],
                                 [0.52066, 0.57620, 0.12462, 0.52066]])
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)
    
    # LG Display LP171WU5-TLB1
    def LGLP171(self, Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.68820, 0.20190, 0.14400, 0.68820],
                                 [0.30590, 0.71720, 0.05100, 0.30590],
                                 [0.51995, 0.07209, 0.17329, 0.51995],
                                 [0.52000, 0.57619, 0.13809, 0.52000]])
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)
    
    # LG Display LP173WF3
    def LGLP173(self, Diagram = 'u_v_'):    
        x, y, u_, v_ = np.array([[0.68200, 0.19900, 0.15100, 0.68200],
                                 [0.30500, 0.72100, 0.04500, 0.30500],
                                 [0.51511, 0.07073, 0.18653, 0.51511],
                                 [0.51832, 0.57659, 0.12508, 0.51832]])
        if Diagram == 'u_v_':
            anal.Show.uv(u_, v_)
        else:
            anal.Show.xy(x, y)

class Draw:
    
    def Gamut(self, Diagram, target, x, y, u_, v_, title = 'Color Space'):
    
        if Diagram == 'u_v_':
            anal.Show().uv(u_, v_, gamut = True, title = title, label = target)
            Area = Find.Area(u_, v_)
        else:
            anal.Show().xy(x, y, gamut = True, title = title, label = target)
            Area = Find.Area(x, y)
            
        return Area

## Analyze Gamut
class Find():
    
    # If xy: u_ = x, v_ = y
    def Area(u_, v_):
        
        Area = ((u_[1] - u_[2]) * (v_[1] + v_[2]) + (u_[0] - u_[1]) * (v_[0] + v_[1]) - (u_[0] - u_[2]) * (v_[0] + v_[2]))/2 * 100
        
        return Area
    
class Convert():
    
    def XYZ_to_space(input_type = 'RGB', R = None, G = None, B = None, W = None,
                     file = 'GW_2019-09-13.txt', space = 'uv'):
        
        if input_type == 'RGB':
            R_Yuv = lx.xyz_to_Yuv(R)
            G_Yuv = lx.xyz_to_Yuv(G)
            B_Yuv = lx.xyz_to_Yuv(B)
            return R_Yuv, G_Yuv, B_Yuv
        
        elif input_type == 'RGBW':
            R_Yuv = lx.xyz_to_Yuv(R)
            G_Yuv = lx.xyz_to_Yuv(G)
            B_Yuv = lx.xyz_to_Yuv(B)
            W_Yuv = lx.xyz_to_Yuv(W)
            return R_Yuv, G_Yuv, B_Yuv, W_Yuv
        
        elif input_type == 'file':
            XYZs = np.loadtxt(file, delimiter = '\t')
            if space == 'uv':
                output = lx.xyz_to_Yuv(XYZs)
            else:
                output = lx.xyz_to_Yxy(XYZs)
            for count, row in enumerate(output):
                count = count + 1
            return XYZs, output, count
    
    def Input_to_gamut(input_type = 'RGB', count = None, output = None, R = None,
                       G = None, B = None, C = None, M = None, Y = None):
        
        if input_type == 'RGB':
            u_, v_ = np.array([[R[:,1], G[:,1],
                                B[:,1], R[:,1]],
                               [R[:,2], G[:,2],
                                B[:,2], R[:,2]]])
        elif input_type == 'RGBCMY':
            u_, v_ = np.array([[R[:,1], Y[:,1],
                                G[:,1], C[:,1],
                                B[:,1], M[:,1],
                                R[:,1]],
                               [R[:,2], Y[:,2],
                                G[:,2], C[:,2],
                                B[:,2], M[:,2],
                                R[:,2]]])
        elif input_type == 'file':
            if count == 4:
                u_, v_ = np.array([[output[0,1], output[1,1],
                                    output[2,1], output[0,1]],
                                   [output[0,2], output[1,2],
                                    output[2,2], output[0,2]]])
            
            elif count == 7 or count == 8:
                u_, v_ = np.array([[output[0,1], output[6,1], output[1,1],
                                    output[4,1], output[2,1], output[5,1],
                                    output[0,1]],
                                   [output[0,2], output[6,2], output[1,2],
                                    output[4,2], output[2,2], output[5,2],
                                    output[0,2]]])
            elif count == 13 or count == 14:
                u_, v_ = np.array([[output[0,1], output[1,1], output[2,1],
                                    output[3,1], output[4,1], output[5,1],
                                    output[6,1], output[7,1], output[8,1],
                                    output[9,1], output[10,1], output[11,1],
                                    output[0,1]],
                                   [output[0,2], output[1,2], output[2,2],
                                    output[3,2], output[4,2], output[5,2],
                                    output[6,2], output[7,2], output[8,2],
                                    output[9,2], output[10,2], output[11,2],
                                    output[0,2]]])
            elif count == 84:
                u_, v_ = np.array([[output[26,1], output[83,1], output[39,1],
                                    output[75,1], output[52,1], output[67,1],
                                    output[26,1]],
                                   [output[26,2], output[83,2], output[39,2],
                                    output[75,2], output[52,2], output[67,2],
                                    output[26,2]]])
                
        return u_, v_
    
def show(input_type = 'file', space = 'uv', count = None, output = None,
         new = True, color = 'k', label = None):
    
    x, y = Convert.Input_to_gamut(input_type = input_type, count = count, output = output)
    
    if space == 'uv':
        anal.Show.uv(x, y, gamut = True, label = label, title = None, color = color, new = new)
    else:
        anal.Show.xy(x, y, gamut = True, label = label, title = None, color = color, new = new)
    
## Compare Gamuts
class Compare():
    
    def Area(self, NewArea, OldArea):
        
        AreaDiff = NewArea / OldArea * 100
        
        return AreaDiff

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    
    return array[idx]

#print (find_nearest([sRGB_Psy, AdobeRGB_Psy, AdobeWide_Psy, DCI_P3_Psy, NTSC1953_Psy, Rec2020_Psy, Rec2100_Psy], value), '%')