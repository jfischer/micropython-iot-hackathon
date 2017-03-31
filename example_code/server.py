# Main program to run on host that is running the MQTT broker
# It reads from the specified port and writes to a CSV file.
import argparse
import asyncio
import time
import sys

from thingflow.base import Scheduler, SensorEvent
from thingflow.adapters.mqtt import MQTTReader
import thingflow.adapters.csv # adds csv_writer() method
import thingflow.filters.select # adds select() method
import thingflow.filters.json # adds json() method

def setup_flow(topic, filename):
    mqtt = MQTTReader('localhost', topics=[(topic, 0),])
    decoded = mqtt.select(lambda m:(m.payload).decode('utf-8'))\
                  .from_json(constructor=SensorEvent)\
                  .select(lambda evt: SensorEvent(sensor_id=evt.sensor_id,
                                                  ts=time.time(),
                                                  val=evt.val))
    decoded.output()
    decoded.csv_writer(filename)
    return mqtt

def main():
    parser = argparse.ArgumentParser(description="Subscribe to the specified port and write the resulting messages")
    parser.add_argument('topic_name', metavar='TOPIC_NAME', type=str,
                        help="Topic for subscription")
    parser.add_argument('csv_filename', metavar="CSV_FILENAME", type=str,
                        help="Name of CSV file to write with sensor data")
    args = parser.parse_args()
    mqtt = setup_flow(args.topic_name, args.csv_filename)
    scheduler = Scheduler(asyncio.get_event_loop())
    stop = scheduler.schedule_on_private_event_loop(mqtt)
    print("Running main loop")
    try:
        scheduler.run_forever()
    except KeyboardInterrupt:
        print("Stopping...")
        stop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
                        
