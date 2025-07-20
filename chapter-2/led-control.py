#!/usr/bin/python3

# Chunis Deng (chunchengfh@gmail.com)

from machine import Pin
from utime import sleep_ms

user_led = Pin('PA5', Pin.OUT)
user_btn = Pin('PC13', Pin.IN)
press_flag = False

while True:
    if user_btn.value() == 0:
        if press_flag == False:
            press_flag = True
            user_led.on()
            print('pressed')
    else:
        if press_flag == True:
            press_flag = False
            user_led.off()
            print('released')
	sleep_ms(100)
