# This code enables ADS1115 to communicate with a microprocessor
# with I2C protcol using only SMBus library.
# Version 0: written by Ruochen Wang - EML UMD, 2019-12-23
# Version 1: written by Ruochen Wang - EML UMD, 2019-12-24

# v1 update: SMBus read/write is not wroking for some reasons
# switch to board and busio

import time
import board
import busio

# constant initialization
DEFAULT_ADDR        = 0x48          # address is default to 0x48 when ADDR=GND
POINTER_CONVER      = 0x00          # sets the pointer to CONV_REG
POINTER_CONFIG      = 0x01          # sets the pointer to CONFIG_REG
MUX_OFFSET          = 0xC           # sel. pin CONFIG_REG[14:12]
COMP_QUE_DISABLE    = 0x0003        # CONFIG_REG[1:0]
DT_RATE_128         = 0x0080        # CONFIG_REG[7:5]
SINGLE_MODE         = 0x0100        # CONFIG_REG[8]
CONT_MODE           = 0x0000        # CONFIG_REG[8]
GAIN_1              = 0x0200        # CONFIG_REG[11:9]
OS_SINGLE           = 0x8000        # single-shot CONFIG[15]
#PIN0                = 0x4           # using pin 0 (AIN0)

def get_voltage(pin_mux=0x0):
    # construct configuration for CONFIG_REG
    # read procedure
    # 1. config CONFIG_REG
    # 2. sel conversion reg
    # 3. read 

    # we construct the config register here to ensure the correct sampling 
    # configeration and allow us to change the configeration more easily
    i2c = busio.I2C(board.SCL, board.SDA)
    config = (OS_SINGLE | (pin_mux<<MUX_OFFSET) | GAIN_1 | CONT_MODE | DT_RATE_128 | COMP_QUE_DISABLE) 

    # construct writing sequence
    # write in each element seperately to ensure 
    # that all para. are bytes
    write_sequence = bytearray(3)
    write_sequence[0] = POINTER_CONFIG 
    write_sequence[1] = (config>>8)&0xFF    # MSB will not be write in 
    write_sequence[2] = config&0xFF

    # write config
    i2c.writeto(DEFAULT_ADDR, write_sequence)

    # sel conversion reg in pointer reg
    # with SMBus(2) as bus:
    i2c.writeto(DEFAULT_ADDR, bytes([POINTER_CONVER]))

    # read
    # with SMBus(2) as bus:
    data_block = bytearray(2)   # for 1 16-bit output 
    i2c.readfrom_into(DEFAULT_ADDR, data_block)
    data = (data_block[0]<<8)|data_block[1]
    volts = data*4.096/32767    # 4.096: when gain = 1

    return [volts]


if __name__=='__main__':
    while True:
        val = get_voltage(4)
        print(val[0])
        time.sleep(1)

