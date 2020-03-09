# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:35:31 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
import sys
import os
import datetime
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import variables.dicts as dic
import technoteam.labsoft as ls
import technoteam.capture as cap
import technoteam.region as reg
import technoteam.evaluation as eva
import technoteam.table as tab

def max_luminance(save_root, file_name=None, min_time=0.0, time_ratio=3.0,
                  pic_count=1):
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
    if file_name is None:
        file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

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
    ls.save(save_root, file_name)

    return max_lum

def get_result_from_folder(load_root, save_root, target='XYZ',
                           region='Center Circle'):
    """


    Parameters
    ----------
    load_root : TYPE
        DESCRIPTION.
    save_root : TYPE
        DESCRIPTION.
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

    for measurement in os.listdir(load_root):
        if measurement.endswith('.ttcs'):
            ls.load(load_root + '/' + measurement)
            if target == 'XYZ':
                if region == 'Whole Image':
                    output = eva.get_image_mean_xyz()
                elif region == 'Center Circle':
                    output = eva.get_circle_mean_xyz()
            elif target == 'Y':
                if region == 'Whole Image':
                    output = max_luminance(save_root)
            results.append(output)

    if results != []:
        results = np.vstack((results))

    return results
