```python
#!/usr/bin/env python3

import spidev
import time


# ============================================================
# Raspberry Pi 5
#
# SPI0:
#   SCLK = GPIO11
#   MOSI = GPIO10
#   MISO = GPIO9
#   CE0  = GPIO8   -> ADC128S102 CS
#   CE1  = GPIO7   -> DAC121S101 SYNC
#
# Both devices use:
#   CPOL = 1
#   CPHA = 1
#   SPI MODE 3
#
# SCLK idle state = HIGH
# ============================================================


# ============================================================
# SPI CONFIGURATION
# ============================================================

SPI_BUS = 0

ADC_CS = 0
DAC_CS = 1

# Use 10 MHz as a starting point.
#
# ADC128S102 commercial device:
# specified SCLK = 8 MHz to 16 MHz
#
# DAC121S101 supports much higher clock rates.
SPI_SPEED = 10_000_000


# ============================================================
# OPEN ADC
# ============================================================

adc = spidev.SpiDev()

adc.open(SPI_BUS, ADC_CS)

adc.max_speed_hz = SPI_SPEED
adc.mode = 3
adc.bits_per_word = 8


# ============================================================
# OPEN DAC
# ============================================================

dac = spidev.SpiDev()

dac.open(SPI_BUS, DAC_CS)

dac.max_speed_hz = SPI_SPEED
dac.mode = 3
dac.bits_per_word = 8


# ============================================================
# ADC128S102
# ============================================================

def read_adc(channel):
    """
    Read one channel from ADC128S102.

    channel:
        0 -> IN0
        1 -> IN1
        ...
        7 -> IN7

    ADC transaction:
        16 SCLK cycles

    First byte:
        DONTC DONTC ADD2 ADD1 ADD0 DONTC DONTC DONTC

    Second byte:
        0x00

    Returned value:
        12-bit ADC result
    """

    if channel < 0 or channel > 7:
        raise ValueError("ADC channel must be 0 to 7")

    # ADC channel command
    command = (channel & 0x07) << 3

    tx = [
        command,
        0x00
    ]

    # 16 clock cycles
    rx = adc.xfer2(tx)

    # ADC128S102:
    #
    # rx[0]:
    # xxxx D11 D10 D9 D8
    #
    # rx[1]:
    # D7 D6 D5 D4 D3 D2 D1 D0

    adc_value = ((rx[0] & 0x0F) << 8) | rx[1]

    return adc_value


# ============================================================
# DAC121S101
# ============================================================

def write_dac(value):
    """
    Write a 12-bit value to DAC121S101.

    DAC input register:

        DB15  = don't care
        DB14  = don't care
        DB13  = PD1
        DB12  = PD0
        DB11  = D11
        ...
        DB0   = D0

    Normal operating mode:

        PD1 = 0
        PD0 = 0

    Therefore:

        12-bit DAC value << 2
    """

    # Limit to 12 bits
    value &= 0x0FFF

    # Normal operation:
    #
    # 00xxxx xxxxxxxx
    #
    # The 12-bit DAC data occupies DB11:DB0.

    command = value << 2

    high_byte = (command >> 8) & 0xFF
    low_byte = command & 0xFF

    tx = [
        high_byte,
        low_byte
    ]

    # 16 SCLK cycles
    dac.xfer2(tx)


# ============================================================
# ADC VOLTAGE CALCULATION
# ============================================================

def adc_to_voltage(adc_value, adc_reference):
    """
    Convert ADC code to voltage.

    ADC resolution = 12 bits
    Maximum code = 4095
    """

    return adc_value * adc_reference / 4095.0


# ============================================================
# DAC VOLTAGE CALCULATION
# ============================================================

def dac_to_voltage(dac_value, dac_supply):
    """
    Convert DAC code to ideal output voltage.

    DAC121S101 uses its supply voltage as the reference.
    """

    return dac_value * dac_supply / 4096.0


# ============================================================
# INITIALIZATION
# ============================================================

# The ADC128S102 requires a conversion to establish
# the requested channel after power-up.
#
# Discard the first result.

read_adc(0)


# ============================================================
# MAIN LOOP
# ============================================================

try:

    while True:

        # ----------------------------------------------------
        # READ ADC IN0
        # ----------------------------------------------------

        adc_value = read_adc(0)

        # Change this to your actual ADC VA/reference voltage.
        ADC_REFERENCE = 5.0

        adc_voltage = adc_to_voltage(
            adc_value,
            ADC_REFERENCE
        )


        # ----------------------------------------------------
        # SEND ADC VALUE TO DAC
        # ----------------------------------------------------

        dac_value = adc_value

        write_dac(dac_value)


        # DAC supply/reference
        DAC_SUPPLY = 3.3

        dac_voltage = dac_to_voltage(
            dac_value,
            DAC_SUPPLY
        )


        # ----------------------------------------------------
        # PRINT ADC
        # ----------------------------------------------------

        print()
        print("======================================")
        print("          ADC128S102 READ")
        print("======================================")

        print("Channel       : IN0")
        print("ADC Value     :", adc_value)
        print(
            "ADC Voltage   : {:.4f} V".format(
                adc_voltage
            )
        )


        # ----------------------------------------------------
        # PRINT DAC
        # ----------------------------------------------------

        print()
        print("======================================")
        print("          DAC121S101 OUTPUT")
        print("======================================")

        print("Source        : ADC IN0")
        print("DAC Value     :", dac_value)
        print(
            "DAC Voltage   : {:.4f} V".format(
                dac_voltage
            )
        )

        print("======================================")


        # 100 ms between measurements
        time.sleep(0.1)


# ============================================================
# CLEANUP
# ============================================================

except KeyboardInterrupt:

    print()
    print("Stopping...")


finally:

    adc.close()
    dac.close()

    print("SPI devices closed.")
```
