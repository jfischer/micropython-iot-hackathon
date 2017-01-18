.. _projects:

7. Projects
===========
We now sketch out several projects you can build starting with your system.
These include interfacing additional sensors, software projects,
as well as incorporating the system in a larger application. Currently, this
section is just a sketch. Over time, we will fill out more details.

Graphing Light Sensor Data
--------------------------
Given the CSV files we have generated, it is quite easy to use
`Jupyter <http://jupyter.org>`__ and
`matplotlib <http://matplotlib.org>`__
to graph the light sensor data over time. Here is an example plot of light
sensor data gathered using the system we have described:

.. image:: _static/lighting-app-front-room.png

Lighting Replay Application
---------------------------
See https://github.com/mpi-sws-rse/antevents-examples/tree/master/lighting_replay_app.
This is an application which uses captured light sensor data to train a
Hidden Markov Model. This model then is replayed when you are not home, to turn
lights on and off in a realistic manner.

Turning on an LED
-----------------
Perhaps the simplest hardware interfacing is to an LED. There are many tutorials
online about how to do this. You will need three connections: from a GPIO pin
to the LED, from the LED to a resistor, and from the resistor to GND.

Temperature Sensor
------------------
There are many temperature sensors on the market. One well documented sensor
is the `MCP9808 breakout board <https://www.adafruit.com/products/1782>`__ from
Adafruit. Like our light sensor, it uses the IC2 bus for communication. Adafruit
even has a tutorial about using this sensor with MicroPython
`here <https://learn.adafruit.com/micropython-hardware-i2c-devices>`__.

Door Open/Close Detector
------------------------
Adafruit describes a project to interface the ESP8266 to a door open/closed
switch here: https://learn.adafruit.com/using-ifttt-with-adafruit-io/overview.
It is Arduino based, but should be easily adaptible to MicroPython.

Another Micropython/ESP8266 Tutorial
------------------------------------
We recently found another tutorial about Micropython and the ESP8266.
It is more focused on lower level sensors and has some interesting
hardware projects. It is called "MicroPython on ESP8266 Workshop" and
is available here: http://micropython-on-esp8266-workshop.readthedocs.io/en/latest/index.html.

Finally, we conclude with some :ref:`advice <teachers-notes>` for hosting a
hackathon.

