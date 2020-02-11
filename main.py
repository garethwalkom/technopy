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
# created for use in Python by Gareth V. Walkom. Once connected to the ax
# server, you can then open the LMK LabSoft4 Standard Color ax (ax
# version of the software is needed to run this script), access the Calibration
# data, and control the camera to make measurements.
#
# Please listen to the TechnoPy playlist while making measurements for inspo:
# https://www.youtube.com/playlist?list=PLu3mtT1o6gSieYEqJEBHm5NX9lWljoED
# =============================================================================
"""

Structure:|
----------

max_luminance():
characterize():
measure_warm_up():
get_result_from_folder():
vr_hmd():                   Characterize a Virtual Reality Head-Mounted-Display.
    characterize():
    __init__():             Initializes LMK for HMD
    analyze():

"""
import os
import datetime
import time
import numpy as np

import activex as ax
import labsoft as ls
import camera as cam
import capture as cap
import image as im
import region as reg
import evaluation as eva
import dicts as dic
import table as tab

# Define the root to the calibration data
CALIB_DATA_ROOT = 'F:/LMK/Calibration Data'

# Define Save Parameters
MEAS_ROOT = 'E:/Measurements/' + str(datetime.date.today()) + '/'

def max_luminance(min_time=0.0, time_ratio=3.0, pic_count=1):
    """
    [ADD THIS]

    Parameters
    ----------
    min_time : TYPE, optional
        DESCRIPTION. The default is 0.0.
    time_ratio : TYPE, optional
        DESCRIPTION. The default is 3.0.
    pic_count : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    max_lum : TYPE
        DESCRIPTION.

    """

    ### Capture Image
    # Capture a ColorHighDyn Image with Max Exposure Time of all Filters
    cap.color_high_dyn(autoscan=False, max_time=0.33,
                       min_time=min_time,
                       time_ratio=time_ratio, pic_count=pic_count)

    ### Evaluate
    # Create a region the size of the whole image
    region_x_points, region_y_points = reg.create_rect_image_size()
    # Get ID of region
    _, index_out = reg.get_id(dic.IMAGE_TYPES['Luminance'], name='1')
    # Select region from index of region
    reg.select(index=index_out)

    # Create statistic
    eva.create_statistic(dic.STATISTIC_TYPES['standardGrey'],
                         dic.IMAGE_TYPES['Luminance'], index_out,
                         param_list=[1])
    # Get max luminance of region
    max_lum = tab.get_cell(table_id=2, table_line_id=0, table_column_id=6)

    max_lum = np.float64(max_lum)

    ### Save Measurement
    ls.save(file_name=MEAS_ROOT + \
            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                dic.FILE_TYPES['ttcs'])

    return max_lum

def characterize(min_time=0.0, time_ratio=3.0, pic_count=1):
    """
    [ADD THIS]

    Parameters
    ----------
    min_time : TYPE, optional
        DESCRIPTION. The default is 0.0.
    time_ratio : TYPE, optional
        DESCRIPTION. The default is 3.0.
    pic_count : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    None.

    """

    car_start = datetime.datetime.now()

    ### Capture Image
    # Capture a ColorHighDyn Image with Max Exposure Time of all Filters
    cap.color_high_dyn(autoscan=False, min_time=min_time,
                       time_ratio=time_ratio, pic_count=pic_count)

    ### Save Measurement
    ls.save(file_name=MEAS_ROOT + \
            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                dic.FILE_TYPES['ttcs'])

    char_fin = datetime.datetime.now()
    print('Measured Image in: {}\n'.format(char_fin - car_start))

def measure_warm_up(time_total=120):
    """
    [ADD THIS]

    Parameters
    ----------
    warm_up : TYPE, optional
        DESCRIPTION. The default is True.
    time_total : TYPE, optional
        DESCRIPTION. The default is 120.

    Returns
    -------
    output : TYPE
        DESCRIPTION.

    """

    time_warm = 0
    output = []

    while time_warm < time_total:
        start = time.time()
        if datetime.datetime.now().minute % 1 == 0:
            max_lum = max_luminance()
            ls.close_labsoft()
            print(time_warm + 1, '(of', time_total, 'minutes)', '|',
                  datetime.datetime.now().time(),
                  '|', max_lum, 'cd/m^2 (max)')
        time_warm = time_warm + 1
        output.append([time_warm, max_lum])
        overlay = time.time() - start
        time.sleep(60 - overlay)

    if output != []:
        output = np.vstack((output))

    return output

