# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 19:42:21 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
from win32com.client import Dispatch
import numpy as np
from matplotlib import pyplot as plt
import luxpy as lx

import activex as ax
import dicts as dic
import image as im
import region as reg

LMK = Dispatch('lmk4.LMKAxServer')

def statistic_exists(image = dic.IMAGE_TYPES['Color'], region = 0):
    """
    Proof, if a statistic exists for a image / region / statistic type.|
    -------------------------------------------------------------------
    Parameters:
        :lmk:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: Image = IMAGE_TYPES['Color'])
            | Image
        :region: int (default: 0)
            | Index of region in this image
    Returns:
        :exists: int
            | 1 = statistic exists
            | 0 = statistic does not exist
        :statistic_type: int
            | Index of statistic type
        :statistic_index: int
            | Index in statistic list?
    """
    err_code, exists, statistic_type, statistic_index = LMK.iHaveStatistic(image, region)
    ax.error_code(err_code) # Check for error

    return exists, statistic_type, statistic_index

def create_statistic(statistic_type = dic.STATISTIC_TYPES['standardColor'],
                    image = dic.IMAGE_TYPES['Color'], region = 0,
                    num_param = 1, param_list = [1]):
    """
    Create a new statistic.|
    -----------------------
    Parameters:
        :lmk:
            | Dispatch('lmk4.LMKAxServer')
        :statistic_type: int (default: STATISTIC_TYPES['standardColor'])
            | Index of statistic type
        :image: int (default: Image = IMAGE_TYPES['Color'])
            | Image
        :region: int (default: 0)
            | Index of region in this image
        :num_param: int (default: 1)
            | Number of parameters for this statistic
        :param_list: QStringList
    """
    [err_code, statistic] = LMK.iCreateStatistic(statistic_type, image, region, num_param, param_list)
    ax.error_code(err_code) # Check for error

    return statistic

def get_standard_statistic(statistic_type = dic.STATISTIC_TYPES['standardColor'],
                         region = 0, color_class = 0):
    """
    Determine parameter of the standard statistic.|
    ----------------------------------------------
    Parameters:
        :lmk:
            | Dispatch('lmk4.LMKAxServer')
        :statistic_type: int (default: STATISTIC_TYPES['standardColor'])
            | Index of statistic type
        :region: int (default: 0)
            | Index of region in this image
        :color_class: int (default: 0)
            | Index of class or color:
                0 = blue
                1 = green
                2 = red
    Returns:
        :area: float
            | Amount of pixels in area of statistic
        :stat_min: float
            | Minimum value
        :stat_max: float
            | Maximum value
        :stat_mean: float
            | Mean value
        :variance: float
            | Variance (...SD?) in values
    """

    stats = {'Area': [], 'Min': [], 'Max': [], 'Mean': [], 'Variance': []}

    err_code, area, stat_min, stat_max, stat_mean, variance = LMK.iGetStandardStatistic2(statistic_type, region, color_class)
    ax.error_code(err_code) # Check for error

    stats['Area'].append(LMK.iGetStandardStatistic2(statistic_type, region, color_class)[1])
    stats['Min'].append(LMK.iGetStandardStatistic2(statistic_type, region, color_class)[2])
    stats['Max'].append(LMK.iGetStandardStatistic2(statistic_type, region, color_class)[3])
    stats['Mean'].append(LMK.iGetStandardStatistic2(statistic_type, region, color_class)[4])
    stats['Variance'].append(LMK.iGetStandardStatistic2(statistic_type, region, color_class)[5])

    return stats

def delete_statistic(statistic_type = dic.STATISTIC_TYPES['standardColor'], stat_no = 0):
    """
    Delete an existing statistic.|
    -----------------------------
    Parameters:
        :lmk:
            | Dispatch('lmk4.LMKAxServer')
        :statistic_type: int (default: STATISTIC_TYPES['standardColor'])
            | Index of statistic type
        :stat_no: int (default: 0)
            | Index of statistic number
    """
    err_code = LMK.iDeleteStatistic(statistic_type, stat_no)
    ax.error_code(err_code) # Check for error

def ProjectRectifLum():
    """
    [ADD THIS]

    Returns
    -------
    None.

    """
    LMK.iExecMenuPoint('Macros|ProjRectLum')

