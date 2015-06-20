# Python4OpenNI2
# Installation instructions and sample applications that use the official python wrappers for OpenNI 2 and OpenCV
# Tested on OMAP4 (ARM) PandaBoard ES running Ubuntu 12.04, Python 2.7.3, and OpenCV.2.4.10

# There a plenty of dependencies that need to be met.
sudo apt-get install gcc-multilib libusb-1.0.0-dev git-core build-essential
sudo apt-get install doxygen graphviz default-jdk freeglut3-dev

# Python
sudo apt-get -y install python-dev python-numpy 
sudo apt-get -y install python-scipy python-setuptools
sudo apt-get -y install ipython python-pip
sudo apt-get -y install libboost-python-dev

#Instructions to...
# Build OpenNI2 installer for PandaBoard ES 
# Install OpenNI2 and Primensense Python Bindings on PandaBoard ES running Ubuntu 12.04.

#==== COMPILE AND INSTALL OPENNI2
# terminal (ctrl+alt+t)
$ mkdir Install/kinect
$cd Install/kinect

# clone from occipital github
$ git clone https://github.com/occipital/OpenNI2
$ cd OpenNI2

# -- Compile
# Remove the floating point operation flag
$gedit ThirdParty/PSCommon/BuildSystem/Platform.ARM

# remove/delete -mfloat-abi=softfp
# save & close
$ PLATFORM=Arm make # This steps took about 20 minutes

# -- Create ARM installer
$ cd Packing/ 
$ python ReleaseVersion.py Arm

# If no errors, the compressed installer will be created in "Final" folder
# OpenNI-Linux-Arm-2.2.tar.bz2
$ cd Final && cp OpenNI-Linux-Arm-2.2.tar.bz2 ~/Install/kinect

# Extract the contents >> OpenNI-Linux-Arm-2.2
# I rename the folder since I have multiple installations/versions
# OpenNI-Linux-Arm-2.2 >> OpenNI2-Arm
cd ~Install/kinect/OpenNI2-Arm
# -- Install
$ sudo ./install.sh

# ==== INSTALL primesense 2.2.0.30-5: TWO OPTIONS
# -- Option 1. via pip -- not my preferred since I have multiple versions
$ pip install primensense

# -- Option 2. Manual Installation -- preferred
# Download from  
#     https://pypi.python.org/pypi/primesense/primesense-2.2.0.30-5.tar.gz
# to system Downloads
$ cd ~/Downloads && mv primesense-2.2.0.30-5.tar.gz ~/Install/kinect

# -- extract
$ tar -xvzf primesense-2.2.0.30-5.tar.gz
$ cd primesense-2.2.0.30-5
$ sudo python setup.py install

# Make python bindings availble (two methods)
# Method 1. Create a symbolic link to OpenNI2/Redist/OpenNI2.so or copy the library to /usr/local/lib/
sudo cp ~/Install/kinect/OpenNI2-Arm/libOpenNI2.so /usr/local/lib # repeat for libNiTE2.so if available
sudo ldconfig

# Method 2. For mulitple Openni installations direct the code to the correct version (see examples) by giving it the path to th library (e.g., 
$ python
>> ...
>> openni2.initialize('~/Install/kinect/OpenNI2-Arm/Redist/') 

#=== TEST
$ python
>> from primesense import openni2
>> openni2.initialize('~/Install/kinect/OpenNI2-Arm/Redist/') 
# check that openni2 was properly initialized
>> if (openni2.is_initialized()):
>>   print "OpenNI2 initialized"
>> else:
>>   raise ValueError("OpenNI2 failed to initialize!!")
