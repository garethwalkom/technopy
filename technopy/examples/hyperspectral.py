# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 18:24:22 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
import os
import numpy as np
import matplotlib.pyplot as plt

from technopy.change_this import roots as root
from technopy.variables import dicts as dic
from technopy.technoteam import labsoft as ls
from technopy.technoteam import camera as cam
from technopy.technoteam import capture as cap
from technopy.technoteam import image as im

class Hyperspectral:
    """
    [ADD THIS]
    """

    def __init__(self, connect_camera=False):
        """
        Initializes LMK for Hyperspectral Camera.|
        -----------------------------------------
        %timeit:


        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """

        self.camera = 'Hyperspectral'
        self.lens = '8mm'
        self.load_hyp = root.LOAD_HYP
        self.save_root = root.SAVE_TEST
        self.load_root = root.LOAD
        self.image = dic.IMAGE_TYPES['Luminance']
        self.file_type = dic.FILE_TYPES['pf']

        ls.open_labsoft()

        if connect_camera is True:
            _, self.camera_no = cam.set_camera(self.camera)
            _, self.lens_no = cam.set_lens(self.camera, self.lens)
            cam.open_camera(self.camera_no, self.lens_no)

    def capture(self):
        """
        [ADD THIS]

        Returns
        -------
        None.

        """

        _, filter_wheel_names = cam.get_filter_wheels()
        for number, filter_name in enumerate(filter_wheel_names[1:]):
            cam.set_filter_wheel(number+1)
            cam.set_autoscan(1)
            cap.single_pic(False)
            im.rotate(src_image=self.image, param='270', dst_image=self.image)
            im.save(self.image, self.save_root + str(filter_name)[1:-1] + \
                    dic.FILE_TYPES['txt'])


    def save_all(self):
        """
        [ADD THIS]

        """
        ## Initialize
        # Open LMK LabSoft4 Standard Color ActiveX
        ls.open_labsoft()

        for wavelength in os.listdir(self.load_hyp):
            if wavelength.endswith(self.file_type):
                self.variable = wavelength[:-3]
                im.load(self.image, self.load_hyp + wavelength)
                im.rotate(src_image=self.image, param='270', dst_image=self.image)
                im.save(self.image, self.save_root + self.variable + \
                        dic.FILE_TYPES['txt'])

    def read_all(self):
        """
        [ADD THIS]

        Returns
        -------
        wavelengths : TYPE
            DESCRIPTION.
        results : TYPE
            DESCRIPTION.

        """

        self.file_type = dic.FILE_TYPES['txt']

        self.wavelengths = []
        self.results = []

        for wavelength in os.listdir(self.load_root):
            if wavelength.endswith(self.file_type):
                variable = wavelength[:-4]
                output = np.loadtxt(self.load_root + variable + self.file_type,
                                    skiprows=2, delimiter='\t')
                self.wavelengths.append(variable)
                self.results.append(output)

        return self.wavelengths, self.results

    def get_pixel(self, row, col, data=None, nms=None, plot=False):
        """
        [ADD THIS]

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
            self.results = data
            self.wavelengths = nms

        self.pixel = []
        for result in self.results:
            self.max_rows = result.shape[0]
            self.max_cols = result.shape[1]
            self.pixel.append(result[row, col])

        if plot is True:
            plt.plot(self.wavelengths, self.pixel)
            plt.title('Pixel at: Row: ' + str(row) + ' Col: ' + str(col))
            plt.xlabel('Wavelength [nm]')

        return self.pixel

if __name__ == '__main__':

    HYPER = Hyperspectral(connect_camera=True)
