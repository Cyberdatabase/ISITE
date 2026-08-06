These are exactly the right questions if you want to **understand ADCs deeply instead of just using them**. I'll explain from the fundamentals to the ADC128S102 and then the bit shifting used in your program.

---

# Part 1: What is an ADC?

ADC stands for **Analog-to-Digital Converter**.

It converts an **analog voltage** into a **digital number**.

## Analog Signal

An analog signal can have any value within a range.

Example:

```text
0V
0.2V
0.75V
1.35V
2.96V
5V
```

The voltage changes continuously.

---

## Digital Signal

A computer or Raspberry Pi cannot directly understand analog voltages.

It understands numbers like

```text
0

1

25

1024

2048

4095
```

So the ADC converts

```text
Voltage
↓

Number
```

---

# Example

Suppose

```text
Reference Voltage = 5V
Resolution = 12 bits
```

Then

| Analog Voltage | Digital Output |
| -------------- | -------------: |
| 0V             |              0 |
| 1V             |            819 |
| 2V             |           1638 |
| 3V             |           2457 |
| 4V             |           3276 |
| 5V             |           4095 |

The ADC is simply answering the question:

> "Where is the input voltage between 0 V and the reference voltage?"

---

# Part 2: How does an ADC work?

Imagine a ruler.

```
0V--------------------------------5V
```

Now divide it into **4096 equal parts**.

```
0
1
2
3
4
.
.
4095
```

When the input voltage is

```text
2.5V
```

the ADC finds that it is about halfway along the ruler and outputs

```text
2048
```

---

# Formula

The relationship is

[
\text{ADC Value}=\frac{V_{IN}}{V_{REF}}\times(2^N-1)
]

Where:

* (V_{IN}) = input voltage
* (V_{REF}) = reference voltage
* (N) = ADC resolution

For a 12-bit ADC:

[
2^{12}=4096
]

Maximum output:

```text
4095
```

---

# Part 3: Things you must know about every ADC

Whenever you study an ADC, check these specifications.

## 1. Resolution

Measured in bits.

Examples

| Bits | Number of Levels |
| ---- | ---------------: |
| 8    |              256 |
| 10   |             1024 |
| 12   |             4096 |
| 16   |            65536 |

Higher resolution means smaller voltage steps.

---

## 2. Reference Voltage

The maximum measurable voltage.

Example

```text
VREF = 5V
```

Input range

```text
0V to 5V
```

If

```text
VREF = 3.3V
```

Input range

```text
0V to 3.3V
```

---

## 3. Number of Channels

ADC128S102

```
IN0

IN1

IN2

...

IN7
```

Total

```text
8 channels
```

---

## 4. Sampling Rate

How many conversions can be done every second.

Usually measured in

```text
kSPS

or

MSPS
```

Example

```text
200 kSPS

=

200000 samples/sec
```

---

## 5. Accuracy

Real ADCs have errors.

Examples

Offset error

Gain error

Noise

Integral Non-Linearity (INL)

Differential Non-Linearity (DNL)

---

## 6. Interface

Some ADCs use

```
SPI

I²C

Parallel
```

ADC128S102 uses

```text
SPI
```

---

# Part 4: ADC128S102 Specifications

| Specification       | Value                     |
| ------------------- | ------------------------- |
| Resolution          | 12-bit                    |
| Channels            | 8                         |
| Interface           | SPI                       |
| Input Range         | 0 V to VA                 |
| Reference           | VA (no separate VREF pin) |
| Digital Supply (VD) | 2.7 V to VA               |
| Analog Supply (VA)  | 2.7 V to 5.25 V           |
| SPI Mode            | Mode 0                    |
| Maximum Output      | 4095                      |

---

# Part 5: How SPI communication works

The Raspberry Pi sends

```
16 clock pulses
```

During these clocks

```
Pi ---> ADC

ADC ---> Pi
```

simultaneously.

This is called

```text
Full Duplex
```

---

# Part 6: Understanding the command

Suppose

```python
channel = 3
```

---

First

```python
channel & 0x07
```

Channel

```
3
```

Binary

```
00000011
```

0x07

```
00000111
```

AND operation

```
00000011

00000111

---------

00000011
```

Result

```
3
```

Why do this?

Because only the lowest **3 bits** are valid channel bits (0–7). If someone accidentally passes a larger number, the mask discards the extra bits.

---

# Part 7: Left Shift

Now

```python
(channel & 0x07) << 3
```

Suppose

```
3
```

Binary

```
00000011
```

Shift left

```
00011000
```

Decimal

```
24
```

Why?

Because the ADC expects the channel number in specific bit positions (D13:D11 of the 16-bit command). Shifting moves the channel bits into those positions.

---

# Manual shifting example

Suppose

```python
channel=5
```

Binary

```
00000101
```

Shift left by 3

```
00101000
```

Decimal

```
40
```

Therefore

```python
tx=[40,0]
```

---

# Part 8: SPI Transfer

```python
rx=spi.xfer2(tx)
```

Suppose

```
tx

[24,0]
```

The Raspberry Pi sends

```
00011000

00000000
```

16 clock pulses.

The ADC sends back

```
00000110

01011010
```

Suppose

```python
rx

[6,90]
```

---

# Part 9: Extract the ADC value

Now

```python
value=((rx[0]&0x0F)<<8)|rx[1]
```

Let's do it manually.

Suppose

```
rx[0]=6
```

Binary

```
00000110
```

Mask

```
0x0F

00001111
```

AND

```
00000110

00001111

---------

00000110
```

Still

```
6
```

---

Shift left by 8

```
00000110

↓

0000011000000000
```

Decimal

```
1536
```

---

Now

```
rx[1]

=

90
```

Binary

```
01011010
```

Decimal

```
90
```

---

Now OR them

```
0000011000000000

0000000001011010

----------------

0000011001011010
```

Decimal

```
1626
```

Therefore

```python
value

=

1626
```

That is the ADC result.

---

# Part 10: Why do we use bitwise operators?

The ADC doesn't return a normal decimal number. It returns **individual bits** packed into bytes.

Bitwise operators let us unpack those bits.

| Operator | Meaning           | Example       |
| -------- | ----------------- | ------------- |
| `&`      | AND (mask bits)   | `15 & 7 = 7`  |
| `\|`     | OR (combine bits) | `4 \| 1 = 5`  |
| `<<`     | Shift left        | `5 << 1 = 10` |
| `>>`     | Shift right       | `10 >> 1 = 5` |

These are fundamental tools when working with SPI, I²C registers, microcontrollers, and embedded systems.

---

## My suggestion for learning

To build a strong foundation, learn these topics in this order:

1. **Binary numbers** (decimal ↔ binary conversion).
2. **Bitwise operators**: `&`, `|`, `^`, `~`, `<<`, `>>`.
3. **SPI protocol**: MOSI, MISO, SCLK, CS, clock edges, and SPI modes.
4. **ADC concepts**: resolution, reference voltage, quantization, sampling.
5. **ADC128S102 timing diagram**: understand exactly how the 16 transmitted bits and 16 received bits align during a conversion.

Once you're comfortable with these, the `read_adc()` function will become much easier to understand because you'll know why every bit is placed where it is.
