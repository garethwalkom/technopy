# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 18:24:22 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

from technopy.variables import dicts as dic
from technopy.technoteam import labsoft as ls
from technopy.technoteam import camera as cam
from technopy.technoteam import capture as cap
from technopy.technoteam import image as im

class Hyperspectral:
    """
    Initialize, capture, and analyze hyperspectral images.|
    ------------------------------------------------------
    """

    def __init__(self, calibration_data_root, camera_no, lens_no, load_root,
                 save_root, data_cube, connect_camera=False):
        """
        Initialize LabSoft for hyperspectral camera.|
        --------------------------------------------

        Parameters
        ----------
        calibration_data_root : TYPE
            DESCRIPTION.
        camera_no : TYPE
            DESCRIPTION.
        lens_no : TYPE
            DESCRIPTION.
        load_root : TYPE
            DESCRIPTION.
        save_root : TYPE
            DESCRIPTION.
        data_cube : TYPE
            DESCRIPTION.
        connect_camera : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """

        self.data_root = calibration_data_root
        self.load_root = load_root
        self.save_root = save_root
        self.data_cube = data_cube
        self.camera_no = camera_no
        self.image = dic.IMAGE_TYPES['Luminance']
        self.file_type = dic.FILE_TYPES['pf']

        self.wavelengths = []
        self.results = []

        ls.open_labsoft()

        if connect_camera is True:
            cam.open_camera(self.data_root, self.camera_no, lens_no)

    def capture(self):
        """
        Capture hyperspectral image.|
        ----------------------------

        Returns
        -------
        None.

        """

        _, filter_wheel_names = cam.get_filter_wheels(self.data_root,
                                                      self.camera_no)
        for number, filter_name in enumerate(filter_wheel_names[1:]):
            cam.set_filter_wheel(number+1)
            cam.set_autoscan(1)
            cap.single_pic(self.data_root, self.camera_no, False)
            im.rotate(src_image=self.image, param='270', dst_image=self.image)
            im.save(self.image, self.save_root + str(filter_name)[1:-1] + \
                    dic.FILE_TYPES['txt'])


    def save_all(self):
        """
        Save all wavelengths as .txt.|
        -----------------------------

        """

        for wavelength in os.listdir(self.data_cube):
            if wavelength.endswith(self.file_type):
                variable = wavelength[:-3]
                im.load(self.image, self.data_cube + wavelength)
                im.rotate(src_image=self.image, param='270',
                          dst_image=self.image)
                im.save(self.image, self.save_root + variable + \
                        dic.FILE_TYPES['txt'])

    def read_all(self):
        """
        Read all .txts and get wavelengths and results.|
        -----------------------------------------------

        Returns
        -------
        wavelengths : TYPE
            DESCRIPTION.
        results : TYPE
            DESCRIPTION.

        """

        file_type = dic.FILE_TYPES['txt']

        for wavelength in os.listdir(self.load_root):
            if wavelength.endswith(file_type):
                variable = wavelength[:-4]
                output = np.loadtxt(self.load_root + variable + file_type,
                                    skiprows=2, delimiter='\t')
                self.wavelengths.append(variable)
                self.results.append(output)

        return self.wavelengths, self.results

    def get_pixel(self, row, col, data=None, nms=None, plot=False):
        """
        Get the spectral radiance of a given pixel.|
        -------------------------------------------

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.
        col : TYPE
            DESCRIPTION.
        data : TYPE, optional
            DESCRIPTION. The default is None.
        nms : TYPE, optional
            DESCRIPTION. The default is None.
        plot : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        if data and nms is not None:
            results = data
            wavelengths = nms
        else:
            results = self.results
            wavelengths = self.wavelengths

        pixel = []
        for result in results:
            pixel.append(result[row, col])

        if plot is True:
            plt.plot(wavelengths, pixel)
            plt.title('Pixel at: Row: ' + str(row) + ' Col: ' + str(col))
            plt.xlabel('Wavelength [nm]')

        return pixel

if __name__ == '__main__':

    # Define Calibration Data Root
    DATA_ROOT = 'F:/LMK/Calibration Data'

    # Define Save/Load Roots
    SAVE_ROOT = 'E:/Measurements/' + str(datetime.date.today()) + '/'
    LOAD_ROOT = 'E:/Measurements/TEST/'

    # Define Hyperspectral Data Cube Root
    DATA_CUBE = 'F:/Program Files/Hyperspectral Camera/GUIHSK23052016/Data_Cube/20200305_081505/'

    # Define Camera and Lens Numbers
    SET = cam.Setup(DATA_ROOT, camera_no=None, lens_no=None)
    CAMERA_NO, LENS_NO, _ = SET.numbers()

    # Initializes hypspectral class and connects to hyperspectral camera
    HYPER = Hyperspectral(DATA_ROOT, CAMERA_NO, LENS_NO,
                          load_root=LOAD_ROOT, save_root=SAVE_ROOT,
                          data_cube=DATA_CUBE, connect_camera=True)
