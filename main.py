#!/usr/bin/python3
# -*- coding:utf-8 -*-

import signal
import socket

from PIL import Image, ImageDraw, ImageFont

from oled import config, olde


def get_host_ip():
    ip = "x.x.x.x"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        print(e)
    finally:
        s.close()
    return ip

font = ImageFont.truetype('/home/pi/workspace/Oled/fonts/Font.ttc', 20)
oled = olde.Oled()


def handler(signum, frame):
    print(f'Signal handler called with signal {signum}')
    oled.teardown()
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    ip = get_host_ip()
    oled.setup()
    oled.clear()

    while True:
        image = Image.new('1', (config.WIDTH, config.HEIGHT), "WHITE")
        draw = ImageDraw.Draw(image)
        draw.line([(0, 0), (127, 0)], fill=0)
        draw.line([(0, 0), (0, 31)], fill=0)
        draw.line([(0, 31), (127, 31)], fill=0)
        draw.line([(127, 0), (127, 31)], fill=0)
        draw.text((2, 16), ip, font=font, fill=0)
        oled.show(image)
        oled.delay(10000)
        ip = get_host_ip()
