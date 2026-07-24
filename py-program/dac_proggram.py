import pigpio
import time

# Connect to pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("Unable to connect to pigpio daemon")
    exit()

# ----------------------------------
# SPI Pin Configuration
# ----------------------------------
CS   = 8      # Chip Select (SYNC)
MISO = 9      # Not used by DAC121S101
MOSI = 10     # DIN
SCLK = 11     # SCLK

BAUD_RATE = 50000
SPI_MODE = 0

# Open Bit-Banged SPI
pi.bb_spi_open(CS, MISO, MOSI, SCLK, BAUD_RATE, SPI_MODE)

# ----------------------------------
# DAC Value (0 - 4095)
# ----------------------------------
dac_value = 2048      # Mid-scale output

# Create 16-bit command
# DB15-DB14 = Don't Care (0)
# DB13-DB12 = Power Down Bits (00 = Normal Mode)
# DB11-DB0  = 12-bit DAC Data

command = (0x0 << 14) | (dac_value & 0x0FFF)

# Split into two bytes
high_byte = (command >> 8) & 0xFF
low_byte  = command & 0xFF

tx_data = [high_byte, low_byte]

# Send data 10 times
for i in range(10):

    pi.bb_spi_xfer(CS, tx_data)

    print("Transfer :", i + 1)
    print("DAC Value :", dac_value)

    time.sleep(0.5)

# Close SPI
pi.bb_spi_close(CS)
pi.stop()