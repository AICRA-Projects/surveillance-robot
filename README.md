# surveillance-robot
Robots play a major role in many walks of life and are extensively used in the areas of defence, 
industries, medical and home applications. They can carry out different risky jobs that cannot be done by human. This 
paper presents Defence Surveillance robot (DSR) for defence purpose that has metal and magnetic field detection 
sensor, LDR sensor for night vision, fire detection sensor with pump motor to extinguish fire, IR sensors for path 
finding and obstacle avoidance, moisture sensor. A robotic arm of 4 degree of freedom is interfaced for explosive 
placement and diffusion. The system provides continuous visual monitoring through the wireless camera attached to the 
robot and sends continuous data to the control unit. Basically three modes of operations are provided i.e. RF mode, 
DTMF mode and Automatic mode.

## How to operate: 
### step 1: Give Power to the robot by connecting White Usb Cable with USB connector of Power Bank 
### step 2: Press "On" in Red switch 
### step 3: Type the link in webBrowser http://Ip_address:5000
### step 4: once you visit in the link you will find 4 different modes will be displayed 
### step 5: Manual mode : will be display with control panel of robot movements and camera which you can use for survillance purpose 
### step 6: Face Tracking mode : It will track your face as you move right or left , face detection is enabled with A.I 
### step 7: Color detection mode : its non locomotion mode for the robot but used for detecting the color from camera , USER can bring RGB object in front of it 
### step 8: Auto pilot mode : Its a autonomous mode of the robot without any manuall instruction robot will move decision making Proces done by using sensors and displayed by camera## Raspberry pi based 

# Methodology
Hardware connections very important which provides the overview of circuit in the project , if connections are correct then output will be displayed on the screen of LCD   
Python is a wonderful and powerful programming language that's easy to use (easy to read and write) and, with Raspberry Pi, lets you connect your project to the real world.
## Step 1: Install Python Packages 
* A package is basically a directory with Python files and a file with the name __init__.py. This means that every directory inside of the Python path, which contains a file named __init__.py, will be treated as a package by Python. It's possible to put several modules into a Package.
* Raspberry pi operated by Raspbian is a Debian-based engineered especially for the Raspberry Pi and it is the perfect general-purpose OS for Raspberry users 
* Install Raspberry pi GPIO packages: pip install RPi.GPIO
* Type " pinout " in Terminal of Raspberry pi 
## Step 2 : Install Opencv in Raspberry pi  
##### to get the current status
* $ sudo rpi-eeprom-update
#### if needed, to update the firmware
* $ sudo rpi-eeprom-update -a
* $ sudo reboot 
#### Version check.
Before you install OpenCV on your Raspberry Pi 4, it is time for a final version check. Many readers just jump into the guide, skipping the introduction, often because they have already an operating system working. For those, please give the command uname -a and check your version.
* $ python3 --version
#### Dependencies.
The OpenCV software uses other third-party software libraries. These have to be installed first. Some come with the Raspbian operating system, others may have been gathered over time, but it's better to be safe than sorry, so here is the complete list. Only the latest packages are installed by the procedure.
* $ sudo apt-get update
* $ sudo apt-get upgrade
* $ sudo apt-get install cmake gfortran
* $ sudo apt-get install libjpeg-dev libtiff-dev libgif-dev
* $ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
* $ sudo apt-get install libgtk2.0-dev libcanberra-gtk*
* $ sudo apt-get install libxvidcore-dev libx264-dev libgtk-3-dev
* $ sudo apt-get install libtbb2 libtbb-dev libdc1394-22-dev libv4l-dev
* $ sudo apt-get install libopenblas-dev libatlas-base-dev libblas-dev
* $ sudo apt-get install libjasper-dev liblapack-dev libhdf5-dev
* $ sudo apt-get install protobuf-compiler
* $ sudo apt-get install qt5-default
* $ cd ~
* $ wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.0.zip
* $ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.0.zip

