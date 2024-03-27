#!/usr/bin/env python
####################################################################
#  SN74HC165 DEMO MODE
#  Author: Maurik Holtrop
####################################################################
#
# THIS CODE IS NOT FUNCTIONAL WITH AN ACTUAL SHIFTER!!!!!
#
# This is a simple Python module to read out a serial shift register SN74HC165,
# or PISO register (Parallel-In Serial-Out), using the RPi.
# The code implements a single ended "Bit-Bang" SPI interface.
# SPI = serial peripheral interface: see https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus
# Single ended, since we read data but do not send any.
# "Bit-Bang" because we do not use the hardware interface, but instead use standard GPIO
# ports which we toggle and read.
# For simplicity, and since we are not using multiple SPI devices in this example, we
# do not have a "Chip-Select-bar" (SSbar) signal.
#####################################################################

# import RPi.GPIO as GPIO  # Setup the GPIO for RPi
import time
import sys


class SN74HC165:
    """This is a demo class for reading out the SN74HC165 chip,
    a parallel in - serial out register, using a Raspberry Pi."""

    def __init__(self, serial_in, serial_clk, serial_load, serial_n=8):
        """Initialize the module.
        Input:
         * Serial_in  = GPIO pin for the input data bit, connect to the Q output of the chip.
         * Serial_CLK = GPIO pin for the clock, connect to CLK of the chip.
         * Selial_Load= GPIO pin for the load signal, connect to LOAD of the chip.
         * Serial_N   = number of bits to clock out after a Load, default=8 (one chip)
         """
#        GPIO.setmode(GPIO.BCM)  # Set the numbering scheme to correspond to numbers on Pi Wedge.
        self._Serial_In = serial_in  # = MISO - GPIO pin for the Q (serial out) pin of the shifter
        self._Serial_CLK = serial_clk  # = CLK  - GPIO pin for the CLK (clock) pin of the shifter
        self._Serial_Load = serial_load  # = Load - GPIO pin the SH/LD-bar pin of the shifter.
        self._Serial_N = serial_n   # Number of bits to shift in. 8 bits for every SN74HC165.
        print("Initialized the RPi for a shifter connected to:")
        print("SN74HC165 Q     to RPi pin {}".format(self._Serial_In))
        print("SN74HC165 CLK   to RPi pin {}".format(self._Serial_CLK))
        print("SN74HC165 SH/LD to RPi pin {}".format(self._Serial_Load))
        print("Shifting {} bits.".format(self._Serial_N))

        # Demo DATA
        tmpdat = [0xDE, 0xAD, 0xBE, 0xEF, 0x12, 0x34, 0x56, 0x78, 0x45, 0xAA,
                  0x55, 0x01, 0xFF, 0x00, 0x14, 0x15, 0x00, 0x00]
        self.demo_numbers = ''.join(["{:08b}".format(x) for x in tmpdat])  # Turn data into bit strings.
        self.nidx = 0
        self.data = [0]
        #
        # Setup the GPIO Pins
        #
#        GPIO.setup(Serial_In,   GPIO.IN)
#        GPIO.setup(Serial_CLK,  GPIO.OUT)
#        GPIO.setup(Serial_Load, GPIO.OUT)
#        GPIO.output(Serial_Load,GPIO.HIGH)  # Load is High = ready to shift. Low = load data.
#        GPIO.output(Serial_CLK, GPIO.LOW)

    def __del__(self):          # This is automatically called when the class is deleted.
        """Delete and cleanup."""
        print("Cleanup.")
#        GPIO.cleanup(self.Serial_In)
#        GPIO.cleanup(self.Serial_CLK)
#        GPIO.cleanup(self.Serial_Load)

    def load_shifter(self):
        """ Load the parallel data into the shifter by toggling Serial_Load low """
        print("Load Shifter.")
        self.data = [int(self.demo_numbers[self.nidx+i]) for i in range(self._Serial_N)]  # Load the demo bits as bits.
        self.nidx += self._Serial_N
        if self.nidx >= len(self.demo_numbers):
            self.nidx = 0
#        GPIO.output(self.Serial_Load,GPIO.LOW)
#        GPIO.output(self.Serial_Load,GPIO.HIGH)

    def read_data(self):
        """ Shift the data into the shifter and return the obtained value.
        The bits are expected to come as Most Significant Bit (MSB) First
        to Least Significant Bit (LSB) last.
        Output:   out  - The data shifted in returned as integer."""

        # The SN74HC165 chip will immediately set the SER output pin equal
        # to the H input pin upon a load. So we need to read the pin first.
        # Then on a clock low->high transition, the shift register shifts the
        # data, and the bit on the G input pin is shifted to SER, etc.
        out = 0
        for i in range(self._Serial_N):        # Run the loop shift_n times.
            # bit = GPIO.input(self._Serial_In)  # First bit is already present on Q after load.
            bit = self.data[i]
            out <<= 1                         # Shift the bits in "out" one position to the left.
            out += bit                        # Add the bit we just read in the LSB location of out.
#            GPIO.output(self.Serial_CLK, GPIO.HIGH) # Clock High loads next bit into Q of chip.
#            GPIO.output(self.Serial_CLK, GPIO.LOW)  # Clock back to low, rest state.

        return out  # Return the data.
