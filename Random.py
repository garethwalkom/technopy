# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 11:09:24 2019
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import luxpy as lx
from skimage.draw import circle
from skimage.color import rgb2gray
from skimage import feature
from scipy import ndimage as ndi
from skimage.filters import roberts, sobel, sobel_h, sobel_v, scharr, scharr_h, scharr_v, prewitt, prewitt_v, prewitt_h

import Gamuts as GAM

def load(file = 'XYZGray255.txt'):

    LMK_TXT = pd.read_csv(file, sep = '\t', header = None)  

    XYZs = LMK_TXT.values
    
    rows = XYZs[:, 0] - XYZs[0, 0] + 1
    cols = XYZs[:, 1] - XYZs[0, 1] + 1
    XYZs = XYZs[:, 2:]
    
    total_rows, total_cols = np.int(rows.max()), np.int(cols.max())
    
    output = XYZs.reshape((total_rows, total_cols, 3))
    
    return output

def dE_Yuv_LMK_Image(color = 'Red', intensity = '255',
                     plot_originals = False,
                     plot_shape = False,
                     plot_uv = True):
    
#    plt.close('all')
    
    root = 'E:/Measurements/2019-09-13/'
        
    New_XYZs = np.loadtxt('Cono_XYZs.csv', delimiter = ',')
    Yuvs_new_all = lx.xyz_to_Yuv(New_XYZs)
    
    RGBs_In = np.loadtxt('list.rgb', dtype = np.uint8)
    RGBs_all = RGBs_In[1:14]
    
    Old_XYZs = np.load('LMK_FactorOne.npy')
    Yuvs_old_all = lx.xyz_to_Yuv(Old_XYZs)
    
    file = 'XYZ' + color + intensity + '.txt'
    if color == 'Gray':
        Yuvs_old = Yuvs_old_all[1:14]
        Yuv_old = Yuvs_old_all[[13]]
        Yuvs_new = Yuvs_new_all[1:14]
        Yuv_new = Yuvs_new_all[[13]]
        threshold = 0.2
        Yuv_threshold = 0.6
    elif color == 'Red':
        Yuvs_old = Yuvs_old_all[14:27]
        Yuv_old = Yuvs_old_all[[26]]
        Yuvs_new = Yuvs_new_all[14:27]
        Yuv_new = Yuvs_new_all[[25]]
        threshold = 0.4
        Yuv_threshold = 0.6
    elif color == 'Green':
        Yuvs_old = Yuvs_old_all[27:40]
        Yuv_old = Yuvs_old_all[[39]]
        Yuvs_new = Yuvs_new_all[27:40]
        Yuv_new = Yuvs_new_all[[26]]
        threshold = 0.4
        Yuv_threshold = 0.6
    elif color == 'Blue':
        Yuvs_old = Yuvs_old_all[40:53]
        Yuv_old = Yuvs_old_all[[52]]
        Yuvs_new = Yuvs_new_all[40:53]
        Yuv_new = Yuvs_new_all[[26]]
        threshold = 0.08
        Yuv_threshold = 0.8
    elif color == 'Cyan':
        Yuvs_old = Yuvs_old_all[68:76]
        Yuv_old = Yuvs_old_all[[75]]
        Yuvs_new = Yuvs_new_all[68:76]
        Yuv_new = Yuvs_new_all[[26]]
        threshold = 0.4
        Yuv_threshold = 0.6
    elif color == 'Magenta':
        Yuvs_old = Yuvs_old_all[60:68]
        Yuv_old = Yuvs_old_all[[67]]
        Yuvs_new = Yuvs_new_all[60:68]
        Yuv_new = Yuvs_new_all[[26]]
        threshold = 0.4
        Yuv_threshold = 0.6
    elif color == 'Yellow':
        Yuvs_old = Yuvs_old_all[76:84]
        Yuv_old = Yuvs_old_all[[83]]
        Yuvs_new = Yuvs_new_all[76:84]
        Yuv_new = Yuvs_new_all[[26]]
        threshold = 0.4
        Yuv_threshold = 0.6
    
    XYZ_Meas = load(root + file)
    print ('NaN exists = ', np.isnan(XYZ_Meas).any())
    
    original_image = XYZ_Meas.copy()
    original_image = original_image / np.nanmean(original_image)
    r, c, d = original_image.shape
    
    if plot_originals is True:
        fig = plt.figure()
        fig.suptitle('RGB: ' + color + ' ' + intensity)
    
        ax1 = fig.add_subplot(131)
        ax1.imshow(original_image)
        ax1.title.set_text('Divided by Original Mean')
    
    threshold_image = original_image.copy()
    threshold_image[threshold_image < threshold] = np.nan
    
    if plot_originals is True:
        ax2 = fig.add_subplot(132)
        ax2.imshow(threshold_image)
        ax2.title.set_text('Subtracted threshold of: ' + '{:.2f}'.format(threshold))
        
    grayscale = rgb2gray(original_image)
    grayscale[grayscale > threshold] = 255
    grayscale[grayscale <= threshold] = 0
    black_padding = np.zeros((50, c))
    gray_img = np.row_stack((black_padding, grayscale))
    
    if plot_originals is True:
        ax3 = fig.add_subplot(133)
        ax3.imshow(gray_img, cmap = plt.get_cmap('gray'), vmin = 0, vmax = 1)
        ax3.title.set_text('Grayscale w/ threshold of: ' + '{:.2f}'.format(threshold))
    
    radius = 100
