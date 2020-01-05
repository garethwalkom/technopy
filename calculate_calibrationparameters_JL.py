# -*-coding:utf-8 -*
from .calibratePCA import calibratePCA
import numpy as np

def calculate_calibrationparameters_JL (MGV,calibrationdate):
    cieobs_cal = 10
    cspace_cal = 'luv'
    bits_cal = MGV['device']['bits']
    print('Setting some calibration parameters in calculate_calibrationparameters_JL.m: \n cieobs = {}, cspace = {}, device_bits = {}'.format(cieobs_cal,cspace_cal,bits_cal))

    # read RGB and corresponding measured XYZ
    RGBcal = dlmread(MGV['droot']+'/CalibrationData/'+ calibrationdate+'/'+str(MGV['calibration']['ChannelCal'])+'/RGBcal.txt')
    XYZcal = dlmread(MGV['droot']+'/CalibrationData/'+calibrationdate+'/'+str(MGV['calibration']['ChannelCal'])+'/XYZcal.txt')

# cieobs = observer: 2 or 10
# XYZcal = Output (measured) XYZ values
# RGBcal = Input RGB values
# cspace_cal = LUV works well
# bits_cal = max bit depth (8-bit)
    result = calibratePCA(cieobs_cal,XYZcal,RGBcal,cspace_cal,bits_cal)

    calibrationpars = result[0]
    xyz0 = result[3]
    xyzw = result[4]
    DEavg = result[7]
    DEmedian = result[8]
    DEstd = result[9]
    DEmax = result[10]



    print('xyz0: {}'.format(xyz0))
    print('xyzw: {}'.format(xyzw))
    print('DEavg: {} DEstd: {}'.format(DEavg,DEstd))
    print('DEmedian: {}'.format(DEmedian))
    print('DEmax: {}'.format(DEmax))

    #write data to file and keep log
    dlmwrite(MGV['droot']+'/CalibrationData/CalibrationParameter/CalibrationPars'+'_'+calibrationdate+'_'+str(MGV['calibration']['ChannelCal'])+'.txt',calibrationpars)
    MGV['calibration']['parameters']=dlmread(MGV['droot']+'/CalibrationData/CalibrationParameter/CalibrationPars'+'_'+calibrationdate+'_'+str(MGV['calibration']['ChannelCal'])+'.txt')

    try :
        with open(MGV['droot']+'/CalibrationData/CalibrationLog.txt','r') as file:
            text = file.read()
            while '  ' in text:
                text = text.replace('  ',' ')
            text = text.replace(' ','\n')

        CalibrationLog = text.split('\n')
        while '' in CalibrationLog:
            CalibrationLog.remove('')

    except :
        CalibrationLog = ['']

    CalibrationLog.append(calibrationdate)
    CalibrationLog.append(str(MGV['calibration']['ChannelCal']))

    MGV['calibration']['datum'] = calibrationdate
    MGV['calibrationlog'] = CalibrationLog
    MGV['calibration']['cieobs_cal'] = cieobs_cal
    MGV['calibration']['cspace_cal'] = cspace_cal

    with open(MGV['droot']+'/CalibrationData/CalibrationLog.txt','w') as MyFile:
        MyFile.write("\n".join(MGV['calibrationlog']))



