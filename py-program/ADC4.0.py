import spidev
import time

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)

spi.max_speed_hz = 100000   # 100 kHz
spi.mode = 0                # SPI Mode 0


def read_adc(channel):

    # Select ADC channel
    tx = [(channel & 0x07) << 3, 0x00]

    # SPI transfer
    rx = spi.xfer2(tx)

    # Convert 12-bit ADC data
    value = ((rx[0] & 0x0F) << 8) | rx[1]

    return value


# Dummy conversion
spi.xfer2([0x00, 0x00])


try:
    while True:

        for channel in range(8):

            adc_value = read_adc(channel)

            voltage = adc_value * 5.0 / 4095

            print("IN{}  ADC: {}  Voltage: {:.3f} V"
                  .format(channel, adc_value, voltage))

        print("----------------------")

        time.sleep(0.5)


finally:
    spi.close()
