Based on your setup:

* **Raspberry Pi 5**
* **ADC128S102**
* **VD = 3.3 V**
* **VA = 5 V**
* **SPI Mode = 0**

here is the recommended configuration.

## 1. What voltage should I apply to IN0?

Since **VA = 5 V**, the ADC input range is:

```text
Minimum = 0 V
Maximum = 5 V
```

**Do not exceed 5 V** on IN0.

For testing, use these voltages:

| IN0 Voltage | Expected ADC Value |
| ----------- | -----------------: |
| 0.0 V       |                  0 |
| 0.5 V       |               ~410 |
| 1.0 V       |               ~819 |
| 1.5 V       |              ~1229 |
| 2.0 V       |              ~1638 |
| 2.5 V       |              ~2048 |
| 3.0 V       |              ~2457 |
| 4.0 V       |              ~3276 |
| 5.0 V       |              ~4095 |

To understand the relationship between input voltage and the digital output, this visualization may help:

genui{"physics_electricity_magnetism_learning_block":{"type_id":"OHMS_LAW"}}

Although the widget is about voltage/current relationships in circuits, the key idea here is that your applied input voltage is what the ADC converts into a proportional digital value.

---

# 2. Raspberry Pi Wiring

| Raspberry Pi 5 | ADC128S102 |
| -------------- | ---------- |
| GPIO8 (CE0)    | CS         |
| GPIO11         | SCLK       |
| GPIO10         | DIN        |
| GPIO9          | DOUT       |
| 3.3 V          | VD         |
| 5 V            | VA         |
| GND            | AGND       |
| GND            | DGND       |

IN0 → Variable voltage (0–5 V)

---

# 3. Final Python Program

```python
import spidev
import time

# Create SPI object
spi = spidev.SpiDev()

# Open SPI bus 0, chip select CE0
spi.open(0, 0)

# SPI configuration
spi.max_speed_hz = 100000      # 100 kHz
spi.mode = 0

def read_adc(channel):
    """
    Read ADC128S102 channel (0-7)
    """

    # Build command
    tx = [(channel & 0x07) << 3, 0x00]

    # SPI transfer
    rx = spi.xfer2(tx)

    # Convert received bytes to 12-bit value
    value = ((rx[0] & 0x0F) << 8) | rx[1]

    return value

# Dummy conversion
spi.xfer2([0x00, 0x00])

try:

    while True:

        adc = read_adc(0)

        voltage = adc * 5.0 / 4095

        print("---------------------")
        print("ADC Value :", adc)
        print("Voltage   : {:.3f} V".format(voltage))

        time.sleep(0.5)

finally:

    spi.close()
```

---

# 4. Expected Output

If IN0 = 0.5 V

```text
ADC Value : 410
Voltage   : 0.500 V
```

If IN0 = 1.0 V

```text
ADC Value : 819
Voltage   : 1.000 V
```

If IN0 = 2.0 V

```text
ADC Value : 1638
Voltage   : 2.000 V
```

If IN0 = 5.0 V

```text
ADC Value : 4095
Voltage   : 5.000 V
```

The displayed voltage should increase smoothly as you increase the voltage applied to IN0.

---

## One important question

You mentioned earlier that your program prints:

```text
Sent: [1,191]
Received: [1,191]
```

That suggests the current code and the SPI command format are not yet matching what the ADC128S102 expects.

**Which ADC128S102 package are you using?**

* DIP (through-hole)
* SOIC (surface-mount)
* A ready-made ADC128S102 module/breakout board

If it's a breakout board, a photo of the board (top and bottom) would help verify the wiring and ensure the correct SPI command format for your hardware.