def get_result_from_folder(MEAS_ROOT='E:/Measurements/2019-09-13-Char/',
                           target='XYZ', region='Center Circle'):
    """
    [AdD THIS]

    Parameters
    ----------
    MEAS_ROOT : TYPE, optional
        DESCRIPTION. The default is 'E:/Measurements/2019-09-13-Char/'.
    target : TYPE, optional
        DESCRIPTION. The default is 'XYZ'.
    region : TYPE, optional
        DESCRIPTION. The default is 'Center Circle'.

    Returns
    -------
    results : TYPE
        DESCRIPTION.

    """

    ls.open_labsoft()

    results = []

    for measurement in os.listdir(MEAS_ROOT):
        if measurement.endswith('.ttcs'):
            ls.load(MEAS_ROOT + '/' + measurement)
            if target == 'XYZ':
                if region == 'Whole Image':
                    output = eva.get_image_mean_xyz()
                elif region == 'Center Circle':
                    output = eva.get_circle_mean_xyz()
            elif target == 'Y':
                if region == 'Whole Image':
                    output = max_luminance()
            results.append(output)

    if results != []:
        results = np.vstack((results))

    return results

class vr_hmd():

    def __init__(self, modulation_frequency=90.0,
                 MEAS_ROOT='E:/Measurements/2020-02-08/OpenVR/',
                 connect_camera=True):
        """
        Initializes LMK for HMD.|
        ------------------------

        Parameters
        ----------
        ModulationFrequency : int, optional
            Modulation frequency of HMD. The default is 90.0.

        Returns
        -------
        None.

        """

        self.MEAS_ROOT = MEAS_ROOT

        ### Initialize
        # Open LMK LabSoft4 Standard Color ax
        ls.open_labsoft()
        if connect_camera is True:
            self.camera, self.camera_no = cam.set_camera(camera='VR')
            self.lens, self.lens_no = cam.set_lens(self.camera,
                                                   lens='Conoscopic')
            cam.open_camera(self.camera_no, self.lens_no)

            ### Adjust Camera
            # Set Modulation Frequency
            cam.set_modulation_frequency(modulation_frequency)
            # Change converting units so it doesn't multiply by two
            cam.set_converting_units()


    def characterize(self, min_time=0.0, time_ratio=3.0, pic_count=1):
        """
        Characterize a Virtual Reality Head-Mounted-Display.|
        ----------------------------------------------------

        Parameters
        ----------
        MinTime : int, optional
            Minimum time for capture. The default is 0.0.
        TimeRatio : int, optional
            Time ratio of capture. The default is 3.0.
        PicCount : int, optional
            Amount of pictures per capture. The default is 1.

        Returns
        -------
        None.

        """
        char_start = datetime.datetime.now()

        ### Capture Image
        cap.color_high_dyn(autoscan=False, min_time=min_time,
                           time_ratio=time_ratio, pic_count=pic_count)

        ### Get Image Mean XYZ
        output_color = eva.get_image_mean_xyz()

        ### Save Measurement
        ls.save(file_name=MEAS_ROOT + \
                datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                    dic.FILE_TYPES['ttcs'])

        char_fin = datetime.datetime.now()
        print('Measured Image in: {}\n'.format(char_fin - char_start))

        return output_color

    def analyze(self, target='XYZ'):
        """
        [ADD THIS]

        Parameters
        ----------
        target : TYPE, optional
            DESCRIPTION. The default is 'XYZ'.

        Returns
        -------
        results : TYPE
            DESCRIPTION.

        """

        results = []

        for measurement in os.listdir(self.MEAS_ROOT):
            if measurement.endswith('.ttcs'):

                ls.load(self.MEAS_ROOT + measurement)

                if target == 'Y':
                    self.IMAGE = dic.IMAGE_TYPES['Luminance']
                    self.COLOR = 0
                    self.IMAGE_NAME = 'Evaluation[1]'
                    self.STATISTIC = dic.STATISTIC_TYPES['standardGrey']

                elif target == 'XYZ':
                    # self.IMAGE = dic.IMAGE_TYPES['Color']
                    self.COLOR = 1
                    self.IMAGE_NAME = 'Evaluation[2]'
                    self.STATISTIC = dic.STATISTIC_TYPES['standardColor']

                self.REGION_NAME = '1'
                images_no = im.get_amount()
                if images_no != 0:
                    im.delete()

                self.IMAGE = im.create(self.COLOR, self.IMAGE_NAME)

                if target == 'Y':
                    eva.coord_trans_lum()
                elif target == 'XYZ':
                    eva.coord_trans_col()

                # Get size of image
                self.image_first_line, self.image_last_line, \
                self.image_first_col, self.image_last_col, \
                self.image_dimensions = im.get_size()

                # If region already exists, delete it
                err_code, self.index_out = \
                    reg.get_id(dic.IMAGE_TYPES[self.IMAGE_NAME],
                               self.REGION_NAME)
                if err_code == 0:
                    reg.delete(dic.IMAGE_TYPES[self.IMAGE_NAME],
                               self.index_out)

                # If statistic already exists, delete it
                exists, self.statistic_type, self.statistic_index  \
                    = eva.statistic_exists(dic.IMAGE_TYPES[self.IMAGE_NAME],
                                           self.index_out)
                if exists == 1:
                    eva.delete_statistic()

                reg.create(self.IMAGE,
                           dic.REGION_TYPES['Rectangle']['identifier'],
                           dic.REGION_TYPES['Rectangle']['points'],
                           x_coords=[567, 1969], y_coords=[391, 2045])

                # Get ID of region
                _, self.index_out = reg.get_id(self.IMAGE,
                                               self.REGION_NAME)
                # Select region from index of region
                reg.select(self.IMAGE, self.index_out)

                ### Evaluate Region
                eva.create_statistic(self.STATISTIC,
                                     self.IMAGE,
                                     self.index_out)

                if target == 'Y':
                    max_lum = tab.get_cell(table_id=2, table_line_id=0,
                                           table_column_id=6)
                    output = np.float64(max_lum)

                elif target == 'XYZ':
                    blue_stats = eva.get_standard_statistic(self.STATISTIC,
                                                            self.index_out,
                                                            color_class=0)
                    b_mean = str(blue_stats['Mean'])[1:-1]
                    b_mean = float(b_mean)
                    green_stats = eva.get_standard_statistic(self.STATISTIC,
                                                             self.index_out,
                                                             color_class=1)
                    g_mean = str(green_stats['Mean'])[1:-1]
                    g_mean = float(g_mean)
                    red_stats = eva.get_standard_statistic(self.STATISTIC,
                                                           self.index_out,
                                                           color_class=2)
                    r_mean = str(red_stats['Mean'])[1:-1]
                    r_mean = float(r_mean)

                    output = eva.convert_cie_rgb(cie_r=r_mean, cie_g=g_mean,
                                                 cie_b=b_mean)

                results.append(output)

        if results != []:
            results = np.vstack((results))

        ls.close_labsoft()
        del ax.LMK

        return results


