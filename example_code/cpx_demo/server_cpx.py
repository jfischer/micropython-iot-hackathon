'''Drive a CircuitPlayground Express neopixel ring with wireless
MQTTReader data from an analog to digital conversor.
Run this program on the MQTT broker host with::

    python server_cpx.py
'''

import asyncio
import thingflow.filters.map   # adds map() method
import thingflow.filters.json  # adds json() method
from thingflow.base import Scheduler, SensorEvent
from thingflow.adapters.mqtt import MQTTReader
from cpx_transducer import RingInputThing, init_cpx

def setup_flow(topic):
    mqtt = MQTTReader('localhost', topics=[(topic, 0),])
    ring = RingInputThing()
    decoded = (mqtt
        .map(lambda m:(m.payload).decode('utf-8'))
        .from_json(constructor=SensorEvent)
        .map(lambda evt: SensorEvent(sensor_id=evt.sensor_id,
            ts=evt.ts, val=int(evt.val * 255))))
    decoded.output()
    decoded.connect(ring)
    return mqtt


init_cpx()
mqtt = setup_flow('sensor-data')

scheduler = Scheduler(asyncio.get_event_loop())
scheduler.schedule_on_private_event_loop(mqtt)
scheduler.run_forever()
