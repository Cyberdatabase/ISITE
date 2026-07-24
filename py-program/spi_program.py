import pigpio
import time

# Connect to pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("Unable to connect to pigpio daemon")
    exit()

# -----------------------------
# Bit-Banged SPI Configuration
# -----------------------------
CS   = 8      # Chip Select
MOSI = 10
MISO = 9
SCLK = 11

BAUD = 50000
SPI_MODE = 0

# Open Bit-Banged SPI
pi.bb_spi_open(CS, MISO, MOSI, SCLK, BAUD, SPI_MODE)

# Data to transmit (example)
value_16bit = 0xABCD

high_byte = (value_16bit >> 8) & 0xFF
low_byte  = value_16bit & 0xFF

tx_data = [high_byte, low_byte]

# Transfer 10 times
for i in range(10):

    count, rx_data = pi.bb_spi_xfer(CS, tx_data)

    print("Transfer :", i + 1)
    print("Bytes Received :", count)
    print("Raw Data :", rx_data)

    time.sleep(0.5)

# Close SPI
pi.bb_spi_close(CS)
pi.stop()