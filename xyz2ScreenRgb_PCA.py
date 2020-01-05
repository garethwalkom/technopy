# -*-coding:utf-8 -*
import numpy as np

def xyz2ScreenRgb_PCA(xyz,calibrationpars,bits):

    bitsize = 2 ^ bits -1
    M = calibrationpars[1:13]
    N = calibrationpars[14:84]
    xyz0 = calibrationpars[[0]]
    xyzw=calibrationpars[[13]]
    n1 = len(M) + len(N) + len(xyz0) + len(xyzw)
    n = len(calibrationpars) - n1
    CiLUT = calibrationpars[n1 +1 :]

    repmat = np.tile(xyz0, [len(xyz), 1])
    xyz2 = np.array(xyz)
    XYZ = xyz2 - xyz0 #flare correction

    XYZ = (XYZ + np.abs(XYZ)) / 2

    rgb = np.dot(np.transpose(N), XYZ)
    for i in range (len(rgb)):
        for j in range (len(rgb[i])):
            if rgb[i][j] < 0:
                rgb[i][j] = 0
            elif rgb[i][j] > 1:
                rgb[i][j] = 1

    Rrgb = []
    for rgbi in range (3):
        #find boundaries for each linearized R,G or B value
        a = [CiLUT[i][rgbi] for i in range (len(CiLUT))]
        b = [0] + [-i / 2 for i in np.diff(a)] + [max(a) + 0.1]
        Ru= [a[i] + b[i] for i in range (len(a))]

        #find all pixels with values within the boundaries and change the R,G
        #or B value to the non linearized dr,dg or db values (=rgb)
        c = [rgb[i][rgbi] for i in range (len(rgb))]
        p = np.digitize(c, Ru)
        Rrgb.append([i -1 for i in p])


    return Rrgb