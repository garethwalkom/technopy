# -*- coding: utf-8 -*-
"""
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

VirtualRealityHmd():        Measure a Virtual Reality Head-Mounted-Display.
    __init__():             Initializes LMK for HMD
    warm_up():              Warm-Up VR-HMD
    measure():              Measure VR-HMD
    analyze():              Analyze Data from Measurement

"""
import os
import datetime
import time
import numpy as np
import pandas as pd

from technopy.variables import dicts as dic
from technopy.useful import bob_the_builder as bob
from technopy.technoteam import labsoft as ls
from technopy.technoteam import camera as cam
from technopy.technoteam import capture as cap
from technopy.technoteam import image as im
from technopy.technoteam import region as reg
from technopy.technoteam import evaluation as eva
from technopy.useful import fantasia as fanta


class VirtualRealityHmd:
    """
    [ADD THIS]
    """

    def __init__(self, calibration_data_root, camera_no, lens_no, mod_freq,
                 load_root, save_root, connect_camera=True):
        """
        Initializes LMK for VR-HMD.|
        ---------------------------

        Parameters
        ----------
        calibration_data_root : TYPE
            DESCRIPTION.
        camera_no : TYPE
            DESCRIPTION.
        lens_no : TYPE
            DESCRIPTION.
        mod_freq : TYPE
            DESCRIPTION.
        load_root : TYPE
            DESCRIPTION.
        save_root : TYPE
            DESCRIPTION.
        connect_camera : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """

        self.data_root = calibration_data_root
        self.save_root = save_root
        self.load_root = load_root
        self.camera_no = camera_no
        self.autoscan = False

        ## Initialize
        # Open LMK LabSoft4 Standard Color ActiveX
        ls.open_labsoft()
        if connect_camera is True:
            cam.open_camera(self.data_root, self.camera_no, lens_no)

            ## Adjust Camera
            # Set Modulation Frequency
            cam.set_modulation_frequency(mod_freq)
            # Change converting units so it doesn't multiply by two
            cam.set_converting_units()

    def warm_up(self, time_total=120):
        """
        Warm-Up VR-HMD.|
        ---------------

        Parameters
        ----------
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
                max_lum = bob.max_luminance(self.save_root)
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

    def exposure_times(self, filter_wheel_names):
        """
        [ADD THIS]

        Returns
        -------
        exposure_times : TYPE
            DESCRIPTION.

        """

        exposure_times = cam.color_autoscan_time(filter_wheel_names)

        return exposure_times


    def measure(self, color_image=True, autoscan=None, exposure_times=None,
                min_time=0.0, max_time=15, time_ratio=3.0, pic_count=1,
                start_ratio=10, time_it=False, analyze=None):
        """
        Capture VR-HMD.|
        ----------------

        Returns
        -------
        output_color : TYPE
            DESCRIPTION.

        """
        if autoscan is None:
            autoscan = self.autoscan

        if time_it is True:
            meas_start = datetime.datetime.now()

        ## Capture Image
        if color_image is True:
            cap.color_high_dyn(self.data_root, self.camera_no, autoscan,
                               exposure_times, max_time, min_time,
                               time_ratio, pic_count)
        else:
            cap.high_dyn_pic(self.data_root, self.camera_no, autoscan,
                             exposure_times, min_time, start_ratio,
                             time_ratio, pic_count)

        # Optional Analyze
        if analyze is not None:
            results = self.analyze(analyze)

        ## Save Measurement
        ls.save(self.save_root, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

        if time_it is True:
            meas_fin = datetime.datetime.now()
            print('Measured Image in: {}\n'.format(meas_fin - meas_start))

        if analyze is not None:
            return results

    def analyze(self, target, cols, lines):
        """
        [ADD THIS]

        %timeit:
            target='Y':
            36.2 s ± 1.55 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
            target='XYZ':
            36.8 s ± 2.06 s per loop (mean ± std. dev. of 7 runs, 1 loop each)

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

        for measurement in os.listdir(self.load_root):
            if measurement.endswith('.ttcs'):

                ls.load(self.load_root, measurement[:-5])

                if target == 'Y':
                    color = 0
                    image_name = 'Evaluation[1]'
                    statistic = dic.STATISTIC_TYPES['standardGrey']

                elif target != 'Y':
                    color = 1
                    image_name = 'Evaluation[2]'
                    statistic = dic.STATISTIC_TYPES['standardColor']

                region_name = '1'
                images_no = im.get_amount()
                if images_no != 0:
                    im.delete()

                if target != 'TEXT':
                    image = im.create(color, image_name)

                if target == 'Y':
                    eva.coord_trans_lum()
                elif target != 'Y':
                    eva.coord_trans_col()

                # If region already exists, delete it
                err_code, index_out = \
                    reg.get_id(dic.IMAGE_TYPES[image_name],
                               region_name)
                if err_code == 0:
                    reg.delete(dic.IMAGE_TYPES[image_name],
                               index_out)

                # If statistic already exists, delete it
                exists, _, _ = eva.statistic_exists(dic.IMAGE_TYPES[image_name],
                                                    index_out)
                if exists == 1:
                    eva.delete_statistic()

                if target != 'TEXT':
                    reg.create_rect(image, cols[0], cols[1],
                                    lines[0], lines[1])

                    # Get ID of region
                    _, index_out = reg.get_id(image,
                                              region_name)
                    # Select region from index of region
                    reg.select(image, index_out)

                    # Evaluate Region
                    eva.create_statistic(statistic,
                                         image,
                                         index_out)

                if target == 'Y':
                    output = eva.get_max_lum()

                elif target == 'XYZ':
                    output = eva.get_xyz(index_out)

                elif target == 'TEXT':
                    im.save(self.save_root, measurement[:-5],
                            dic.FILE_TYPES['txt'], dic.IMAGE_TYPES['Color'])

                if target != 'TEXT':
                    results.append(output)

        if results != []:
            results = np.vstack((results))

        return results

