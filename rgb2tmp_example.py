# Copyright (C) 2018 MERIDIAN Innovation Limited. All rights reserved.
import cv2
import numpy as np
import math
import time

from statistics import stdev

# Constant defined
XCAM_WIDTH = 32
XCAM_HEIGHT = 32
VIDEO_WIDTH = XCAM_WIDTH * 6      # Defined from firmware
VIDEO_HEIGHT = XCAM_HEIGHT * 6

np.set_printoptions(threshold=np.nan)
np.set_printoptions(precision=1, suppress=True)
cap = cv2.VideoCapture(0)
cap.set(3,XCAM_WIDTH)                     # CV_CAP_PROP_FRAME_WIDTH
cap.set(4,XCAM_HEIGHT)                    # CV_CAP_PROP_FRAME_HEIGHT

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

def getTrimmedFrame(original_frame, src_frame, width, height):
    for i in range(width):
      for j in range(height):
        index, value = find_nearest(color_table,original_frame[3+6*i][3+6*j])
        src_frame[i][j] = (index - 600)/10
        
########################## Routines ##########################
# 0 <= sd_threshould <= 1 
def dead_pixel_test(sd_threshould):
  std_tempArray = [[[0] * XCAM_WIDTH for i in range(XCAM_HEIGHT)] for frame in range(2)]
  print("Dead Pixel Testing")
  print("Please cover the camera with constant room temperature object within 3 seconds")
  for count in range(2):
      # Take 2 frame
      _, frame = cap.read()
      title = str("frame" + str(count))
      cv2.imshow(title,frame)
      getTrimmedFrame(frame,std_tempArray[count],XCAM_WIDTH,XCAM_HEIGHT)

      if(count == 0):
        print("Now fully cover the camera with human hand within 3 seconds")
        time.sleep(3)
        print("Second capturing")
      else:
        print("Done")
      
  arr = np.asarray(std_tempArray)
  std_arr = np.std(arr, axis=0)
  index = np.where(std_arr < sd_threshould)
  #print(std_arr[[std < 0.5 for std in std_arr]])
  for k in range(len(index[0])):
    print("[" + str(index[1][k]) + "," + str(index[0][k]) + "]")

  cv2.waitKey(1)
  
def rgb2tmp(x,y):
    while(1):

        # Take each frame
        check, frame = cap.read()
        if not check:
          print("Open XCAM failure...")
          print("Check cap = cv2.VideoCapture(0) pointing to XCAM device")
          break
        index, value = find_nearest(color_table,frame[3+6*x][3+6*y])
        value_str = str(np.array2string(value, precision=1, separator=','))
        print("index = " + str(index) + ":" + value_str+ ", " + str((index - 600)/10))
    
        cv2.imshow('frame',frame)
    
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
################################################################################################################
# This is the testing application of using Meridian Innovation Limited 32x32 XCAM.
# 
# Settings
# - XCAM_single (YUYV output thermal image)
# - Non-adaptive color mapping mode
# - *Using defalut colorPalette0
# - SetTempDisplay(0)
#
# Functions
# 1) Dead Pixel Testing
# 2) rgb2tmp Example
# 3) YUYV2tmp Example
#
# createColorTable() : create the color table following the same algorithm on MCU firmware, it is palette dependent*
# find_nearest(array, value): find the nearest point that matching to the target RGB value, since the cap.read()
#                             convert the YUYV stream to BGR internally, the convertion makes precision issue,
#                             which is why we cannot directly mapping by comparing R,G,B value only.
#                             Also openCV does not support getting YUYV raw streaming instead of BGR.
# "frame" is the raw data captured by cap.read() which is in BGR color space in size of 192x192, 6 times enlarged.
# You can get original 32x32 pixel value by trimming the array.
################################################################################################################
while 1:
  print("-------------------------MI XCAM test-------------------------")
  color_table = np.asarray(createColorTable())
  print("1) Dead Pixel Testing")
  print("2) rgb2tmp Example")
  print("3) YUYV2tmp Example")
  print("q) Quit")
  choice = input("Input: ")
  cv2.destroyAllWindows()
  if(choice == "1"):
      dead_pixel_test(0.05)
  elif(choice == "2"):
      print("Demo will also convert target pixel from rgb to temperature value")
      print("Input the target coordination in the format of x,y where 0<= x,y < 32")
      x,y = input("Coordinate = ").split(",")
      print("Press Esc to quit")
      time.sleep(3)
      rgb2tmp(int(x),int(y))
  elif(choice == "3"):
      print("Not implemented yet")
  elif(choice == "q"):
      break
  else:
      print("Wrong input!")


cv2.destroyAllWindows()
cap.release()