#    C_rr, C_cc = rectangle(((r // 2) - (radius // 2), (c // 2) - (radius // 2)), extent = (radius, radius), shape = (r, c))
#    L_rr, L_cc = rectangle(((r // 2) - (radius // 2), (c // 4) - (radius // 2)), extent = (radius, radius), shape = (r, c))
#    R_rr, R_cc = rectangle(((r // 2) - (radius // 2), (c // 1) - (radius * 2)), extent = (radius, radius), shape = (r, c))
#    TC_rr, TC_cc = rectangle(((r // 2) - (radius // 2), (c // 2) - (radius // 2)), extent = (radius, radius), shape = (r, c))
#    TL_rr, TL_cc = rectangle(((r // 2) - (radius // 2), (c // 2) - (radius // 2)), extent = (radius, radius), shape = (r, c))
#    TR_rr, TR_cc = rectangle(((r // 2) - (radius // 2), (c // 2) - (radius // 2)), extent = (radius, radius), shape = (r, c))
#    BC_rr, BC_cc = rectangle(((r // 2) - (radius // 2), (c // 2) - (radius // 2)), extent = (radius, radius), shape = (r, c))
#    BL_rr, BL_cc = rectangle(((r // 2) - (radius // 2), (c // 2) - (radius // 2)), extent = (radius, radius), shape = (r, c))
#    BR_rr, BR_cc = rectangle(((r // 2) - (radius // 2), (c // 2) - (radius // 2)), extent = (radius, radius), shape = (r, c))
    numbers = {'One': [], 'Two': [], 'Three': [], 'Four': [], 'Five': [], 'Six': [], 'Seven': [], 'Eight': []}
    
    for i, number in enumerate(numbers):
        numbers[number].append(circle(r // 2, c // 2, radius * (i + 1), original_image.shape))
    
    def shape(rows, cols, shape_name, plot = False, XYZ_Meas = XYZ_Meas):
        
        if plot is True:
            fig = plt.figure()
        
        Yuv_image = lx.xyz_to_Yuv(XYZ_Meas)
        Yuv_image_show = Yuv_image / np.nanmean(Yuv_image)
        
        if plot is True:
            ax4 = fig.add_subplot(131)
            ax4.imshow(Yuv_image_show)
            ax4.title.set_text('Converted to Yuv')
        
        Yuv_threshold_image = Yuv_image.copy()
        Yuv_threshold_image[Yuv_threshold_image[..., 0] < Yuv_threshold] = np.nan
        Yuv_threshold_image_show = Yuv_image_show.copy()
        Yuv_threshold_image_show[Yuv_threshold_image_show[..., 0] < Yuv_threshold] = np.nan
        
        if plot is True:
            ax5 = fig.add_subplot(132)
            ax5.imshow(Yuv_threshold_image_show)
            ax5.title.set_text('Subtracted threshold of: ' + '{:.2f}'.format(Yuv_threshold))
        
        whole_display = np.atleast_2d([np.nanmean(Yuv_threshold_image[:, :, i]) for i in range(3)])
        shape = np.atleast_2d([np.mean(Yuv_image[rows, cols, i]) for i in range(3)])
        
        Yuv_image_show[rows, cols, 1] = 1
        
#        dE_whole_display = np.nansum(((Yuv_image_show - whole_display)[..., 1:] ** 2), axis = 2) ** 0.5
        
        dE = np.nansum(((Yuv_image - shape)[..., 1:] ** 2), axis = 2) ** 0.5
        dE_show = np.nansum(((Yuv_image_show - shape)[..., 1:] ** 2), axis = 2) ** 0.5
        
        dE_shape = np.nansum(((whole_display - shape)[..., 1:] ** 2), axis = 1) ** 0.5
        print ('Shape', shape_name, 'dE:', str(dE_shape)[1:-1])
        
        if plot is True:      
            ax6 = fig.add_subplot(133)
            ax6.imshow(dE_show)
            ax6.title.set_text('dE: ' + str(dE_shape)[1:-1])
            
            ax6.title.set_text('Shape: ' + str(shape_name) + ' of RGB: ' + color + ' ' + intensity)
        
        return whole_display, shape
    
    shapes_out = []
        
    for i, number in enumerate(numbers):
        shape_rr = numbers[number][0][0]
        shape_cc = numbers[number][0][1]
        whole_display, shape_out = shape(shape_rr, shape_cc, shape_name = i + 1, plot = plot_shape)
        shapes_out.append(shape_out)
    
    if plot_uv is True:
        fig = plt.figure()
#        GAM.New.OpenVR_Left(new = False, color = 'r')
#        GAM.Output.OpenVR_Cono(new = False, color = 'm')
#        GAM.ColorSpace.AdobeRGB(new = False, color = 'g')
#        GAM.ColorSpace.DCI_P3(new = False, color = 'b')
        
        ax7 = fig.add_subplot(111)
        for (RGB, u, v) in zip(RGBs_all, Yuvs_old[:, 1], Yuvs_old[:, 2]):
            lx.plot_color_data(float(u), float(v), formatstr = 'kd')
            ax7.annotate(RGB, (u, v))
            
        for (RGB, u, v) in zip(RGBs_all, Yuvs_new[:, 1], Yuvs_new[:, 2]):
            lx.plot_color_data(float(u), float(v), formatstr = 'bo')
            ax7.annotate(RGB, (u, v))
        
        lx.plot_color_data(Yuv_old[:, 1], Yuv_old[:, 2], formatstr = 'rd')
        ax7.annotate('~Old Lens', (Yuv_old[:, 1], Yuv_old[:, 2]))
        
        lx.plot_color_data(Yuv_new[:, 1], Yuv_new[:, 2], formatstr = 'ro')
        ax7.annotate('~Last Meas', (Yuv_new[:, 1], Yuv_new[:, 2]))
        
        lx.plot_color_data(whole_display[:, 1], whole_display[:, 2], formatstr = 'go')
        ax7.annotate('Whole Display', (whole_display[:, 1], whole_display[:, 2]))
    
        def plot_shape(shape, shape_name):
        
            lx.plot_color_data(shape[:, 1], shape[:, 2], formatstr = 'yo')
            ax7.annotate('Shape:' + str(shape_name), (shape[:, 1], shape[:, 2]))
            
        for i, shape_out in enumerate(shapes_out):
            plot_shape(shape_out, i + 1)
        
        ax7.title.set_text('Yuv of areas in RGB: ' + color + ' ' + intensity)
        
def get_object_corners(gray_img):
    
#    img = gray_img.copy()
#    
#    blur = cv2.GaussianBlur(img,(3,3),0)
#    
#    corners = cv2.goodFeaturesToTrack(blur.astype('float32'),
#                                      maxCorners = 4, qualityLevel = 0.1,
#                                      minDistance = 1400)
#    corners = np.int0(corners)
#    
#    for i in corners: 
#        x, y = i.ravel() 
#        cv2.circle(blur, (x, y), 100, 0.1, 10)
#        
#    plt.figure()
#    plt.imshow(blur)
    
    image = gray_img.copy()
    
    indices = list(np.where(image != [0]))
    
    merged_list = [(indices[0][i], indices[1][i]) for i in range(0, len(indices[0]))]
    
    stacked = np.vstack(merged_list)
    
    stacked_df = pd.DataFrame(stacked)
    stacked_df[2] = stacked_df[0] + stacked_df[1]
    
    min_id = stacked_df[2].idxmin()
    stacked_df.loc[[min_id]]
    
    min_y = np.int64(stacked_df.loc[[min_id]][0])
    min_y = str(min_y)[1:-1]
    min_y = np.int64(min_y)
    
    min_x = np.int64(stacked_df.loc[[min_id]][1])
    min_x = str(min_x)[1:-1]
    min_x = np.int64(min_x)
    
    max_id = stacked_df[2].idxmax()
    stacked_df.loc[[max_id]]
    
    max_y = np.int64(stacked_df.loc[[max_id]][0])
    max_y = str(max_y)[1:-1]
    max_y = np.int64(max_y)
    
    max_x = np.int64(stacked_df.loc[[max_id]][1])
    max_x = str(max_x)[1:-1]
    max_x = np.int64(max_x)
    
    y_calc = stacked_df.loc[stacked_df[1] == max_x].min()[0]
    x_calc = stacked_df.loc[stacked_df[0] == max_y].min()[1]
    min_x = max(min_x, x_calc)
    min_y = max(min_y, y_calc)
    
    # Top left
    cv2.circle(image, (min_x, min_y), 20, 0, 7)
    # Bottom right
    cv2.circle(image, (max_x, max_y), 20, 0, 7)
    # Bottom left
    cv2.circle(image, (min_x, max_y), 20, 0, 7)
    # Top right
    cv2.circle(image, (max_x, min_y), 20, 0, 7)    
    
    cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 0, 0), 5)
    
    plt.figure()
    plt.imshow(image)
    
        
