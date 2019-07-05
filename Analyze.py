# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 08:57:18 2019
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
import time
import glob
import csv
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import luxpy as lx
from luxpy.toolboxes import spectro as sp
import errno

class CheckExists:

    def File(CSV_Root, MeasDate, header):
        ### Check if file and header exist already
        print ('Checking if file and header exist...')
        startCheckMeasExists = time.time()
        if os.path.isfile(CSV_Root): # If the root to the file is the file
            print ('File exists')
            readCSV = open(MeasDate + '.csv', 'r', newline='') # Open and read file
            # Check CSV using pandas dataframe to check if it already containts measurement being written
            checkCSV = pd.read_csv(MeasDate + '.csv', 'r', delimiter='\t', skiprows=1, names = header) 
            file = open(MeasDate + '.csv', 'a', newline='') # Append file
            writer = csv.DictWriter(file, fieldnames=header, delimiter='\t') # Enable dictionary to be written to file using defined headers
            header_exist = any('Meas_Date' in line for line in readCSV) # Define if header exists by searching fora value within it
            if not header_exist: # Check if header exists
                readCSV.seek(0, os.SEEK_END) # Seek whole CSV file for header
                print ('Writing header to file...\n')
                writer.writeheader() # If header does not exist, write header in file
            print ('Header in file exists')
        else: # If the file does not exist
            print ('File is missing')
            print ('Writing File...')
            file = open(MeasDate + '.csv', 'w', newline='') # Create a CSV and make it writable
            writer = csv.DictWriter(file, fieldnames=header, delimiter='\t') # Enable dictionary to be written to file using defined headers
            print ('Header is missing')
            print ('Writing header to file...')
            writer.writeheader() # If header does not exist, write header in file
            # Check CSV using pandas dataframe to check if it already containts measurement being written
            checkCSV = pd.read_csv(MeasDate + '.csv', 'r', delimiter='\t', skiprows=1, names = header)
            
        print ('Measurement exists check took: {0:.3f} seconds\n'.format(time.time() - startCheckMeasExists))
        
        return writer, file, checkCSV
    
    def Meas(checkCSV, MeasDate, MeasTarget, header):
        ## Checked by looking if unique data in measurement matches a row in CSV file
        measExists = checkCSV[checkCSV['Meas_Date'].isin([MeasDate]) & checkCSV['Meas_Target'].isin([MeasTarget]) & checkCSV['R_In'].isin([R_In]) & checkCSV['G_In'].isin([G_In]) & checkCSV['B_In'].isin([B_In])]
    
        return measExists

class Split:
    
    ### Split path name
    ## Name of the file needs to be the RGB (0-1) input of the measurement.
    ## E.g. 1-0-0
    ## This is then split accordingly and then written to a file later
    def Path(path):
        
        return path.strip('/').strip('\\').split('/')[-1].split('\\')[-1]
    
    def Meas(readFile):
        ### Split file name
        ## File name is split to get RGB Input
        MeasName = Split.Path(readFile)[:-4] # Splits the file and removes '.txt' using '[:-4]'
        R_In = '-'.join(MeasName.split('-')[:-2]) # Split file name to get R input
        G_In = '-'.join(MeasName.split('-')[1:][:-1]) # Split file name to get G input
        B_In = '-'.join(MeasName.split('-')[2:]) # Split file name to get B input
        
        return MeasName, R_In, G_In, B_In
    
class Measure:
    def SPD(device = 'jeti', Tint = 0, wait = 0.1):
        # Initializes spectrometer 'jeti' or 'oceanoptics'
        sp.init(device)
        
        spds = []
        
        time.sleep(wait)
        spd = sp.get_spd(manufacturer = device, Tint = Tint)
        spds.append(spd)
        
        if spds != []:
            spds = np.vstack((spds[0][0,:],[x[1,:] for x in spds]))
            
        return spds

