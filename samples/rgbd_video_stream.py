#!/usr/bin/env python
'''
Created on 19Jun2015

Stream rgb and depth images side by side using opencv-python (cv2)

Requires the following libraries:
1. OpenNI-Linux-<Platform>-2.2 <Library and driver>
2. primesense-2.2.0.30 <python bindings>
3. Python 2.7+
4. OpenCV 2.4.X

Current features:
1. Convert primensense oni -> numpy
2. Stream and display depth
    press esc to exit
3. Sync and registered depth & rgb streams

NOTE: 
1. On device streams:  IR and RGB streams do not work together
   Depth & IR  = OK
   Depth & RGB = OK
   RGB & IR    = NOT OK
@author: Carlos Torres <carlitos408@gmail.com>
'''

import numpy as np
import cv2
from primesense import openni2#, nite2
from primesense import _openni2 as c_api


## Path of the OpenNI redistribution OpenNI2.so or OpenNI2.dll
# Windows
#dist = 'C:\Program Files\OpenNI2\Redist\OpenNI2.dll'
# Linux
dist = '/home/carlos/Install/kinect/OpenNI2-Linux-<platform>-2.2/Redist/'

## initialize openni and check
openni2.initialize(dist) #
if (openni2.is_initialized()):
    print "openNI2 initialized"
else:
    print "openNI2 not initialized"

## Register the device
dev = openni2.Device.open_any()

## Create the streams stream
rgb_stream = dev.create_color_stream()
depth_stream = dev.create_depth_stream()

## Configure the depth_stream -- changes automatically based on bus speed
print 'Get b4 video mode', depth_stream.get_video_mode() # Checks depth video configuration
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=320, resolutionY=240, fps=30))

## Start the streams
rgb_stream.start()
depth_stream.start()

## Synchronize the streams
dev.set_depth_color_sync_enabled(True) # synchronize the streams

## IMPORTANT: ALIGN DEPTH2RGB (depth wrapped to match rgb stream)
dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)

## Use 'help' to get more info
# help(dev.set_image_registration_mode)


def get_rgb():
    """
    Returns numpy 3L ndarray to represent the rgb image.
    """
    bgr   = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(240,320,3)
    rgb   = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    return rgb    
#get_rgb


def get_depth():
    """
    Returns numpy ndarrays representing the raw and ranged depth images.
    Outputs:
        dmap:= distancemap in mm, 1L ndarray, dtype=uint16, min=0, max=2**12-1
        d4d := depth for dislay, 3L ndarray, dtype=uint8, min=0, max=255    
    Note1: 
        fromstring is faster than asarray or frombuffer
    Note2:     
        .reshape(120,160) #smaller image for faster response 
                OMAP/ARM default video configuration
        .reshape(240,320) # Used to MATCH RGB Image (OMAP/ARM)
                Requires .set_video_mode
    """
    dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(240,320)  # Works & It's FAST
    d4d = np.uint8(depth.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
    return dmap, d4d
#get_depth


## main loop
done = False
while not done:
    key = cv2.waitKey(1)
    ## Read keystrokes
    if (key&255) == 27:
        print "\tESC key detected!"
        done = True
    #if
    
    ## Streams
    #RGB
    rgb = get_rgb()
    
    #DEPTH
    _,d4d = get_depth()


    ## Display the stream syde-by-side
    cv2.imshow('depth || rgb', np.hstack((d4d,rgb)) )
# end while

## Release resources 
cv2.destroyAllWindows()
rgb_stream.stop()
depth_stream.stop()
openni2.unload()
print ("Terminated")