def edge_detection(image, r, c):
    
    fig = plt.figure()
    fig.suptitle('Edge Detection')
    
    grayscale = rgb2gray(image)
    
    ax1 = fig.add_subplot(2, 5, 1)
    ax1.imshow(grayscale)
    ax1.title.set_text('Grayscale Image')
    
    sigma = 1
    
    edge_canny = feature.canny(grayscale, sigma = sigma)
    
    ax2 = fig.add_subplot(2, 5, 2)
    ax2.imshow(edge_canny)
    ax2.title.set_text('Canny Edge')
    
    filter_gaussian = ndi.gaussian_filter(grayscale, 4)
    
    ax3 = fig.add_subplot(2, 5, 3)
    ax3.imshow(filter_gaussian)
    ax3.title.set_text('Gaussian Filter')
    
    edge_roberts = roberts(grayscale)
    
    ax4 = fig.add_subplot(2, 5, 4)
    ax4.imshow(edge_roberts)
    ax4.title.set_text('Roberts Edge')
    
    edge_sobel = sobel(grayscale)
    
    ax5 = fig.add_subplot(2, 5, 5)
    ax5.imshow(edge_sobel)
    ax5.title.set_text('Sobel Edge')
    
    edge_scharr = scharr(grayscale)
    
    ax6 = fig.add_subplot(2, 5, 6)
    ax6.imshow(edge_scharr)
    ax6.title.set_text('Scharr Edge')
    
    edge_prewitt = prewitt(grayscale)
    
    ax7 = fig.add_subplot(2, 5, 7)
    ax7.imshow(edge_prewitt)
    ax7.title.set_text('Prewitt Edge')
    
    def angle(dx, dy):
        return np.mod(np.arctan2(dy, dx), np.pi)
    
    true_angle = angle(c, r)
    
    def diff_angle(angle_1, angle_2):
        return np.minimum(np.pi - np.abs(angle_1 - angle_2), np.abs(angle_1 - angle_2))
    
    angle_sobel = angle(sobel_h(grayscale), sobel_v(grayscale))
    diff_sobel = diff_angle(true_angle, angle_sobel)
    
    ax8 = fig.add_subplot(2, 5, 8)
    ax8.imshow(diff_sobel)
    ax8.title.set_text('Sobel Error')
    
    angle_scharr = angle(scharr_h(grayscale), scharr_v(grayscale))
    diff_scharr = diff_angle(true_angle, angle_scharr)
    
    ax9 = fig.add_subplot(2, 5, 9)
    ax9.imshow(diff_scharr)
    ax9.title.set_text('Scharr Error')
    
    angle_prewitt = angle(prewitt_h(grayscale), prewitt_v(grayscale))
    diff_prewitt = diff_angle(true_angle, angle_prewitt)
    
    ax10 = fig.add_subplot(2, 5, 10)
    ax10.imshow(diff_prewitt)
    ax10.title.set_text('Prewitt Error')
    

