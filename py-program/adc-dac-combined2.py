import spidev
import time

# -----------------------------
# ADC (CE0)
# -----------------------------
adc = spidev.SpiDev()
adc.open(0, 0)
adc.max_speed_hz = 100000
adc.mode = 0

# -----------------------------
# DAC (CE1)
# -----------------------------
dac = spidev.SpiDev()
dac.open(0, 1)
dac.max_speed_hz = 100000
dac.mode = 0


def read_adc(channel):
    """Read ADC128S102 channel (0-7)."""

    tx = [(channel & 0x07) << 3, 0x00]
    rx = adc.xfer2(tx)

    value = ((rx[0] & 0x0F) << 8) | rx[1]

    return value


def write_dac(value):
    """Write a 12-bit value (0-4095) to the DAC121S101."""

    value &= 0x0FFF

    command = value << 2

    high_byte = (command >> 8) & 0xFF
    low_byte = command & 0xFF

    dac.xfer2([high_byte, low_byte])


# Dummy conversion for ADC
adc.xfer2([0x00, 0x00])


try:

    while True:

        print("\n========== ADC Readings ==========")

        adc_values = []

        # Read all 8 ADC channels
        for channel in range(8):

            adc_value = read_adc(channel)
            adc_values.append(adc_value)

            voltage = adc_value * 5.0 / 4095

            print(
                "IN{} : ADC = {:4d}   Voltage = {:.3f} V"
                .format(channel, adc_value, voltage)
            )

        # ---------------------------------
        # Send IN0 value to DAC
        # ---------------------------------
        dac_value = adc_values[0]

        write_dac(dac_value)

        dac_voltage = dac_value * 5.0 / 4095

        print("\n========== DAC Output ==========")
        print("Source Channel : IN0")
        print("DAC Value      :", dac_value)
        print("Output Voltage : {:.3f} V".format(dac_voltage))

        print("----------------------------------------")

        time.sleep(0.5)

finally:

    adc.close()
    dac.close()
