#!/bin/bash
# Create zipfile for the MicroPython IoT Hackathon

set -e  # Stop if there is any error
CURRENT_PATH=$(pwd)

TMP_PATH=$(mktemp -d)
trap "rm -rf $TMP_PATH" EXIT  # Ensure temporary path gets removed on exit
cd $TMP_PATH

# Get tool wheels
pip3.6 wheel -w micropython-iot-software/python-tools esptool adafruit-ampy \
    wheel paho_mqtt thingflow git+https://github.com/wendlers/mpfshell

# Get firmware
cd micropython-iot-software
wget http://micropython.org/resources/firmware/esp8266-20170612-v1.9.1.bin

# Get repos
git clone https://github.com/jfischer/micropython-iot-hackathon
git clone https://github.com/mpi-sws-rse/thingflow-python
rm -rf micropython-iot-hackathon/.git
rm -rf thingflow-python/.git

# Download terminal programs
mkdir terminal; cd terminal
wget https://the.earth.li/~sgtatham/putty/latest/w32/putty-0.70-installer.msi
wget ftp.us.debian.org/debian/pool/main/s/screen/screen_4.5.0-6_amd64.deb
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
