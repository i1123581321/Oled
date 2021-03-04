#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from util.oled import OLED_0in91
from PIL import Image, ImageDraw, ImageFont
import signal
from get_info import get_host_ip, get_weather

screen_update_time = 10
ip_update_time = 60
weather_update_time = 600
F = True

L_weather = ""
Q_weather = ""
ip = ""

font = ImageFont.truetype('/home/pi/workspace/Oled/Font.ttc', 12)
disp = OLED_0in91()


def update_screen(t, flag):
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)

    draw.line([(0, 0), (127, 0)], fill=0)
    draw.line([(0, 0), (0, 31)], fill=0)
    draw.line([(0, 31), (127, 31)], fill=0)
    draw.line([(127, 0), (127, 31)], fill=0)
    draw.text((12, 3), L_weather if F else Q_weather, font=font, fill=0)
    draw.text((25, 16), ip, font=font, fill=0)

    disp.show_image(disp.getbuffer(image))

    time.sleep(t)
    disp.clear()


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    disp.teardown()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handler)
    Q_weather = get_weather("Q")
    L_weather = get_weather("L")
    ip = get_host_ip()

    ip_cnt = 0
    weather_cnt = 0

    disp.init()
    disp.clear()

    try:
        while True:
            update_screen(screen_update_time, F)
            F = not F
            ip_cnt += screen_update_time
            weather_cnt += screen_update_time
            if ip_cnt == ip_update_time:
                ip_cnt = 0
                ip = get_host_ip()
            if weather_cnt == weather_update_time:
                weather_cnt = 0
                Q_weather = get_weather("Q")
                L_weather = get_weather("L")

    except KeyboardInterrupt:
        print("ctrl + c:")
        disp.teardown()
        exit()