if __name__ == '__main__':

    SETUP = True
    MEASURE = False
    ANALYZE = False
    ANALYZE_MAX_YS = False
    ANALYZE_XYZS = False
    SHOW_YUVS = False

    # Define Calibration Data Root
    DATA_ROOT = 'F:/LMK/Calibration Data'

    # Define Save/Load Roots
    SAVE_ROOT = 'E:/Measurements/' + str(datetime.date.today()) + '/'
    LOAD_ROOT = 'E:/Measurements/2020-03-12/'

    if SETUP is True:
        VR = VirtualRealityHmd(DATA_ROOT, camera_no='tts20035',
                               lens_no='oTTC-163_D0224',
                               mod_freq=90, save_root=SAVE_ROOT,
                               load_root=LOAD_ROOT, connect_camera=True)

    if MEASURE is True:

        FILTER_WHEEL = []
        _, FILTER_WHEEL_NAMES = cam.get_filter_wheels(DATA_ROOT,
                                                      camera_no='tts20035')
        for FILTER_WHEEL_NAME in FILTER_WHEEL_NAMES:
            FILTER_WHEEL.append(str(FILTER_WHEEL_NAME)[2:-2])
        ALL_EXPOSURE_TIMES = pd.DataFrame(columns=FILTER_WHEEL)

        EXPOSURE_TIMES = VR.exposure_times(FILTER_WHEEL_NAMES)
        ALL_EXPOSURE_TIMES = ALL_EXPOSURE_TIMES.append(EXPOSURE_TIMES,
                                                       ignore_index=True)
        VR.measure(exposure_times=ALL_EXPOSURE_TIMES.iloc[-1])

    if ANALYZE is True:

        FIRST_COL = 567
        LAST_COL = 1969
        FIRST_LINE = 391
        LAST_LINE = 2045

        if ANALYZE_MAX_YS is True:
            MAX_YS = VR.analyze('Y', cols=[FIRST_COL, LAST_COL],
                                lines=[FIRST_LINE, LAST_LINE])
        if ANALYZE_XYZS is True:
            XYZS = VR.analyze('TEXT', cols=[FIRST_COL, LAST_COL],
                              lines=[FIRST_LINE, LAST_LINE])

    if SHOW_YUVS is True:
        LABEL = 'Oculus Rift CV1'

        DIFF, MEAN = fanta.y_diff(MAX_YS, XYZS)
        YUVS = fanta.xyz_to_yuv(XYZS)
        fanta.show(space='uv', new=False, color='r', input_type='file',
                   count=len(YUVS), output=YUVS, label=LABEL)
        fanta.uv(YUVS[3, 0], YUVS[3, 1], label=LABEL, color='r', new=False)
