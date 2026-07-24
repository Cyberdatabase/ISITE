import pigpio
import time

pi = pigpio.pi()

if not pi.connected:
    print("pigpio not connected")
    exit()

CS = 8
MOSI = 10
MISO = 9
SCLK = 11

pi.bb_spi_open(CS, MISO, MOSI, SCLK, 50000, 0)

for i in range(10):

    # Select Channel 0
    tx = [0x00, 0x00]

    count, rx = pi.bb_spi_xfer(CS, tx)

    # Convert received bytes into 12-bit ADC value
    adc_value = ((rx[0] & 0x0F) << 8) | rx[1]

    print("Reading", i + 1)
    print("ADC Value =", adc_value)

    time.sleep(0.5)

pi.bb_spi_close(CS)
pi.stop()