class Read:
    
    def LMK(readTxt):
        ## Read measurement into pandas dataframe and name columns
        startReadFile = time.time()
        print ('Reading LMK Measurement...')
        LMK_Meas = pd.read_csv(readTxt, delimiter = '\t',
                               names=['Pix X', 'Pix Y', 'X', 'Y', 'Z'])
        print ('Measurement read in: {0:.3f} seconds\n'.format(time.time() - startReadFile))
        
        ### Get XYZ from file
        startGet_XYZ = time.time()
        print ('Getting XYZ from LMK Measurement...')
        xyzm = LMK_Meas.values
        row_no = xyzm[:,0] - xyzm[0,0] + 1  # image started at row 11
        col_no = xyzm[:,1] - xyzm[0,1] + 1  # image started at col 61
        xyzm = xyzm[:,2:]
        row_max, col_max = np.int(row_no.max()), np.int(col_no.max())
        im_meas_xyzm = xyzm.reshape((row_max, col_max, 3))
        xyz = im_meas_xyzm.reshape(np.hstack((im_meas_xyzm.shape[0]*im_meas_xyzm.shape[1],3)))
        print ('Got XYZ in: {0:.3f} seconds\n'.format(time.time() - startGet_XYZ))
        
        return xyz

class Calculate:
    
    def XYZ(xyz):
        ### Calculate Mean XYZ
        print ('Calculating XYZ ...')
        xyz_mean = np.array([[xyz[:,0].mean(), xyz[:,1].mean(), xyz[:,2].mean()]])
        xyz_SD = np.array([[xyz[:,0].std(), xyz[:,1].std(), xyz[:,2].std()]])
        
        XYZ_Mean = np.around(xyz_mean, decimals=3)
        XYZ_SD = np.around(xyz_SD, decimals=3)
        
        X_Mean = XYZ_Mean[:,0]
        X_Mean = str(X_Mean)[1:-1]
        X_SD = XYZ_SD[:,0]
        X_SD = str(X_SD)[1:-1]
        Y_Mean = XYZ_Mean[:,1]
        Y_Mean = str(Y_Mean)[1:-1]
        Y_SD = XYZ_SD[:,1]
        Y_SD = str(Y_SD)[1:-1]
        Z_Mean = XYZ_Mean[:,2]
        Z_Mean = str(Z_Mean)[1:-1]
        Z_SD = XYZ_SD[:,2]
        Z_SD = str(Z_SD)[1:-1]
        
        return xyz_mean, X_Mean, X_SD, Y_Mean, Y_SD, Z_Mean, Z_SD 
    
    def Yxy(xyz):
        ### Calculate (Y, x, y)
        print ('Calculating Y, x, y ...')
        Yxy = lx.xyz_to_Yxy(xyz)
        Yxy_mean = np.array([[Yxy[:,0].mean(), Yxy[:,1].mean(), Yxy[:,2].mean()]])
        
        Yxy_Mean = np.around(Yxy_mean, decimals=3)
        
        x = Yxy_Mean[:,1]
        x = str(x)[1:-1]
        y = Yxy_Mean[:,2]
        y = str(y)[1:-1]
        
        return x, y
    
    def Yuv(xyz):
        ### Calculate CIE 1976 (Y, u', v')
        print ('Calculating Y, u_, v_ ...')
        Yuv = lx.xyz_to_Yuv(xyz)
        Yuv_mean = np.array([[Yuv[:,0].mean(), Yuv[:,1].mean(), Yuv[:,2].mean()]])
    #    cov = np.cov(u_, v_) # Calculate covariance of u_ v_
        
        Yuv_Mean = np.around(Yuv_mean, decimals=3)
        
        u_ = Yuv_Mean[:,1]
        u_ = str(u_)[1:-1]
        v_ = Yuv_Mean[:,2]
        v_ = str(v_)[1:-1]
        
        return u_, v_
    
    def LMS(xyz):
        ### Calculate Cone Fundamentals (L, M, S)
        print ('Calculating L, M, S ...')
        LMS = lx.xyz_to_lms(xyz)
        LMS_mean = np.array([[LMS[:,0].mean(), LMS[:,1].mean(), LMS[:,2].mean()]])
        LMS_SD = np.array([[LMS[:,0].std(), LMS[:,1].std(), LMS[:,2].std()]])
        
        return LMS_mean, LMS_SD
    
    def Lab(xyz):
        ### Calculate CIE 1976 (L*, a*, b*)
        print ('Calculating L*, a*, b* ...')
        Lab = lx.xyz_to_lab(xyz)
        Lab_mean = np.array([[Lab[:,0].mean(), Lab[:,1].mean(), Lab[:,2].mean()]])
        
        Lab_Mean = np.around(Lab_mean, decimals=3)
        
        CIE_L_ = Lab_Mean[:,0]
        CIE_L_ = str(CIE_L_)[1:-1]
        CIE_a_ = Lab_Mean[:,1]
        CIE_a_ = str(CIE_a_)[1:-1]
        CIE_b_ = Lab_Mean[:,2]
        CIE_b_ = str(CIE_b_)[1:-1]
        
        return CIE_L_, CIE_a_, CIE_b_
    
    def sRGB(xyz):
        ### Calculate sRGB output
        print ('Calculating sR, sG, sB ...')
        sRGB = lx.xyz_to_srgb(xyz)
        sRGB_mean = np.array([[sRGB[:,0].mean(), sRGB[:,1].mean(), sRGB[:,2].mean()]])
        
        sRGB_Mean = np.around(sRGB_mean, decimals=3)
                    
        R_Out = sRGB_Mean[:,0]
        R_Out = str(R_Out)[1:-1]
        G_Out = sRGB_Mean[:,1]
        G_Out = str(G_Out)[1:-1]
        B_Out = sRGB_Mean[:,2]
        B_Out = str(B_Out)[1:-1]
        
        return R_Out, G_Out, B_Out
    
    def Luv(xyz):
        ### Calculate CIE 1976 (L*, u*, v*)
        print ('Calculating L*, u*, v* ...')
        Luv = lx.xyz_to_luv(xyz)
        Luv_mean = np.array([[Luv[:,0].mean(), Luv[:,1].mean(), Luv[:,2].mean()]])
        Luv_SD = np.array([[Luv[:,0].std(), Luv[:,1].std(), Luv[:,2].std()]])
        
        return Luv_mean, Luv_SD
    
    def Vrb(xyz):
        ### Calculate V, r, b [Macleod & Boyton, 1979]
        print ('Calculating V, r, b ...')
        Vrb = lx.xyz_to_Vrb_mb(xyz)
        Vrb_mean = np.array([[Vrb[:,0].mean(), Vrb[:,1].mean(), Vrb[:,2].mean()]])
        Vrb_SD = np.array([[Vrb[:,0].std(), Vrb[:,1].std(), Vrb[:,2].std()]])
        
        return Vrb_mean, Vrb_SD
        
    def Ydlep(xyz):
        ### Calculate Y, dl, ep
        print ('Calculating Y, dl, ep ...')
        Ydlep = lx.xyz_to_Ydlep(xyz_mean)
        
        return Ydlep
    
