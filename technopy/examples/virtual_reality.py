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

from technopy.change_this import roots as root
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
        # Open LMK LabSoft4 Standard Color ActiveX
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

    def warm_up(self, time_total=120):
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
                max_lum = bob.max_luminance()
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


    def measure(self, autoscan=False, min_time=0.0, time_ratio=3.0,
                pic_count=1):
        """
        Measure a Virtual Reality Head-Mounted-Display.|
        -----------------------------------------------

        Returns
        -------
        output_color : TYPE
            DESCRIPTION.

        """
        meas_start = datetime.datetime.now()

        ## Capture Image
        cap.color_high_dyn(autoscan, min_time, time_ratio, pic_count)

        ## Save Measurement
        ls.save(file_name=self.save_root + \
                datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                    dic.FILE_TYPES['ttcs'])

        meas_fin = datetime.datetime.now()
        print('Measured Image in: {}\n'.format(meas_fin - meas_start))

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

        return results

if __name__ == '__main__':

    VR = VirtualRealityHmd(connect_camera=False)

    # label = 'Oculus Rift CV1'

    # MAX_Ys = VR.analyze('Y')
    # XYZs = VR.analyze('XYZ')

    # diff, mean = fanta.y_diff(MAX_Ys, XYZs)
    # u_v_ = fanta.xyz_to_u_v_(XYZs)
    # u_v_ = u_v_.astype(float)
    # fanta.show(space='uv', new=False, color='r', input_type='file',
    #       count=7, output=u_v_, label=label)
    # fanta.uv(u_v_[3,0], u_v_[3,1], label=label, color='r', new=False)
