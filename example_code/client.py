# Main program for ESP8266 to sample light sensor and send sensor events
# to an MQTT broker.


# Configuration is stored in a separate config.py
from config import SENSOR_ID, WIFI_ESSID, WIFI_PASSWORD, MQTT_HOST,\
                   MQTT_TOPIC, SLEEP_TIME

from wifi import wifi_connect, disable_wifi_ap
from thingflow import *
from tsl2591 import Tsl2591
from mqtt_writer import MQTTWriter

# setup network
disable_wifi_ap()
wifi_connect(WIFI_ESSID, WIFI_PASSWORD)

# create objects
m =  MQTTWriter(SENSOR_ID, MQTT_HOST, 1883, MQTT_TOPIC)
tsl = Tsl2591(SENSOR_ID)
sched = Scheduler()

# schedule and run
sched.schedule_sensor(tsl, SLEEP_TIME, m)
print("Running main loop with sample every %s seconds..." % SLEEP_TIME)
sched.run_forever()

