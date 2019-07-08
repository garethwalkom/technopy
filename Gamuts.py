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
import pandas as pd

import Analyze as anal

## Define Gamuts
# Each array should be ordered depending on what data you want to use (e.g.: x, y, u_ (u'), v_, (v'))
# Then, to draw array as a gamut, the rows must be ordered correctly to follow
# the line of the gamut and then closed back to the starting point
# (e.g.: R, G, B, R or R, Y, G, C, B, M, R)
# Split each column into seperate variables, so they can be called individually later

Psych_RGB = np.array([0, 15, 25, 50, 100, 150, 200, 245, 250, 255])

Psych_XYZ = np.array([[0.00708, 0.00328, 0.00788], # 0, 0, 0
                      [4.414, 4.531, 5.462], # 15, 15, 15
                      [7.424, 7.639, 9.196], # 25, 25, 25
                      [14.55, 14.93, 17.97], # 50, 50, 50
                      [30.47, 31.13, 37.66], # 100, 100, 100
                      [46.7, 47.75, 57.98], # 150, 150, 150
                      [62.09, 62.56, 76.16], # 200, 200, 200
                      [76.06, 76.38, 92.45], # 245, 245, 245
                      [78.12, 78.36, 94.76], # 250, 250, 250
                      [78.95, 79.15, 95.74] # 255, 255, 255
                      ])

Psych_df = pd.DataFrame(Psych_XYZ, index = Psych_RGB, columns = ['X', 'Y', 'Z'])

OpenVR_RGB = np.array([0, 15, 30, 45, 51, 60, 102, 128, 153, 178, 204, 245, 255])

## Outputs from Measurements
class Output():
    # Oculus Rift HMD Measurements with PsychToolbox
    def Psych(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.67550, 0.24660, 0.14570, 0.67550],
                                 [0.32240, 0.71020, 0.04767, 0.32240],
                                 [0.48970, 0.08944, 0.17760, 0.48970],
                                 [0.52590, 0.57950, 0.13080, 0.52590]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
        
        return Area
    
    def OpenVR():
        u_, v_ = np.array([[0.48957, 0.20859, 0.09020, 0.11675, 0.17706, 0.32982, 0.48957],
                           [0.52589, 0.56361, 0.57946, 0.44267, 0.13181, 0.32601, 0.52589]])
    
        anal.Analyze.uv(u_, v_, gamut = True)
        Area = Analyze.Area(u_, v_)
        
        return Area
    
## Color Spaces
class ColorSpace():
    # sRGB Gamut (Rec.709 is the same)
    def sRGB(Diagram = 'u_v_'):      
        x, y, u_, v_ = np.array([[0.64000, 0.30000, 0.15000, 0.64000],
                                 [0.33000, 0.60000, 0.06000, 0.33000],
                                 [0.45070, 0.12500, 0.17544, 0.45070],
                                 [0.52289, 0.56250, 0.15789, 0.52289]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
        
        return Area
    
    # Adobe sRGB Gamut
    def AdobeRGB(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.64000, 0.21000, 0.15000, 0.64000],
                                 [0.33000, 0.71000, 0.06000, 0.33000],
                                 [0.45070, 0.07568, 0.17544, 0.45070],
                                 [0.52289, 0.57568, 0.15789, 0.52289]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # Adobe Wide Gamut RGB
    def AdobeWide(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.73469, 0.11416, 0.15664, 0.73469],
                                 [0.26531, 0.82621, 0.01770, 0.26531],
                                 [0.62337, 0.03600, 0.21612, 0.62337],
                                 [0.50650, 0.58614, 0.05495, 0.50650]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # DCI P3 Gamut
    def DCI_P3(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.68000, 0.26500, 0.15000, 0.68000],
                                 [0.32000, 0.69000, 0.06000, 0.32000],
                                 [0.49635, 0.09860, 0.17544, 0.49635],
                                 [0.52555, 0.57767, 0.15789, 0.52555]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # NTSC 1953 Gamut
    def NTSC1953(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.67000, 0.21000, 0.14000, 0.67000],
                                 [0.33000, 0.71000, 0.08000, 0.33000],
                                 [0.47687, 0.07568, 0.15217, 0.47687],
                                 [0.52847, 0.57568, 0.19565, 0.52847]])

        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # Rec. 2020 Gamut
    def Rec2020(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.70792, 0.17024, 0.13137, 0.70792],
                                 [0.29203, 0.79652, 0.04588, 0.29203],
                                 [0.55648, 0.05574, 0.15983, 0.55648],
                                 [0.51651, 0.58674, 0.12558, 0.51651]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # Rec. 2100 Gamut
    def Rec2100(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.70800, 0.17000, 0.13100, 0.70800],
                                 [0.29220, 0.79700, 0.04600, 0.29220],
                                 [0.55634, 0.05563, 0.15927, 0.55634],
                                 [0.51662, 0.58680, 0.12584, 0.51662]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    ## ACES Gamut
    def ACES(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.73470, 0.00000, 0.00010, 0.73470],
                                 [0.26530, 1.00000, -0.07700, 0.26530],
                                 [0.62339, 0.00000, 0.00019, 0.62339],
                                 [0.50649, 0.60000, -0.33385, 0.50649]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # ProPhoto RGB Gamut
    def ProPhotoRGB(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.73470, 0.15960, 0.03660, 0.73470],
                                 [0.00010, 0.84040, 0.26530, 0.00010],
                                 [0.62340, 0.05000, 0.05000, 0.62340],
                                 [0.50650, 0.59250, 0.00030, 0.50650]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area

