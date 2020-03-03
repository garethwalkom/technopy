# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 22:06:28 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

# get_no_displays():          Number of connected displays.
# get_target():               Get current target for template image generation.
# set_target():               Set target for template image generation.
# get_target_properties():    Get properties of current target.
# get_list_of_categories():   Get list of categories of template images.
# get_list_of_operations():   Get list of tpes of tamplate images for the given category.
# set_operation():            Set a type of template or an option.
# get_list_of_param_names():  Get a parameter name list for the given template image type.
# get_param_value():          Get a certain parameter value.
# set_param_value():          Set a certain parameter value.
# hide_dialog():              Make template image dialog invisible.
# create_image():             Create template image with the adjusted parameters.
# delete_image():             Remove template image from the display.
# load_image():               Load template image file to the target.

"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from technoteam import activex as ax

def get_no_displays():
    """
    Number of connected displays.|
    -----------------------------
    At lease there is one - on which the program is shown.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :no_displays: int
            | Get number of available displays, at least one.
    """
    err_code, no_displays = ax.LMK.iTIG_GetNumberTargetDisplays()
    ax.error_code(err_code) # Check for error

    return no_displays

def get_target():
    """
    Get current target for template image generation.|
    -------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :display_id: int
            | -1 = Use given image name
            | 0...N-1 = One of the connected displays
        :display_name: QString
            | Image name is only returned if 'DisplayID' == -1
    """
    err_code, display_id, display_name = ax.LMK.iTIG_GetTarget()
    ax.error_code(err_code) # Check for error

    return display_id, display_name

def set_target(display_id, display_name):
    """
    Get current target for template image generation.|
    -------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :display_id: int
            | -1 = Use given image name
            | 0...N-1 = One of the connected displays
        :display_name: QString
            | Image name is only necessary if 'DisplayID' == -1
    """
    err_code = ax.LMK.iTIG_SetTarget(display_id, display_name)
    ax.error_code(err_code) # Check for error

def get_target_properties():
    """
    Get properties of current target.|
    ---------------------------------
    The size of the target image is fixed.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :target_type: int
            | 1 = Monochrome image
            | 2 = Color image
            | 3 = Display
            |       in this case the type (monochrome or color)
            |       is chosen automatically
        :target_height: int
            | Height in millimeters
        :target_width: int
            | Width in millimeters
        :target_lines: int
            | Number of image lines
        :target_columns: int
            | Number of image columns
    """
    err_code, target_type, target_height, \
        target_width, target_lines, \
            target_columns = ax.LMK.iTIG_GetTargetProperties()
    ax.error_code(err_code) # Check for error

    return target_type, target_height, target_width, target_lines, target_columns

def get_list_of_categories():
    """
    Get list of categories of template images.|
    ------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :categories: QStringList
            | Shows list of categories for TIG
    """
    err_code, categories = ax.LMK.iTIG_GetListOfCategories()
    ax.error_code(err_code) # Check for error

    return categories

def get_list_of_operations(category):
    """
    Get list of types of template images for the given category.|
    ------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :category: QString
            | Chosen category
    Returns:
        :operations: QStringList
            | Shows list of template image types for given category
    """
    [err_code, operations] = ax.LMK.iTIG_GetListOfOperations(category)
    ax.error_code(err_code) # Check for error

    return operations

def set_operation(category, operation, check=1):
    """
    Set a type of template image or an option.|
    ------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :category: QString
            | Name of category
        :operation: QString
            | Name of operation or option
        :check: int
            | Set or unset.
            | This parameter is only valied if this is an option.
            |   (checkbox, not a radio button)
    """
    err_code = ax.LMK.iTIG_SetOperation(category, operation, check)
    ax.error_code(err_code) # Check for error

def get_list_of_param_names():
    """
    Get a parameter name list for the given template image type.|
    ------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :parameters: QStringList
            | Show parameter names in a list
    """
    err_code, parameters = ax.LMK.iTIG_GetListOfParameterNames()
    ax.error_code(err_code) # Check for error

    return parameters

def get_param_value(parameter):
    """
    Get a certain parameter value.|
    ------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :parameter: QString
            | Name of parameter
    Returns:
        :parameter_value: float
            | Value of parameter (if bool, then 0 or 1)
    """
    err_code, parameter_value = ax.LMK.iTIG_GetParameterValue(parameter)
    ax.error_code(err_code) # Check for error

    return parameter_value

def set_param_value(parameter, parameter_value):
    """
    Set a certain parameter value.|
    ------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :parameter: QString
            | Name of parameter
        :parameter_value: float
            | Value of parameter (if bool, then 0 or 1)
    """
    err_code = ax.LMK.iTIG_SetParameterValue(parameter, parameter_value)
    ax.error_code(err_code) # Check for error

def show_dialog():
    """
    Make template image dialog visible.|
    -----------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    """
    err_code = ax.LMK.iTIG_ShowDialog()
    ax.error_code(err_code) # Check for error

def hide_dialog():
    """
    Make template image dialog invisible.|
    -------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    """
    err_code = ax.LMK.iTIG_HideDialog()
    ax.error_code(err_code) # Check for error

def create_image():
    """
    Create template image with the adjusted parameters.|
    ---------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    """
    err_code = ax.LMK.iTIG_CreateImage()
    ax.error_code(err_code) # Check for error

def delete_image():
    """
    Remove template image from the display.|
    ---------------------------------------
    Template images can only be deleted from a display. If the target is an
    evaluation image, deletion is not possible.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    """
    err_code = ax.LMK.iTIG_DeleteImage()
    ax.error_code(err_code) # Check for error

def load_image(file_name):
    """
    Load template image file to the target.|
    ---------------------------------------
    This operation is only allowed for category 'User Defined'.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :file_name: QString
            | Name of an image file.
            | Allowed file extensions:
            |   .puc, .pus, .pf, .pco, .pcf, .bmp, .png, .jpg
    """
    err_code = ax.LMK.iTIG_LoadImage(file_name)
    ax.error_code(err_code) # Check for error
