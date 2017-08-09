#!/bin/bash
# Create zipfile for the MicroPython IoT Hackathon
# This is current as of 8/2017.

CURRENT_PATH=$(pwd)

if [ ! -f docs/conf.py ]; then
    echo "Could not find Sphinx configuration file at ./docs/conf.py"
    exit 1
fi
RELEASE=`cd docs; python3 -c "import conf; print(conf.release)"`
echo "RELEASE is $RELEASE"

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

# create root dir
mkdir micropython-iot-software

# Get tool wheels
$PIP wheel -w micropython-iot-software/python-tools --no-binary=:all: esptool adafruit-ampy \
    wheel paho_mqtt thingflow git+https://github.com/wendlers/mpfshell

# Get firmware
cd micropython-iot-software
BASE=`pwd` # save for later
wget http://micropython.org/resources/firmware/esp8266-20170612-v1.9.1.bin

# Get repos
git clone https://github.com/mpi-sws-rse/thingflow-python
rm -rf thingflow-python/.git
git clone https://github.com/jfischer/micropython-iot-hackathon
mv micropython-iot-hackathon/example_code ./example_code

# build the docs
echo "building docs"
pip install sphinx_rtd_theme # theme for docs
mkdir docs
mv micropython-iot-hackathon/lecture.pdf ./docs
cd micropython-iot-hackathon/docs
make html
mv _build/html $BASE/docs/micropython-iot-hackathon
cd $BASE
rm -rf micropython-iot-hackathon # no longer need the original code
cd thingflow-python/docs
make html
mv _build/html $BASE/docs/thingflow-python
rm -rf _build
cd $BASE

# clone and build micropython docs
mkdir $BASE/mpbuild
cd $BASE/mpbuild
git clone https://github.com/micropython/micropython.git
cd micropython
git checkout -b v1.9.1
cd docs
make MICROPY_PORT=esp8266 html
cd build/esp8266
mv html $BASE/docs/micropython
cd $BASE
rm -rf ./mpbuild

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
cp $BASE/example_code/client.py .
cp ../thingflow-python/micropython/*.py .
cp ../thingflow-python/micropython/sensors/*.py .
cd $BASE

echo "Generating README.txt..."
echo "MicroPython IoT Hackathon Downloads Archive" >README.txt
echo "===========================================" >>README.txt
echo "Generated from version $RELEASE on `date`" >>README.txt
echo "To get started, see docs/micropython-iot-hackathon/index.html" >>README.txt
echo >>README.txt
echo "File Layout" >>README.txt
echo "-----------" >>README.txt
echo "docs/" >>README.txt
echo "  micropython-iot-hackathon/" >>README.txt
echo "  micropython/" >> README.txt
echo "  thingflow-python/" >>README.txt
echo "drivers/  (serial drivers for MacOS and Windows)" >>README.txt
echo "esp8266-20170612-v1.9.1.bin (MicroPython firmware image)" >>README.txt
echo "example_code/ (from micropython-iot-hackathon repo)" >>README.txt
echo "micropython/ (ThingFlow and other code for ESP8266)" >>README.txt
echo "python-tools/ (Python libraries for your laptop)" >>README.txt
echo "terminal/ (PuTTY for Windows, screen for Linux)" >>README.txt
echo "thingflow-python/ (ThingFlow source and example code)" >>README.txt
echo >>README.txt
echo "Have fun!" >>README.txt
cd ..

# Create a zip file
zip -r micropython-iot-software.zip micropython-iot-software

# Cleanup
cd $CURRENT_PATH
mv $TMP_PATH/micropython-iot-software.zip .
echo "Successfully created micropython-iot-software.zip"
