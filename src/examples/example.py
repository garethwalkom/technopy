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
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import datetime
import time
import numpy as np
import luxpy as lx
from matplotlib import pyplot as plt

from change_this import roots as root
from variables import dicts as dic
from technoteam import labsoft as ls
from technoteam import camera as cam
from technoteam import capture as cap
from technoteam import image as im
from technoteam import region as reg
from technoteam import evaluation as eva
from technoteam import table as tab

from luxpy.toolboxes import spectro as sp

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

def y_diff(max_ys, xyzs):

    diff = []

    for index, _ in enumerate(xyzs):
        diff.append(100 - (100 * float(xyzs[index, 1]) / float(max_ys[index
                                                                      , 0])))
    diff = np.vstack(diff)
    mean = diff.mean()

    return diff, mean

def xyz_to_u_v_(xyzs):

    u_v_ = []
    for xyz in xyzs:
        u_v_.append(eva.xyz_to_u_v_(xyz))
    u_v_ = np.vstack(u_v_)

    return u_v_

def xyz_to_space(input_type='RGB', R=None, G=None, B=None, W=None,
                 file='GW_2019-09-13.txt', space='uv'):

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
        XYZs = np.loadtxt(file, delimiter='\t')
        if space == 'uv':
            output = lx.xyz_to_Yuv(XYZs)
        else:
            output = lx.xyz_to_Yxy(XYZs)
        for count, _ in enumerate(output):
            count = count + 1
        return XYZs, output, count

def input_to_gamut(input_type='RGB', count=None, output=None, R=None,
                   G=None, B=None, C=None, M=None, Y=None):

    if input_type == 'RGB':
        u_out, v_out = np.array([[R[:, 1], G[:, 1],
                                  B[:, 1], R[:, 1]],
                                 [R[:, 2], G[:, 2],
                                  B[:, 2], R[:, 2]]])
        return u_out, v_out

    elif input_type == 'RGBCMY':
        u_out, v_out = np.array([[R[:, 1], Y[:, 1],
                                  G[:, 1], C[:, 1],
                                  B[:, 1], M[:, 1],
                                  R[:, 1]],
                                 [R[:, 2], Y[:, 2],
                                  G[:, 2], C[:, 2],
                                  B[:, 2], M[:, 2],
                                  R[:, 2]]])
        return u_out, v_out

    elif input_type == 'file':
        if count == 4:
            u_out, v_out = np.array([[output[0, 1], output[1, 1],
                                      output[2, 1], output[0, 1]],
                                     [output[0, 2], output[1, 2],
                                      output[2, 2], output[0, 2]]])
            return u_out, v_out

        elif count == 7 or count == 8:
            u_out, v_out = np.array([[output[0, 0], output[6, 0], output[1, 0],
                                      output[4, 0], output[2, 0], output[5, 0],
                                      output[0, 0]],
                                     [output[0, 1], output[6, 1], output[1, 1],
                                      output[4, 1], output[2, 1], output[5, 1],
                                      output[0, 1]]])
            return u_out, v_out

        elif count == 13 or count == 14:
            u_out, v_out = np.array([[output[0, 1], output[1, 1], output[2, 1],
                                      output[3, 1], output[4, 1], output[5, 1],
                                      output[6, 1], output[7, 1], output[8, 1],
                                      output[9, 1], output[10, 1], output[11, 1],
                                      output[0, 1]],
                                     [output[0, 2], output[1, 2], output[2, 2],
                                      output[3, 2], output[4, 2], output[5, 2],
                                      output[6, 2], output[7, 2], output[8, 2],
                                      output[9, 2], output[10, 2], output[11, 2],
                                      output[0, 2]]])
            return u_out, v_out

        elif count == 84:
            u_out, v_out = np.array([[output[26, 1], output[83, 1], output[39, 1],
                                      output[75, 1], output[52, 1], output[67, 1],
                                      output[26, 1]],
                                     [output[26, 2], output[83, 2], output[39, 2],
                                      output[75, 2], output[52, 2], output[67, 2],
                                      output[26, 2]]])

            return u_out, v_out

