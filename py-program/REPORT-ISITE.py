Yes. Here is a **detailed master prompt** you can use to generate the complete internship report template. It is designed so the AI **asks you for missing information instead of inventing anything**.

```text
I need you to create a professional technical internship project report template for my ISRO internship.

IMPORTANT:
- Do NOT mention “45 days” anywhere in the report.
- My actual internship/reporting period should be written as:
  02 July 2026 to 14 August 2026.
- July 1, 2026 was the original joining date, but I could not join that day. I actually joined on July 2, 2026. Do not unnecessarily mention the original July 1 date in the report.
- Do not invent experimental results, circuit connections, measurements, observations, names, dates, specifications, or activities.
- Wherever information is missing, put a clearly marked question/prompt for me to fill in.
- The final report should look like a genuine professional ISRO technical internship report, not like an AI-generated school assignment.
- Use formal technical English.
- Maintain consistency in terminology, units, component names, equations, tables, and headings.
- Do not make unsupported claims about “space qualification”, “radiation hardness”, “flight certification”, etc. merely because I call the components “space-grade”. Only state such claims if I provide official information.
- Do not claim that I designed a new ADC/DAC or developed new hardware. My work was primarily interfacing, communication, testing, observation, and understanding of the system.
- Keep the technical explanation sufficiently detailed for an M.Sc. Applied Electronics project report.

==================================================
STUDENT / INTERNSHIP DETAILS ALREADY KNOWN
==================================================

Student name:
SACHINDRA.P

College:
PSG College of Arts & Science, Coimbatore

Programme:
M.Sc. Applied Electronics

Department:
Department of Electronics

Academic status:
Passed out – May 2026

Registration number:
24MEL006

ISRO centre/unit:
ISITE, ISRO

Group/division:
SAG – Space Astronomy Group

Internship guide/supervisor:
Gyansham Kumar

Actual internship period:
02 July 2026 – 14 August 2026

==================================================
PROJECT INFORMATION ALREADY KNOWN
==================================================

The initial objective given by the ISRO guide was to interface an ADC and DAC with Raspberry Pi and understand:

1. ADC interfacing with Raspberry Pi
2. DAC interfacing with Raspberry Pi
3. SPI protocol communication
4. How SPI data is transferred
5. Analog-to-digital conversion
6. Digital data processing/transmission
7. Digital-to-analog conversion
8. Practical behaviour of the ADC and DAC
9. Testing the system using externally supplied voltages
10. Measuring/verifying the resulting signals

Main hardware:

- Raspberry Pi 5
- ADC128S102
- DAC121S101

ADC:
- Part number: ADC128S102
- ADC channels tested: IN0, IN1 and IN2
- External variable power supply used as the input
- Input voltage range tested: approximately 0–1 V
- ADC reference voltage used in the experiment: 5 V

DAC:
- Part number: DAC121S101
- DAC reference voltage used in the experiment: 3.3 V

Communication:
- SPI
- Python
- spidev library

Verification:
- Measurements were verified using measurement equipment.
- Multimeter and/or oscilloscope was used.
- Exact measurement details must be asked from me rather than invented.

==================================================
PROJECT TITLE
==================================================

Use a technically accurate title such as:

“SPI-Based Interfacing and Data Transfer Between ADC128S102 and DAC121S101 Using Raspberry Pi 5”

You may suggest 3 alternative professional titles and ask me to choose one before generating the final report.

==================================================
PYTHON CODE
==================================================

The following is the actual code used in the project. Include it in the Appendix and explain it technically in the main report.

[PASTE THE FOLLOWING CODE EXACTLY]

import spidev
import time

# ==========================================
# ADC - CE0
# ==========================================
adc = spidev.SpiDev()
adc.open(0, 0)
adc.max_speed_hz = 1000000
adc.mode = 3


# ==========================================
# DAC - CE1
# ==========================================
dac = spidev.SpiDev()
dac.open(0, 1)
dac.max_speed_hz = 1000000
dac.mode = 1


# ==========================================
# ADC READ
# ==========================================
def read_adc(channel):

    tx = [(channel & 0x07) << 3, 0x00]

    # --------------------------------------
    # First conversion
    # Select channel
    # Result is discarded
    # --------------------------------------
    adc.xfer2(tx)

    # --------------------------------------
    # Second conversion
    # Now read the selected channel
    # --------------------------------------
    rx = adc.xfer2(tx)
    print ("rx ", rx)
   

    value = ((rx[0] & 0x0F) << 8) | rx[1]

    return value


# ==========================================
# DAC WRITE
# ==========================================
def write_dac(value):

    value &= 0x0FFF

    high_byte = (value >> 8) & 0xFF
    low_byte = value & 0xFF

    print("High Byte", high_byte)
    print("Low Byte", low_byte)
    dac.xfer2([0x00,0x00])

    dac.xfer2([high_byte, low_byte])


# ==========================================
# MAIN
# ==========================================
try:

    while True:

        adc_value = read_adc(0)

        # ADC reference = 5V
        adc_voltage = adc_value * 5.0 / 4096.0

        print("ADC Value   :", adc_value)
        print("Input Voltage : {:.3f} V".format(adc_voltage))
        print("--------------------------------")

        # ----------------------------------
        # Send ADC value to DAC
        # ----------------------------------
        write_dac(adc_value)

        # DAC reference = 3.3V
        dac_voltage = adc_value * 3.3 / 4096.0

        print("DAC Value      :", adc_value)
        print("Output Voltage : {:.3f} V".format(dac_voltage))
        print("--------------------------------")

        time.sleep(5)

finally:

    adc.close()
    dac.close()

==================================================
IMPORTANT TECHNICAL VERIFICATION
==================================================

Before finalizing technical explanations, verify the datasheet-level details of:

- ADC128S102 resolution
- ADC input channels
- ADC SPI timing/protocol
- ADC SPI mode
- ADC command format
- ADC conversion sequence
- ADC reference-voltage requirements
- DAC121S101 resolution
- DAC SPI timing/protocol
- DAC SPI mode
- DAC input data format
- DAC reference-voltage requirements
- Raspberry Pi 5 SPI interfaces
- CE0/CE1 operation
- Voltage-level compatibility

If there is any discrepancy between my code and the official datasheet, DO NOT silently change my code.

Instead write:

“Implementation note: The experimental software configuration was used as implemented during testing. The relevant device datasheet should be consulted for the exact electrical and timing requirements.”

Clearly distinguish:
1. What was actually implemented.
2. What the datasheet specifies.
3. What was experimentally observed.

==================================================
REPORT STRUCTURE
==================================================

Create a detailed report with approximately 25–35 pages when formatted in Microsoft Word.

Use the following structure.

------------------------------------------
PAGE 1 – COVER PAGE
------------------------------------------

Include:
- ISRO / ISITE
- SAG – Space Astronomy Group
- Internship Project Report
- Project title
- Student name
- Registration number
- M.Sc. Applied Electronics
- Department of Electronics
- PSG College of Arts & Science, Coimbatore
- Internship period
- Guide name

Ask me:
[Q1] What exact official name/logo wording should appear for ISRO/ISITE?
[Q2] Do you have an official project title from ISRO?
[Q3] What exact designation should be written after the guide's name?
[Q4] Should the college department name be written exactly as “Department of Electronics”?

------------------------------------------
PAGE 2 – CERTIFICATE
------------------------------------------

Create a formal certificate template.

Do NOT invent:
- designation
- official ISRO wording
- certificate number
- signatures
- dates

Use placeholders/questions for missing information.

Ask:
[Q5] What designation should be written for the ISRO guide?
[Q6] Is there an official certificate format provided by ISRO?
[Q7] Do you have the name/designation of the department head or approving authority?
[Q8] Do you want signature placeholders?

------------------------------------------
PAGE 3 – DECLARATION
------------------------------------------

Prepare a formal student declaration.

Ask:
[Q9] Should the declaration mention only this project or the entire internship work?

------------------------------------------
PAGE 4 – ACKNOWLEDGEMENT
------------------------------------------

Prepare a professional acknowledgement mentioning:
- ISRO/ISITE
- SAG – Space Astronomy Group
- Guide Gyansham Kumar
- PSG College of Arts & Science
- Department of Electronics
- Faculty/supporting staff

Do not invent names.

Ask:
[Q10] Are there any additional people you specifically want acknowledged?

------------------------------------------
PAGE 5 – ABSTRACT
------------------------------------------

Write a technical abstract based only on known information.

It should cover:
- Raspberry Pi 5
- ADC128S102
- DAC121S101
- SPI
- Python
- external variable voltage
- ADC acquisition
- digital transfer
- DAC conversion
- experimental verification

Do not insert numerical accuracy/error results until I provide them.

Ask:
[Q11] What was the main conclusion you personally obtained from the experiment?
[Q12] Did the ADC and DAC operate successfully?
[Q13] Was the measured output close to the expected output?

------------------------------------------
CHAPTER 1 – INTRODUCTION
------------------------------------------

Explain:
1. Embedded systems
2. Data acquisition
3. ADC
4. DAC
5. Digital interfaces
6. SPI
7. Raspberry Pi
8. Importance of reliable data transfer
9. Relevance to electronics instrumentation/testing

Do not make unsupported claims about actual ISRO flight systems.

------------------------------------------
CHAPTER 2 – ORGANIZATION / INTERNSHIP OVERVIEW
------------------------------------------

Include:
- ISRO
- ISITE
- SAG
- role of internship
- technical learning environment

Ask:
[Q14] What activities did you observe or participate in within SAG?
[Q15] Were there any laboratory safety/technical procedures explained to you?
[Q16] Were there any presentations/training sessions apart from this project?

------------------------------------------
CHAPTER 3 – PROJECT AIM AND OBJECTIVES
------------------------------------------

Write a formal Aim.

Then list detailed objectives:
- interface ADC
- interface DAC
- configure SPI
- acquire ADC data
- convert ADC digital code into voltage
- transfer digital data
- generate DAC output
- compare expected and measured values
- understand practical SPI communication

Ask:
[Q17] Did your guide give you any additional objective?
[Q18] Did you test all ADC channels individually?

------------------------------------------
CHAPTER 4 – SYSTEM OVERVIEW
------------------------------------------

Explain the complete signal flow:

External Variable Voltage
        ↓
ADC128S102
        ↓
SPI
        ↓
Raspberry Pi 5
        ↓
SPI
        ↓
DAC121S101
        ↓
Analog Output

Explain each block.

Ask:
[Q19] Please describe exactly how the ADC, Raspberry Pi and DAC were physically connected.
[Q20] Was the ADC and DAC powered from separate supplies or the Raspberry Pi supply?
[Q21] What grounds were connected together?
[Q22] Was a breadboard, PCB, evaluation board, or custom setup used?

------------------------------------------
CHAPTER 5 – HARDWARE DESCRIPTION
------------------------------------------

Create subsections:

5.1 Raspberry Pi 5
5.2 ADC128S102
5.3 DAC121S101
5.4 External variable power supply
5.5 Multimeter
5.6 Oscilloscope, if used
5.7 Connecting wires/breadboard/PCB

For each component, explain:
- purpose
- relevant technical specifications
- role in the experiment

Ask me for missing specifications rather than inventing them.

------------------------------------------
CHAPTER 6 – SPI PROTOCOL
------------------------------------------

Explain in detail:

- What is SPI?
- Master/slave architecture
- SCLK
- MOSI
- MISO
- Chip Select
- full-duplex communication
- clock polarity
- clock phase
- SPI modes 0–3
- CE0 and CE1
- SPI frame/data transfer
- why SPI is suitable for ADC/DAC interfacing

Then specifically explain the project's ADC and DAC SPI communication.

Ask:
[Q23] Which Raspberry Pi GPIO pins were physically used?
[Q24] Was SPI enabled using Raspberry Pi configuration?
[Q25] Did you use `/dev/spidev0.0` and `/dev/spidev0.1`?
[Q26] Did you observe SPI signals using an oscilloscope or logic analyzer?

------------------------------------------
CHAPTER 7 – ADC128S102
------------------------------------------

Explain:
- ADC function
- resolution
- channels
- conversion
- digital output code
- reference voltage
- channel selection
- SPI communication
- conversion sequence
- relation between input voltage and digital code

Explain the project's `read_adc(channel)` function line by line.

Ask:
[Q27] Which channels were tested: IN0, IN1, IN2?
[Q28] What voltage was applied to each channel?
[Q29] Were unused ADC inputs left floating or connected appropriately?
[Q30] Provide any measured ADC codes.

------------------------------------------
CHAPTER 8 – DAC121S101
------------------------------------------

Explain:
- DAC function
- resolution
- digital input
- reference voltage
- SPI transfer
- output voltage relationship
- role of DAC in this experiment

Explain `write_dac(value)` line by line.

Ask:
[Q31] Was DAC output measured directly with a multimeter?
[Q32] Was DAC output observed using an oscilloscope?
[Q33] What DAC output values did you observe?

------------------------------------------
CHAPTER 9 – SOFTWARE ENVIRONMENT
------------------------------------------

Explain:
- Raspberry Pi OS, if known
- Python
- spidev
- time module
- SPI device initialization
- CE0 and CE1
- SPI speed
- SPI modes
- error handling/cleanup

Ask:
[Q34] Which Raspberry Pi OS version was used?
[Q35] Which Python version?
[Q36] How was spidev installed?
[Q37] Was SPI enabled through `raspi-config` or another method?

------------------------------------------
CHAPTER 10 – PROGRAM IMPLEMENTATION
------------------------------------------

Break the actual code into:

10.1 Library import
10.2 ADC initialization
10.3 DAC initialization
10.4 ADC channel selection
10.5 First conversion
10.6 Second conversion
10.7 Digital code extraction
10.8 ADC voltage calculation
10.9 DAC data preparation
10.10 DAC transmission
10.11 DAC voltage calculation
10.12 Continuous loop
10.13 Five-second delay
10.14 Resource cleanup

Explain every important line.

Do not modify the original code unless I specifically request it.

------------------------------------------
CHAPTER 11 – EXPERIMENTAL SETUP
------------------------------------------

Provide a place for:

- circuit diagram
- wiring diagram
- Raspberry Pi GPIO table
- ADC connection table
- DAC connection table
- power supply details
- measurement instruments

Ask:
[Q38] Give the exact Raspberry Pi GPIO pin numbers.
[Q39] Give ADC pin-to-Raspberry-Pi connections.
[Q40] Give DAC pin-to-Raspberry-Pi connections.
[Q41] Give power and ground connections.
[Q42] What instrument model numbers were used?
[Q43] What was the multimeter model?
[Q44] What was the oscilloscope model?

------------------------------------------
CHAPTER 12 – EXPERIMENTAL PROCEDURE
------------------------------------------

Create a numbered procedure covering:

1. Raspberry Pi preparation
2. SPI enabling
3. Hardware connection
4. Power supply connection
5. ADC input application
6. SPI communication
7. ADC reading
8. ADC voltage calculation
9. transfer of digital code
10. DAC conversion
11. measurement of DAC output
12. comparison
13. testing multiple channels

Ask:
[Q45] What exact sequence did you follow in the laboratory?
[Q46] How long did you allow the system to stabilize?
[Q47] Did you repeat each measurement?

------------------------------------------
CHAPTER 13 – OBSERVATIONS AND RESULTS
------------------------------------------

Create tables such as:

Table: ADC Channel Testing

| Channel | Applied Voltage | ADC Digital Code | Calculated Voltage | Measured Voltage | Error |
| IN0 | | | | | |
| IN1 | | | | | |
| IN2 | | | | | |

Table: DAC Testing

| ADC Code Sent to DAC | Expected DAC Voltage | Measured DAC Voltage | Error |
| | | | |

Ask me to fill the values.

Do NOT invent readings.

------------------------------------------
CHAPTER 14 – CALCULATIONS
------------------------------------------

Explain the ADC calculation:

ADC voltage = ADC digital value × Vref / 4096

using Vref = 5 V where appropriate.

Explain DAC calculation:

DAC output voltage = DAC code × Vref / 4096

using Vref = 3.3 V where appropriate.

Also explain:
- LSB size
- percentage error
- absolute error

Ask:
[Q48] Provide actual measured values so the calculations can be completed.
[Q49] Should the report include percentage error calculations?

------------------------------------------
CHAPTER 15 – DATA TRANSFER ANALYSIS
------------------------------------------

Explain the complete process:

Analog input
→ ADC sampling/conversion
→ ADC digital code
→ SPI transfer to Raspberry Pi
→ Python processing
→ digital code transfer to DAC
→ DAC conversion
→ analog output

Discuss:
- data format
- bytes
- bit masking
- shifting
- SPI frames
- channel selection
- digital code reconstruction

Explain this code:

value = ((rx[0] & 0x0F) << 8) | rx[1]

and:

value &= 0x0FFF

------------------------------------------
CHAPTER 16 – RESULTS AND DISCUSSION
------------------------------------------

Discuss:
- whether ADC acquisition worked
- whether SPI communication worked
- whether DAC output was generated
- relationship between input voltage and ADC code
- relationship between digital code and DAC output
- agreement between calculated and measured values
- channel testing
- practical observations

Only use actual results provided by me.

Ask:
[Q50] What were the major observations?
[Q51] Was the output stable?
[Q52] Did you observe any noise/fluctuation?
[Q53] What was the maximum deviation you observed?
[Q54] Did all tested channels behave similarly?

------------------------------------------
CHAPTER 17 – PROBLEMS ENCOUNTERED AND TROUBLESHOOTING
------------------------------------------

Ask me:

[Q55] What problems did you face?
Examples:
- no SPI response
- incorrect ADC readings
- incorrect channel selection
- DAC output absent
- wrong SPI mode
- wiring problems
- grounding problems
- software errors
- power supply issues
- unstable measurements

[Q56] How did you solve each problem?

Do not invent troubleshooting events.

------------------------------------------
CHAPTER 18 – LEARNING OUTCOMES
------------------------------------------

Discuss actual technical learning:
- SPI
- Raspberry Pi
- ADC
- DAC
- Python
- embedded interfacing
- debugging
- measurement techniques
- datasheet interpretation

Ask:
[Q57] What were your main personal technical learnings?
[Q58] Did you learn to read datasheets during this project?
[Q59] Did you learn any new Python/Linux commands?

------------------------------------------
CHAPTER 19 – APPLICATIONS
------------------------------------------

Explain possible general applications of ADC/DAC and SPI systems in:
- data acquisition
- instrumentation
- embedded systems
- control systems
- sensor interfaces
- laboratory test systems
- communication/electronic systems

Do not claim that this exact project is deployed in a specific ISRO flight system unless I provide evidence.

------------------------------------------
CHAPTER 20 – LIMITATIONS
------------------------------------------

Discuss only verified limitations.

Ask:
[Q60] What limitations did you observe?
Examples:
- limited input voltage testing
- limited number of channels tested
- limited sampling rate
- measurement equipment limitations
- breadboard limitations
- noise
- reference voltage limitations

------------------------------------------
CHAPTER 21 – FUTURE SCOPE
------------------------------------------

Suggest technically reasonable future improvements, clearly labeling them as proposed future work.

Possible areas:
- automated multi-channel acquisition
- graphical user interface
- data logging
- real-time plotting
- automated calibration
- error analysis
- higher-speed acquisition
- SPI signal analysis
- extended voltage testing
- long-duration testing

------------------------------------------
CHAPTER 22 – CONCLUSION
------------------------------------------

Write a concise technical conclusion based only on actual results.

Do not claim successful operation until I confirm it.

------------------------------------------
REFERENCES
------------------------------------------

Include placeholders for:
- ADC128S102 datasheet
- DAC121S101 datasheet
- Raspberry Pi 5 documentation
- Python documentation
- spidev documentation
- SPI technical references
- any ISRO-provided technical documents

Do not fabricate document numbers, revision numbers, URLs, authors, or publication dates.

------------------------------------------
APPENDIX A – COMPLETE PYTHON CODE
------------------------------------------

Include the exact original code I provided.

------------------------------------------
APPENDIX B – EXPERIMENTAL DATA
------------------------------------------

Provide blank tables for all measured values.

------------------------------------------
APPENDIX C – PHOTOGRAPHS
------------------------------------------

Since I currently do not have photographs, provide placeholders:

[PHOTO 1 – Raspberry Pi 5 experimental setup]
[PHOTO 2 – ADC128S102 connection]
[PHOTO 3 – DAC121S101 connection]
[PHOTO 4 – Measurement instrument]
[PHOTO 5 – SPI testing setup]

Do not create fake photographs.

==================================================
QUESTIONNAIRE AT THE END
==================================================

After creating the report template, provide a consolidated questionnaire containing every missing detail I need to answer.

Group questions under:

A. Personal details
B. ISRO/internship details
C. Hardware
D. GPIO/pin connections
E. ADC testing
F. DAC testing
G. SPI configuration
H. Software
I. Measurements
J. Troubleshooting
K. Results
L. Learning outcomes
M. Certificate details
N. References

Number every question clearly.

==================================================
FORMATTING REQUIREMENTS
==================================================

Make the final report suitable for Microsoft Word.

Recommended formatting:
- A4 page size
- Times New Roman
- Body text: 12 pt
- Chapter headings: 16 pt bold
- Section headings: 14 pt bold
- 1.5 line spacing
- Justified paragraphs
- Proper margins
- Page numbers
- Figure captions
- Table captions
- Equation numbering
- Table of Contents placeholder
- List of Figures
- List of Tables
- Abbreviations list

Use professional academic formatting.

IMPORTANT:
Do not repeatedly call it a “45-day internship”.
Do not mention “45 days” anywhere.
Use only the actual internship dates:
02 July 2026 – 14 August 2026.

Finally, produce the report as a fill-in template where every missing fact is represented by a question or clearly marked placeholder. I will answer the questions, and then you will use my answers to produce the final polished report.
```
