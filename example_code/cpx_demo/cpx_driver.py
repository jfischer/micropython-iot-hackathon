'''Circuit Playground Express (CPX) REPL driver

Run this module on a host computer with CPX plugged in a USB port::

    import cpx_driver

    cpx = cpx_driver.CPX()
    cpx.light                                  # Get light sensor data
    cpx.neopixel(rgb=(0, 10, 0))               # Turn all neopixels green
    cpx.neopixel(buf=cpx_driver.vumeter(255))  # Turn neopixels as max vumeter
'''

# author:      Daniel Mizyrycki
# license:     MIT
# repository:  https://github.com/mzdaniel/micropython-iot

import serial
import itertools

class Serial:
    '''Drive serial communication'''

    def __init__(self, dev_file):
        self.prompt = '>>> '
        self.serial = serial.Serial(dev_file, baudrate=115200, rtscts=True,
            timeout=0.01)

    def read(self):
        data = self.serial.readall().decode()
        if data[-len(self.prompt):] == self.prompt:
            data = data[:-len(self.prompt)]
        return data

    def write(self, data):
        self.serial.write((data + '\r\n').encode())
        self.serial.flush()
        self.serial.readline()

    def flush(self):
        self.serial.flush()
        data = self.serial.readall().decode()
        if data[-4:] != self.prompt:
            pass  # handle condition if we didn't get prompt


class CPX:
    '''Circuit Playground Driver'''
    pixel_count = 10
    dev_file='/dev/ttyACM0'

    def __init__(self, dev_file=dev_file):
        ''' SerialException conditions:
                Device or resource busy: '/dev/ttyACM0'
                No such file or directory: '/dev/ttyACM0'
        '''
        self.serial = Serial(dev_file)
        self.send_nores('')  # CPX require a new line to enter REPL
        self.send_nores('import analogio, digitalio, board')
        self.send_nores('light = analogio.AnalogIn(board.LIGHT)')
        self.send_nores('from neopixel_write import neopixel_write')
        self.send_nores('neopixel_pin = digitalio.DigitalInOut(board.NEOPIXEL)')
        self.send_nores('neopixel_pin.direction = digitalio.Direction.OUTPUT')
        self.send_nores('neopixel = lambda buf: neopixel_write(neopixel_pin, buf)')
        self.neopixel_buf = bytearray(self.pixel_count * 3)  # 10 neopixels with 3 bytes per pixel

    def send_nores(self, line):
        self.serial.write(line)
        self.serial.read()

    def send_res(self, line):
        self.serial.write(line)
        return self.serial.read()

    def send_res_int(self, line):
        return int(self.send_res(line))

    @property
    def light(self):
        '''Get Light sensor data'''
        return self.send_res_int('light.value')

    def neopixel(self, rgb=None, pix_nr=None, buf=None):
        ''' Drive neopixel ring
            if no pix_nr is given, use rgb on all pixels
            use buf if no rgb or pix_nr are given'''
        if buf:  # Prepare buf for CPX  (it uses grb)
            buf = [i for i in buf]
            buf = tuple(itertools.chain(*zip(buf[1::3], buf[0::3], buf[2::3])))
        if not rgb and pix_nr is None and buf:
            self.send_nores('neopixel(bytearray(%s))' % str(buf))
            self.neopixel_buf = bytearray(buf)
        elif rgb and pix_nr is None:
            rgb = (rgb[1], rgb[0], rgb[2])
            self.send_nores('neopixel(bytearray(%s*%s))' % (
                str(rgb), self.pixel_count))
            self.neopixel_buf = bytearray(rgb * self.pixel_count)
        elif rgb and pix_nr is not None:
            rgb = [rgb[1], rgb[0], rgb[2]]
            buf = [i for i in self.neopixel_buf]
            buf = buf[:pix_nr*3] + rgb + buf[(pix_nr+1)*3:]
            self.send_nores('neopixel(bytearray(%s))' % str(buf))
            self.neopixel_buf = bytearray(buf)


def vumeter(level, pixel_count=CPX.pixel_count, bright_coef=0.05):
    '''Return a vumeter neopixel buffer based on level 0-255
       bright_coef is used to dim cpx bright neopixels'''

    def clamp(n, min, max):
        '''Return   n if min <= n <= max
                  min if n < min
                  max if n > max
        '''
        return sorted((min, n, max))[1]

    def wheel(level):
        '''Convert a linear level into rgb color tuple
        >>> level_to_rgb(0)
        (255, 0, 0)
        >>> level_to_rgb(127)
        (1, 254, 0)
        >>> level_to_rgb(128)
        (0, 255, 0)
        >>> level_to_rgb(255)
        (0, 1, 254)
        >>> level_to_rgb(256)
        (0, 0, 255)
        '''
        level = clamp(level, 0, 256)
        if level < 128:
            return (255-level*2, level*2, 0)
        elif level < 256:
            level -= 128
            return (0, 255-level*2, level*2)
        else:
            return (0, 0, 255)

    def level_to_rgb(level, brightness=1):
        '''Transform level to rgb for strip sensor
           0 <= level <= 255'''
        brightness = clamp(brightness, 0, 1)
        rgb = tuple(int(c*brightness*bright_coef) for c in wheel(level))
        return rgb

    def vumeter_brightness(level, pixel_count=pixel_count):
        '''Transform level to a vumeter brightness
        >>> brightness(0, 10)
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> brightness(1, 10)
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> brightness(25, 10)
        [250, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> brightness(26, 10)
        [255, 5, 0, 0, 0, 0, 0, 0, 0, 0]
        >>> brightness(255, 10)
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        '''
        coef = 255/pixel_count
        return [0 if level < coef*i else
            255 if coef*(i+1) <= level else
            int(level%coef*10) for i in range(10)]

    colors = [int(i*256/pixel_count) for i in range(pixel_count)]
    buf = bytearray(sum((level_to_rgb(level=c, brightness=b/255)
        for c, b in zip(colors, vumeter_brightness(level))), ()))
    return buf
