#!/usr/bin/python

# Dennis Deng (ddeng@semtech.com)

import sys
from machine import Pin
from time import sleep

import sx1280
import common_config


rcv_cnt = 0
def rx():
    global rcv_cnt
    #print("enter rx()")

    sx1280.sx128x_set_rx(None, 0, 0)
    while sx1280.sx128x_get_irq_pin_status(None) == False:
        sleep(0.01)

    irq_val = bytearray(2)
    sx1280.sx128x_get_irq_status(None, irq_val)
    sx1280.sx128x_clear_irq_status(None, sx1280.SX128X_IRQ.ALL)
    irq_val = irq_val[1] << 8 | irq_val[0]
    print('\nrecv: irq_val = ', bin(irq_val))

    if irq_val == 0x2:  # rx_done
        lora_status = sx1280.sx128x_pkt_status_lora_t()
        sx1280.sx128x_get_lora_pkt_status(None, lora_status)

        rx_status = sx1280.sx128x_rx_buffer_status_t()
        sx1280.sx128x_get_rx_buffer_status(None, rx_status)

        rx_buf = bytearray(rx_status.pld_len_in_bytes)
        sx1280.sx128x_read_buffer(None, rx_status.buffer_start_pointer, rx_buf, rx_status.pld_len_in_bytes)

        print(f'rssi ={lora_status.rssi}, snr = {lora_status.snr}, buf len = {len(rx_buf)}')
        print('rx_buf:', rx_buf)
        if rx_buf[:3] == b'PER' and rx_buf[5:] == bytearray(range(5, 16)):
            print("Match value")
            rx_led(1); sleep(0.001); rx_led(0)
            cnt = rx_buf[3] * 256 + rx_buf[4]
            rcv_cnt += 1
            lost = cnt - rcv_cnt
            print("#send = %d, #recv = %d, #lost = %d" %(cnt, rcv_cnt, lost))


if sys.platform == 'pyboard':
    rx_led = Pin('PC0', Pin.OUT)
elif sys.platform == 'esp32':
    rx_led = Pin(1, Pin.OUT)
else:  # define 2 dull functions to by pass led control
    def rx_led(val): pass

rx_led(0)

print("I'm Rx")
while True:
    #print('\nloop again...')
    rx()
