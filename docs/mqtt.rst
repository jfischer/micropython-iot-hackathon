.. _mqtt:

Messaging with MQTT
===================
MQTT (MQ Telemetry Transport) is a lightweight publish/subscribe messaging
protocol frequently used in IoT applications. It is a very thin layer over
TCP/IP, and has many implementations. MQTT is even an OASIS
standard [#]_. The Micropython software for ESP8266
includes a client implementation in the ``umqtt`` module [#]_.

MQTT Basics
-----------
An MQTT-based application will include two or more *clients*, which are
applications exchanging messages, and a *broker*, which is a server that
accepts incoming messages and routes them to the appropriate destination
client. As with most *publish-subscribe* systems, message sends involve
*publishing* on a specified *topic*. The broker then forwards the message
to all *subscribers* of that topic. These primitives can be used to build
different interaction patterns. The picture below shows an example:

.. image:: _static/mqtt-example.png

Here, we see a broker with three topics: *topic1*, *topic2*, and *topic3*,
which interact with clients using two different interaction patterns.
*Client-A* and *Client-B* are pubishing their messages to *topic1*. When a
message is received at the broker, it is passed on to any current subscribers
to the topic. In this case, both *Client-D* and *Client-E* will receive each
message. We will call this a *push* pattern, as it is one directional, and the
interaction is initiated by the publisher. In an IoT context, the
publisher is usually a sensor node and the subscriber(s) are servers
that process and store the sensor data.

*Client-C* and *Client-F* are interacting in a request-response or
*pull* pattern. *Client-C* sends request messages to *topic2*. These
are received by *Client-F*, which sends responses on *topic3*. In an
IoT context, this pattern may be useful when the server wishes to
poll the sensor nodes for data or for situations where the sensor nodes
need to query a server for configuration data.

In our application, we will be using the simpler push pattern.

Quality of Service
~~~~~~~~~~~~~~~~~~
Networked systems are never 100% reliable -- systems may crash, connections
can be lost, or parts of an appliciation taken down for maintenance. This is
even more true for IoT systems, where sensors may be in harsh physical
environments. Middleware like MQTT can improve reliability by storing messages
and implementing handshake protocols. However, this has a cost in terms of
resources and system complexity. MQTT gives you flexibility by specifying a
*Quality of Service* (QoS) with each message.

``QoS`` is a parameter available on each publish call. It is one of three
levels:

* `0` -- at most once. This means that the system will make a best effort to
  deliver the message, but will not store it and will drop the message in the
  event of an error. This is typically the behavior you would use in a sensor
  application: if a message is lost, the next sensor sample will be coming
  soon, anyway.
* `1` -- at least once. This means that the system will use storage and
  handshaking to ensure that the message is delivered. However, in doing so
  it may send the same message multiple times, resulting in duplicates.
* `2` -- exactly one. This means that each message will be delivered, and
  the handshaking protocol will ensure that duplicates are not passed to
  clients. This is the behaviour you want if you are implementing a banking
  system (but not so much in the IoT world).

For our application, we will use QoS level `0`.


Host-side Setup
---------------
Now, let us install an MQTT broker on our host system.


ESP8266 Setup
-------------
MicroPython already has an MQTT client in its standard library, so we do not need
to do much on the ESP8266-side. We will just copy over some convenience
modules provided by AntEvents.

On your host machine, go to the ``micropython`` subdirectory of your AntEvents
repository. Run ``mpfshell`` and copy the scripts for WiFi configuration and
MQTT as follows (substituting your tty device name for ``TTYDEVICE``)::

  open TTYDEVICE
  put wifi.py
  put mqtt_writer.py


Interactive Testing
-------------------
Now, go to the MicroPython REPL (via either the ``repl`` command of ``mpfshell``
or through ``screen``). We will first run our import statements:

.. code-block:: python

    >>> from antevents import *
    >>> from tsl2591 import Tsl2591
    >>> from wifi import wifi_connect
    >>> from mqtt_writer import MQTTWriter
  
Next, we configure the WiFi connection and then connect to the MQTT broker. Here
is the code in the REPL (replace ``my_wifi_sid``, ``my_wifi_password``, and
``mqtt_broker_ip`` with values for your environment):

.. code-block:: python

    >>> SID='my_wifi_sid'
    >>> PASSWORD='my_wifi_password'
    >>> MQTT_HOST='mqtt_broker_ip'
    >>> wifi_connect(SID, PASSWORD)
    network config: ( ... )
    >>> m = MQTTWriter('esp8266', MQTT_HOST, 1883, 'test-topic')
    Connecting to xxx.xxx.xxx.xxx:1883
    Connection successful

We can now create a sensor and connect two downstream components: ``Output``,
which prints events to the standard output, and ``m``, our MQTTWriter instance.
Here is the REPL session:

.. code-block:: python

    >>> sensor = SensorPub(Tsl2591('lux-1'))
    >>> sensor.subscribe(Output())
    <closure>
    >>> sensor.subscribe(m)
    <closure>

Finally, we instantiate an AntEvents scheduler and schedule our sensor to be
sampled once every two seconds:

.. code-block:: python
   
    >>> sched = Scheduler()
    >>> sched.schedule_periodic(sensor, 2.0)
    <closure>
    >>> sched.run_forever()
    ('lux-1', 611, 284.1312)
    ('lux-1', 613, 284.1312)
    ('lux-1', 615, 284.1312)
    ...


To verify that these messages are being sent to our broker, we can use the
utility ``mosquito_sub`` on the host machine. It takes one command line
argument, the topic name (in our case ``test-topic``). We should see something
like the following when we run it:

.. code-block:: bash

    $ mosquitto_sub -t test-topic
    ["lux-1", 624, 284.1312]
    ["lux-1", 626, 288.2113]
    ["lux-1", 627, 77.0304]
    ["lux-1", 629, 35.90401]
    ...

Great, now you have gotten live sensor data off your ESP8266 board!

Putting it all Together
-----------------------


.. [#] http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html

.. [#] The ``umqtt`` module is not in the official Micropython documentation,
       but module is definitely present in the firmware image. The API is simple
       enough that you can understand it by a quick read of the source code:
       https://github.com/micropython/micropython-lib/tree/master/umqtt.simple and
       https://github.com/micropython/micropython-lib/tree/master/umqtt.robust.
