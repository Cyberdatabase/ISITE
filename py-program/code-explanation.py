Below is your program with **detailed comments explaining every line**.

```python
# ----------------------------------------------------------
# Import the SPI library.
# This library allows Python to communicate with SPI devices
# such as the ADC128S102.
# ----------------------------------------------------------
import spidev


# ----------------------------------------------------------
# Import the time library.
# It is used to create delays (sleep).
# ----------------------------------------------------------
import time


# ----------------------------------------------------------
# Create an SPI object.
#
# SpiDev() creates a software object that represents the
# Raspberry Pi's SPI hardware.
#
# At this point, no SPI port is opened yet.
# ----------------------------------------------------------
spi = spidev.SpiDev()


# ----------------------------------------------------------
# Open SPI communication.
#
# open(bus, device)
#
# bus = 0
# device = 0
#
# On Raspberry Pi:
#
# SPI Bus 0
#
# CE0  -> GPIO8
# CE1  -> GPIO7
#
# Since device=0, GPIO8 (CE0) is used as Chip Select.
# ----------------------------------------------------------
spi.open(0, 0)


# ----------------------------------------------------------
# Set SPI clock speed.
#
# Unit = Hertz (Hz)
#
# 100000 Hz
# =
# 100 kHz
#
# This means the SPI clock produces
# 100,000 clock pulses every second.
#
# The ADC uses these clock pulses to shift data in and out.
#
# Lower speed = Easier for debugging.
# Higher speed = Faster communication.
# ----------------------------------------------------------
spi.max_speed_hz = 100000


# ----------------------------------------------------------
# Set SPI Mode.
#
# SPI has four modes:
#
# Mode 0
# Mode 1
# Mode 2
# Mode 3
#
# ADC128S102 requires Mode 0.
#
# Mode 0 means:
#
# CPOL = 0
# Clock is LOW when idle.
#
# CPHA = 0
# Data is sampled on the rising edge.
# ----------------------------------------------------------
spi.mode = 0


# ----------------------------------------------------------
# Function to read one ADC channel.
#
# channel can be:
#
# 0
# 1
# 2
# ...
# 7
#
# Returns:
#
# 12-bit ADC value (0-4095)
# ----------------------------------------------------------
def read_adc(channel):

    # ------------------------------------------------------
    # Build the command to send to the ADC.
    #
    # channel & 0x07
    #
    # Ensures only the lowest 3 bits remain.
    #
    # Example
    #
    # channel = 0
    #
    # Binary
    #
    # 000
    #
    # Shift left by 3 bits
    #
    # 00000000
    #
    # For channel 1
    #
    # 001 << 3
    #
    # becomes
    #
    # 00001000
    #
    # First byte selects the ADC input channel.
    #
    # Second byte is dummy data.
    # ------------------------------------------------------
    tx = [(channel & 0x07) << 3, 0x00]


    # ------------------------------------------------------
    # SPI Transfer.
    #
    # xfer2() simultaneously:
    #
    # Sends:
    #
    # tx
    #
    # and
    #
    # Receives:
    #
    # rx
    #
    # SPI is FULL DUPLEX.
    #
    # That means while Raspberry Pi sends one bit,
    # the ADC sends one bit back at exactly the same time.
    #
    # tx example
    #
    # [0x00,0x00]
    #
    # rx example
    #
    # [0x06,0x5A]
    # ------------------------------------------------------
    rx = spi.xfer2(tx)


    # ------------------------------------------------------
    # Convert received bytes into one 12-bit ADC value.
    #
    # Suppose:
    #
    # rx[0] = 0x06
    #
    # Binary
    #
    # 00000110
    #
    # rx[1] = 0x5A
    #
    # Binary
    #
    # 01011010
    #
    # rx[0] & 0x0F
    #
    # keeps only lower 4 bits.
    #
    # Then shift left by 8.
    #
    # Finally OR with second byte.
    #
    # Result becomes one 12-bit number.
    # ------------------------------------------------------
    value = ((rx[0] & 0x0F) << 8) | rx[1]


    # ------------------------------------------------------
    # Return ADC value.
    # ------------------------------------------------------
    return value


# ----------------------------------------------------------
# First SPI transfer.
#
# ADC128S102 is pipeline based.
#
# First transfer starts the first conversion.
#
# Returned data from this transfer is generally not the
# requested channel's conversion result.
#
# Therefore perform one dummy transfer before reading.
# ----------------------------------------------------------
spi.xfer2([0x00, 0x00])


# ----------------------------------------------------------
# try-finally ensures SPI is closed properly even if
# the program is interrupted.
# ----------------------------------------------------------
try:

    # ------------------------------------------------------
    # Infinite loop.
    #
    # Reads channel 0 continuously.
    # ------------------------------------------------------
    while True:

        # --------------------------------------------------
        # Read ADC channel 0.
        #
        # adc will be between
        #
        # 0
        #
        # and
        #
        # 4095
        # --------------------------------------------------
        adc = read_adc(0)


        # --------------------------------------------------
        # Convert ADC value into voltage.
        #
        # Formula
        #
        # Voltage
        #
        # =
        #
        # ADC Value
        #
        # ×
        #
        # Reference Voltage
        #
        # ÷
        #
        # 4095
        #
        # Since VA = 5V
        #
        # Voltage
        #
        # =
        #
        # adc × 5 / 4095
        # --------------------------------------------------
        voltage = adc * 5.0 / 4095


        # --------------------------------------------------
        # Print separator.
        # --------------------------------------------------
        print("---------------------")


        # --------------------------------------------------
        # Print digital ADC count.
        # --------------------------------------------------
        print("ADC Value :", adc)


        # --------------------------------------------------
        # Print calculated voltage.
        #
        # {:.3f}
        #
        # Means display three digits after the decimal point.
        #
        # Example
        #
        # 2.45678
        #
        # becomes
        #
        # 2.457
        # --------------------------------------------------
        print("Voltage   : {:.3f} V".format(voltage))


        # --------------------------------------------------
        # Wait for 0.5 second.
        #
        # Without this delay,
        # the program would print thousands of readings
        # every second.
        # --------------------------------------------------
        time.sleep(0.5)


# ----------------------------------------------------------
# finally always executes.
#
# Close SPI communication before exiting.
# ----------------------------------------------------------
finally:

    spi.close()
```

### How the program works (flow)

```text
Start
   │
   ▼
Import libraries
   │
   ▼
Create SPI object
   │
   ▼
Open SPI (Bus 0, CE0)
   │
   ▼
Set SPI speed = 100 kHz
   │
   ▼
Set SPI Mode = 0
   │
   ▼
Dummy SPI transfer
   │
   ▼
Read Channel 0
   │
   ▼
Receive 12-bit ADC value
   │
   ▼
Convert ADC value to voltage
   │
   ▼
Print ADC value and voltage
   │
   ▼
Wait 0.5 s
   │
   └──────────────► Repeat
```

One important note: the line

```python
value = ((rx[0] & 0x0F) << 8) | rx[1]
```

is the heart of the program. It takes the two bytes returned by the ADC and combines them into the single 12-bit conversion result (0–4095). Understanding this line is key to understanding how the ADC128S102 communicates over SPI.
