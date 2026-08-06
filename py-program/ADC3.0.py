import spidev
import time

# Create SPI object
spi = spidev.SpiDev()

# Open SPI bus 0, chip select CE0
spi.open(0, 0)

# SPI configuration
spi.max_speed_hz = 100000      # 100 kHz
spi.mode = 0

def read_adc(channel):
    """
    Read ADC128S102 channel (0-7)
    """

    # Build command
    tx = [(channel & 0x07) << 3, 0x00]

    # SPI transfer
    rx = spi.xfer2(tx)

    # Convert received bytes to 12-bit value
    value = ((rx[0] & 0x0F) << 8) | rx[1]

    return value

# Dummy conversion
spi.xfer2([0x00, 0x00])

try:

    while True:

        adc = read_adc(0)

        voltage = adc * 5.0 / 4095

        print("---------------------")
        print("ADC Value :", adc)
        print("Voltage   : {:.3f} V".format(voltage))

        time.sleep(0.5)

finally:

    spi.close()