* $ unzip opencv.zip
* $ unzip opencv_contrib.zip
* $ mv opencv-4.5.0 opencv
* $ mv opencv_contrib-4.5.0 opencv_contrib
#### Install a virtual environment.
Step one is some administration. We only use Python 3 because the support of Python 2.7 has stopped at the beginning of 2020. You have first to determine your Python 3 version   and location.
The Python location in the above commands was /usr/bin/python3.7. This location is passed as an argument in the echo command. The next step is installing the virtual      environment software. This can be done with the following commands.
* $ sudo pip3 install virtualenv
* $ sudo pip3 install virtualenvwrapper
* $ echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.7" >> ~/.bashrc
#### reload profile
* $ source ~/.bashrc
* $ echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
* $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
* $ source ~/.bashrc
* $ mkvirtualenv cv450
#### without sudo!!!!
* $ pip3 install numpy
#### Build Make 
* $ cd ~/opencv/
* $ mkdir build
* $ cd build
* $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
          -D ENABLE_NEON=ON \
          -D ENABLE_VFPV3=ON \
          -D WITH_OPENMP=ON \
          -D WITH_OPENCL=OFF \
          -D BUILD_TIFF=ON \
          -D WITH_FFMPEG=ON \
          -D WITH_TBB=ON \
          -D BUILD_TBB=ON \
          -D BUILD_TESTS=OFF \
          -D WITH_EIGEN=OFF \
          -D WITH_GSTREAMER=OFF \
          -D WITH_V4L=ON \
          -D WITH_LIBV4L=ON \
          -D WITH_VTK=OFF \
          -D WITH_QT=OFF \
          -D OPENCV_ENABLE_NONFREE=ON \
          -D INSTALL_C_EXAMPLES=OFF \
          -D INSTALL_PYTHON_EXAMPLES=OFF \
          -D BUILD_opencv_python3=TRUE \
          -D OPENCV_GENERATE_PKGCONFIG=ON \
          -D BUILD_EXAMPLES=OFF ..
* Before we can start the actual build, the memory swap space needs to be enlarged. For daily use a swap memory of 100 Mbyte is sufficient. However, with the massive build ahead of use, extra memory space is crucial. Enlarge the swap space with the following command.
* $ sudo nano /etc/dphys-swapfile
* This command opens Nano, a very lightweight text editor, with the system file dphys-swapfile. With the arrow keys, you can move the cursor to the CONF_SWAPSIZE line where the new value 2048 can be entered. Next, close the session with the <Ctrl+X> key combination. With <Y> and <Enter> changes are being saved in the same file.
* $ sudo /etc/init.d/dphys-swapfile stop
* $ sudo /etc/init.d/dphys-swapfile start
* $ make -j4
#### Make
Now everything is ready for the great build. This takes a lot of time. Be very patient is the only advice here. Don't be surprised if at 99% your build seems to be crashed. That is 'normal' behaviour. Even when your CPU Usage Monitor gives very low ratings like 7%. In reality, your CPU is working so hard it has not enough time to update these usage numbers correctly.
You can speed things up with four cores working simultaneously (make -j4). On a Raspberry Pi 4, it takes just over an hour to build the whole library. Sometimes the system crashes for no apparent reason at all at 99% or even 100%. In that case, restart all over again, as explained at the end of this page, and rebuild with make -j1.
Probably you get a whole bunch of warnings during the make. Don't pay to much attention to it. They are generated by subtle differences in template overload functions due to little version differences. 
* $ sudo make install
* $ sudo ldconfig
#### cleaning (frees 300 KB)
* $ make clean
* $ sudo apt-get update
## Step 3: Steps to implement human Face recognition with Python & OpenCV:
1. Imports:

import cv2
import os
2. Initialize the classifier:

cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

3. Apply faceCascade on webcam frames:

video_capture = cv2.VideoCapture(0)
while True:
    # Capture frame-by-frame
    ret, frames = video_capture.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Display the resulting frame
    cv2.imshow('Video', frames)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
4. Release the capture frames:

video_capture.release()
cv2.destroyAllWindows()

  
## Install Web Hosting 
* pip install Flask
#### Step 1: 
  Check Arduino I2c Connection with Raspberry pi 
#### Step 2 :
  Host Flask webste with camera enable 
#### Step 3 :
  Check opencv with face detection and Color detection 
#### Step 4 :
  Integrate each setup with code and check the interface 
#### Step 5 :
  ZIP file with define code for survelliance robot
#### Step 6 :
  check each script for the interface 
#### Step 7 :
  Check power Connectivity with power bank and lithuim ion battery 
## Hardware 
  * Raspberry Pi 4 
  * Arduino Nano 
  * Ultrasonic sensor x 3
  * USB Camera 
  * Omni Wheels
  * DC BO motors
  * Battery and power bank
  * Servo Motor 
