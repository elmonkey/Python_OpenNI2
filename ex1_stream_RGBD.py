#!/usr/bin/env python
'''
Official primense openni2 and nite2 python bindings.
Uses the following libraries:
1. OpenNI-Windows-x64-2.2.0.32 <Librariy & Drivers>
2. NiTE-Windows-x64-2.0.0 <middleware>
3. primesense-2.2.0.30 <python bindings>
Library Summary: openNI2.2, NiTE2.0, and pythonbinings2.2.0.30

Created on 3Sep2014

1. Binding Installation
    a) download from https://pypi.python.org/pypi/primesense/2.2.0.30-5
       on a terminal cd to location where it was downloaded
        cd C:\downloads\primensense
        python setup.py install 
    
    or
    b) direct 
       on terminal 
        pip install primensense
    
2. Troubleshooting
    http://stackoverflow.com/questions/19962339/creating-a-usertracker-crashes-in-nite2-python-bindings
    http://stackoverflow.com/questions/24287004/crash-on-nite-initialisation-in-python-program-written-using-primesense2-2-0-30

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
from primesense import openni2, nite2




def mask_rgbd(d4d,rgb):
    """
    Overlays images and uses some blur to slightly smooth the mask
    (3L ndarray, 3L ndarray) -> 3L ndarray
    """
    mask = d4d.copy()
    #mask = cv2.GaussianBlur(mask, (5,5),0)
    idx =(mask>0)
    mask[idx] = rgb[idx]
    return mask
#mask_rgbd




## initialize openni and check
openni2.initialize()# accepts the path of the OpenNI redistribution
if (openni2.is_initialized()):
    print "openNI2 initialized"
else:
    print "openNI2 not initialized"

## initialize nite and check
nite2.initialize()
if (nite2.is_initialized()):
    print "nite2 initialized"
else:
    print "nite2 not initialized"


dev = openni2.Device.open_any()
#ut = nite2.UserTracker(dev)

## create the streams
depth_stream = dev.create_depth_stream()
rgb_stream = dev.create_color_stream()

## start the streams
depth_stream.start()
rgb_stream.start()

## synchronize the streams
dev.set_depth_color_sync_enabled(True) # synchronize the streams

## IMPORTANT: ALIGN DEPTH2RGB (depth wrapped to match rgb stream)
dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)

##help(dev.set_image_registration_mode)




## main loop
done = False
while not done:
    key = cv2.waitKey(5)
    if key == 27:
        done = True
    
    depth_frame = depth_stream.read_frame()
    depth_data  = depth_frame.get_buffer_as_uint16()
    
    rgb_frame = rgb_stream.read_frame()
    rgb_data  = rgb_frame.get_buffer_as_uint8()
    
    # convert to numpy
    depth = np.asarray(depth_data,dtype=np.uint16).reshape(240,320)
    # correct the range: directly ncasting it as unit8 causes stripes
    depth = np.uint8(depth.astype(float) *255/ 2**13-1) #depth images are 12bits
    depth = cv2.cvtColor(depth,cv2.COLOR_GRAY2RGB)
    
    rgb   = np.asarray(rgb_data,dtype=np.uint8).reshape(240,320,3)
    rgb   = cv2.cvtColor(rgb,cv2.COLOR_BGR2RGB)
    # overlay rgb over the depth stream
    rgbd  = mask_rgbd(depth,rgb)
    
    cv2.imshow('depth || rgb || rgbd', np.hstack((depth,rgb,rgbd)) )
# end while

## Release resources 
cv2.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")
print type(depth_data)
