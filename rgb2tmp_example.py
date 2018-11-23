import cv2
import numpy as np
import math

np.set_printoptions(threshold=np.nan)
np.set_printoptions(precision=1, suppress=True)

def createColorTable():
  colorPalette0 =  np.array([[176,0,240],
                          [142,0,240],
                          [108,0,240],
                          [65,0,240],
                          [0,0,235],
                          [0,0,218],
                          [0,0,201],
                          [0,0,184],
                          [0,0,163],
                          [0,19,133],
                          [0,48,110],
                          [0,74,104],
                          [0,100,110],
                          [0,97,119],
                          [0,104,151],
                          [0,119,160],
                          [0,136,160],
                          [0,153,168],
                          [0,170,170],
                          [0,189,189],
                          [0,206,206],
                          [0,219,219],
                          [0,228,228],
                          [0,236,236],
                          [0,240,225],
                          [0,235,204],
                          [0,232,155],
                          [0,225,117],
                          [0,217,119],
                          [0,200,119],
                          [0,184,110],
                          [0,174,80],
                          [0,157,80],
                          [0,140,80],
                          [0,133,72],
                          [0,140,34],
                          [25,142,0],
                          [55,160,0],
                          [65,177,0],
                          [82,194,0],
                          [104,206,0],
                          [131,214,0],
                          [157,223,0],
                          [189,231,0],
                          [231,232,0],
                          [224,223,0],
                          [224,206,0],
                          [224,180,0],
                          [224,153,0],
                          [224,128,0],
                          [224,102,0],
                          [224,76,0],
                          [224,51,0],
                          [219,17,0],
                          [206,0,0],
                          [183,0,0],
                          [157,0,0],
                          [131,0,0],
                          [104,0,0],
                          [80,0,0],
                          [80,0,0]], np.int32)
  colorTable = np.zeros([1200,3], dtype=np.int32)
  
  # BGR2RGB
  colorPalette0[:,[0,2]] = colorPalette0[:,[2,0]]
  for i in range(len(colorPalette0) - 1):  # 60
    for j in range(20):
       colorTable[i*20 + j] = colorPalette0[i] + (colorPalette0[i+1]-colorPalette0[i])*j/20

  return colorTable
  
def find_nearest(array, value):
    idx = [] 
    array = np.asarray(array)
    
    for i in range(len(array)):
      idx.append(np.abs(math.sqrt((array[i][0] - value[0])**2 + (array[i][1] - value[1])**2 + (array[i][2] - value[2])**2)))#.argmin()
    idx_numpy = np.array(idx)
    targetIdx = idx_numpy.argmin()
    return targetIdx, array[targetIdx]

################################################################################################################
# This is the example of showing how to convert RGB value captured by videoCapture object to temperature value
# using Meridian Innovation Limited XCAM.
# 
# Settings
# - XCAM_single (YUYV output thermal image)
# - Non-adaptive color mapping mode
# - Using defalut colorPalette0
# - SetTempDisplay(0)
#
# createColorTable() : create the color table following the same algorithm on MCU, it is firmware dependent
# find_nearest(array, value): find the nearest point that matching to the target RGB value, since the cap.read()
#                             convert the YUYV stream to BGR internally, the convertion makes precision issue,
#                             which is why we cannot directly mapping by comparing R,G,B value only.
#                             Also openCV does not support getting YUYV raw streaming instead of BGR.
# "frame" is the raw data captured by cap.read() which is in BGR color space in size of 192x192, 6 times enlarged.
# You can get original 32x32 pixel value by trimming the array.
################################################################################################################
cap = cv2.VideoCapture(0)
cap.set(3,192)
cap.set(4,192)
color_table = np.asarray(createColorTable())

while(1):

    # Take each frame
    _, frame = cap.read()
    index, value = find_nearest(color_table,frame[0][0])
    value_str = str(np.array2string(value, precision=1, separator=','))
    print("index = " + str(index) + ":" + value_str+ ", " + str((index - 600)/10))
    
    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
