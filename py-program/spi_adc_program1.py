import time
import spidev

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)              # Bus 0, Device (CE) 0
spi.max_speed_hz = 1000000  # Max frequency for ADC128S102 (typically 0.8MHz - 3.2MHz)
spi.mode = 0                # SPI Mode 0 (CPOL=0, CPHA=0)

def read_adc(channel):
    """Reads a 12-bit value (0 to 4095) from the specified ADC channel (0-7)."""
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")
    
    # ADC128S102 control register format:
    # 3 leading zeros + 3-bit channel address + 2 trailing zeros
    # Example for Channel 0: 000 000 00 -> 0x00
    # Example for Channel 1: 000 001 00 -> 0x08
    high_byte = (channel << 3) & 0x38
    low_byte = 0x00  # Trailing 8 bits don't matter during transmission
    
    # Send the channel address and read back 2 bytes simultaneously
    # spi.xfer2 maintains the CS line low during the entire transfer
    reply = spi.xfer2([high_byte, low_byte])
    
    # The ADC128S102 returns data shifted based on timing.
    # Typically, the 12-bit result spans across the 2 returned bytes:
    # Upper 4 bits of the 12-bit result are in reply[0] (lower 4 bits)
    # Lower 8 bits of the 12-bit result are in reply[1]
    adc_value = ((reply[0] & 0x0F) << 8) | reply[1]
    
    return adc_value

try:
    print("Testing ADC128S102 using a for-loop. Starting 5 iterations...")
    
    # Read Channel 0 exactly 5 times
    target_channel = 0
    
    for iteration in range(1, 6):
        print(f"\n--- Starting Iteration {iteration}/5 ---")
        
        # Read the raw 12-bit digital value
        raw_value = read_adc(target_channel)
        
        # Convert the digital value to an approximate voltage (Assuming VA = 3.3V reference)
        voltage = (raw_value * 3.3) / 4095.0
        
        print(f"Channel {target_channel} Raw Digital Value: {raw_value}")
        print(f"Calculated Voltage: {voltage:.3f} V")
        
        time.sleep(2)
        
    print("\nFinished all 5 iterations successfully.")

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

finally:
    # Safely close SPI connection when done
    spi.close()
    print("SPI connection closed safely.")