def ProjectRectifCol():
    """
    [ADD THIS]

    Returns
    -------
    None.

    """
    LMK.iExecMenuPoint('Macros|ProjRectCol')

def CoordTransformLum():
    """
    [ADD THIS]

    Returns
    -------
    None.

    """
    LMK.iExecMenuPoint('Macros|CoordTransLum')

def CoordTransformCol():
    """
    [ADD THIS]

    Returns
    -------
    None.

    """
    LMK.iExecMenuPoint('Macros|CoordTransCol')


def get_image_mean_xyz():
    """
    Create region size of image and get mean XYZ.|
    ----------------------------------------------
    """

    # Create a region the size of the whole image
    region_x_points, region_y_points = reg.create_rect_image_size()
    # Get ID of region
    err_code, index_out = reg.get_id(dic.IMAGE_TYPES['Color'], name = '1')
    # Select region from index of region
    reg.select(index = index_out)

    ### Evaluate Region
    create_statistic(dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], index_out, param_list = [1])

    blue_stats = get_standard_statistic(color_class = 0)
    b_mean = str(blue_stats['Mean'])[1:-1]
    b_mean = float(b_mean)
    green_stats = get_standard_statistic(color_class = 1)
    g_mean = str(green_stats['Mean'])[1:-1]
    g_mean = float(g_mean)
    red_stats = get_standard_statistic(color_class = 2)
    r_mean = str(red_stats['Mean'])[1:-1]
    r_mean = float(r_mean)

    output_color = convert_cie_rgb(cie_r = r_mean, cie_g = g_mean, cie_b = b_mean)

    return output_color

def get_circle_mean_xyz():
    """
    Get size of image, create eclipse in center, get mean XYZ from circle.|
    ----------------------------------------------------------------------
    """

    # Get size of image
    image_first_lin, image_last_line, image_first_col, image_last_col, image_dimensions = im.get_size()

    # If region already exists, delete it
    err_code, index_out = reg.get_id()
    if err_code == 0:
        reg.delete()

    # If statistic already exists, delete it
    exists, statistic_type, statistic_index = statistic_exists()
    if exists == 1:
        delete_statistic()

    # Create a region the size of the whole image
    region_x_points, region_y_points = reg.create(x_coords = [image_last_col/2, 1700, 1700],
                                                  y_coords = [image_last_line/2, 1700, 1700])
    # Get ID of region
    err_code, index_out = reg.get_id(dic.IMAGE_TYPES['Color'], name = '1')
    # Select region from index of region
    reg.select(index = index_out)

    ### Evaluate Region
    create_statistic(dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], index_out, param_list = [1])

    blue_stats = get_standard_statistic(color_class = 0)
    b_mean = str(blue_stats['Mean'])[1:-1]
    b_mean = float(b_mean)
    green_stats = get_standard_statistic(color_class = 1)
    g_mean = str(green_stats['Mean'])[1:-1]
    g_mean = float(g_mean)
    red_stats = get_standard_statistic(color_class = 2)
    r_mean = str(red_stats['Mean'])[1:-1]
    r_mean = float(r_mean)

    output_color = convert_cie_rgb(cie_r = r_mean, cie_g = g_mean, cie_b = b_mean)

    return output_color


# def get_grid_mean_xyz():
#     """
#     Create regions as a grid in image and get mean XYZ.|
#     ---------------------------------------------------
#     """

#     # Create a region the size of the whole image
#     reg.CreateGrid(LMK)
#     # Get ID of region
#     err_code, Index_Zero = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '1')
#     err_code, Index_One = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '2')
#     err_code, Index_Two = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '3')
#     err_code, Index_Three = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '4')
#     err_code, Index_Four = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '5')
#     err_code, Index_Five = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '6')
#     err_code, Index_Six = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '7')
#     err_code, Index_Seven = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '8')
#     err_code, Index_Eight = reg.GetID(LMK, dic.IMAGE_TYPES['Color'], Name = '9')
#     # Select region from index of region
#     reg.Select(LMK, Index = Index_Zero)
#     reg.Select(LMK, Index = Index_One)
#     reg.Select(LMK, Index = Index_Two)
#     reg.Select(LMK, Index = Index_Three)
#     reg.Select(LMK, Index = Index_Four)
#     reg.Select(LMK, Index = Index_Five)
#     reg.Select(LMK, Index = Index_Six)
#     reg.Select(LMK, Index = Index_Seven)
#     reg.Select(LMK, Index = Index_Eight)

