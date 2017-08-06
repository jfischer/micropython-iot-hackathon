.. _quick_installation:

9. Quick Software Setup
=======================

These set of steps are designed as a fast alternative initial software and
firmware setup. They are particularly recommended when time is a concern, or
blocking issues arise.

We copy-and-paste tested using a modern Debian 9 with python 3.6.2 (from sid)
and the screen program. Regardless, python tools and programs are particularly portable across OSs. Mac OSX and Windows will need USB serial drivers. Look
at :ref:`os_specifics` for OS specific needs.

The script `make_zip.sh <https://github.com/jfischer/micropython-iot-hackathon/blob/master/make_zip.sh>`_ at the root of this repo was used to build
micropython-iot-software.zip, removing network dependency and improving
reliability.


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
    [Control-A + k + y]

    # Upload libraries to micropython
    export AMPY_PORT=/dev/ttyUSB0
    ampy put micropython-iot-software/micropython lib
    ampy put micropython-iot-software/micropython/client.py main.py

    # Check data can be read
    screen /dev/ttyUSB0 115200
    >>> from tsl2591 import Tsl2591
    >>> tsl = Tsl2591('lux-1')
    >>> tsl.sample()
    [Control-A + k + y]


Have fun!
