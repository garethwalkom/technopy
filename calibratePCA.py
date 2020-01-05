# -*-coding:utf-8 -*
import numpy as np
import luxpy as lx
import ScreenRgb2xyz_PCA

def calibratePCA(RGB_Input, XYZ_meas, cspace = 'lms', cieobs = '1931_2', bit_depth = 8):

    xyz = np.atleast_2d(XYZ_meas)
    rgb = np.atleast_2d(RGB_Input)

    bitsize = 2 ** bit_depth -1 # max bitsize opties
    temp = rgb < np.ones(rgb.shape) # convert to 0-bitsize range if necessary

    if not ((rgb > 1).any()):
        rgb *= bitsize

    # find black, white, all grays, pure RGB and binary rgb, others
    p0 = (rgb[:, 0] == 0) & (rgb[:, 1] == 0) & (rgb[:, 2] == 0) # black
    p255 = (rgb[:, 0] == bitsize) & (rgb[:, 1] == bitsize) & (rgb[:, 2] == bitsize) # white
    pgrays = (rgb[:, 0] == rgb[:, 1]) & (rgb[:, 0] == rgb[:, 2]) & (rgb[:, 2] == rgb[:, 1]) # grey
    prgbpure = np.zeros((rgb.shape[0], 3), dtype = np.bool) # creates a matrix of booleans
    prgbpure[:, 0] = (rgb[:, 1] == 0) & (rgb[:, 2] == 0) # red
    prgbpure[:, 1] = (rgb[:, 2] == 0) & (rgb[:, 0] == 0) # green
    prgbpure[:, 2] = (rgb[:, 0] == 0) & (rgb[:, 1] == 0) # blue

    prgbbin = np.zeros((rgb.shape[0], 3), dtype = np.bool) # creates a matrix of booleans
    prgbbin[:, 0] = (rgb[:, 0] == 0) & (rgb[:, 1] == rgb[:, 2]) # cyan
    prgbbin[:, 1] = (rgb[:, 1] == 0) & (rgb[:, 0] == rgb[:, 2]) # magenta
    prgbbin[:, 2] = (rgb[:, 2] == 0) & (rgb[:, 0] == rgb[:, 1]) # yellow

    pothers = ~ ((pgrays) & (np.sum(prgbpure, 1) > 0) & (np.sum(prgbbin, 1) > 0))

    xyz0 = xyz[p0, :].mean(axis = 0) # black, #mean should there be more than 1

    xyzw = xyz[p255, :].mean(axis = 0) # white

    XYZ = xyz - xyz0 # substract black --> flare correction

    channels = ['r', 'g', 'b']

#    # define matrix to convert xyz 2 lms
#    Mlms = lx._CMF[cieobs]['M']
#	
#    # convert xyz to lms
#    LMS = np.dot(Mlms, XYZ.T).T
    
    LMS = lx.xyz_to_lms(XYZ, cieobs = cieobs)

    # calculate tone response curves
    Cis = []
    RGB = np.zeros((rgb.shape[0], 3))
    roundrgb = np.round(rgb)
    for rgbi in range(3):
        LMSpure_ci = LMS[prgbpure[:, rgbi], rgbi]

        # normalize to a max of 1
        LMSpure_ci /= LMSpure_ci.max()
        
        # get rgbs for pure channel ci
        RGBpure_ci = rgb[prgbpure[:, rgbi], rgbi] #only take rgbi channel

        #build full rgb set for channel ci %--> lookup table for later (faster)
        RGBfull_ci = np.arange(bitsize) # is vector !
			
        # using LMS directly to calculate Tone Response Curves, Ci
        Ci = lx.cie_interp(np.vstack((RGBpure_ci, LMSpure_ci)), RGBfull_ci, kind = 'cubic') # could use cie_interp
        Ci[Ci < 0] = 0 # no negative RGB values!

        p0 = np.where(Ci == 0)# set all new 0s to the real zero value (use np.where)
        if not bool(p0):

            p0 = p0[-1]

            Ci[np.range(p0)] = 0

