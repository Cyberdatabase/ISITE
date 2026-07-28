Absolutely. Below is a complete beginner-to-end guide for building a **PyQt GUI on a Raspberry Pi 3** to control an **ADC121S101** and **DAC128S102** using SPI.

---

# Step 1: Hardware Required

| Component                      |  Quantity |
| ------------------------------ | --------: |
| Raspberry Pi 3 Model B/B+      |         1 |
| MicroSD Card (16 GB or larger) |         1 |
| Raspberry Pi OS                |         1 |
| ADC121S101                     |         1 |
| DAC128S102                     |         1 |
| Breadboard                     |         1 |
| Jumper wires                   | As needed |
| 3.3 V power supply (from Pi)   |         1 |

---

# Step 2: Install Raspberry Pi OS

1. Download Raspberry Pi Imager.
2. Flash Raspberry Pi OS onto the SD card.
3. Insert the SD card into the Pi.
4. Connect:

   * Keyboard
   * Mouse
   * HDMI monitor
   * Power supply
5. Boot the Raspberry Pi.

---

# Step 3: Update the System

Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```

This may take a few minutes.

---

# Step 4: Enable SPI

Run:

```bash
sudo raspi-config
```

Navigate to:

```text
Interface Options
      ↓
SPI
      ↓
Enable
```

Exit and reboot:

```bash
sudo reboot
```

---

# Step 5: Verify SPI

After reboot:

```bash
ls /dev/spidev*
```

Expected output:

```text
/dev/spidev0.0
/dev/spidev0.1
```

If you see both devices, SPI is enabled.

---

# Step 6: Install Python

Check Python:

```bash
python3 --version
```

You should see Python 3.x.

---

# Step 7: Install Required Packages

```bash
sudo apt install python3-pip -y
```

Install PyQt5:

```bash
sudo apt install python3-pyqt5 -y
```

Install SPI library:

```bash
pip3 install spidev
```

(Optional) Install a plotting library:

```bash
pip3 install pyqtgraph
```

---

# Step 8: Verify Installation

Check PyQt:

```bash
python3
```

Then:

```python
from PyQt5.QtWidgets import QApplication
```

No error means PyQt is installed correctly.

Exit:

```python
exit()
```

---

# Step 9: Create a Project Folder

```bash
mkdir SPI_GUI
```

Go into it:

```bash
cd SPI_GUI
```

---

# Step 10: Create Project Files

```text
SPI_GUI
│
├── main.py
├── gui.py
├── spi_driver.py
├── adc121s101.py
├── dac128s102.py
└── requirements.txt
```

Create the files:

```bash
touch main.py
touch gui.py
touch spi_driver.py
touch adc121s101.py
touch dac128s102.py
touch requirements.txt
```

---

# Step 11: Open the Folder

Install a code editor if needed:

```bash
sudo apt install geany -y
```

Open the project:

```bash
geany .
```

Or use another editor such as Thonny or VS Code.

---

# Step 12: Copy the Code

Copy the Python code into each file.

Save all files.

---

# Step 13: Connect the Hardware

Example wiring:

| Raspberry Pi  | ADC121S101 | DAC128S102 |
| ------------- | ---------- | ---------- |
| GPIO11 (SCLK) | SCLK       | SCLK       |
| GPIO10 (MOSI) | DIN        | DIN        |
| GPIO9 (MISO)  | DOUT       | —          |
| GPIO8 (CE0)   | CS         | —          |
| GPIO7 (CE1)   | —          | CS         |
| 3.3 V         | VCC        | VCC        |
| GND           | GND        | GND        |

**Note:** Double-check the datasheets for your exact chip package and pin numbering before wiring.

---

# Step 14: Run the Program

Open a terminal in the project folder:

```bash
cd SPI_GUI
```

Run:

```bash
python3 main.py
```

---

# Step 15: Expected GUI

A window similar to this should appear:

```text
+-------------------------------------------------+
|         ADC121S101 / DAC128S102                 |
+-------------------------------------------------+
| ADC Value : 0                                   |
|                                                 |
| [ Read ADC ]                                    |
|                                                 |
| DAC Channel: [0 ▼]                              |
|                                                 |
| 0 ---------------------------- 4095             |
|               Slider                            |
|                                                 |
+-------------------------------------------------+
```

---

# Step 16: Test the DAC

Move the slider.

The GUI sends the new value to the DAC.

Example:

```text
Slider = 1500

↓

DAC Output ≈ 1.21 V (depends on VREF)
```

Measure the DAC output with a multimeter or oscilloscope.

---

# Step 17: Test the ADC

Apply a known analogue voltage to the ADC input (within its allowed input range).

Click **Read ADC**.

Example:

```text
ADC = 2048

Voltage = 1.65 V
```

---

# Step 18: Automatic Updates

Instead of clicking **Read ADC**, use a timer in the GUI:

```python
from PyQt5.QtCore import QTimer

timer = QTimer()
timer.timeout.connect(self.read_adc)
timer.start(100)
```

This updates the ADC every 100 ms.

---

# Step 19: Debug SPI

If communication doesn't work, check:

```bash
lsmod | grep spi
```

You should see SPI kernel modules loaded.

---

# Step 20: Check GPIO Pins

Use:

```bash
pinout
```

This prints the Raspberry Pi GPIO pin assignments.

---

# Step 21: Install Helpful Tools

GPIO utility:

```bash
sudo apt install gpiod -y
```

System monitor:

```bash
sudo apt install htop -y
```

Logic analyser software (if you have a compatible analyser):

```bash
sudo apt install pulseview -y
```

---

# Step 22: Run at Startup (Optional)

Create a desktop launcher or configure the application to start automatically after login if you want it to behave like a dedicated instrument.

---

# Step 23: Troubleshooting

| Problem                       | Possible Cause                      | Solution                                                        |
| ----------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| `ModuleNotFoundError: spidev` | Package missing                     | `pip3 install spidev`                                           |
| `No module named PyQt5`       | PyQt not installed                  | `sudo apt install python3-pyqt5`                                |
| `/dev/spidev0.0` missing      | SPI disabled                        | Enable SPI in `raspi-config`                                    |
| GUI opens but no ADC data     | Wiring or SPI settings              | Check CS, SCLK, MOSI, MISO, SPI mode, and clock speed           |
| DAC output doesn't change     | Wrong chip select or command format | Verify CE1 wiring and the command format from the DAC datasheet |

---

# Recommended Final Project

```text
SPI_ADC_DAC_PROJECT/
│
├── main.py                 # Application entry point
├── gui.py                  # Main PyQt interface
├── spi_driver.py           # SPI communication layer
├── adc121s101.py           # ADC driver
├── dac128s102.py           # DAC driver
├── config.py               # SPI settings
├── logger.py               # Transaction logging
├── graph.py                # Real-time plotting
├── resources/
│   ├── icons/
│   └── ui/
├── logs/
└── requirements.txt
```

## My Recommendation

Rather than starting with a very large application, build it in stages:

1. **Stage 1:** Get SPI communication working from the terminal (no GUI).
2. **Stage 2:** Build a simple PyQt window with one button to read the ADC and one slider to control the DAC.
3. **Stage 3:** Add continuous ADC updates, voltage conversion, and a transaction log.
4. **Stage 4:** Add advanced features such as real-time graphs, configurable SPI settings, multiple DAC channels, and error/status indicators.

This staged approach makes it much easier to diagnose hardware and software issues as you develop the application.
