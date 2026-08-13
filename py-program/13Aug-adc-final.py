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