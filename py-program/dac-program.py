import time
import spidev

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device (CE) 0
spi.max_speed_hz = 1000000  # Set clock speed to 1MHz
spi.mode = 0  # SPI Mode 0


def set_voltage(value):
  """Sends a 12-bit value (0 to 4095) to the DAC121S101."""
  # Ensure value is within 12-bit range
  value = max(0, min(4095, value))

  # Format 16-bit packet: 4 leading zeros + 12-bit data value
  # Split into two 8-bit bytes (high byte and low byte)
  high_byte = (value >> 8) & 0x0F  # Top 4 bits are 0
  low_byte = value & 0xFF

  # Transfer data via SPI
  spi.xfer2([high_byte, low_byte])


try:
  print("Testing DAC121S101. Press Ctrl+C to stop.")
  while True:
    # Output mid-scale voltage (~1.65V if supplied with 3.3V)
    print("Setting DAC to mid-scale (2048)")
    set_voltage(2048)
    time.sleep(2)

    # Output full-scale voltage (~3.3V)
    print("Setting DAC to full-scale (4095)")
    set_voltage(4095)
    time.sleep(2)

    # Output zero volts
    print("Setting DAC to 0V (0)")
    set_voltage(0)
    time.sleep(2)

except KeyboardInterrupt:
  spi.close()
  print("\nProgram stopped and SPI closed.")

