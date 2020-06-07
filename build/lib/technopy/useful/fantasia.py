# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:26:09 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

What a mess, needs to be adjusted.

"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import luxpy as lx
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import technoteam.evaluation as eva


def y_diff(max_ys, xyzs):
    """
    [ADD THIS]

    Parameters
    ----------
    max_ys : TYPE
        DESCRIPTION.
    xyzs : TYPE
        DESCRIPTION.

    Returns
    -------
    diff : TYPE
        DESCRIPTION.
    mean : TYPE
        DESCRIPTION.

    """

    diff = []

    for index, _ in enumerate(xyzs):
        diff.append(100 - (100 * float(xyzs[index, 1]) / float(max_ys[index
                                                                      , 0])))
    diff = np.vstack(diff)
    mean = diff.mean()

    return diff, mean

def xyz_to_yuv(xyzs):
    """
    [ADD THIS]

    Parameters
    ----------
    xyzs : TYPE
        DESCRIPTION.

    Returns
    -------
    u_v_ : TYPE
        DESCRIPTION.

    """

    yuv = lx.xyz_to_Yuv(xyzs)

    return yuv

def xyz_to_space(input_type='RGB', R=None, G=None, B=None, W=None,
                 file='GW_2019-09-13.txt', space='uv'):
    """
    [ADD THIS]

    Parameters
    ----------
    input_type : TYPE, optional
        DESCRIPTION. The default is 'RGB'.
    R : TYPE, optional
        DESCRIPTION. The default is None.
    G : TYPE, optional
        DESCRIPTION. The default is None.
    B : TYPE, optional
        DESCRIPTION. The default is None.
    W : TYPE, optional
        DESCRIPTION. The default is None.
    file : TYPE, optional
        DESCRIPTION. The default is 'GW_2019-09-13.txt'.
    space : TYPE, optional
        DESCRIPTION. The default is 'uv'.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

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
    """
    [ADD THIS]

    Parameters
    ----------
    input_type : TYPE, optional
        DESCRIPTION. The default is 'RGB'.
    count : TYPE, optional
        DESCRIPTION. The default is None.
    output : TYPE, optional
        DESCRIPTION. The default is None.
    R : TYPE, optional
        DESCRIPTION. The default is None.
    G : TYPE, optional
        DESCRIPTION. The default is None.
    B : TYPE, optional
        DESCRIPTION. The default is None.
    C : TYPE, optional
        DESCRIPTION. The default is None.
    M : TYPE, optional
        DESCRIPTION. The default is None.
    Y : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    u_out : TYPE
        DESCRIPTION.
    v_out : TYPE
        DESCRIPTION.

    """

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
    """
    [ADD THIS]

    Parameters
    ----------
    input_type : TYPE, optional
        DESCRIPTION. The default is 'file'.
    space : TYPE, optional
        DESCRIPTION. The default is 'uv'.
    count : TYPE, optional
        DESCRIPTION. The default is None.
    output : TYPE, optional
        DESCRIPTION. The default is None.
    new : TYPE, optional
        DESCRIPTION. The default is True.
    color : TYPE, optional
        DESCRIPTION. The default is 'k'.
    label : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """

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