## Define White Points
# This needs to be seperate from the previous imported data, as we don't want
# the gamut line being drawn to the white point
# Same structure as columns from data [x, y, u_ (u'), v_ (v')] 
class WhitePoint():
    
    def A(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.44758], [0.40745], [0.25597], [0.52430]])
        
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_)
        else:
            anal.Analyze.xy(x, y)
            
    def B(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.34842], [0.35161], [0.21367], [0.48517]])
        
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_)
        else:
            anal.Analyze.xy(x, y)
            
    def C(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.31006], [0.31616], [0.20089], [0.46089]])
        
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_)
        else:
            anal.Analyze.xy(x, y)
            
    def D50(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.34567], [0.35850], [0.20916], [0.48808]])
        
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_)
        else:
            anal.Analyze.xy(x, y)

    def D65(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.31270], [0.32900], [0.19783], [0.46832]])
        
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_)
        else:
            anal.Analyze.xy(x, y)

## Monitors       
class Monitor():
    
    # AU Optronics M270DAN01.1 Gamut
    def AUM270(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.68900, 0.20800, 0.14900, 0.68900],
                                 [0.29900, 0.71400, 0.05000, 0.29900],
                                 [0.528983, 0.074605, 0.180497, 0.528983],
                                 [0.51651, 0.57622, 0.13628, 0.51651]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Display LM240WU4 Gamut
    def LGLMWU4(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.68000, 0.20600, 0.15100, 0.68000],
                                 [0.31000, 0.69300, 0.05500, 0.31000],
                                 [0.507463, 0.075569, 0.179869, 0.507463],
                                 [0.52052, 0.57199, 0.14741, 0.52052]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Display LM240WU5-SLA1 Gamut
    def LGLMWU5(Diagram = 'u_v_'):    
        x, y, u_, v_ = np.array([[0.69000, 0.20500, 0.15000, 0.69000],
                                 [0.30000, 0.71500, 0.04500, 0.30000],
                                 [0.528736, 0.073411, 0.185185, 0.528736],
                                 [0.51724, 0.57610, 0.12500, 0.51724]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Displays: LM240WU9-SLA1 / LM270WQ3-SLA1 / LM300WQ6-SLA1 Gamut
    def LGLMWU9(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.68000, 0.21000, 0.14700, 0.68000],
                                 [0.31000, 0.70000, 0.05400, 0.31000],
                                 [0.507463, 0.076503, 0.175313, 0.507463],
                                 [0.52052, 0.57377, 0.14490, 0.52052]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Display LM270WQ2-SLA1 Gamut
    def LGLMWQ2(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.67800, 0.20200, 0.14800, 0.67800],
                                 [0.30900, 0.68900, 0.05100, 0.30900],
                                 [0.506726, 0.074374, 0.178528, 0.506726],
                                 [0.51962, 0.57078, 0.13842, 0.51962]])

        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Display LM300WQ5 Gamut
    def LGLMWQ5(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.67800, 0.21000, 0.14600, 0.67800],
                                 [0.30900, 0.69200, 0.05500, 0.30900],
                                 [0.506726, 0.077178, 0.173397, 0.506726],
                                 [0.51962, 0.57222, 0.14697, 0.51962]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # Samsung LTM240CS02
    def SAMLTM(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.69200, 0.20500, 0.14800, 0.69200],
                                 [0.29500, 0.71700, 0.06500, 0.29500],
                                 [0.53685, 0.073254, 0.16992, 0.53685],
                                 [0.51493, 0.57647, 0.16791, 0.51493]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # Mitsubishi LaserVue
    def MITSLV(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.71903, 0.17024, 0.15947, 0.71903],
                                 [0.28093, 0.79652, 0.01523, 0.28093],
                                 [0.583025, 0.055735, 0.222737, 0.583025],
                                 [0.51253, 0.58674, 0.04786, 0.51253]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area

