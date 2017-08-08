#!/bin/bash
# Create zipfile for the MicroPython IoT Hackathon
# This is current as of 8/2017.

CURRENT_PATH=$(pwd)

TMP_PATH=$(mktemp -d)
trap "rm -rf $TMP_PATH" EXIT  # Ensure temporary path gets removed on exit
cd $TMP_PATH

#Find pip
PIP36=`which pip3.6`
PIP3=`which pip3`
PIPBARE=`which pip`
if [[ "$PIP36" != "" ]]; then
  PIP=$PIP36
elif [[ "$PIP3" != "" ]]; then
  PIP=$PIP3
elif [[ "$PIPBARE" != "" ]]; then
  PIP=$PIPBARE
else
  echo "Could not find pip3.6, pip3, or pip"
  exit 1
fi
echo "Using $PIP as pip program"
if [[ `which wget` == "" ]]; then
  echo "Could not find wget"
  exit 1
fi

set -e  # Stop if there is any error

# Get tool wheels
$PIP wheel -w micropython-iot-software/python-tools --no-binary=:all: esptool adafruit-ampy \
    wheel paho_mqtt thingflow git+https://github.com/wendlers/mpfshell

# Get firmware
cd micropython-iot-software
wget http://micropython.org/resources/firmware/esp8266-20170612-v1.9.1.bin

# Get repos
git clone https://github.com/jfischer/micropython-iot-hackathon
git clone https://github.com/mpi-sws-rse/thingflow-python
rm -rf micropython-iot-hackathon/.git
rm -rf thingflow-python/.git

# build the docs
echo "building docs"
pip install sphinx_rtd_theme # theme for docs
mkdir docs
cd micropython-iot-hackathon/docs
make html
mv _build/html ../../docs/micropython-iot-hackathon
rm -rf _build
cd ../..
cd thingflow-python/docs
make html
mv _build/html ../../docs/thingflow-python
rm -rf _build
cd ../..


# Download terminal programs
mkdir terminal; cd terminal
wget https://the.earth.li/~sgtatham/putty/latest/w32/putty-0.70-installer.msi
wget ftp.us.debian.org/debian/pool/main/s/screen/screen_4.5.0-6_amd64.deb
cd ..

# Download drivers
mkdir drivers; cd drivers
wget https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip
wget https://www.silabs.com/documents/public/software/Mac_OSX_VCP_Driver.zip
cd ..

# Prepare esp8266 modules to upload
mkdir micropython; cd micropython
cp ../micropython-iot-hackathon/example_code/client.py .
cp ../thingflow-python/micropython/*.py .
cp ../thingflow-python/micropython/sensors/*.py .
cd ../..

# Create a zip file
zip -r micropython-iot-software.zip micropython-iot-software

# Cleanup
cd $CURRENT_PATH
mv $TMP_PATH/micropython-iot-software.zip .
echo "Successfully created micropython-iot-software.zip"
