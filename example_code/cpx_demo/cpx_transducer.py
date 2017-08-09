'''Implement CircuitPlayground Express (CPX) ThingFlow 
   sensors and transducers'''

from thingflow.base import InputThing, SensorAsOutputThing
from cpx_driver import CPX, vumeter

cpx = None

def init_cpx(devname='/dev/tty.usbmodem1451'):
    '''Initialize cpx. Use '/dev/ttyACM0' on linux'''
    global cpx
    cpx = CPX(devname)

def check_cpx_initialized():
    if not cpx:
        raise Exception('CPX board was not initialized.\n'
            'Call transducer.init_cpx function to initialize CPX board.')


class LightSensor(SensorAsOutputThing):
    '''Create a Circuit Playground LightSensor'''
    def __init__(self, sensor_id='lux'):
        check_cpx_initialized()
        super().__init__(self)
        self.sensor_id = sensor_id  # Required by SensorAsOutputThing
    def sample(self):
        return cpx.light


class RingInputThing(InputThing):
    def __init__(self, *args, **kwargs):
        '''Ensure the underlying CPX has been initialized'''
        check_cpx_initialized()
        super().__init__()

    def on_next(self, evt):
        '''Display on neopixels the 0 <= level <= 255 transformation to a
           pretty intensity colorwheel (ore pixels light-up varying in
           intensity and turning from red to blue.
        '''
        level = evt.val
        cpx.neopixel(buf=vumeter(level))

