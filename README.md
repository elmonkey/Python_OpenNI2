# Python4OpenNI2
# Sample applications that use the official python wrappers for OpenNI 2 (opencv)
# There a plenty of dependencies that need to be met.

#Build from source and installation instructions for OpenNI2 and Primensense Python Bindings on PandaBoard ES running Ubuntu 12.04.

#==== COMPILE AND INSTALL OPENNI2
# on a terminal (ctrl+alt+t)
mkdir Install/kinect
cd Install/kinect
# clone from occipital github
git clone https://github.com/occipital/OpenNI2
cd OpenNI2

# -- Compile
# Remove the floating point operation flag
gedit ThirdParty/PSCommon/BuildSystem/Platform.ARM
# remove/delete -mfloat-abi=softfp
# save & close
PLATFORM=Arm make # This steps took about 20 minutes

# -- Create ARM installer
cd Packing/ 
python ReleaseVersion.py Arm
# If no errors, the binaries are in the "Final" folder
cd Final/OpenNI

# --
sudo ./install.sh

# ==== INSTALL primesense 2.2.0.30-5: TWO OPTIONS

# -- via pip -- not my preferred
pip install primensense

# -- Manual Installation -- preferred
# Download from  
#     https://pypi.python.org/pypi/primesense/primesense-2.2.0.30-5.tar.gz
# to Downloads
cd ~/Downloads && mv primesense-2.2.0.30-5.tar.gz ~/Install/kinect
# -- extract
tar -xvzf primesense-2.2.0.30-5.tar.gz
cd primesense-2.2.0.30-5
sudo python setup.py install
# create a symbolic link for OpenNI2.so or direct the code (see examples) to the location where the library is located (e.g., openni2.initialize('~/Install/kinect/OpenNI2-Linux-Arm-2.2/Redist/') # notice that OpenNI2.so is not included in the path.

#=== TEST
python
>> import primesense
