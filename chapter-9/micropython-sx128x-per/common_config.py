#!/usr/bin/python

# Dennis Deng (ddeng@semtech.com)


import sx1280


data = range(16)
power_in_dbm = 8
freq = 2405000000


# sx128x init
sx1280.sx128x_gpio_spi_init()
sx1280.sx128x_hal_reset(None)

sx1280.sx128x_set_standby(None, sx1280.SX128X_STANDBY_CFG.XOSC)
sx1280.sx128x_set_lna_settings(None, sx1280.SX128X_LNA.LOW_POWER_MODE)
sx1280.sx128x_set_reg_mode(None, sx1280.SX128X_REG_MODE.DCDC)

sx1280.sx128x_set_pkt_type(None, sx1280.SX128X_PKT_TYPE.LORA)

modpara = sx1280.sx128x_mod_params_lora_t()
modpara.sf = sx1280.SX128X_LORA_RANGING.SF7
modpara.bw = sx1280.SX128X_LORA_RANGING_BW._400
modpara.cr = sx1280.SX128X_LORA_RANGING_CR._4_5
sx1280.sx128x_set_lora_mod_params(None, modpara)

pktpara = sx1280.sx128x_pkt_params_lora_t()
pktpara.preamble_len.mant = 12
pktpara.preamble_len.exp = 0
pktpara.pld_len_in_bytes = len(data)
pktpara.header_type = sx1280.SX128X_LORA_RANGING_PKT.EXPLICIT
pktpara.crc_is_on = True
pktpara.invert_iq_is_on = True
sx1280.sx128x_set_lora_pkt_params(None, pktpara)

# set up irq
irqflags = sx1280.SX128X_IRQ.RX_DONE | sx1280.SX128X_IRQ.TX_DONE | sx1280.SX128X_IRQ.TIMEOUT
sx1280.sx128x_set_dio_irq_params(None, irqflags, irqflags, sx1280.SX128X_IRQ.NONE, sx1280.SX128X_IRQ.NONE)

sx1280.sx128x_set_rf_freq(None, freq)
sx1280.sx128x_set_tx_params(None, power_in_dbm, sx1280.SX128X_RAMP._20_US)

tx_base_address = 0x80
rx_base_address = 0x00
sx1280.sx128x_set_buffer_base_address(None, tx_base_address, rx_base_address)
sx1280.sx128x_write_buffer(None, tx_base_address, data, len(data))