#        pmaxLMS = np.max(Ci).astype(np.uint8)
#        Ci[(Ci < Ci.max()) & (RGBfull_ci > pmaxLMS)] = Ci.max() # cut-off high values (corresponding to

        # calculate conversion matrixes using linearized RGB
        # linearize all rgbs using Ci
        RGB[:, rgbi] = Ci[roundrgb[:, rgbi] + 1, rgbi]
		
        Cis.append(Ci)

    Cis = np.array(Cis)
   
   ########### 
    ## M = (RGB\XYZ)'; %RGB2XYZ conversion matrix, first estimate
    M = np.linalg.lstsq(RGB, XYZ)
   
    # further optimize matrix elements of M, to get minimal colour error
#    opts = optimset('fminsearch')
#
#    opts.MaxIter = 1000
#    opts.MaxFunEvals = 1000
#    opts.TolX = 1e-9
#    opts.TolFun = 1e-9

    # create vector from matrix
    x0 = M.flatten()

    # calculate weights based on cspace
    x = lx.math.minimizebnd(rmsdE_(x0, xyz, RGB, xyz0, xyzw, pgrays, cspace), x0) # can use lx.math.minimizebnd

    # create matrix from vector
    M = np.vstack((x[:3], x[3:6], x[7:]))

    # calculate inverse conversion matrix
    N = np.linalg.inv(M)

    # create calibrationpars array
    calibrationpars = np.array([M, N, xyz0, xyzw, Ci])

    # calculate lab parameters
    XYZcalc = ScreenRgb2xyz_PCA(rgb, calibrationpars)
    labcalc = lx.colortf(XYZcalc, tf = cspace, xyzw = xyzw)
    lab = lx.colortf(xyz, tf = cspace, xyzw = xyzw)

    # calculate colour difference between measured and 'modelled' lab
    DEi = np.sqrt((lab[:, 1] - labcalc[:, 1]) **2 + (lab[:, 2] - labcalc[:, 2]) ** 2 + (lab[:, 3] - labcalc[:, 3]) **2)
    DEavg = np.mean(DEi)
    DEmedian = np.median(DEi)
    DEstd = np.std(DEi)
    DEmax = max(DEi)

    # check calibration: roundtrip mode (xyz meas->rgb =N*xyz meas ->xyz calc = M*rgb=M*inv(N)*xyz meas =xyz meas!)
    RGB2 = (N * XYZ)
    XYZcalc1 = (M * RGB2 + np.matlib.repmat(xyz0, 1, np.size(RGB2, 1)))  
    labcalc2 = lx.colortf(XYZcalc1, tf = cspace, xyzw = xyzw)

    dEi2 = np.sqrt((lab[:, 1] - labcalc2[:, 1]) ** 2 + (lab[:, 2] - labcalc2[:, 2]) ** 2 + (lab[:, 3] - labcalc2[:, 3]) ** 2)
    dE2 = np.sqrt(sum(dEi2) / len(dEi2))
    dEavg2 = np.mean(dEi2)
    dEmedian2 = np.median(dEi2)
    dEstd2 = np.std(dEi2)
    dEmax2 = max(dEi2)

    dEsummary_roundtrip = [dE2, dEavg2, dEmedian2, dEstd2, dEmax2]
		
def rmsdE_(x, XYZ, RGB, xyz0, xyzW, pgrays, cspace):

    M = np.vstack((x[:3], x[3:6], x[7:]))

    XYZcalc = (M * RGB)

    XYZcalc = (XYZcalc + xyz0)
   
    if XYZcalc < 0:
        XYZcalc = 0 # no negative XYZ
        
    luvcalc = lx.colortf(XYZcalc, tf = cspace, xyzw = xyzW)
    
    luv = lx.colortf(XYZ, tf = cspace, xyzw = xyzW)

    dEi = np.sqrt((luv[:, 1] - luvcalc[:, 1]) ** 2 + (luv[:, 2] - luvcalc[:, 2]) ** 2 + (luv[:, 3] - luvcalc[:, 3]) ** 2);

    dE = lx.math.rms(dEi)

    dEachrom = lx.math.rms(dEi[pgrays]) 
	
    dEwhite = lx.math.rms(dEi[pgrays][-1]) 

    dE = dE * dEachrom * dEwhite # %add extra weigth to the achromatic stimuli!! --> whitepoint preserving!

    return dE