Sure — here is the same newer version with **minimal comments only**.

```python
import spidev
import time

# ADC CE0
adc = spidev.SpiDev()
adc.open(0, 0)
adc.max_speed_hz = 100000
adc.mode = 3
adc.bits_per_word = 8

# DAC CE1
dac = spidev.SpiDev()
dac.open(0, 1)
dac.max_speed_hz = 100000
dac.mode = 3
dac.bits_per_word = 8


def read_adc(channel):

    if channel < 0 or channel > 7:
        raise ValueError("Channel must be 0-7")

    tx = [(channel & 0x07) << 3, 0x00]
    rx = adc.xfer2(tx)

    return ((rx[0] & 0x0F) << 8) | rx[1]


def write_dac(value):

    value &= 0x0FFF

    command = value << 2

    high = (command >> 8) & 0xFF
    low = command & 0xFF

    dac.xfer2([high, low])


read_adc(0)

try:

    while True:

        adc_value = read_adc(0)
        adc_voltage = adc_value * 5.0 / 4095.0

        dac_value = adc_value
        write_dac(dac_value)

        dac_voltage = dac_value * 3.3 / 4095.0

        print()
        print("=========== ADC Readings ===========")
        print("ADC Channel : IN0")
        print("ADC Value   :", adc_value)
        print("ADC Voltage : {:.3f} V".format(adc_voltage))
        print("------------------------------------")

        print("=========== DAC Output =============")
        print("Source      : ADC IN0")
        print("DAC Value   :", dac_value)
        print("DAC Voltage : {:.3f} V".format(dac_voltage))
        print("------------------------------------")

        time.sleep(0.5)

except KeyboardInterrupt:

    print("\nProgram stopped.")

finally:

    adc.close()
    dac.close()
```

This keeps the code simple while using **SPI Mode 3 for both CE0 and CE1**.
