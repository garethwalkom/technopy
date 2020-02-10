# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:37:15 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
from win32com.client import Dispatch

import activex as ax

LMK = Dispatch('lmk4.LMKAxServer')

def get_number():
    """
    Returns the number of tables in the result tab widget.|
    ------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
    Returns:
        :tables_no: int
            | Returns the number of tables
    """
    err_code, tables_no = LMK.iTableGetNumber()
    ax.error_code(err_code) # Check for error

    return tables_no

def table_get_name_and_caption(table_id=2):
    """
    Returns the name and the caption of an existing table.|
    ------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :table_id: int (default: 2)
            | Index of wished table
    Returns:
        :table_name: QStringList
            | Returns the name of the table
        :table_caption: QStringList
            | Returns the caption of the table
    """
    err_code, table_name, table_caption = LMK.iTableGetNameAndCaption(table_id)
    ax.error_code(err_code) # Check for error

    return table_name, table_caption

def get_index(table_name_or_caption='Last capture'):
    """
    Search for a table, given by name or caption.|
    ---------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :table_name_or_caption: QString (default: 'Last capture')
            | Searched name or caption of table
    Returns:
        :table_id: int (default: 2)
            | Index of table
            | -1 = not found
    """
    err_code, table_id = LMK.iTableGetIndex(table_name_or_caption)
    ax.error_code(err_code) # Check for error

    return table_id

def get_number_columns(table_id=2):
    """
    Returns the number of columns of a table.|
    -----------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :table_id: int (default: 2)
            | Index of wished table
    Returns:
        :table_number_columns: int
            | Returns the number of columns in table
    """
    err_code, table_number_columns = LMK.iTableGetNumberColumns(table_id)
    ax.error_code(err_code) # Check for error

    return table_number_columns

def get_number_lines(table_id=2):
    """
    Returns the number of lines of a table.|
    ---------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :table_id: int (default: 2)
            | Index of wished table
    Returns:
        :table_number_lines: int
            | Returns the number of lines in table
    """
    err_code, table_number_lines = LMK.iTableGetNumberLines(table_id)
    ax.error_code(err_code) # Check for error

    return table_number_lines

def get_column(table_id=2, table_column_id=0):
    """
    Returns the column header of a column of a table.|
    -------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :table_id: int (default: 2)
            | Index of wished table
        :table_column_id: int (default: 0)
            | Index of wished column
    Returns:
        :table_column_name: QString
            | Returns the name of the column
        :table_column_caption: QString
            | Returns the caption of the column
        :table_column_unit: QString
            | Returns the unit of the column
    """
    err_code, table_column_name, table_column_caption,\
        table_column_unit = LMK.iTableGetColumn(table_id, table_column_id)
    ax.error_code(err_code) # Check for error

    return table_column_name, table_column_caption, table_column_unit

def get_cell(table_id=2, table_line_id=1, table_column_id=8):
    """
    Returns the content of a cell of a table.|
    -----------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :table_id: int (default: 2)
            | Index of wished table
        :table_line_id: int (default: 1)
            | Index of wished table line
        :table_column_id: int (default: 8)
            | Index of wished table column
    Returns:
        :table_cell: QString
            | Returns the content of table cell
    """
    err_code, table_cell = LMK.iTableGetCell(table_id, table_line_id, table_column_id)
    ax.error_code(err_code) # Check for error

    return table_cell

def get_all_content(table_id=2):
    """
    Returns all cells of a table as a list.|
    ---------------------------------------
    The entries are sorted line by line.
    -----------------------------------------------------------------------
    Parameters:
        :LMK:
            | Dispatch('lmk4.LMKAxServer')
        :table_id: int (default: 2)
            | Index of wished table
    Returns:
        :table_content: QStringList
            | List with content of all cells
    """
    [err_code, table_content] = LMK.iGetAllContent(table_id)
    ax.error_code(err_code) # Check for error

    return table_content
