# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 19:23:42 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

create():                   Creates an image.
delete():
save():                     Save image.
load():                     Load image from .pcf.
get_amount():
get_size():                 Get image size and parameter.
rotate():                   Rotates image to desired image.
show():                     Show image.

"""
import sys
import os
from skimage import io
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import variables.dicts as dic
import technoteam.activex as ax

def create(image=0, name='Evaluation[1]'):
    """
    Creates an image.|
    ---------------------------
    The image gets the size of the previous image (luminance image or previous
    evalutation image.)
    ---------------------------------------------------------------------------

    %timeit:
        41.4 ms ± 41.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    Parameters
    ----------
    LMK :
        Dispatch('lmk4.LMKAxServer')
    image : int, optional
        0=Grey image, 1=Color image. The default is 0.
    name : QString, optional
        Wished image  name. The default is 'Evaluation[1]'.

    Returns
    -------
    index : int
        Index of the image created

    """

    err_code, index = ax.LMK.iImageCreate(image, name)
    ax.error_code(err_code)

    return index

def delete(image=dic.IMAGE_TYPES['Color']):
    """
    [ADD THIS]

    %timeit:
        27.2 ms ± 373 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

    Parameters
    ----------
    image : TYPE, optional
        DESCRIPTION. The default is dic.IMAGE_TYPES['Color'].

    Returns
    -------
    None.

    """
    ax.LMK.iImageDelete(image)

def save(file_root, file_name, file_type=dic.FILE_TYPES['png'],
         image=dic.IMAGE_TYPES['Color']):
    """
    Save image.|
    -----------
    The function overwrites an existing file.
    -----------------------------------------------------------------------

    Parameters
    ----------
    file_root : QString
        Destination file root.
    file_name : QString
        Destination file name.
    file_type : QString, optional
        Destination file type. The default is dic.FILE_TYPES['png'].
    image : int, optional
        Index of image to save. The default is dic.IMAGE_TYPES['Color'].

    Returns
    -------
    None.

    """

    if not os.path.exists(file_root):
        os.makedirs(file_root)
    err_code = ax.LMK.iSaveImage(image, file_root + file_name + file_type)
    ax.error_code(err_code) # Check for error

def load(file_root, file_name, file_type=dic.FILE_TYPES['pcf'],
         image=dic.IMAGE_TYPES['Color']):
    """
    Load image from .pcf.|
    ---------------------
    Loads a saved image from .pcf. Of course, the image needs to be saved
    first.
    -----------------------------------------------------------------------

    Parameters
    ----------
    file_root : QString
        Source file root.
    file_name : QString
        Source file name.
    file_type : QString, optional
        Source file type.
        .pus = Camera Image
        .pf = Luminance Image
        .pcf = Color Image
        The default is dic.FILE_TYPES['pcf'].
    image : int, optional
        Index of image to Load to. The default is dic.IMAGE_TYPES['Color'].

    Returns
    -------
    None.

    """

    err_code = ax.LMK.iLoadImage(image, file_root + file_name + file_type)
    ax.error_code(err_code) # Check for error

def get_amount():
    """
    [ADD THIS]

    %timeit:
        127 µs ± 2.64 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

    Returns
    -------
    images_no : TYPE
        DESCRIPTION.

    """

    err_code, images_no = ax.LMK.iGetNumberImages()
    ax.error_code(err_code) # Check for error

    return images_no

def get_size(image=dic.IMAGE_TYPES['Color']):
    """
    Get image size and parameter.|
    -----------------------------
    These informations are needed for the other access functions.
    See also Image.SetSize()
    -----------------------------------------------------------------------

    %timeit:
        142 µs ± 6.26 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: -1)
            | Index of image to inform about
    Returns:
        | Number of lines is LastLine - FirstLine + 1.
        | Number of columns is LastColumn - FirstColumn + 1.
        :first_line: int
            | Gets the index of the first line
        :last_line: int
            | Gets the index of the last line
        :first_col: int
            | Gets the index of the first column
        :last_col: int
            | Gets the index of the last column
        :dimensions: int
            | 1 = gray images
            | 3 = color images
    """
    err_code, image_first_line, image_last_line, image_first_col, \
        image_las_col, image_dimensions = ax.LMK.iImageGetSize(image)
    ax.error_code(err_code) # Check for error

    return image_first_line, image_last_line, image_first_col, \
        image_las_col, image_dimensions

def rotate(code=dic.OPERATION_TYPES['Rotate'],
           src_image=dic.IMAGE_TYPES['Luminance'], param='180',
           dst_image=dic.IMAGE_TYPES['Evaluation[1]']):
    """

    Rotates image to desired image.|
    -------------------------------

    Uses image arithmetic with one source image, one parameter, and one
    desination image.
    ---------------------------------------------------------------------------

    %timeit:
        149 ms ± 10.4 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

    Parameters
    ----------
    LMK :
        Dispatch('lmk4.LMKAxServer')
    code : QString, optional
        Operation code, see OPERATION_TYPES{}. The default is OPERATION_TYPES['Rotate'].
    src_image : int, optional
        Index of source image. The default is IMAGE_TYPES['Luminance'].
    param : QString, optional
        Parameter of algorithm. The default is '180'.
    dst_image : int, optional
        Index of destination image. The default is IMAGE_TYPES['Evaluation[1]'].

    Returns
    -------
    None.

    """
    err_code = ax.LMK.imageArithmeticIP1(code, src_image, param, dst_image)
    ax.error_code(err_code) # Check for error

def show(file_root, file_name, file_type=dic.FILE_TYPES['png']):
    """
    Show image.|
    -----------
    Shows a saved image. Of course, the image needs to be saved first.
    -----------------------------------------------------------------------

    Parameters
    ----------
    file_root : QString
        Source file root.
    file_name : QString
        Source file name.
    file_type : QString, optional
        Source file type.
        The default is dic.FILE_TYPES['png'].

    Returns
    -------
    image : uint8
        Stores image into a numpy array and show it.

    """

    image = io.imread(file_root + file_name + file_type)
    io.imshow(image)

    return image
