# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 19:28:01 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

create():                   Create a region.
create_rect_image_size():   Create a rectangular region the size of the whole image.
create_grid():              Create a grid region within whole image with
                                defined amount of squares.
get_id():                   Get index of region given region name.
select():                   Selects or deselects a region.
delete():                   Delete a region.

"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import technoteam.activex as ax
import technoteam.image as im
import variables.dicts as dic

def create(image=dic.IMAGE_TYPES['Color'], region='Ellipse',
           x_coords=[1226, 500, 500], y_coords=[1026, 500, 500]):
    """
    Create a region.|
    ----------------

    Parameters
    ----------
    image : TYPE, optional
        DESCRIPTION. The default is dic.IMAGE_TYPES['Color'].
    region : TYPE, optional
        DESCRIPTION. The default is 'Ellipse'.
    x_coords : TYPE, optional
        DESCRIPTION. The default is [1226, 500, 500].
    y_coords : TYPE, optional
        DESCRIPTION. The default is [1026, 500, 500].

    Returns
    -------
    region_x_points : TYPE
        DESCRIPTION.
    region_y_points : TYPE
        DESCRIPTION.

    """
    [err_code, region_x_points, region_y_points] \
        = ax.LMK.iCreateRegion(image, dic.REGION_TYPES[region]['identifier'],
                               dic.REGION_TYPES[region]['points'], x_coords,
                               y_coords)
    ax.error_code(err_code) # Check for error

    return region_x_points, region_y_points

def create_rect(image, first_col=567, last_col=1969,
                first_line=391, last_line=2045):
    """
    [ADD THIS]

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    first_col : TYPE, optional
        DESCRIPTION. The default is 567.
    last_col : TYPE, optional
        DESCRIPTION. The default is 1969.
    first_line : TYPE, optional
        DESCRIPTION. The default is 391.
    last_line : TYPE, optional
        DESCRIPTION. The default is 2045.

    Returns
    -------
    None.

    """

    create(image, 'Rectangle', x_coords=[first_col, last_col],
           y_coords=[first_line, last_line])

def create_rect_image_size(image=dic.IMAGE_TYPES['Color'],
                           region_id=dic.REGION_TYPES['Rectangle']['identifier'],
                           region_points=dic.REGION_TYPES['Rectangle']['points']):
    """
    Create a rectangular region the size of the whole image.|
    --------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Index of region list (same as image index)
            | Im is usually defined as 'Image', but we needed to call in Image() here
        :region_id: int (default: REGION_TYPES['Rectangle']['identifier'])
            | Type of region from REGION_TYPES{}
        :NumPoints: int (default: REGION_TYPES['Rectangle']['points'])
            | Number of points from REGION_TYPES{}
    Returns:
        :region_x_points: QStringList
            | List of x-points
        :region_y_points: QStringList
            | List of y-points
    """
    [image_first_line, image_last_line, image_first_col,
     image_last_col, _] = im.get_size()
    x_coords = [image_first_col, image_last_col]
    y_coords = [image_first_line, image_last_line]
    [err_code, region_x_points, region_y_points] \
        = ax.LMK.iCreateRegion(image, region_id, region_points, x_coords, y_coords)
    ax.error_code(err_code) # Check for error

    return region_x_points, region_y_points

def create_grid(image=dic.IMAGE_TYPES['Color'],
                region_id=dic.REGION_TYPES['Rectangle']['identifier'],
                region_points=dic.REGION_TYPES['Rectangle']['points'],
                x_squares=3, y_squares=3):
    """
    Create a grid region within whole image with defined amount of squares.|
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Index of region list (same as image index)
            | Im is usually defined as 'Image', but we needed to call in Image() here
        :region_id: int (default: REGION_TYPES['Rectangle']['identifier'])
            | Type of region from REGION_TYPES{}
        :region_points: int (default: REGION_TYPES['Rectangle']['points'])
            | Number of points from REGION_TYPES{}
        :x_squares: int (default: 3)
            | Number of squares in grid along X axis
        :y_squares: int (default: 3)
            | Number of squares in grid along Y axis
    Returns:
        :X: QStringList
            | List of x-points
        :Y: QStringList
            | List of y-points
    """
    [image_first_line, image_last_line, image_first_col, image_last_col, _] = im.get_size()
    image_second_col = int(image_last_col/x_squares)
    image_third_col = int((image_last_col/x_squares)*2)
    image_second_line = int(image_last_line/y_squares)
    image_third_line = int((image_last_line/y_squares)*2)

#        X_Size = int(Image_LastColumn/X_Squares)
#        Y_Size = int(Image_LastLine/Y_Squares)
#
#        for Y in range(Image_FirstLine, Image_LastLine, Y_Size):
#            Y_Pos = ((Image_FirstColumn, Y - Image_FirstLine), \
# (Image_LastColumn, Y - Image_FirstLine))

    x_a = [image_first_col, image_second_col]
    y_a = [image_first_line, image_second_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_a, y_a)

    x_b = [image_second_col, image_third_col]
    y_b = [image_first_line, image_second_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_b, y_b)

    x_c = [image_third_col, image_last_col]
    y_c = [image_first_line, image_second_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_c, y_c)

    x_d = [image_first_col, image_second_col]
    y_d = [image_second_line, image_third_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_d, y_d)

    x_e = [image_second_col, image_third_col]
    y_e = [image_second_line, image_third_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_e, y_e)

    x_f = [image_third_col, image_last_col]
    y_f = [image_second_line, image_third_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_f, y_f)

    x_g = [image_first_col, image_second_col]
    y_g = [image_third_line, image_last_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_g, y_g)

    x_h = [image_second_col, image_third_col]
    y_h = [image_third_line, image_last_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_h, y_h)

    x_i = [image_third_col, image_last_col]
    y_i = [image_third_line, image_last_line]
    ax.LMK.iCreateRegion(image, region_id, region_points, x_i, y_i)

#        X = [Image_FirstColumn, Image_LastColumn]
#        Y = [Image_FirstLine, Image_LastLine]
#        [err_code, Region_X_Points, Region_Y_Points] = ax.LMK.iCreateRegion(Im,
# Type, NumPoints, X, Y)

def get_id(image=dic.IMAGE_TYPES['Color'], name='1'):
    """
    Get index of region given region name.|
    --------------------------------------

    %timeit:
        133 µs ± 3 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Input: Index of region list (same as image index)
        :name: QString (default: '1')
            | InputL Name of region
    Returns:
        :index_out: int
            | Output: Index of this region
    """
    err_code, index_out = ax.LMK.iGetIndexOfRegion(image, name)

    return err_code, index_out

def select(image=dic.IMAGE_TYPES['Color'], index=0, check=1):
    """
    Selects or deselects a region.|
    ------------------------------

    %timeit:
        124 µs ± 376 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Input: Index of region list (same as image index)
        :index: int (default: 0)
            | Index of region
        :check: int (default: 1)
            | 1= select region, 0= deselect region
    """
    err_code = ax.LMK.iSelectRegion(image, index, check)
    ax.error_code(err_code) # Check for error

def delete(image=dic.IMAGE_TYPES['Color'], index=0):
    """
    Delete a region.|
    ----------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Input: Index of region list (same as image index)
        :index: int (default: 0)
            | Index of region to delete
    """
    err_code = ax.LMK.iDeleteRegion(image, index)
    ax.error_code(err_code) # Check for error
