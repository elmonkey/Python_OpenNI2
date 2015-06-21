# OpenNI2 Python

Installation instructions and sample using the official Python wrappers for OpenNI2 and OpenCV

* Tested on 
    + OMAP4 (ARM) PandaBoard ES running Ubuntu 12.04, Python 2.7.3, OpenNI2.2, and OpenCV.2.4.10
    + Linux Ubuntu 14.04 x64
    + Windows 7 x64

## Dependencies (Windows use wheels)

* OpenNI

`sudo apt-get install libudev-dev libusb-1.0.0-dev`

`sudo apt-get install gcc-multilib git-core build-essential`

`sudo apt-get install doxygen graphviz default-jdk freeglut3-dev`


* Python Environment

`sudo apt-get -y install python-dev python-numpy `

`sudo apt-get -y install python-scipy python-setuptools`

`sudo apt-get -y install ipython python-pip`

`sudo apt-get -y install libboost-python-dev`

Compile and Install OpenNI2. Open a terminal (ctrl+alt+t). 
NOTE: root and ~ are used to represent home/yourname/


## OpenNI2 Windows 7 x64

OpenNI2. Download msi installer from [structure io](OpenNI-Windows-x64-2.2.0.33) and follow the instructions

Primesense Python Bindings
* Pip, from terminal: 

    + pip install primensense
    
* Manual, download from [python wrapper](https://pypi.python.org/pypi/primesense/2.2.0.30-5)
    
    + On an administrator terminal (i.e., right click on a terminal and select "run as administrator")
    + Go to where the bindings were downloaded (e.g., cd C:\downloads\primensense)
    + python setup.py install


## OpenNI2 in OMAP/ARM (PandaBoard ES and BeagleBoard -xm)

`mkdir Install/kinect`

`cd Install/kinect`

Clone from occipital github

`git clone https://github.com/occipital/OpenNI2`

`cd OpenNI2`

Compile. Remove the floating point operation flag

`gedit ThirdParty/PSCommon/BuildSystem/Platform.ARM`

Remove/delete "-mfloat-abi=softfp" (save & close)

`PLATFORM=Arm make # This steps took about 20 minutes`

Create ARM installer

`cd Packing/`

`python ReleaseVersion.py Arm`

If no errors, the compressed installer will be created in "Final" folder (i.e., OpenNI-Linux-Arm-2.2.tar.bz2).

`cd Final && cp OpenNI-Linux-Arm-2.2.tar.bz2 ~/Install/kinect`

Extract the contents to OpenNI-Linux-Arm-2.2 and rename the folder (helps with multiple installations/versions)

`mv ~/Install/kinect/OpenNI-Linux-Arm-2.2 ~/Install/kinect/OpenNI2-Arm`

`cd ~/Install/kinect/OpenNI2-Arm`

Install

`sudo ./install.sh`

## Install OpenNI2 in Ubuntu 14.04
`mkdir Install/kinect`

`cd Install/kinect`

Clone from occipital github

`git clone https://github.com/occipital/OpenNI2`

`cd OpenNI2`

`make`

`cd Packing`

`python ReleaseVersion.py x64`

If no errors, the compressed installer will be created in "Final" folder (i.e., OpenNI-Linux-64-2.2.tar.bz2).

`cd Final && cp OpenNI-Linux--2.2.tar.bz2 ~/Install/kinect`

Extract the contents to OpenNI-Linux-x64-2.2 and rename the folder (helps with multiple installations/versions)

`mv ~/Install/kinect/OpenNI-Linux-x64-2.2 ~/Install/kinect/OpenNI2-x64`

`cd ~/Install/kinect/OpenNI2-x64`

Install

`sudo ./install.sh`


## Install Python bindings in Ubuntu (12.04 ARM and 14.04 x64)

* Option 1. via pip -- not preferred

`sudo pip install primensense`

* Option 2. Manual Installation -- preferred

Download from: [python wrappers](https://pypi.python.org/pypi/primesense/primesense-2.2.0.30-5.tar.gz) and save in system Downloads

Copy the tar.gz file to a known location

`cd ~/Downloads && mv primesense-2.2.0.30-5.tar.gz ~/Install/kinect`

Extract

`tar -xvzf primesense-2.2.0.30-5.tar.gz`

`cd primesense-2.2.0.30-5`

`sudo python setup.py install`

Direct the system to the location of libOpenNI2.so (Two methods)

* Method 1. Create a symbolic link to OpenNI2/Redist/OpenNI2.so or copy the library to /usr/local/lib/

`sudo cp root/Install/kinect/OpenNI2-Arm/libOpenNI2.so /usr/local/lib # repeat for libNiTE2.so if available`

`sudo ldconfig`

* Method 2. For mulitple OpenNI installations. Direct the code to library location using:

`openni2.initialize(root+"/Install/kinect/OpenNI2-Arm/Redist/")`


## Test the setup using the initialize and is_initialize methods

`python`

`>>from primesense import openni2`

`>>openni2.initialize(root+"/Install/kinect/OpenNI2-Arm/Redist/")`

`>>if (openni2.is_initialized()):`

`>>    print "OpenNI2 initialized"`

`>>else:`

`>>    raise ValueError("OpenNI2 failed to initialize!!")`
