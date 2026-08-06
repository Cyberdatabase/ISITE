import spidev
import time

spi = spidev.SpiDev()

spi.open(0, 0)

spi.max_speed_hz = 100000

spi.mode = 0


def read_adc(channel):

    # Build the two-byte command.
    # The channel number (0-7) is placed in bits D13:D11.
    tx = [(channel & 0x07) << 3, 0x00]

    # Send the command while receiving two bytes.
    rx = spi.xfer2(tx)

    # Extract the 12-bit ADC value.
    value = ((rx[0] & 0x0F) << 8) | rx[1]

    return value


# The first transfer starts a conversion.
# Its returned data is not yet the requested result.
spi.xfer2([0x00, 0x00])

try:

    while True:

        adc_value = read_adc(0)

        voltage = adc_value * 3.3 / 4095

        print("ADC =", adc_value)

        print("Voltage = {:.3f} V".format(voltage))

        print("-----------------------")

        time.sleep(0.5)

finally:

    spi.close()
