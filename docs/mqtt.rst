.. _mqtt:

Messaging with MQTT
===================
MQTT (MQ Telemetry Transport) is a lightweight publish/subscribe messaging
protocol frequently used in IoT applications. It is a very thin layer over
TCP/IP, and has many implementations. MQTT is even an OASIS
standard [#]_. The Micropython software for ESP8266
includes a client implementation in the ``umqtt`` module [#]_.

Host-side Setup
-----------------

ESP8266 Setup
-------------
On your host machine, go to the ``micropython`` subdirectory of your AntEvents
repository. Run ``mpfshell`` and copy the scripts for WiFi configuration and
MQTT as follows (substituting your tty device name for ``TTYDEVICE``)::

  open TTYDEVICE
  put wifi.py
  put mqtt_writer.py

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


.. [#] http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html

.. [#] The ``umqtt`` module is not in the official Micropython documentation,
       but module is definitely present in the firmware image. The API is simple
       enough that you can understand it by a quick read of the source code:
       https://github.com/micropython/micropython-lib/tree/master/umqtt.simple and
       https://github.com/micropython/micropython-lib/tree/master/umqtt.robust.