class Analyze:
    
    def SPD(spd, color='k', linestyle='--'):
        lx.SPD(spd).plot(color = color, linestyle = linestyle,
              ylabel = 'Spectral radiance (W/nm.m².sr)')
        """
        Plot Spectral Power Distribution (SPD) using Luxpy.|
        ---------------------------------------------------
        
        Args:
            :spd:
                spd(s) must be array or string
            :color:
                'k'
                Change to adjust color of line color.
            :linestyle:
                '--'
                Change to adjust style of line.
                
        Returns:
            
        """
        
    def xy(x, y, gamut=None, label='x, y', facecolors='none', color='k',
           linestyle='--', title='x, y', grid=True, **kwargs):
        """
        Plot x, y color coordinates using Luxpy.|
        ----------------------------------------
        
        Args:
            :x:
                x coordinate(s) - must be float, int, or array
            :y:
                y coordinate(s) - must be float, int, or array
            :gamut:
                None
                Anything bar 'None' will assume a gamut is going to be created.
                This expects a plot in the order of a line in the diagram e.g.
                R, G, B, R or R, Y, G, C, B, M, R. Must go back to starting
                value to complete gamut line.
            :label:
                'x, y'
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
                'x, y'
                Change to adjust title of figure.
            :grid:
                True
                Change to 'None' for no grid in diagram.
            :kwargs:
                Additional keyword arguments for use with matplotlib.pyplot
                
        Returns:
            
        """
        plt.figure()
        ax_xy = plt.axes()
        lx.plot_chromaticity_diagram_colors(256,0.3,1,lx._CIEOBS,'Yxy',{},True,ax_xy,
                                            grid,'Times New Roman',12)
        if gamut is None:
            plt.scatter(float(x), float(y), label = label, facecolors = facecolors, edgecolors = color)
        else:
            ax_xy.plot(x, y, label = label, color = color, linestyle = linestyle)
        ax_xy.set_title(title)
        ax_xy.set_xlim([-0.1, 0.8])
        ax_xy.set_ylim([-0.1, 0.9])
        ax_xy.legend()
        
    def uv(u_, v_, gamut=None, label='u_, v_', facecolors='none', color='k',
           linestyle='--', title='u_, v_', grid=True, **kwargs):
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
        plt.figure()
        ax_uv = plt.axes()
        lx.plot_chromaticity_diagram_colors(256,0.3,1,lx._CIEOBS,'Yuv',{},True,ax_uv,
                                            grid,'Times New Roman',12)
        if gamut is None:
            plt.scatter(float(u_), float(v_), label = label, facecolors = facecolors, edgecolors = color)
        else:
            ax_uv.plot(u_, v_, label = label, color = color, linestyle = linestyle)
        ax_uv.set_title(title)
        ax_uv.set_xlim([-0.1, 0.7])
        ax_uv.set_ylim([-0.1, 0.7])
        ax_uv.legend()

