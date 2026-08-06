Yes. The best way is to keep the `read_adc(channel)` function and use a **for loop** to scan all 8 ADC channels (IN0 to IN7). This keeps the code small and reusable.

Here is the modified program:

```python
import spidev
import time


# ----------------------------------------------------
# Create SPI object
# ----------------------------------------------------
spi = spidev.SpiDev()


# ----------------------------------------------------
# Open SPI Bus 0, Chip Select CE0
# Raspberry Pi:
# Bus 0
# CE0 = GPIO8
# ----------------------------------------------------
spi.open(0, 0)


# ----------------------------------------------------
# SPI settings
#
# 100000 Hz = 100 kHz SPI clock
#
# ADC128S102 uses SPI Mode 0
# ----------------------------------------------------
spi.max_speed_hz = 100000
spi.mode = 0



def read_adc(channel):
    """
    Read ADC128S102 channel

    channel:
    0 -> IN0
    1 -> IN1
    2 -> IN2
    ...
    7 -> IN7

    Returns:
    12-bit ADC value (0-4095)
    """


    # ------------------------------------------------
    # Select ADC channel
    #
    # ADC128S102 requires channel number
    # in bits D13:D11.
    #
    # Example:
    #
    # channel = 3
    #
    # 00000011
    #
    # << 3
    #
    # 00011000
    #
    # First byte contains channel information.
    # Second byte is dummy data.
    # ------------------------------------------------
    tx = [(channel & 0x07) << 3, 0x00]


    # ------------------------------------------------
    # Send command and receive ADC data
    #
    # SPI is full duplex:
    #
    # Raspberry Pi sends tx
    # ADC sends rx
    # ------------------------------------------------
    rx = spi.xfer2(tx)


    # ------------------------------------------------
    # Combine received two bytes
    #
    # ADC output is 12 bits:
    #
    # rx[0] = upper 4 bits
    # rx[1] = lower 8 bits
    #
    # Example:
    #
    # rx[0] = 00000111
    # rx[1] = 11111111
    #
    # Result:
    #
    # 0111 1111 1111
    #
    # = 2047
    # ------------------------------------------------
    value = ((rx[0] & 0x0F) << 8) | rx[1]


    return value



# ----------------------------------------------------
# Dummy conversion
#
# ADC128S102 is pipeline based.
# First reading is discarded.
# ----------------------------------------------------
spi.xfer2([0x00, 0x00])



try:

    while True:


        # --------------------------------------------
        # Scan all 8 analog channels
        #
        # range(8) produces:
        #
        # 0,1,2,3,4,5,6,7
        #
        # Corresponding to:
        #
        # IN0-IN7
        # --------------------------------------------
        for channel in range(8):


            # Read ADC channel
            adc_value = read_adc(channel)


            # Convert ADC value to voltage
            #
            # VA = 5V
            #
            # Formula:
            #
            # Voltage = ADC * VREF / 4095
            #
            voltage = adc_value * 5.0 / 4095



            # Display channel number
            print("Channel IN{}".format(channel))


            # Display ADC count
            print("ADC Value :", adc_value)


            # Display voltage
            print("Voltage   : {:.3f} V".format(voltage))


            print("----------------------")


            # Small delay between channels
            time.sleep(0.1)



        # Delay after one complete scan
        time.sleep(0.5)



finally:

    # Close SPI when program exits
    spi.close()
```

---

## Example Output

If you connect different voltages:

```
Channel IN0
ADC Value : 409
Voltage   : 0.500 V
----------------------

Channel IN1
ADC Value : 819
Voltage   : 1.000 V
----------------------

Channel IN2
ADC Value : 1638
Voltage   : 2.000 V
----------------------

Channel IN3
ADC Value : 2457
Voltage   : 3.000 V
----------------------

Channel IN4
ADC Value : 3276
Voltage   : 4.000 V
----------------------

Channel IN5
ADC Value : 2048
Voltage   : 2.501 V
----------------------

Channel IN6
ADC Value : 0
Voltage   : 0.000 V
----------------------

Channel IN7
ADC Value : 4095
Voltage   : 5.000 V
----------------------
```

---

## Why using a function is better here

Without a function, you would need:

```python
read IN0 code
read IN1 code
read IN2 code
...
read IN7 code
```

which creates repeated code.

With:

```python
read_adc(channel)
```

the same function handles:

```python
read_adc(0)   # IN0

read_adc(1)   # IN1

read_adc(2)   # IN2

...

read_adc(7)   # IN7
```

The only thing that changes is the channel number.

This is the normal style used in embedded programming and data acquisition systems.