class Plot3D():
    
    def __init__(self, file = 'Oculus3D.txt', dtype = 'float64', delim = '\t'):
    
        self.data = Open.TXT(file = file, dtype = dtype, delimiter = delim)
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        
        self.plot()

    def plot(self):
    
        self.ax.plot_trisurf(self.data[:,0], self.data[:,1], self.data[:,2], cmap='plasma')
        
        return self.data
    
    def animate(self, i):
        
        # Elavation angle: -180 deg to 180 deg
        self.ax.view_init(elev=(i-45)*4, azim=10)
        
        return self.fig

class Open():
    
    def TXT(file = 'list.rgb', dtype = 'uint8', delimiter = None, skiprows = 0, encoding = "utf-16"):
        
        TXT = np.loadtxt(fname = file, dtype = dtype, delimiter = delimiter, skiprows = skiprows, encoding = encoding)
        
        return TXT
    
    def TXT_LMK(self, root = '/Luminance_Camera/',
                filename  = 'Cornell_Box_Color_Image_XYZ_List.txt',
                first_row = 11, first_col = 61):
        
        first_rowscols = [first_row, first_col]
    
        LMK_TXT = pd.read_csv(root + filename, sep = '\t', skiprows = 2, header = None)  
        
        XYZs = LMK_TXT.values
        
        rows = XYZs[:, 0] - XYZs[0, 0] + 1  # image started at row 11
        cols = XYZs[:, 1] - XYZs[0, 1] + 1  # image started at col 61
        XYZs = XYZs[:, 2:]
        
        total_rows, total_cols = np.int(rows.max()), np.int(cols.max())
        
        output = XYZs.reshape((total_rows, total_cols, 3))
        
        return output, first_rowscols

