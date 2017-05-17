# Read from an MQTT queue and write events to Influxdb
import argparse
import asyncio
import time
import sys
from collections import namedtuple


from thingflow.base import Scheduler, SensorEvent
from thingflow.adapters.mqtt import MQTTReader
import thingflow.filters.select # adds select() method
import thingflow.filters.json # adds json() method
from thingflow.adapters.influxdb import InfluxDBWriter

Sensor = namedtuple('Sensor', ['series_name', 'fields', 'tags'])

def setup_flow(args):
    mqtt = MQTTReader(args.mqtt_host, topics=[(args.topic_name, 0),])
    decoded = mqtt.select(lambda m:(m.payload).decode('utf-8'))\
                  .from_json(constructor=SensorEvent)\
                  .select(lambda evt: SensorEvent(sensor_id=evt.sensor_id,
                                                  ts=time.time(),
                                                  val=evt.val))
    decoded.output()
    w = InfluxDBWriter(msg_format=Sensor(series_name=args.influx_measurement,
                                         fields=['val', 'ts'], tags=['sensor_id']),
                       generate_timestamp=False,
                       username=args.influx_username,
                       password=args.influx_password,
                       database=args.influx_database)
    decoded.connect(w)
    return mqtt

def main():
    parser = argparse.ArgumentParser(description="Subscribe to the specified topic and write the resulting messages to Influxdb")
    parser.add_argument('--mqtt-host', type=str, default='localhost',
                        help="Hostname or IP address of MQTT broker (defaults to localhost)")
    parser.add_argument('--topic-name', type=str, default='sensor-data',
                        help="Topic for subscription (defaults to sensor-data)")
    parser.add_argument('--influx-host', type=str, default='localhost',
                        help="Influx db host (defaults to localhost)")
    parser.add_argument('--influx-username', type=str, default='root',
                        help="Influx db username (defaults to root)")
    parser.add_argument('--influx-password', type=str, default=None,
                        help="Influx db password (defaults to None)")
    parser.add_argument('--influx-database', type=str, default='sensor-data',
                        help="Influx db database (defaults to sensor-data)")
    parser.add_argument('--influx-measurement', type=str, default='lux',
                        help="Influx db measurement (defaults to lux)")
    args = parser.parse_args()
    mqtt = setup_flow(args)
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
                        
