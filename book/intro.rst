.. _intro:

Introduction
=============
Background
-----------
MicroPython [#]_ is an implementation of Python 3 that can on on small devices
without a traditional operating system. It requires just 256k of code space and
16k of RAM. One of the microcontrollers supported is the ESP8266 [#]_, a low cost
mirocontroller with a 32-bit CPU, a built-in WiFi radio, and a number of
input/output ports useful for interfacing with the physical world.

Overview of this Document
-------------------------
We cover the construction and programming of a ESP8266-based system starting
with the parts you need and moving toward end-to-end applications. The following
topics are covered:

* :ref:`parts-and-tools` - the parts you will need to find/purchase and the
  tools required to build and debug the system.
* :ref:`hardware-assembly` - connect a light sensor up to the ESP8266.
* :ref:`firmware-and-testing` - install firmware and interact with the board over
  a USB connection.
* :ref:`antevents-application` - use the AntEvents framework to build a
  simple light sensor sampling application.
* :ref:`mqtt` - use the MQTT protocol to send our sensor events over the
  wireless network.
* :ref:`projects` - we sketch out some follow-on projects involving additional
  sensors and larger applications. This is the jumping point for you to be
  creative and try out your own ideas.
* :ref:`teachers-notes` - some notes for instructors who are using the material
  as a template for a class.

.. [#] http://www.micropython.org

.. [#] https://en.wikipedia.org/wiki/ESP8266