class Image():
    
    def Create(self, height = 181, width = 361):
        
        image = np.zeros([height, width, 3], dtype = np.uint8)
        
        return image
    
    def Fill(self, image, first_row = 0, last_row = 90, first_col = 0, last_col = 361, color = 255):
        
        image[first_row:last_row, first_col, last_col].fill(color)
        
    def Save(self, image, save_name = 'uv_map'):
        
        plt.imsave(save_name, image)
        
    def Show(self, image):
        
        plt.imshow(image)
        
    def extra_lum(self, image, log = 2):
    
        d3 = lambda x: np.dstack((x, x, x))
        Llog = np.log10(image[:, :, 1, None]) # log10 of luminance image
        imagel = image.copy()
        image0 = image.copy()
        logL_mask = d3((Llog > log)[:, :, 0])
        imagel[logL_mask] = np.nan
        image0[logL_mask] = np.finfo('float').eps
        fig = plt.figure()
        ax1 = fig.add_subplot(121)
        ax1.imshow(np.log10(image[:, :, 1]))
        ax2 = fig.add_subplot(122)
        cax2 = ax2.imshow(np.log10(imagel[:, :, 1]))
        image[logL_mask] = np.nan 
        cbar = plt.colorbar(cax2)
        cbar.set_label('log10(L (cd/m²))')
        
        return image