def show(input_type='file', space='uv', count=None, output=None,
         new=True, color='k', label=None):

    x, y = input_to_gamut(input_type=input_type, count=count, output=output)

    if space == 'uv':
        uv(x, y, gamut=True, label=label, title=None, color=color, new=new)

def uv(u_, v_, gamut=None, label='u_, v_', facecolors='none', color='k',
       linestyle='--', title='u_, v_', grid=True, new=False):
    """
    Plot u', v' color coordinates using Luxpy.|
    ------------------------------------------

    Args:
        :u_:
            u' coordinate(s) - must be float, int, or array
        :v_:
            v' coordinate(s) - must be float, int, or array
        :gamut:
            None
            Anything bar 'None' will assume a gamut is going to be created.
            This expects a plot in the order of a line in the diagram e.g.
            R, G, B, R or R, Y, G, C, B, M, R. Must go back to starting
            value to complete gamut line.
        :label:
            'u_, v_'
            Change to adjust label within diagram of the input.
        :facecolors:
            'none'
            Change to adjust face color of value within diagram. Only if
            gamut=None
        :color:
            'k'
            Change to adjust color of either edge color or line color,
            depending on if 'gamut' is chosen.
        :linestyle:
            '--'
            Change to adjust style of line if gamut is not None.
        :title:
            'u_, v_'
            Change to adjust title of figure.
        :grid:
            True
            Change to 'None' for no grid in diagram.
        :kwargs:
            Additional keyword arguments for use with matplotlib.pyplot

    Returns:

    """
    if new is True:
        plt.figure()
        ax_uv = plt.axes()
        lx.plot_chromaticity_diagram_colors(256, 0.3, 1, lx._CIEOBS, 'Yuv',
                                            {}, True, ax_uv, grid,
                                            'Times New Roman', 12)
    else:
        ax_uv = plt.axes()

    if gamut is None:
        plt.scatter(float(u_), float(v_), label=label, facecolors=facecolors,
                    edgecolors=color)
    else:
        ax_uv.plot(u_, v_, label=label, color=color, linestyle=linestyle)
    ax_uv.set_title(title)
    ax_uv.set_xlim([-0.1, 0.7])
    ax_uv.set_ylim([-0.1, 0.7])
    ax_uv.legend()

def SPD(device = 'jeti', Tint = 0, wait = 0.1):
    # Initializes spectrometer 'jeti' or 'oceanoptics'
    sp.init(device)

    spds = []

    time.sleep(wait)
    spd = sp.get_spd(manufacturer = device, Tint = Tint)
    spds.append(spd)

    if spds != []:
        spds = np.vstack((spds[0][0,:],[x[1,:] for x in spds]))

    return spds

class VirtualRealityHmd():
    """
    [ADD THIS]
    """

    def __init__(self, camera='VR', lens='Conoscopic', mod_freq=90.0,
                 connect_camera=True):
        """
        Initializes LMK for VR-HMD.|
        ---------------------------
        %timeit:
            2.28 s ± 56.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

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

        # ls.close_labsoft()
        # del ax.LMK

        return results

if __name__ == '__main__':

    test = 1

    # label = 'Oculus Rift CV1: Warm-Up Time'

    # VR = VirtualRealityHmd(connect_camera=False)

    # MAX_Ys = VR.analyze('Y')
    # XYZs = VR.analyze('XYZ')

    # diff, mean = y_diff(MAX_Ys, XYZs)
    # u_v_ = xyz_to_u_v_(XYZs)
    # u_v_ = u_v_.astype(float)
    # show(space='uv', new=False, color='r', input_type='file',
    #      count=7, output=u_v_, label=label)
    # uv(u_v_[3,0], u_v_[3,1], label=label, color='r', new=False)
