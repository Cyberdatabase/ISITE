Test Program (Slow SPI for CRO Observation)

import spidev
import time

spi = spidev.SpiDev()

# Bus 0, Device 0 (CE0)
spi.open(0, 0)

# Slow SPI speed for CRO
spi.max_speed_hz = 10000      # 10 kHz
spi.mode = 0
spi.bits_per_word = 8

print("SPI Started")

for i in range(20):

    # Read Channel 0
    tx = [0x00, 0x00]
    rx = spi.xfer2(tx)

    adc = ((rx[0] & 0x0F) << 8) | rx[1]

    print(f"Transfer {i+1}: {rx}  ADC = {adc}")

    time.sleep(1)

spi.close()