#     ### Evaluate Region
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Zero, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_One, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Two, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Three, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Four, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Five, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Six, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Seven, ParamList = [1])
#     CreateStatistic(LMK, dic.STATISTIC_TYPES['standardColor'], dic.IMAGE_TYPES['Color'], Index_Eight, ParamList = [1])

#     Blue_Stats_Zero = GetStandardStatistic(LMK, Region = 0, Class = 0)
#     B_Mean_Zero = str(Blue_Stats_Zero['Mean'])[1:-1]
#     B_Mean_Zero = float(B_Mean_Zero)
#     Green_Stats_Zero = GetStandardStatistic(LMK, Region = 0, Class = 1)
#     G_Mean_Zero = str(Green_Stats_Zero['Mean'])[1:-1]
#     G_Mean_Zero = float(G_Mean_Zero)
#     Red_Stats_Zero = GetStandardStatistic(LMK, Region = 0, Class = 2)
#     R_Mean_Zero = str(Red_Stats_Zero['Mean'])[1:-1]
#     R_Mean_Zero = float(R_Mean_Zero)

#     Blue_Stats_One = GetStandardStatistic(LMK, Region = 1, Class = 0)
#     B_Mean_One = str(Blue_Stats_One['Mean'])[1:-1]
#     B_Mean_One = float(B_Mean_One)
#     Green_Stats_One = GetStandardStatistic(LMK, Region = 1, Class = 1)
#     G_Mean_One = str(Green_Stats_One['Mean'])[1:-1]
#     G_Mean_One = float(G_Mean_One)
#     Red_Stats_One = GetStandardStatistic(LMK, Region = 1, Class = 2)
#     R_Mean_One = str(Red_Stats_One['Mean'])[1:-1]
#     R_Mean_One = float(R_Mean_One)

#     Blue_Stats_Two = GetStandardStatistic(LMK, Region = 2, Class = 0)
#     B_Mean_Two = str(Blue_Stats_Two['Mean'])[1:-1]
#     B_Mean_Two = float(B_Mean_Two)
#     Green_Stats_Two = GetStandardStatistic(LMK, Region = 2, Class = 1)
#     G_Mean_Two = str(Green_Stats_Two['Mean'])[1:-1]
#     G_Mean_Two = float(G_Mean_Two)
#     Red_Stats_Two = GetStandardStatistic(LMK, Region = 2, Class = 2)
#     R_Mean_Two = str(Red_Stats_Two['Mean'])[1:-1]
#     R_Mean_Two = float(R_Mean_Two)

#     Blue_Stats_Three = GetStandardStatistic(LMK, Region = 3, Class = 0)
#     B_Mean_Three = str(Blue_Stats_Three['Mean'])[1:-1]
#     B_Mean_Three = float(B_Mean_Three)
#     Green_Stats_Three = GetStandardStatistic(LMK, Region = 3, Class = 1)
#     G_Mean_Three = str(Green_Stats_Three['Mean'])[1:-1]
#     G_Mean_Three = float(G_Mean_Three)
#     Red_Stats_Three = GetStandardStatistic(LMK, Region = 3, Class = 2)
#     R_Mean_Three = str(Red_Stats_Three['Mean'])[1:-1]
#     R_Mean_Three = float(R_Mean_Three)

#     Blue_Stats_Four = GetStandardStatistic(LMK, Region = 4, Class = 0)
#     B_Mean_Four = str(Blue_Stats_Four['Mean'])[1:-1]
#     B_Mean_Four = float(B_Mean_Four)
#     Green_Stats_Four = GetStandardStatistic(LMK, Region = 4, Class = 1)
#     G_Mean_Four = str(Green_Stats_Four['Mean'])[1:-1]
#     G_Mean_Four = float(G_Mean_Four)
#     Red_Stats_Four = GetStandardStatistic(LMK, Region = 4, Class = 2)
#     R_Mean_Four = str(Red_Stats_Four['Mean'])[1:-1]
#     R_Mean_Four = float(R_Mean_Four)

