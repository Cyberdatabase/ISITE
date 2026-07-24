import spidev
import time
import pigpio

pi=pigpio.pi()

if not pi.connected
   print("pi-not connected")
   exit()
   
spi_bb_pi.bb_spi_open(8,10,9,11, 50000,0)

value_bit = 0xABCD
high_byte = (value_16bit >> 8) & 0xFF
low_byte = value_16bit & 0xFF
to_send = [high_byte, low_byte]

while True:
	count,received_data= pi.bb_spi_xfer(8, to_send)
	print(count)
	print(received_data)
	
pi.bb_spi_close(8)
pi.stop()
