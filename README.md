
This guide assumes Carmine devices and Primesense's API's and drivers (OpenNI2 and NiTE2). Steps to install and configure opeNI2 with Msft's Kinect are being tested. In the meantime, the following link provides an easy to follwo guide (untested) for to use [OpenNI2 with Kinect](http://cupofpixel.blogspot.com/2013/04/how-to-use-openni-2-nite-2-kinect-on.html). The freenect driver link appears to be broken so use the direct [[link](https://github.com/OpenKinect/libfreenect/tree/master/OpenNI2-FreenectDriver)] instead. 

# OpenNI2 Python
Compile and Install OpenNI2

Installation instructions and samples using the official Python wrappers for OpenNI2 and OpenCV. Adapted from [Occipital](https://github.com/occipital/OpenNI2)

* Tested on the following systems (running Python 2.7.3, OpenNI2.2, and OpenCV.2.4.10)

    + Windows 7 x64
    + Linux Ubuntu 14.04 x64
    + PandaBoard ES/BeagleBoard-xm running Ubuntu 12.04 OMAP/ARM
        + [Panda](https://docs.google.com/document/d/1MjW0vVms-r4gm0KSYxb3JSKimJ_kvG0yLDgu_mTnBzk/edit?usp=sharing) ubuntu installation -- gdoc instructions
        + [Beagle](https://docs.google.com/document/d/1sOKNSICoNeKMtrbIBvHbpXfJDbkfdD-jI5BVD8dfOMc/edit?usp=sharing) ubuntu installation -- gdoc instructions


NOTE: root and ~ are used to represent home/<username>/

## Dependencies

Windows use wheels from [LDF](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

Linux Ubuntu
* OpenNI

`sudo apt-get install libudev-dev libusb-1.0.0-dev`

`sudo apt-get install gcc-multilib git-core build-essential`

`sudo apt-get install doxygen graphviz default-jdk freeglut3-dev`

* JDK 
There is a known issue with x86 architectures and jdk. Follow this [[link](https://www.digitalocean.com/community/tutorials/how-to-install-java-on-ubuntu-with-apt-get)] to add the jdk repo.

`sudo apt-get install python-software-properties`

`sudo add-apt-repository ppa:webupd8team/java`

`sudo apt-get update`

**NOTE**: the workaround was tested with jdk6 (commands to install other versions are on the site).

`sudo apt-get install oracle-java6-installer`

Then finally update the flags using the command from this [[link](http://stackoverflow.com/questions/25851510/openni2-error-when-running-make)]

`export LDFLAGS+="-lc"`


* Python Environment

`sudo apt-get -y install python-dev python-numpy `

`sudo apt-get -y install python-scipy python-setuptools`

`sudo apt-get -y install ipython python-pip`

`sudo apt-get -y install libboost-python-dev`

## OpenNI2 Windows 7 x64 [installation](https://github.com/occipital/OpenNI2) details

OpenNI2. Download msi installer from [structure io](OpenNI-Windows-x64-2.2.0.33) and follow the instructions

Primesense Python Bindings
* Pip, from terminal: 

    + pip install primensense
    
* Manual, download from [python wrapper](https://pypi.python.org/pypi/primesense/2.2.0.30-5)
    
    + On an administrator terminal (i.e., right click on a terminal and select "run as administrator")
    + Go to where the bindings were downloaded (e.g., cd C:\downloads\primensense)
    + python setup.py install

## Install OpenNI2 in Ubuntu 14.04
`mkdir Install/kinect/openni2`

`cd Install/kinect/openni2`

Clone from occipital github

`git clone https://github.com/occipital/OpenNI2`

`cd OpenNI2`

`make`

`cd Packing`

`python ReleaseVersion.py x64 #x86`

If no errors, the compressed installer will be created in "Final" folder (i.e., OpenNI-Linux-64-2.2.tar.bz2).

`cd Final && cp OpenNI-Linux--2.2.tar.bz2 ~/Install/kinect/openni2`

Extract the contents to OpenNI-Linux-x64-2.2 and rename the folder (helps with multiple installations/versions)

`mv ~/Install/openni2/OpenNI-Linux-x64-2.2 ~/Install/kinect/openni2/OpenNI2-x64`

`cd ~/Install/kinect/openni2/OpenNI2-x64`

Install

`sudo ./install.sh`

## OpenNI2 in PandaBoard-ES and BeagleBoard-xM

`mkdir Install/kinect/openni2`

`cd Install/kinect/openni2`

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

`cd Final && cp OpenNI-Linux-Arm-2.2.tar.bz2 ~/Install/kinect/openni2`

Extract the contents to OpenNI-Linux-Arm-2.2 and rename the folder (helps with multiple installations/versions)

`mv ~/Install/kinect/openni2/OpenNI-Linux-Arm-2.2 ~/Install/kinect/openni2/OpenNI2-Arm`

`cd ~/Install/kinect/openni2/OpenNI2-Arm`

Install

`sudo ./install.sh`


## Install Python bindings in Ubuntu (12.04 ARM and 14.04 x64)

* Option 1. via pip -- not preferred

`sudo pip install primensense`

* Option 2. Manual Installation -- preferred

Download from: [primesense python wrapper](https://pypi.python.org/pypi/primesense/) and save in system Downloads

Copy the tar.gz file to a known location

`cd ~/Downloads && mv primesense-2.2.0.30-5.tar.gz ~/Install/kinect/openni2`

Extract

`tar -xvzf primesense-2.2.0.30-5.tar.gz`

`cd primesense-2.2.0.30-5`

`sudo python setup.py install`

Direct the system to the location of libOpenNI2.so (Two methods)

* Method 1. Create a symbolic link to OpenNI2/Redist/OpenNI2.so or copy the library to /usr/local/lib/

`sudo cp root/Install/kinect/openni2/OpenNI2-Arm/libOpenNI2.so /usr/local/lib # repeat for libNiTE2.so if available`

`sudo ldconfig`

* Method 2. For mulitple OpenNI installations. Direct the code to library location using:

`openni2.initialize(root+"/Install/kinect/openni2/OpenNI2-Arm/Redist/")`


## Test the setup using the initialize and is_initialize methods

`python`

`>>from primesense import openni2`

`>>openni2.initialize(root+"/Install/kinect/openni2/OpenNI2-Arm/Redist/")`

`>>if (openni2.is_initialized()):`

`>>    print "OpenNI2 initialized"`

`>>else:`

`>>    raise ValueError("OpenNI2 failed to initialize!!")`
