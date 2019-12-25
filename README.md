# ADS1115

This project contains a python file that allows microprocessors to communicate with ADS1115 under I2C protocol. The program only requires 2 libraries, busio and board. (Although the time library is imported, it serves no function in the method).

The method takes 1 argument and outputs 1 value in an array.
The input argument should be one of the eight modes of ADS1115 pin selection. For details, please refer to page 19 of TI's Ultra-Small, Low-Power, 16-Bit ADC with Internal Reference (Rev. B) https://cdn-shop.adafruit.com/datasheets/ads1115.pdf

NOTE 1: The BBGW user must change python3.5/dist-package/board.py line 55 from "BEAGLEBONE_BLACK" to "BEAGLEBONE_GREEN_WIRELESS" to avoid "board not support" error caused by board.py.