#if __name__ == '__main__':
#    # Define Camera Parameters
#    ModulationFrequency = 90.0   # Modulation Frequency
#    MinTime = 0.0                # Smallest Exposure Time (proposal: 0.0)
#    TimeRatio = 3.0              # TimeRatio between two times (proposal: 3.0)
#    PicCount = 1                 # Number of shots per integration time
#
#    ### Initialize [REQUIRED]
#    # Open LMK LabSoft4 Standard Color ax [REQUIRED]
#    LabSoft.Open()
#    # Connect to Camera [REQUIRED]
#    Camera.Open(CALIB_DATA_ROOT)
#
#    ### Adjust Camera
#    # Set Modulation Frequency
#    Camera.SetModulationFrequency(ModulationFrequency)
#    # Calculate Max Exposure Times for all filters
#    ExposureTimes = Camera.ColorAutoScanTime()
#
#    ### Capture Image
#    # Capture a ColorHighDyn Image with Max Exposure Time of all Filters
#    Capture.ColorHighDyn(MaxTime = max(ExposureTimes.items(),
#                                            key=operator.itemgetter(1))[1],
#        MinTime = MinTime, TimeRatio = TimeRatio, PicCount = PicCount)
#
#    ### Create Region on Image
#    # Create an ellipse region on image
#    Region.Create(IMAGE_TYPES['Color'],
#                          REGION_TYPES['Ellipse']['identifier'],
#                          REGION_TYPES['Ellipse']['points'],
#                          X = [1226, 500, 500], Y = [1026, 500, 500])
#    # Create a region the size of the whole image
#    Region_X_Points, Region_Y_Points = Region.CreateRectImageSize()
#    # Get ID of region
#    err_code, Index_Out = Region.GetID(IMAGE_TYPES['Color'], Name = '1')
#    # Select region from index of region
#    Region.Select(Index = Index_Out)
#
#    ### Evaluate Image
#    # Create a standard color statistic
#    Evaluation.CreateStatistic(STATISTIC_TYPES['standardColor'],
#                               IMAGE_TYPES['Color'], Index_Out, ParamList = [1])

#    Blue_Stats = Evaluation.GetStandardStatistic(Class = 0)
#    Green_Stats = Evaluation.GetStandardStatistic(Class = 1)
#    Red_Stats = Evaluation.GetStandardStatistic(Class = 2)

    # Get Pixel Color
#    R, G, B = Evaluation.GetPixelColor(Line = 800, Column = 1300)
##    Convert CIE-RGB to XYZ
#    Output_Color = Evaluation.Convert_CIE_RGB(CIE_R = R, CIE_G = G, CIE_B = B)
#    # Convert XYZ into Yuv
#    u_v_ = Evaluation.XYZ_To_u_v_(Output_Color)
#    # Show u'v' in diagram
#    Evaluation.Show_u_v_(u_ = u_v_[:,0], v_ = u_v_[:,1])

#    ### Save
#    # Save measurement as an image
#    Image.Save(IMAGE_TYPES['Color'], MEAS_ROOT + MEAS_NAME + EXTENSION)
#    # Save measurement as .ttcs file. Can be reopened again.
#    LabSoft.Save(PathName = MEAS_ROOT + 'Meas' + FILE_TYPES['ttcs'])
