import spidev
import time

# ADC on CE0
adc = spidev.SpiDev()
adc.open(0, 0)
adc.max_speed_hz = 100000
adc.mode = 0

# DAC on CE1
dac = spidev.SpiDev()
dac.open(0, 1)
dac.max_speed_hz = 100000
dac.mode = 0


def read_adc(channel):

    tx = [(channel & 0x07) << 3, 0x00]

    rx = adc.xfer2(tx)

    value = ((rx[0] & 0x0F) << 8) | rx[1]

    return value


def write_dac(value):

    value &= 0x0FFF

    command = value << 2

    high = (command >> 8) & 0xFF
    low = command & 0xFF

    dac.xfer2([high, low])


# Dummy conversion
adc.xfer2([0x00, 0x00])

try:

    while True:

        adc_value = read_adc(0)

        write_dac(adc_value)

        voltage = adc_value * 5.0 / 4096

        print("ADC :", adc_value)
        print("DAC :", adc_value)
        print("Voltage : {:.3f} V".format(voltage))
        print("------------------------")

        time.sleep(0.2)

finally:

    adc.close()
    dac.close()
