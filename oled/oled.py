from . import config
from smbus import SMBus
import time

def Oled():
    def __init__(self):
        self.bus = SMBus(1)

    def command(self, cmd):
        bus.write_byte_data(config.ADDRESS, 0x00, cmd)

    def data(self, data):
        bus.write_byte_data(config.ADDRESS, 0x40, data)

    def delay(self, ms):
        time.sleep(ms / 1000.0)

    def setup():
        self.command(0xAE)
        self.command(0x40)
        self.command(0xB0)
        self.command(0xC8)
        self.command(0x81)
        self.command(0xff)
        self.command(0xa1)
        self.command(0xa6)
        self.command(0xa8)
        self.command(0x1f)
        self.command(0xd3)
        self.command(0x00)
        self.command(0xd5)
        self.command(0xf0)
        self.command(0xd9)
        self.command(0x22)
        self.command(0xda)
        self.command(0x02)
        self.command(0xdb)
        self.command(0x49)
        self.command(0x8d)
        self.command(0x14)

        self.delay(200)
        self.command(0xaf)

    def show(self, image):
        buf = [0xff] * (config.PAGE * config.COLUMN)
        pixels = image.load()
        for y in range(config.HEIGHT):
            for x in range(config.WIDTH):
                if pixels[x, y] == 0:
                    buf[x + int(y / 8) * config.WIDTH] &= ~(1 << (y % 8))
        for x in range(config.PAGE * config.COLUMN):
            buf[x] = ~buf[x]
        for i in range(config.PAGE):
            self.command(0xB0 + i)
            self.command(0X00)
            self.command(0x10)
            for j in range(config.COLUMN):
                self.data(buf[j + config.WIDTH * i])

    def clear(self):
        buf = [0x00] * (config.PAGE * config.COLUMN)
        for i in range(config.PAGE):
            self.command(0xB0 + i)
            self.command(0X00)
            self.command(0x10)
            for j in range(config.COLUMN):
                self.data(buf[j + config.WIDTH * i])

    def teardown(self):
        self.clear()
        self.bus.close()