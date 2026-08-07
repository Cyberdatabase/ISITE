import spidev
import time

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)

spi.max_speed_hz = 100000
spi.mode = 0


def write_dac(value):
    """
    Write 12-bit value to DAC121S101

    value : 0 - 4095
    """

    value &= 0x0FFF

    command = value << 2

    high_byte = (command >> 8) & 0xFF
    low_byte = command & 0xFF

    spi.xfer2([high_byte, low_byte])


try:

    while True:

        for value in range(0, 4096, 256):

            write_dac(value)

            voltage = value * 5.0 / 4096

            print("DAC Value :", value)
            print("Output Voltage : {:.3f} V".format(voltage))
            print("---------------------")

            time.sleep(1)

finally:

    spi.close()
