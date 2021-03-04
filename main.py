#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from util.oled import OLED_0in91
from PIL import Image, ImageDraw, ImageFont
import socket
import signal

font1 = ImageFont.truetype('/home/pi/workspace/oled/Font.ttc', 12)
disp = OLED_0in91()


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def update_screen(t):
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)

    draw.line([(0, 0), (127, 0)], fill=0)
    draw.line([(0, 0), (0, 31)], fill=0)
    draw.line([(0, 31), (127, 31)], fill=0)
    draw.line([(127, 0), (127, 31)], fill=0)

    draw.text((12, 3), 'Current IP Address', font=font1, fill=0)
    draw.text((20, 15), get_host_ip(), font=font1, fill=0)

    disp.show_image(disp.getbuffer(image))

    time.sleep(t)
    disp.clear()


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    disp.teardown()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handler)

    disp.init()
    disp.clear()

    try:
        while True:
            update_screen(60)

    except KeyboardInterrupt:
        print("ctrl + c:")
        disp.teardown()
        exit()
