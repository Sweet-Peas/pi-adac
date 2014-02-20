#!/usr/bin/python

import spidev
import time
import RPi.GPIO as gpio

CMD_READ       = 0x8000
CMD_WRITE      = 0x0000
CMD_PG_DATA    = 0x0000
CMD_PG_CTRL    = 0x0800
# Data registers
CMD_ADC0       = 0x00
CMD_ADC1       = 0x01
CMD_ADC2       = 0x02
CMD_ADC3       = 0x03
CMD_ADC4       = 0x04
CMD_ADC5       = 0x05
CMD_ADC6       = 0x06
CMD_ADC7       = 0x07
CMD_DAC0       = 0x09
CMD_DAC1       = 0x0A
CMD_DAC2       = 0x0B
# Control registers
CMD_SHUTDOWN   = 0x00
CMD_RESET      = 0x01
CMD_CONFIG     = 0x02
CMD_STATUS     = 0x02

AD_VALUE_MASK  = 0x0FFF
AD_VALID       = 0x10
AD_ADDRESS     = 0xE0
CFG_STAT_RSTC  = 0x0010
RESET_PIN      = 22

#
# Write a command to the ADC
#
def write_ctrl ( reg, command ):
	# Create command bytes
	cmd = CMD_WRITE + CMD_PG_CTRL | (reg << 6)
	cmd1 = (cmd >> 8) & 0xff
	cmd2 = cmd & 0xff
	# Create control data bytes
	dat1 = (command >> 8) & 0xff
	dat2 = command & 0xff
	# Write the command
	spi.xfer2([cmd1, cmd2, dat1, dat2])

#
# Read control registers
#
def read_ctrl ( reg ):
	# Create command bytes
	cmd = CMD_READ + CMD_PG_CTRL | (reg << 6)
	cmd1 = (cmd >> 8) & 0xff
	cmd2 = cmd & 0xff
	# Send command and read response
	trans = spi.xfer2([cmd1, cmd2, 0, 0])
	return ((trans[2] << 8) | trans[3])

#
# This function performs a soft reset of the device
#
def soft_reset ( ):
	# Write the reset sequence to the chip
	spi.xfer2([0x08, 0x40, 0x0b, 0xb3])
	# Read back the status register
	cond = True
	while cond:
		result = read_ctrl (CMD_STATUS)
		if result & CFG_STAT_RSTC == CFG_STAT_RSTC:
			cond = False
	# Set unipolar mode
	write_ctrl (0x02, 0x09)

#
# read ADC Value
#
def read_adc ( channel ):
	cmd = CMD_READ + CMD_PG_DATA + (channel << 6)
	cmd1 = (cmd >> 8) & 0xff
	cmd2 = cmd & 0xff
	# Look for a valid A/D value
	cond = True
	while cond:
		adcdata = spi.xfer2([cmd1, cmd2, 0, 0])
		if adcdata[2] & AD_VALID == AD_VALID:
			cond = False

	adcvalue = ((adcdata[2] << 8) | adcdata[3]) & AD_VALUE_MASK
	return adcvalue
	
# Reset ADC
try:
	gpio.setmode (gpio.BOARD)
	gpio.setup (RESET_PIN, gpio.OUT)

	# Reset pulse
	gpio.output (RESET_PIN, gpio.LOW)
	time.sleep (0.01)
	gpio.output (RESET_PIN, gpio.HIGH)

	spi = spidev.SpiDev()

	print "Opening SPI"
	spi.open(0,0)
	spi.mode = 1

	# Perform a soft reset of the ADC
	soft_reset()

	i = 2
	while True:
		print "(%d: %d), " % (i, read_adc(i))
		time.sleep(1)

	print "Closing SPI"
	spi.close()
	gpio.cleanup()
except:
	spi.close()
	gpio.cleanup()

