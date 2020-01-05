# -*-coding:utf-8 -*
import math
import xyz2ScreenRgb_PCA
from luxpy.color.ctf.colortransforms import xyz_to_srgb

def xyz2RGB(xyz, RGBtype, bitratio, calibrationpars, bits):
    if RGBtype == 'device':
        if calibrationpars != []:
            raise IndexError('Empty set of calibration parameters. Run calibration!')
        RGB = [round(i) for i in xyz2ScreenRgb_PCA.xyz2ScreenRgb_PCA(xyz, calibrationpars, bits)]

    if RGBtype == 'srgb':
        RGB = xyz_to_srgb(xyz)[0]
        RGB = [round(i * bitratio) for i in RGB]


    return RGB