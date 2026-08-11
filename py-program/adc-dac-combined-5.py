import spidev
import time

adc = spidev.SpiDev()
adc.open(0, 0)
adc.max_speed_hz = 8000000
adc.mode = 3
adc.bits_per_word = 8

dac = spidev.SpiDev()
dac.open(0, 1)
dac.max_speed_hz = 8000000
dac.mode = 0
dac.bits_per_word = 8


def adc_transfer(channel):

    command = ((channel & 0x07) << 3) & 0xFF

    return adc.xfer2([command, 0x00])


def adc_code(rx):

    return ((rx[0] & 0x0F) << 8) | rx[1]


def read_adc(channel):

    adc_transfer(channel)

    rx = adc_transfer(channel)

    return adc_code(rx)


def write_dac(value):

    value &= 0x0FFF

    high_byte = (value >> 8) & 0xFF
    low_byte = value & 0xFF

    dac.xfer2([high_byte, low_byte])


try:

    while True:

        adc_value = read_adc(0)

        adc_voltage = adc_value * 5.0 / 4096.0

        write_dac(adc_value)

        dac_voltage = adc_value * 3.3 / 4096.0

        print()
        print("=========== ADC ===========")
        print("Channel : IN0")
        print("Value   :", adc_value)
        print("Voltage : {:.3f} V".format(adc_voltage))

        print()
        print("=========== DAC ===========")
        print("Value   :", adc_value)
        print("Voltage : {:.3f} V".format(dac_voltage))

        print("---------------------------")

        time.sleep(0.5)

except KeyboardInterrupt:

    print("\nStopped.")

finally:

    adc.close()
    dac.close()
