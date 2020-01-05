# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 08:41:05 2019
@method: Kevin A.G. Smet
@author: Gareth V. Walkom (walkga04 at googlemail.com)
"""
import numpy as np
import matplotlib.pyplot as plt
import luxpy as lx

plt.close('all')

# =============================================================================
#     1. Initialize parameters for LUT.
#     2. Normalizes RGBs to max bit depth.
#     3. Seperate colors.
#     4. Check black/white for stability.
#     5. Subtract black from all values.
#     6. Convert XYZ to LMS
#     7. Calculate tone-response curves.
#     8. Get 3 values (L, M, & S) for each pure color (L = R, M = G, S = G).
#     9. Normalize to a max of 1 (e.g., not 255).
#     10. Select only the values from RGB with pure values (e.g., if red input, then get red channel).
#     11. Build full set of RGBs up to the max bit size (e.g. 255).
#     12. Use LMS to calculate tone response curves by interpolating pures with RGBs_TRC.
#     13. If TRC is less than zero, then make value 0.
#     14. Define max LMS values.
#     15. Linearize all RGBs using TRC.
#     16. Add TRC to list and convert to array.
#     17. Find approximation matrix of linearized RGBs and XYZs.
#     18. Improve approximation.
#     19. Yuv to XYZ to flare corrected XYZ to linear RGB (tone response curves) to input RGB…. Or inverse
#     20. Then test (create calibrationspars array (and below))
# =============================================================================

class LUT:
        
    def __init__(self, RGBs_In, XYZs_Meas, cspace='luv', cieobs='1931_2', bit_depth=8):
        """
        1. Initialize parameters for LUT.|
        ---------------------------------
        Parameters:
            :RGBs_In: txt file
                | RGB values inputted for characterization
            :XYZs_Meas: numpy array
                | XYZs measured from characterization
            :cspace: string (Default: 'luv')
                | Chosen color space
            :cieobs: string (Default: '1931_2')
                | Chosen CIE Observer
            :bit_depth: int (Default: 2)
                | Bit-depth of characterized display
        """
        if isinstance(RGBs_In,str):
            RGBs_In = np.loadtxt(RGBs_In, dtype = np.uint8)
            
        if isinstance(XYZs_Meas,str):
#            XYZs_Meas = np.load(XYZs_Meas)#[()]
            XYZs_Meas = np.loadtxt(XYZs_Meas, delimiter = '\t')
        
        self.RGBs_In = np.atleast_2d(RGBs_In)
        self.XYZs_Meas = np.atleast_2d(XYZs_Meas)
        self.cspace = cspace
        self.cieobs = cieobs
        self.bit_depth = bit_depth
        self.normalize_to_max_bitdepth()
        self.bRGB_K, self.bRGB_W, self.bRGB_Grays, self.bRGB_pures, self.bCMY_pures = self.seperate_color_types()
        self.XYZ_K, self.XYZ_W = self.get_mean_blacks_whites()
        self.XYZs_Corr = self.flare_correction(self.XYZs_Meas.copy())
        self.calc_TRCs()
        self.linRGBs = self.linearize_RGB(self.RGBs_In, self.TRCs, mode = 'forward')
        self.M, self.N = self.get_conversion_matrices(self.XYZs_Corr, self.linRGBs,  cspace = cspace, out = 'M,N', verbosity = 1)
        self.XYZ_calc = self.RGB_to_XYZ(self.RGBs_In)
        self.dE, self.dEi, LUV1, LUV2 = self.DErms(self.XYZ_calc, self.XYZs_Meas, self.XYZ_W, cspace = cspace, out = 'dE,dEi,LUV1,LUV2')
        
        plt.figure()
        ax = plt.axes()
        colors=['r','g','b']
        symbols=['*','+','x']
        for i in range(3):
            plt.plot(self.RGBs_TRC, self.TRCs[i, :], colors[i] + '-')
            plt.plot(self.RGBs_In[:, i, None], self.linRGBs[:, i, None], colors[i] + symbols[i])
        ax.set_title('Tone Response Curves')
        
        plt.figure()
        plt.plot(LUV1[:,1],LUV1[:,2],'bo')
        plt.plot(LUV2[:,1],LUV2[:,2],'rd')
        
        self.Yuvs = self.XYZs_to_Yuvs()
        self.Plot_Yuvs(annotate = True)
        
        print ('Improved Approximation Matrix:\n', self.M)
        print ('dE:', self.dE)
                
    def normalize_to_max_bitdepth(self):
        """
        2. Normalizes RGBs to max bit depth.|
        ------------------------------------
        """
        self.RGB_Max = 2 ** self.bit_depth -1 # Max RGB, calculated from bit depth
#        temp = self.RGBs_In < np.ones(self.RGBs_In.shape) # Convert to 0-bitsize range if necessary
        
        if not ((self.RGBs_In > 1).any()):
            self.RGBs_In *= self.RGB_Max
            

    def seperate_color_types(self):
        """
        3. Seperate colors.|
        -------------------
        Returns:
            :RGB_K: array of bools
                | Defined blacks from RGBs_In
            :RGB_W: array of bools
                | Defined whites from RGBs_In
            :RGB_Grays: array of bools
                | Defined grays from RGBs_In
            :RGB_pures: array of bools
                | Defined pure Red, Green, Blue values in RGBs_In
            :CMY_pures: array of bools
                | Defined pure Cyan, Magenta, Yellow values in RGBs_In
        """
        RGB_Max = self.RGB_Max
        RGB_K = (self.RGBs_In[:, 0] == 0) & (self.RGBs_In[:, 1] == 0) & (self.RGBs_In[:, 2] == 0) # Black RGBs
        RGB_W = (self.RGBs_In[:, 0] == RGB_Max) & (self.RGBs_In[:, 1] == RGB_Max) & (self.RGBs_In[:, 2] == RGB_Max) # White RGBs
        RGB_Grays = (self.RGBs_In[:, 0] == self.RGBs_In[:, 1]) & (self.RGBs_In[:, 0] == self.RGBs_In[:, 2]) & (self.RGBs_In[:, 2] == self.RGBs_In[:, 1]) # Gray RGBs
        
        RGB_pures = np.zeros((self.RGBs_In.shape[0], 3), dtype = np.bool) # Creates a matrix of booleans for pure RGBs
        RGB_pures[:, 0] = (self.RGBs_In[:, 1] == 0) & (self.RGBs_In[:, 2] == 0) # Red RGBs
        RGB_pures[:, 1] = (self.RGBs_In[:, 2] == 0) & (self.RGBs_In[:, 0] == 0) # Green RGBs
        RGB_pures[:, 2] = (self.RGBs_In[:, 0] == 0) & (self.RGBs_In[:, 1] == 0) # Blue RGBs
        
        CMY_pures = np.zeros((self.RGBs_In.shape[0], 3), dtype = np.bool) # Creates a matrix of booleans for pure CMYs
        CMY_pures[:, 0] = (self.RGBs_In[:, 0] == 0) & (self.RGBs_In[:, 1] == self.RGBs_In[:, 2]) # Cyan
        CMY_pures[:, 1] = (self.RGBs_In[:, 1] == 0) & (self.RGBs_In[:, 0] == self.RGBs_In[:, 2]) # Magenta
        CMY_pures[:, 2] = (self.RGBs_In[:, 2] == 0) & (self.RGBs_In[:, 0] == self.RGBs_In[:, 1]) # Yellow

#        RGB_other =~ (RGB_Grays & np.sum(RGB_pures, 1) & np.sum(CMY_pures, 1)) # Other RGBs
        
        return RGB_K, RGB_W, RGB_Grays, RGB_pures, CMY_pures
    
    def get_mean_blacks_whites(self):
        """
        4. Check black/white for stability.|
        -----------------------------------
        Might have an unstable black/white, so could need to measure the black/
        white multiple times, then take the mean(only works with black & white)
        -----------------------------------------------------------------------
        Returns:
            :XYZ_K: array
                | XYZ of Black
            :XYZ_W: array
                | XYZ of White
        """
        XYZ_K = self.XYZs_Meas[self.bRGB_K, :].mean(axis = 0) # Black XYZ
        
        XYZ_W = self.XYZs_Meas[self.bRGB_W, :].mean(axis = 0) # White XYZ
        
        return XYZ_K, XYZ_W
    
    def flare_correction(self, XYZ, mode = 'subtract'):
        """
        5. Subtract black from all values.|
        ----------------------------------
        Parameters:
            :XYZ: array
                | All XYZs
            :mode: string (Default: 'subtract')
                | 'subract' = subtracts black from XYZs to correct for flare
                | 'sum' = sums black to all XYZs to add flare correction back
        Returns:
            :XYZ + self.XYZ_K - lx._EPS:
                | Flare corrected XYZs
        """
        if mode == 'subtract':
#            return XYZ - self.XYZ_K + lx._EPS # Flare correction, calculated by subtracting the black XYZ
            return XYZ - self.XYZ_K # Flare correction, calculated by subtracting the black XYZ
        elif mode == 'sum':
            return XYZ + self.XYZ_K - lx._EPS
            
        else:
            raise Exception('flare_corrrection(): mode not recognized')
            
    def linearize_RGB(self, RGBs, TRCs, mode ='forward'):
        """
        15. Linearize all RGBs using TRC.|
        ---------------------------------
        Parameters:
            :RGBs: array
                | All RGBs
            :TRCs: array
                | All tone reponse curves (TRCs)
            :mode: string (Default: 'forward')
                | 'forward' = linearize to RGB
                | 'backward' [STILL TO BE IMPLIMETED]
        Returns:
            :linRGBs: array
                | Linearized RGBs
        """
        if mode == 'forward':
            RGBs = np.round(RGBs)
            linRGBs = np.zeros(RGBs.shape)
            for i in range(3):
                linRGBs[:, i] = TRCs[i, RGBs[:, i]]

            return linRGBs
        else:
            pass

    def calc_TRCs(self):
        """
        7. Calculate tone-response curves.|
        ----------------------------------
        Calculated for Red, Green, and Blue
        -----------------------------------------------------------------------
        """
        TRCs = []
        # 6. Convert XYZ to LMS
        LMS =  lx.xyz_to_lms(self.XYZs_Corr, cieobs = self.cieobs)
        LMS[0] = [0, 0, 0]
        for RGB in range(3):
            # 8. Get 3 values (L, M, & S) for each pure color (L = R, M = G, S = G).
            LMS_pure_TRC = LMS[self.bRGB_pures[:, RGB], :]
        
            # 9. Normalize to a max of 1 (e.g., not 255).
            LMS_pure_TRC /= LMS_pure_TRC.max()
            
            # 10. Select only the values from RGB with pure values (e.g., if red input, then get red channel).
            RGB_pure_TRC = self.RGBs_In[self.bRGB_pures[:, RGB], RGB].copy() # Only take RGB channel
            
            # 11. Build full set of RGBs up to the max bit size (e.g. 255).
            self.RGBs_TRC = np.arange(self.RGB_Max+1) # All RGBs for TRC
        			
            # 12. Use LMS to calculate tone response curves by interpolating pures with RGBs_TRC.
            TRC = lx.cie_interp(np.vstack((RGB_pure_TRC, LMS_pure_TRC[:, RGB])), self.RGBs_TRC, kind = 'cubic')
            
            # 13. If TRC is less than zero, then make value 0.
            TRC[TRC < 0] = 0 # No negative RGB values!
            TRC_K = np.where(TRC[1] == 0) # Set all new 0s to the real zero value
            if not bool(TRC_K):
        
                TRC_K = TRC_K[-1]
        
                TRC[np.range(TRC_K)] = 0
        
                # 14. Define max LMS values.
                # Find the mean of the max values from 255, then make that the max,
                # and nothing greater than 255
                LMS_max = np.max(TRC).astype(np.uint8)
                print ('LMS_max:', LMS_max)
                TRC[(TRC < TRC.max()) & (self.RGBs_TRC > LMS_max)] = TRC.max() # Cut high values (when values start to decrease)
        	 
            # 16. Add TRC to list and convert to array.
            TRCs.append(TRC[1])
        if TRCs != []:
            TRCs = np.vstack((TRCs))
        self.TRCs = TRCs.copy()
    
    def optimfcn_for_conversion_matrices(self, M, XYZs, RGBs, cspace, out):
        """
        Optimize function for conversion matrices.|
        ------------------------------------------
        Parameters:
            :M: array
                | Conversion matrix
            :XYZs: array
                | All XYZs
            :RGBs:
                | All RGBs
            :cspace: string
                | Color space
            :out: string
                | Variables to output
        Returns:
            :XYZ_calc: array
                | Calculated XYZs
            :dEi: array
                | Individual differences
            :dE: float
                | Conversion matrix difference
        """
        if M.ndim == 1:
            M = M.reshape((3,3))
        
        XYZ_calc = np.dot(M,RGBs.T).T
    
        XYZ_calc = self.flare_correction(XYZ_calc, mode = 'sum')
        
        XYZ_calc[XYZ_calc <= 0] = 0 + lx._EPS
            
        dE, dEi = self.DErms(XYZ_calc,XYZs,self.XYZ_W, cspace=cspace)
    
        dE_achrom = lx.math.rms(dEi[self.bRGB_Grays], axis=1)
#    	
        dE_white = lx.math.rms(dEi[self.bRGB_Grays][-1], axis=1) 
    
        F = dE * dE_achrom * dE_white # Add extra weight to the achromatic stimuli!! --> whitepoint preserving!
        if out == 'F':
            return F
        elif out == 'XYZ_calc,dEi,dE':
            return XYZ_calc, dEi, dE
        else:
            return eval(out)
        
    def DErms(self, XYZ1, XYZ2, XYZ_W, cspace='luv', out='dE,dEi'):
        """
        Root mean squared difference.|
        -----------------------------
        Parameters:
            :XYZ1: array
                | First XYZ to compare difference
            :XYZ2: array
                | Second XYZ to compare difference
            :XYZ_W: array
                | Max white in XYZ
            :cspace: string (Default: 'luv')
                | Designated color space
            :out: string (Default: 'dE, dEi')
                | Variables to output
        Returns:
            :dE: float
                | Difference
            :dEi: array
                | Individual differences
        """
        LUV1 = lx.colortf(XYZ1, tf = cspace, xyzw = XYZ_W)
        
        LUV2 = lx.colortf(XYZ2, tf = cspace, xyzw = XYZ_W)
    
        dEi = np.sqrt((LUV1[:, 0] - LUV2[:, 0]) ** 2 + (LUV1[:, 1] - LUV2[:, 1]) ** 2 + (LUV1[:, 2] - LUV2[:, 2]) ** 2)
    
        dE = lx.math.rms(dEi, axis=1)
        
        if out=='dE,dEi':
            return dE, dEi
        else:
            return eval(out)

    def get_conversion_matrices(self, XYZs, linRGBs, cspace, out='M,N', verbosity = 1):
        """
        17. Find approximation matrix of linearized RGBs and XYZs.|
        ----------------------------------------------------------
        Make sure that the error we get is as low as possible: XYZ * M = RGB
        -----------------------------------------------------------------------
        Parameters:
            :XYZs: array
                | All XYZs
            :linRGBs: array
                | Linearized RGBs
            :cspace: string
                | Designated color space
            :out: string
                | Variables to output
            :verbosity: int
                | 1 = show approximation matrix
        Returns: 
            :M: array
                | Conversion matrix
            :N: array
                | Inverse of conversion matrix
        """
        
        [approx_matrix, _, _, _] = np.linalg.lstsq(linRGBs, XYZs, rcond = None) # RGB2XYZ conversion matrix, first estimate
        
        if verbosity == 1:
            print ('Approximation Matrix:\n', approx_matrix, '\n')
        
        # 18. Improve approximation.
        x0 = approx_matrix.flatten()
        res = lx.math.minimizebnd(self.optimfcn_for_conversion_matrices,x0,
                                  args=(self.XYZs_Meas, linRGBs, cspace,'F')) # can use lx.math.minimizebnd
        XYZ_calc, dEi, dE = self.optimfcn_for_conversion_matrices(res['x'], self.XYZs_Meas, linRGBs, cspace,'XYZ_calc,dEi,dE') # can use lx.math.minimizebnd

        M = res['x'].reshape((3,3))

        N = np.linalg.inv(M)
        
        
        if out == 'M,N':
            return M,N
        else:
            return eval(out)
    
    def RGB_to_XYZ(self, RGBs):
        """
        RGB to XYZ.|
        -----------
        Parameters:
            :RGBs: array
                | All RGBs
        Returns:
            :XYZs: array
                | XYZs converted from RGBs
        """
        linRGBs = self.linearize_RGB(RGBs, self.TRCs, mode='forward')
        XYZs = np.dot(self.M, linRGBs.T).T
        XYZs = self.flare_correction(XYZs, mode = 'sum')
        XYZs[XYZs <= 0] = 0 + lx._EPS
        
        return XYZs

    def XYZ_to_RGB(self,XYZs):
        """
        RGBs_In to XYZs_In.|
        -------------------
        Parameters:
            :XYZs: array
                | All XYZs
        Returns:
            :self.linearize_RGB(linRGBs, self.TRCs, mode='inverse'): array
                | Deinearized RGBs from XYZ [STILL TO BE IMPLIMENTED]
        """
        XYZs = self.flare_correction(XYZs, mode = 'subtract')
        linRGBs = np.dot(self.N, XYZs.T).T
        return self.linearize_RGB(linRGBs, self.TRCs, mode='inverse')


    def test_calib_pars(self, XYZ_calc, XYZ_W):
        """    
        20. Test calibrationspars array.|
        --------------------------------
        STILL TO BE CHANGED
        """
#        calibrationpars = (approx_matrix, approx_matrix_inv, XYZ_K, XYZ_W, TRC)
        
        # Ccalculate lab parameters
#        XYZ_calc = self.RGB_to_XYZ(RGBs_In, calibrationpars)
        LAB_calc = lx.colortf(XYZ_calc, tf = self.cspace, xyzw = XYZ_W)
        LAB = lx.colortf(self.XYZs_Meas, tf = self.cspace, xyzw = XYZ_W)
        
        # Calculate colour difference between measured and 'modeled' lab
        DEi = np.sqrt((LAB[:, 0] - LAB_calc[:, 0]) **2 + (LAB[:, 1] - LAB_calc[:, 1]) ** 2 + (LAB[:, 2] - LAB_calc[:, 2]) **2)
        DEavg = np.mean(DEi)
        DEmedian = np.median(DEi)
        DEstd = np.std(DEi)
        DEmax = max(DEi)
        
        return  LAB, DEavg, DEmedian, DEstd, DEmax
    
    def check_calibration(self, approx_matrix, approx_matrix_inv, XYZs_Corr, XYZ_K, XYZ_W, LAB):
        """
        Check calibration.|
        ------------------
        STILL TO BE CHANGED
        """
        
        # Check calibration: roundtrip mode (XYZs meas->rgb =N*XYZs meas ->XYZs calc = M*rgb=M*inv(N)*XYZs meas =XYZs meas!)
        RGB_check = (approx_matrix_inv * XYZs_Corr)
        XYZ_calc_check = (approx_matrix * RGB_check + np.matlib.repmat(XYZ_K, 1, np.size(RGB_check, 1)))  
        LAB_calc_check = lx.colortf(XYZ_calc_check, tf = self.cspace, xyzw = XYZ_W)
        
        dEi2 = np.sqrt((LAB[:, 0] - LAB_calc_check[:, 0]) ** 2 + (LAB[:, 1] - LAB_calc_check[:, 1]) ** 2 + (LAB[:, 2] - LAB_calc_check[:, 2]) ** 2)
        dE2 = np.sqrt(sum(dEi2) / len(dEi2))
        dEavg2 = np.mean(dEi2)
        dEmedian2 = np.median(dEi2)
        dEstd2 = np.std(dEi2)
        dEmax2 = max(dEi2)
        
        dE_check_summary = [dE2, dEavg2, dEmedian2, dEstd2, dEmax2]
        
        return dE_check_summary
    
    def XYZs_to_Yuvs(self):
        
        Yuvs = []
        
        for XYZ in self.XYZs_Meas:
            Yuv = lx.xyz_to_Yuv(XYZ)
            Yuvs.append(Yuv)
        Yuvs = np.vstack((Yuvs))
        
        return Yuvs
    
    def Plot_Yuvs(self, annotate = True, gamut = None, label = "u', v'",
                  facecolors = 'none', color = 'k', linestyle = '--',
                  title = "u', v'", grid = True):
        
        plt.figure()
        ax_uv = plt.axes()
        lx.plot_chromaticity_diagram_colors(256,0.3,1,lx._CIEOBS,'Yuv',{},True,ax_uv,
                                            grid,'Times New Roman',12)
        if gamut is None:
            for (RGB, u, v) in zip(self.RGBs_In[1:], self.Yuvs[1:,1], self.Yuvs[1:,2]):
                plt.scatter(float(u), float(v), label = label, facecolors = facecolors, edgecolors = color)
                if annotate is True:
                    plt.annotate(RGB, (u, v))
        else:
            for Yuv in self.Yuvs:
                ax_uv.plot(Yuv[1], Yuv[2], label = label, color = color, linestyle = linestyle)
#        ax_uv.set_title(title)
        ax_uv.set_xlim([-0.1, 0.7])
        ax_uv.set_ylim([-0.1, 0.7])
        
if __name__ == '__main__':
    
#    LUT = LUT('list.rgb', 'LMK_FactorOne.npy', cspace='luv', cieobs='1931_2', bit_depth=8)
    LUT = LUT('RGBcal.txt', 'GW_2019-09-13.txt', cspace='luv', cieobs='1931_2', bit_depth=8)
#    XYZs_In = LUT.RGB_to_XYZ()
#    LAB, DEavg, DEmedian, DEstd, DEmax = LUT.test_calib_pars(XYZ_calc, XYZ_W)
#    dE_check_summary = LUT.check_calibration(approx_matrix, approx_matrix_inv, XYZs_Corr, XYZ_K, XYZ_W, LAB)