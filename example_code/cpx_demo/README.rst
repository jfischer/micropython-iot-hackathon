==============================================
ThingFlow CircuitPlayground Express (CPX) demo
==============================================
This directory contains example code to drive a CircuitPlayground Express
neopixel ring with wireless data.

The setup involves a ESP8266 that captures an analog signal from a
potentiometer and transmits it wirelessly using an MQTTWriter. Then the host
computer decodes the wireless MQTTReader data and bridges it to the CPX to lit
the neopixel ring. One interesting aspect of this setup, is that CPX runs a
derivative version of micropython too and the host drives the CPX using its
REPL. This way the host can technically talk to the full array of sensors and
transducers without being artificially limited by APIs.

Files in this directory
=======================

* ``cpx_driver.py`` - Implement REPL bridge, exposing the light sensor and the
  neopixel ring drivers
* ``cpx_transducer.py`` - ThingFlow thin layer on top of cpx_driver
* ``server_cpx.py`` - ThingFlow CPX demo
