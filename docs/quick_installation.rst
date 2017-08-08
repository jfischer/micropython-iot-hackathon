.. _quick_installation:

9. Quick Software Setup
=======================
This set of steps is designed as a fast alternative initial software and
firmware setup. They are particularly recommended when time is a concern, or
blocking issues arise.

The script `make_zip.sh <https://github.com/jfischer/micropython-iot-hackathon/blob/master/make_zip.sh>`_ at the root of this repo was used to build
micropython-iot-software.zip, removing network dependency and improving reliability. The instructions
below assume that you have this zip file available, either created through make_zip.sh
or given to you by your instructor.

To check that the light sensor is working, you will need to wire up your board
and connect it to your USB port, as described in the
:ref:`hardware assembly <hardware-assembly>` chapter.

We include two version of the instructions, one for Debian 9 Linux and one for MacOS.
If you have another system, please follow the full instructions in
:ref:`Firmware and Testing <firmware-and-testing>`.
You should still be able to use the files from the zip, as most are portable
across OSs. Look at :ref:`here <os_specifics>` for OS-specific needs.

Debian 9 Linux
--------------
We copy-and-paste tested these instructions
using a modern Debian 9 with python 3.6.2 (from sid) and the screen program.

::

    # Create project directory and virtual environment
    mkdir -p ~/micropython-iot-hackathon
    cd ~/micropython-iot-hackathon
    python3.6 -m venv venv

    # Activate python virtual environment [Notice the (venv) prompt indicating
    # you are now within the virtual environment]
    source venv/bin/activate

    # Install software
    unzip micropython-iot-software.zip
    pip install --upgrade micropython-iot-software/python-tools/*whl

    # Upload to latest firmware. (Use /dev/tty.SLAB_USBtoUART for OSX)
    esptool.py --port /dev/ttyUSB0 erase_flash
    esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --verify \
      -fm dio 0 micropython-iot-software/esp8266-20170612-v1.9.1.bin

    # Enter the micropython REPL using the terminal  (and press Enter key to
    # see the promt ">>>".  To exit, use Ctrl-a + \ + y)
    screen /dev/ttyUSB0 115200
    >>> print('Hello world')
    [Exit screen, using: Control-A + k + y]

    # Upload libraries to micropython
    export AMPY_PORT=/dev/ttyUSB0
    ampy put micropython-iot-software/micropython lib
    ampy put micropython-iot-software/micropython/client.py main.py

    # Check data can be read
    screen /dev/ttyUSB0 115200
    >>> from tsl2591 import Tsl2591
    >>> tsl = Tsl2591('lux-1')
    >>> tsl.sample()
    [Exit screen, using: Control-A + k + y]

 
MacOS
-----
First, download and install the Anaconda for Python 3.6 distribution from https://www.continuum.io/downloads.
We will use the ``conda`` virtual environment tool instead of the standard Python 3 ``venv``.

To communicate with the ESP8266 over your Mac's USB port, you will also need to
install a serial driver (found in your zip distribution at
``micropython-iot-software/drivers/Mac_OSX_VCP_Driver.zip``).

This was tested on MacOS Sierra.

::

    # Create project directory and virtual environment
    mkdir -p ~/micropython-iot-hackathon
    cd ~/micropython-iot-hackathon
    # Create virtual environment. Enter "y" when asked whether to proceed.
    conda create -n micropython-iot-hackathon python=3.6 anaconda

    # Activate python virtual environment [Notice the (micropython-iot-hackathon)
    # prompt indicating you are now within the virtual environment].
    source activate micropython-iot-hackathon

    # Install software
    unzip micropython-iot-software.zip
    pip install --upgrade micropython-iot-software/python-tools/*whl

    # Upload to latest firmware. (Use /dev/tty.SLAB_USBtoUART for OSX)
    esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
    esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --verify \
      -fm dio 0 micropython-iot-software/esp8266-20170612-v1.9.1.bin

    # Enter the micropython REPL using the terminal  (and press Enter key to
    # see the promt ">>>".  To exit, use Ctrl-a + \ + y)
    screen /dev/tty.SLAB_USBtoUART 115200
    >>> print('Hello world')
    [Exit screen, using: Control-A + k + y]

    # Upload libraries to micropython
    export AMPY_PORT=/dev/tty.SLAB_USBtoUART
    ampy put micropython-iot-software/micropython lib
    ampy put micropython-iot-software/micropython/client.py main.py

    # Check data can be read
    screen /dev/tty.SLAB_USBtoUART 115200
    >>> from tsl2591 import Tsl2591
    >>> tsl = Tsl2591('lux-1')
    >>> tsl.sample()
    [Exit screen, using: Control-A + k + y]


Have fun!
