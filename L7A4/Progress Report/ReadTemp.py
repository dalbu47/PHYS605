from DevLib import MCP320x, MAX7219
import time


Max_data = 25
Max_clock = 27
Max_cs_bar = 26

M = MAX7219(Max_data, Max_clock, Max_cs_bar)

def Main():
    ''' Example ADC read main function. This will read values from the ADC and print them in a loop.'''
    # Define "input" to be Python2 and Python3 compatible.

    clock_speed = 1000000
    chip_select = 0

    adc = MCP320x(0,clock_speed,chip_select,chip="MCP3208")  # The 0 is there to select the SPI interface.

    try:
        while True:
            ADCval0 = adc.read_adc(0)  # Read the data from the analog input number 0.
            volt0 = (ADCval0/4096)*3.3
            temp0 = 0.1*volt0
            print("Ch: {:2d} Value: {:4d} (0x{:04X} = 0b{:012b})".format(0,ADCval0,ADCval0,ADCval0))
            print("")
            ADCval1 = adc.read_adc(1)  # Read the data from the analog input number 0.
            volt1 = (ADCval1/4096)*3.3
            temp1 = (45/3.3)*volt1
            # Print the value in decimal, hexadecimal, and binary format.
            # Binary format: {:0b} prints the value in 1 and 0,
            print("Ch: {:2d} Value: {:4d} (0x{:04X} = 0b{:012b})".format(0,ADCval1,ADCval1,ADCval1))
            print("")
            M.write_float(temp1)
            time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)



# This following bit of code allows you to load this script into Python at the commandline
# or as part of another script, and in those cases NOT execute the Main() function.
# If you execute the script from the command prompt, then the name of the scrtipt will
# be set to __main__, so then execute the Main() function.
if __name__ == "__main__":
    Main()
