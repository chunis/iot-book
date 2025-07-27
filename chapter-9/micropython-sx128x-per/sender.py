#!/usr/bin/python

# Dennis Deng (ddeng@semtech.com)

import sys
from machine import Pin
from time import sleep

import sx1280
import common_config

if sys.platform == 'pyboard':
    from pyb import Timer
else:
    from machine import Timer


if sys.platform == 'pyboard':
    tx_led = Pin('PC1', Pin.OUT)
elif sys.platform == 'esp32':
    tx_led = Pin(0, Pin.OUT)
else:  # define 2 dull functions to by pass led control
    def tx_led(val): pass

tx_led(0)

# data format (len = 16): 'P', 'E', R', N1, N2, \x05, \x06, ..., \x0f
data = list(common_config.data)
data[:3] = [ord(x) for x in 'PER']
cnt = 0
def tx_beacon(timer):
    global cnt
    print("enter tx_beacon()")

    sx1280.sx128x_clear_irq_status(None, sx1280.SX128X_IRQ.ALL)

    cnt += 1
    data[3] = cnt // 256
    data[4] = cnt % 256
    print('data:', data)
    sx1280.sx128x_write_buffer(None, common_config.tx_base_address, data, len(data))
    sx1280.sx128x_set_tx(None, 0, 0)

    while sx1280.sx128x_get_irq_pin_status(None) == False:
        sleep(0.01)

    tx_led(1); sleep(0.001); tx_led(0)


def start():
    freq = 5
    if sys.platform == 'pyboard':
        from micropython import schedule
        tim = Timer(4, freq=10)
        tim.init(freq=5, callback=lambda x: schedule(tx_beacon, x))
    elif sys.platform == 'esp32':
        tim = Timer(0)
        tim.init(period=int(1000/freq), mode=Timer.PERIODIC, callback=tx_beacon)
    else:
        print("platform '%s' doesn't support" %sys.platform)

start()
