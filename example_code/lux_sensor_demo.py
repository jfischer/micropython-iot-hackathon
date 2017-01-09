# Simple demo of reading the tsl2591 lux sensor from the
# ESP8266 running micropython.
# This just samples the sensor in a loop and prints the
# events.

from antevents import *
from tsl2591 import Tsl2591
tsl = Tsl2591('lux-1')
sched = Scheduler()

sched.schedule_sensor(tsl, 2.0, Output())
sched.run_forever()