if __name__ == '__main__':
    # Initiate timer for whole morphing
    start = time.time()
    print ('Started script to export LMK measurements from a folder...')
    print ('Setting up parameters...')
    startSetup = time.time()
    
    ### Define root to files
    ## Define aspects of measurements to add to file.
    MeasDevice = 'LMK'
    MeasDate = '20190413'
    MeasTarget = 'Test'
    CSV_Root = MeasDate + '.csv'
    readTxts = glob.glob(MeasDevice + '/' + MeasDate + '/' + MeasTarget + '/*.txt')
    
    ### Define header of output file
    header = ['Meas_Date', 'Meas_Target', 'R_In', 'G_In', 'B_In', 'X_Mean', 'X_SD', 
              'Y_Mean', 'Y_SD', 'Z_Mean', 'Z_SD', 'x', 'y', 'u_', 'v_', 'CIE-L*',
              'CIE-a*', 'CIE-b*', 'R_Out', 'G_Out', 'B_Out']
    
    print ('Parameter setup took: {0:.3f} seconds\n'.format(time.time() - startSetup))
    
    writer, file, checkCSV = CheckExists.File(CSV_Root, MeasDate, header)
    
    ### Add measurements to file
    with file:
        for readTxt in readTxts: # For each measurement in root folder
            try:
                ### Split file name
                MeasName, R_In, G_In, B_In = Split.Meas(readTxt)
    
                ### Check if measurement exists
                print ('Checking measurement exists...')
                measExists = CheckExists.Meas(checkCSV, MeasDate, MeasTarget, header)
                if not measExists.empty: # If measurement exists in CSV file
                    print ('Measurement:', MeasName, 'exists in file')
                    print ('Next measurement:\n')
                    break # Break out of loop to next measurement
                else: # If measurement does not exist in CSV file
                    print ('Measurement:', MeasName, 'does not exist')
                    startAddMeas = time.time()
                    print ('Adding measurement:', MeasName)
                
                ### Read measurement
                with open('{}'.format(readTxt), 'r') as f:
                    pass
                
                xyz = Read.LMK(readTxt)
                
                startCalcs = time.time()
                print ('Starting Calculations...')
                xyz_mean, X_Mean, X_SD, Y_Mean, Y_SD, Z_Mean, Z_SD  = Calculate.XYZ(xyz)
                x, y = Calculate.Yxy(xyz)
                u_, v_ = Calculate.Yuv(xyz)
                CIE_L_, CIE_a_, CIE_b_ = Calculate.Lab(xyz)
                R_Out, G_Out, B_Out = Calculate.sRGB(xyz)   
                print ('Calculations finished in: {0:.3f} seconds\n'.format(time.time() - startCalcs))
                
                ### Write row using dictionary with final outputs
                writer.writerow({'Meas_Date': MeasDate, 'Meas_Target': MeasTarget, 
                                 'R_In': R_In, 'G_In' : G_In, 'B_In': B_In, 'X_Mean' 
                                 : X_Mean, 'X_SD': X_SD, 'Y_Mean': Y_Mean, 'Y_SD'
                                 : Y_SD, 'Z_Mean': Z_Mean, 'Z_SD': Z_SD, 'x'
                                 : x, 'y': y, 'u_': u_, 'v_': v_, 'CIE-L*'
                                 : CIE_L_, 'CIE-a*': CIE_a_, 'CIE-b*': CIE_b_, 
                                 'R_Out': R_Out, 'G_Out': G_Out, 'B_Out': B_Out})
                print ('Measurement:', MeasName, 'added in: {0:.3f} seconds\n'.format(time.time() - startAddMeas))
            
            ### Stop loop if error
            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise
    
    ### Finishing print statement
    print ('------------------------------')
    print ('All measurements added to file in: {0:.3f} seconds\n'.format(time.time() - start))