#     Blue_Stats_Five = GetStandardStatistic(LMK, Region = 5, Class = 0)
#     B_Mean_Five = str(Blue_Stats_Five['Mean'])[1:-1]
#     B_Mean_Five = float(B_Mean_Five)
#     Green_Stats_Five = GetStandardStatistic(LMK, Region = 5, Class = 1)
#     G_Mean_Five = str(Green_Stats_Five['Mean'])[1:-1]
#     G_Mean_Five = float(G_Mean_Five)
#     Red_Stats_Five = GetStandardStatistic(LMK, Region = 5, Class = 2)
#     R_Mean_Five = str(Red_Stats_Five['Mean'])[1:-1]
#     R_Mean_Five = float(R_Mean_Five)

#     Blue_Stats_Six = GetStandardStatistic(LMK, Region = 6, Class = 0)
#     B_Mean_Six = str(Blue_Stats_Six['Mean'])[1:-1]
#     B_Mean_Six = float(B_Mean_Six)
#     Green_Stats_Six = GetStandardStatistic(LMK, Region = 6, Class = 1)
#     G_Mean_Six = str(Green_Stats_Six['Mean'])[1:-1]
#     G_Mean_Six = float(G_Mean_Six)
#     Red_Stats_Six = GetStandardStatistic(LMK, Region = 6, Class = 2)
#     R_Mean_Six = str(Red_Stats_Six['Mean'])[1:-1]
#     R_Mean_Six = float(R_Mean_Six)

#     Blue_Stats_Seven = GetStandardStatistic(LMK, Region = 7, Class = 0)
#     B_Mean_Seven = str(Blue_Stats_Seven['Mean'])[1:-1]
#     B_Mean_Seven = float(B_Mean_Seven)
#     Green_Stats_Seven = GetStandardStatistic(LMK, Region = 7, Class = 1)
#     G_Mean_Seven = str(Green_Stats_Seven['Mean'])[1:-1]
#     G_Mean_Seven = float(G_Mean_Seven)
#     Red_Stats_Seven = GetStandardStatistic(LMK, Region = 7, Class = 2)
#     R_Mean_Seven = str(Red_Stats_Seven['Mean'])[1:-1]
#     R_Mean_Seven = float(R_Mean_Seven)

#     Blue_Stats_Eight = GetStandardStatistic(LMK, Region = 8, Class = 0)
#     B_Mean_Eight = str(Blue_Stats_Eight['Mean'])[1:-1]
#     B_Mean_Eight = float(B_Mean_Eight)
#     Green_Stats_Eight = GetStandardStatistic(LMK, Region = 8, Class = 1)
#     G_Mean_Eight = str(Green_Stats_Eight['Mean'])[1:-1]
#     G_Mean_Eight = float(G_Mean_Eight)
#     Red_Stats_Eight = GetStandardStatistic(LMK, Region = 8, Class = 2)
#     R_Mean_Eight = str(Red_Stats_Eight['Mean'])[1:-1]
#     R_Mean_Eight = float(R_Mean_Eight)

#     Output_Color_Zero = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Zero, CIE_G = G_Mean_Zero, CIE_B = B_Mean_Zero)
#     Output_Color_One = Convert_CIE_RGB(LMK, CIE_R = R_Mean_One, CIE_G = G_Mean_One, CIE_B = B_Mean_One)
#     Output_Color_Two = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Two, CIE_G = G_Mean_Two, CIE_B = B_Mean_Two)
#     Output_Color_Three = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Three, CIE_G = G_Mean_Three, CIE_B = B_Mean_Three)
#     Output_Color_Four = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Four, CIE_G = G_Mean_Four, CIE_B = B_Mean_Four)
#     Output_Color_Five = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Five, CIE_G = G_Mean_Five, CIE_B = B_Mean_Five)
#     Output_Color_Six = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Six, CIE_G = G_Mean_Six, CIE_B = B_Mean_Six)
#     Output_Color_Seven = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Seven, CIE_G = G_Mean_Seven, CIE_B = B_Mean_Seven)
#     Output_Color_Eight = Convert_CIE_RGB(LMK, CIE_R = R_Mean_Eight, CIE_G = G_Mean_Eight, CIE_B = B_Mean_Eight)