## Laptops
class Laptop():
    
    # AU Optronics B156HW01: V0 / V1 / V2 / V3 / V5 / V6
    def AUOW01(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.62300, 0.33600, 0.14800, 0.62300],
                                 [0.35100, 0.57400, 0.05300, 0.35100],
                                 [0.41770, 0.14583, 0.17725, 0.41770],
                                 [0.52950, 0.56055, 0.14281, 0.52950]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # AU Optronics B156XW04 V5
    def AUOW04(Diagram = 'u_v_'):    
        x, y, u_, v_ = np.array([[0.59000, 0.33000, 0.15000, 0.59000],
                                 [0.34000, 0.55000, 0.14000, 0.34000],
                                 [0.40000, 0.14765, 0.13699, 0.40000],
                                 [0.51864, 0.55369, 0.28767, 0.51864]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Displays: LP156WF3 / LP171WU8-SLB1
    def LGLP15(Diagram = 'u_v_'):    
        x, y, u_, v_ = np.array([[0.68600, 0.20600, 0.14500, 0.68600],
                                 [0.30800, 0.71500, 0.04500, 0.30800],
                                 [0.51540, 0.07378, 0.17846, 0.51540],
                                 [0.52066, 0.57620, 0.12462, 0.52066]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Display LP171WU5-TLB1
    def LGLP171(Diagram = 'u_v_'):
        x, y, u_, v_ = np.array([[0.68820, 0.20190, 0.14400, 0.68820],
                                 [0.30590, 0.71720, 0.05100, 0.30590],
                                 [0.51995, 0.07209, 0.17329, 0.51995],
                                 [0.52000, 0.57619, 0.13809, 0.52000]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
    # LG Display LP173WF3
    def LGLP173(Diagram = 'u_v_'):    
        x, y, u_, v_ = np.array([[0.68200, 0.19900, 0.15100, 0.68200],
                                 [0.30500, 0.72100, 0.04500, 0.30500],
                                 [0.51511, 0.07073, 0.18653, 0.51511],
                                 [0.51832, 0.57659, 0.12508, 0.51832]])
        if Diagram == 'u_v_':
            anal.Analyze.uv(u_, v_, gamut = True)
            Area = Analyze.Area(u_, v_)
        else:
            anal.Analyze.xy(x, y, gamut=True)
            Area = Analyze.Area(x, y)
            
        return Area
    
## Analyze Gamut
class Analyze():
    
    # If xy: u_ = x, v_ = y
    def Area(u_, v_):
        
        Area = ((u_[1] - u_[2]) * (v_[1] + v_[2]) + (u_[0] - u_[1]) * (v_[0] + v_[1]) - (u_[0] - u_[2]) * (v_[0] + v_[2]))/2 * 100
        
        return Area

## Compare Gamuts
class Compare():
    
    def Area(NewArea, OldArea):
        
        AreaDiff = NewArea / OldArea * 100
        
        return AreaDiff

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

value = 100

#print (find_nearest([sRGB_Psy, AdobeRGB_Psy, AdobeWide_Psy, DCI_P3_Psy, NTSC1953_Psy, Rec2020_Psy, Rec2100_Psy], value), '%')