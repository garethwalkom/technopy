# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:50:00 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
CAMERA_NAMES = {'Old':'ttf8847',
                'VR': 'tts20035',
                'Hyperspectral': 'tte4202ir_52127ir'}

OLD_LENSES = {'6.5': 'o13196f6_5',
              '12': 'o95653f12',
              '25': 'oB225463f25',
              '50': 'oC216813f50'}

VR_LENSES = {'50mm': 'oM00442f50',
             'Conoscopic': 'oTTC-163_D0224',
             'NED_2mm': 'oTTNED-12_50_2mmEP',
             'NED_4mm': 'oTTNED-12_50_4mmEP'}

HYPERSPECTRAL_LENSES = {'8mm':'oDietzschf8'}

## Access Color Spaces
# Dictionary containing all available color spaces.
# WARNING: All statistics are gathered in CIE-RGB. To use another color space,
# this must be converted using GetColor()
COLOR_SPACES = {
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
IMAGE_TYPES = {
        'Camera': -3,
        'Luminance': -2,
        'Color': -1,
        'Evaluation[1]': 0,
        'Evaluation[2]': 1,
        'Evaluation[3]': 2,
        'Evaluation[4]': 3,
        'Evaluation[5]': 4,}

## Access Available File Types
# Not really needed, but nice to have them all in one dict
FILE_TYPES = {
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
REGION_TYPES = {
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

## Access Operations
# Possible operations and their parameters
OPERATION_TYPES = {
    'Addition': 'add',
    'Subtraction': 'sub',
    'Multiplication': 'mul',
    'Division': 'div',
    'Minimum': 'min',
    'Maximum': 'max',
    'Greater than': 'grt',
    'Smaller than': 'smt',
    'Binarization': 'bin',
    'Power': 'pow',
    'Mirror': 'mir',
    'Rotate': 'rot',
    'Scaling': 'sca',
    'Box filter': 'box',
    'Median filter': 'med',
    'Erosion': 'ero',
    'Dilation': 'dil',
    'Negation': 'neg',
    'Inversion': 'inv',
    'Exponent': 'exp',
    'Logarithmus': 'log'}

## Access Statistics
# Comments show which REGION_TYPES and IMAGE_TYPES the statistic types can be used with
STATISTIC_TYPES = {
        'standardGrey': 0,
        # Rectangle, Line   :: Camera, Luminance :: Standard statistic in grey images
        'standardColor': 1,
        # Rectangle, Line   :: Color             :: Standard statistic in color images
        'sectionalGrey': 2,
        # Rectangle, Line   :: Camera, Luminance :: Sectional view in grey images
        'sectionalColor': 3,
        # Rectangle, Line   :: Color             :: Sectional view in color images
        'histogramGrey': 4,
        #                   :: [ERROR]           :: Histogram in grey images
        'histogramColor': 5,
        #                   :: [ERROR]           :: Histogram in color images
        'bitHistogramGrey': 6,
        #                   :: [ERROR]           :: Bit histogram in grey images (only
        #                                           images of camera image type)
        'bitHistorgramColor': 7,
        #                   :: [ERROR]           :: Bit histogram in color images (only
        #                                           images of color camera image type)
        'projectionGrey': 8,
        #                   :: [ERROR]           :: Projection in grey images
        'projectionColor': 9,
        #                   :: [ERROR]           :: Projection in color images
        'luminanceGrey': 20,
        #                   :: [ERROR]           :: Luminance objects in grey images
        'integralGrey': 22,
        #                   :: [ERROR]           :: Integral objects in grey images
        'integralColor': 23,
        #                   :: [ERROR]           :: Integral objects in color images
        'symbolGrey': 24,
        #                   :: [ERROR]           :: Symbol objects in grey images
        'symbolColor': 25,
        #                   :: [ERROR]           :: Symbol objects in color images
        'lightArcGrey': 26,
        #                   :: [ERROR]           :: Light arc objects in grey images
        'spiralWoundGrey': 28,
        #                   :: [ERROR]           :: Spiralwoundfilaments in grey images
        'chromaticityLineColor': 31,
        #                   :: [ERROR]           :: Chromaticity line diagrams in color
        #                                           images
        'chromaticityAreaColor': 33,
        #                   :: [ERROR]           :: Chromaticity area diagrams in color
        #                                           images
        'threeDviewGrey': 34,
        #                   :: [ERROR]           :: 3D view in grey images
        'integralNegativeGrey': 36,
        #                   :: [ERROR]           :: Integral objects in grey images
        #                                           (negative contrast)
        'integralNegativeColor': 38,
        #                   :: [EEROR]           :: Symbol objects in grey images
        #                                           (negative contrast)
        'symbolNegativeColor': 39,
        #                   :: [ERROR]           :: Symbol objects in color images
        #                                           (negative contrast)
        'contrastGrey': 40}
        #                   :: [ERROR]           :: Contrasts objects in grey images