#     return Output_Color_Zero, Output_Color_One, Output_Color_Two, Output_Color_Three, Output_Color_Four, Output_Color_Five, Output_Color_Six, Output_Color_Seven, Output_Color_Eight

def get_color_histogram_values(image = dic.IMAGE_TYPES['Color'],
                            color_space = dic.COLOR_SPACES['XYZ']):
    """
    Get the values of the histogram in a color image.|
    -------------------------------------------------
    The color space is always RGB.
    -----------------------------------------------------------------------
    Parameters:
        :lmk:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Index of object
        :color_space: int (default: COLOR_SPACES['XYZ'])
            | Wished color space from COLOR_SPACES{}
    Returns:
        :num_param: int
            | Number of values
        :x_coords: QStringList
            | x-coordinates
        :hist_values: QStringList
            | Histogram values
    """
    err_code, num_param, x_coords, hist_values = LMK.iGetColorHistogramValues(image, color_space)
    ax.error_code(err_code) # Check for error

    return num_param, x_coords, hist_values

def get_pixel_color(image = dic.IMAGE_TYPES['Color'], line = 500, column = 500):
    """
    Get a pixel value of a color image.|
    -----------------------------------
    Parameters:
        :lmk:
            | Dispatch('lmk4.LMKAxServer')
        :image: int (default: IMAGE_TYPES['Color'])
            | Index of image
        :line: int (default: 500)
            | Line index
        :column: int (default: 500)
            | Column index
    Returns:
        | The function returns an error if the pixel position is
            outside or the image is a color image.
        :cie_r: float
            | Gets the red component of the pixel value
        :cie_g: float
            | Gets the green component of the pixel value
        :cie_b: float
            | Gets the blue component of the pixel value
    """
    err_code, cie_r, cie_g, cie_b = LMK.iImageGetPixelColor(image, line, column)
    ax.error_code(err_code) # Check for error

    return cie_r, cie_g, cie_b

def convert_cie_rgb(cie_r = 255.0, cie_g = 0.0, cie_b = 0.0, r_ref = 0.0,
                 g_ref = 0.0, b_ref = 0.0, color_space = dic.COLOR_SPACES['XYZ']):
    """
    Conversion of a color value from CIE-RGB to another color space.|
    ----------------------------------------------------------------
    The color value is given in CIE-RGB and is converted into a color value
    in the target color space. If there is a reference color needed for this
    color space, the reference color is also in CIE-RGB. If there is no
    reference color needed, the three variables can be set to zero.
    The destination color space is given by the value of COLOR_SPACES{}.
    The three components of the destionation color are available
    in '_Out' after the function call returned.
    -----------------------------------------------------------------------
    Parameters:
        :lmk:
            | Dispatch('lmk4.LMKAxServer')
        :cie_r: float (default: 255.0)
            | 	Red component of input color
        :cie_g: float (default: 0.0)
            | 	Green component of input color
        :cie_b: float (default: 0.0)
            | 	Blue component of input color
        :r_ref: float (default: 0.0)
            | Red component of reference color
        :g_ref: float (default: 0.0)
            | Green component of reference color
        :b_ref: float (default: 0.0)
            | Blue component of reference color
        :color_space: int (default: COLOR_SPACES['XYZ'])
            | 	Wished destination color space
    Returns:
        :output_color: array
            | Calculated color in an array shape of (1, 3)
    """
    [err_code, out_i, out_ii, out_iii] = \
        LMK.iGetColor(cie_r, cie_g, cie_b, r_ref, g_ref, b_ref, color_space)
    ax.error_code(err_code) # Check for error

    # Place new values into an array
    output_color = np.array([[out_i], [out_ii], [out_iii]])
    # Transpose array into (1, 3) shape
    output_color = output_color.T

    return output_color

def xyz_to_xy(xyz):
    """
    Convert XYZ to x, y.|
    ---------------
    Parameters:
        :xyz: array (shape: (1, 3))
    Returns:
        :xy_mean: array (shape: (1, 2))
    """
    y_xy = lx.xyz_to_Yxy(xyz)
    y_xy_mean = np.array([[y_xy[:,0].mean(), y_xy[:,1].mean(), y_xy[:,2].mean()]])

    y_xy_mean = np.around(y_xy_mean, decimals=3)

    x_mean = y_xy_mean[:,1]
    x_mean = str(x_mean)[1:-1]
    y_mean = y_xy_mean[:,2]
    y_mean = str(y_mean)[1:-1]

    xy_mean = np.array([[x_mean], [y_mean]])
    xy_mean = xy_mean.T

    return xy_mean

