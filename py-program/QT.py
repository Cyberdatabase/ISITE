Yes. A Raspberry Pi 3 can communicate with both the ADC121S101 and DAC128S102 over the SPI bus.
Typically, they share SCLK and MOSI, while the ADC uses MISO and each device has its own chip select (CS).

For example:

Raspberry Pi          ADC121S101          DAC128S102
----------------------------------------------------
GPIO11 (SCLK)  -----> SCLK               SCLK
GPIO10 (MOSI)  -----> DIN                DIN
GPIO9  (MISO)  <----- DOUT               --
GPIO8  (CE0)   -----> CS                 --
GPIO7  (CE1)   ------------------------> CS

1. SPI Driver (spi_driver.py)

import spidev

class SPIBus:

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)          # Bus 0, Device 0
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0

    def select_device(self, device):
        self.spi.close()
        self.spi.open(0, device)

    def transfer(self, tx):
        return self.spi.xfer2(tx)

    def close(self):
        self.spi.close()

------------------------------------------------------------------------------------------------------------------------------
2. ADC121S101 Driver (adc121s101.py)

The ADC121S101 outputs a 12-bit conversion result.

class ADC121S101:

    def __init__(self, spi):
        self.spi = spi

    def read(self):

        self.spi.select_device(0)      # CE0

        rx = self.spi.transfer([0x00, 0x00])

        value = ((rx[0] & 0x0F) << 8) | rx[1]

        return value

    def voltage(self, vref=3.3):

        value = self.read()

        return (value * vref) / 4095.0

-----------------------------------------------------------------------------------------------------------------------------

3. DAC128S102 Driver (dac128s102.py)

class DAC128S102:

    def __init__(self, spi):
        self.spi = spi

    def write(self, channel, value):

        self.spi.select_device(1)      # CE1

        value &= 0x0FFF

        command = ((channel & 0x07) << 12) | value

        high = (command >> 8) & 0xFF
        low = command & 0xFF

        self.spi.transfer([high, low])

--------------------------------------------------------------------------------------------------------------

4. PyQt GUI (gui.py)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QWidget):

    def __init__(self, adc, dac):

        super().__init__()

        self.adc = adc
        self.dac = dac

        self.setWindowTitle("ADC121S101 + DAC128S102")

        self.resize(500,300)

        self.label = QLabel("ADC : 0")

        self.button = QPushButton("Read ADC")

        self.button.clicked.connect(self.read_adc)

        self.slider = QSlider(Qt.Horizontal)

        self.slider.setRange(0,4095)

        self.slider.valueChanged.connect(self.write_dac)

        self.channel = QComboBox()

        for i in range(8):
            self.channel.addItem(str(i))

        layout = QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(QLabel("DAC Channel"))
        layout.addWidget(self.channel)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def read_adc(self):

        value = self.adc.read()

        voltage = self.adc.voltage()

        self.label.setText(
            f"ADC = {value}    Voltage = {voltage:.3f} V"
        )

    def write_dac(self, value):

        ch = self.channel.currentIndex()

        self.dac.write(ch, value)

------------------------------------------------------------------------------------------------------------------------------
5. Main Program (main.py)

import sys

from PyQt5.QtWidgets import QApplication

from spi_driver import SPIBus
from adc121s101 import ADC121S101
from dac128s102 import DAC128S102
from gui import Window

spi = SPIBus()

adc = ADC121S101(spi)
dac = DAC128S102(spi)

app = QApplication(sys.argv)

window = Window(adc, dac)

window.show()

app.exec_()

spi.close()

--------------------------------------------------------------------------------------------------------------------

Suggested GUI

----------------------------------------------------

ADC121S101 / DAC128S102 Controller

SPI

Bus              0
Clock            1 MHz
Mode             0

----------------------------------------------------

ADC

Raw Data

3214

Voltage

2.589 V

[ Read ]

----------------------------------------------------

DAC

Channel

0 ▼

Output Value

|-------------------------------|

0                       4095

2048

[ Write ]

----------------------------------------------------

Status

SPI Ready

----------------------------------------------------------------------------------------------------------------------------

