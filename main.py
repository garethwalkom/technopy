# -*- coding: utf-8 -*-
"""

Structure:|
----------

max_luminance():
measure_warm_up():
get_result_from_folder():
VirtualRealityHmd():        Characterize a Virtual Reality Head-Mounted-Display.
    __init__():             Initializes LMK for HMD
    characterize():
    analyze():
        create_region():

"""
import os
import datetime
import time
import numpy as np

import roots as root
import dicts as dic
import activex as ax
import labsoft as ls
import camera as cam
import capture as cap
import image as im
import region as reg
import evaluation as eva
import table as tab

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
    _, _ = reg.create_rect_image_size()
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
    ls.save(file_name=root.SAVE + \
            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                dic.FILE_TYPES['ttcs'])

    return max_lum

def measure_warm_up(time_total=120):
    """
    [ADD THIS]

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

def get_result_from_folder(target='XYZ', region='Center Circle'):
    """
    [ADD THIS]

    Parameters
    ----------
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

    for measurement in os.listdir(root.LOAD):
        if measurement.endswith('.ttcs'):
            ls.load(root.LOAD + '/' + measurement)
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

class VirtualRealityHmd():
    """
    [ADD THIS]
    """

    def __init__(self, camera='VR', lens='Conoscopic', mod_freq=90.0,
                 connect_camera=True):
        """
        Initializes LMK for VR-HMD.|
        ---------------------------

        Parameters
        ----------
        camera : TYPE, optional
            DESCRIPTION. The default is 'VR'.
        lens : TYPE, optional
            DESCRIPTION. The default is 'Conoscopic'.
        mod_freq : TYPE, optional
            DESCRIPTION. The default is 90.0.
        autoscan : TYPE, optional
            DESCRIPTION. The default is False.
        min_time : TYPE, optional
            DESCRIPTION. The default is 0.0.
        time_ratio : TYPE, optional
            DESCRIPTION. The default is 3.0.
        pic_count : TYPE, optional
            DESCRIPTION. The default is 1.
        connect_camera : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """

        self.save_root = root.SAVE
        self.load_root = root.LOAD
        self.camera = camera
        self.lens = lens
        self.mod_freq = mod_freq

        ## Initialize
        # Open LMK LabSoft4 Standard Color ax
        ls.open_labsoft()
        if connect_camera is True:
            _, self.camera_no = cam.set_camera(self.camera)
            _, self.lens_no = cam.set_lens(self.camera, self.lens)
            cam.open_camera(self.camera_no, self.lens_no)

            ## Adjust Camera
            # Set Modulation Frequency
            cam.set_modulation_frequency(self.mod_freq)
            # Change converting units so it doesn't multiply by two
            cam.set_converting_units()


    def characterize(self, autoscan=False, min_time=0.0, time_ratio=3.0,
                     pic_count=1):
        """
        Characterize a Virtual Reality Head-Mounted-Display.|
        ----------------------------------------------------

        Returns
        -------
        output_color : TYPE
            DESCRIPTION.

        """
        char_start = datetime.datetime.now()

        ## Capture Image
        cap.color_high_dyn(autoscan, min_time, time_ratio, pic_count)

        ## Save Measurement
        ls.save(file_name=self.save_root + \
                datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                    dic.FILE_TYPES['ttcs'])

        char_fin = datetime.datetime.now()
        print('Measured Image in: {}\n'.format(char_fin - char_start))

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

        for measurement in os.listdir(self.load_root):
            if measurement.endswith('.ttcs'):

                ls.load(self.load_root + measurement)

                if target == 'Y':
                    color = 0
                    image_name = 'Evaluation[1]'
                    statistic = dic.STATISTIC_TYPES['standardGrey']

                elif target == 'XYZ':
                    color = 1
                    image_name = 'Evaluation[2]'
                    statistic = dic.STATISTIC_TYPES['standardColor']

                region_name = '1'
                images_no = im.get_amount()
                if images_no != 0:
                    im.delete()

                image = im.create(color, image_name)

                if target == 'Y':
                    eva.coord_trans_lum()
                elif target == 'XYZ':
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

                reg.create_rect(image)

                # Get ID of region
                _, index_out = reg.get_id(image,
                                          region_name)
                # Select region from index of region
                reg.select(image, index_out)

                ## Evaluate Region
                eva.create_statistic(statistic,
                                     image,
                                     index_out)

                if target == 'Y':
                    output = eva.get_max_lum()

                elif target == 'XYZ':
                    output = eva.get_xyz(index_out)

                results.append(output)

        if results != []:
            results = np.vstack((results))

        ls.close_labsoft()
        del ax.LMK

        return results