def xyz_to_u_v_(xyz):
    """
    Conver XYZ to u', v'.|
    ---------------
    Parameters:
        :xyz: array (shape: (1, 3))
    Returns:
        :u_v_mean: array (shape: (1, 2))
    """
    y_uv = lx.xyz_to_Yuv(xyz)
    y_uv_mean = np.array([[y_uv[:,0].mean(), y_uv[:,1].mean(), y_uv[:,2].mean()]])

    y_uv_mean = np.around(y_uv_mean, decimals=3)

    u_mean = y_uv_mean[:,1]
    u_mean = str(u_mean)[1:-1]
    v_mean = y_uv_mean[:,2]
    v_mean = str(v_mean)[1:-1]

    u_v_mean = np.array([[u_mean], [v_mean]])
    u_v_mean = u_v_mean.T

    return u_v_mean

def Show_xy(x_val, y_val, label='x, y', facecolors='none', color='k',
            linestyle='--', title='x, y', grid=True, **kwargs):
    """
    Plot x, y color coordinates using Luxpy.

    Parameters:
        :x_val: float, int, or array
            | x coordinate(s)
        :y_val: float, int, or array
            | y coordinate(s)
        :label: string (default: 'x, y')
            | Change to adjust label within diagram of the input.
        :facecolors: string (default: 'none')
            | Change to adjust face color of value within diagram. Only if
                gamut=None
        :color: string (default: 'k')
            | Change to adjust color of either edge color or line color,
                depending on if 'gamut' is chosen.
        :linestyle: string (default: '--')
            | Change to adjust style of line if gamut is not None.
        :title: string (default: 'x, y')
            | Change to adjust title of figure.
        :grid: True of None (default: True)
            | Change to 'None' for no grid in diagram.
        :kwargs:
            | Additional keyword arguments for use with matplotlib.pyplot

    Returns:

    """
    plt.figure()
    ax_xy = plt.axes()
    lx.plot_chromaticity_diagram_colors(256,0.3,1,lx._CIEOBS,'Yxy',{},True,ax_xy,
                                        grid,'Times New Roman',12)
    plt.scatter(float(x_val), float(y_val), label = label, facecolors = facecolors, edgecolors = color)
    ax_xy.set_title(title)
    ax_xy.set_xlim([-0.1, 0.8])
    ax_xy.set_ylim([-0.1, 0.9])
    ax_xy.legend()

def Show_u_v_(u_val, v_val, label='u_, v_', facecolors='none', color='k',
       linestyle='--', title='u_, v_', grid=True, **kwargs):
    """
    Plot u', v' color coordinates using Luxpy.

    Parameters:
        :u_val: float, int, or array
            | u' coordinate(s)
        :v_val: float, int, or array
            | v' coordinate(s)
        :label: string (default: 'u_, v_')
            | Change to adjust label within diagram of the input.
        :facecolors: string (default: 'none')
            | Change to adjust face color of value within diagram. Only if
                gamut=None
        :color: string (default: 'k')
            | Change to adjust color of either edge color or line color,
                depending on if 'gamut' is chosen.
        :linestyle: string (default: '--')
            | Change to adjust style of line if gamut is not None.
        :title: string (default: 'u_, v_')
            | Change to adjust title of figure.
        :grid: True of None (default: True)
            | Change to 'None' for no grid in diagram.
        :kwargs:
            | Additional keyword arguments for use with matplotlib.pyplot

    Returns:

    """
    plt.figure()
    ax_uv = plt.axes()
    lx.plot_chromaticity_diagram_colors(256,0.3,1,lx._CIEOBS,'Yuv',{},True,ax_uv,
                                        grid,'Times New Roman',12)
    plt.scatter(float(u_val), float(v_val), label = label, facecolors = facecolors, edgecolors = color)
    ax_uv.set_title(title)
    ax_uv.set_xlim([-0.1, 0.7])
    ax_uv.set_ylim([-0.1, 0.7])
    ax_uv.legend()