import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import time
import RPi.GPIO as GPIO

temp_0V = 0.4
temp_C = 0.010 #where temp_C is temperature coefficient

chan_temperatureerature = None
chan_LDR = None
button_delay = 22

initial_tempTime = 0
initial_LDRTime = 0

delayTime = 10

def temp_Thread():
    global chan_temperature
    global initial_tempTime
    global delayTime

    # Setup thread at set time delay
    thread = threading.Timer(delayTime, temp_thread)
    thread.daemon = True
    thread.start()

    # Set start time
    currentTime = int(round(time.time()))
    if (initial_tempTime == 0):
        initial_tempTime = currentTime

    # Read values from ADC
    voltage_temp = chan_temperature.voltage
    temp_value = chan_temperature.value
    
     # Convert to voltage temp to Temperature 
    temp = (voltage_temp - temp_0V)/temp_C

    # Print temp readings
    print('Runtime\t\tTemp Reading\tTemp')
    print('{0:.0f}s\t\t{1}\t\t{2:.3f}\t\t C'.format((currentTime - initial_tempTime), temp_value, temp))

def LDR_Thread():
    global chan_LDR
    global initial_LDRTime
    global delayTime

    # Setup thread at set time delay
    thread = threading.Timer(delayTime, LDR_Thread)
    thread.daemon = True
    thread.start()

    # Set start time
    currentTime = int(round(time.time()))
    if (initial_LDRTime == 0):
        initial_LDRTime = currentTime

    # Read values from ADC
    LDR_value = chan_LDR.value
    LDR_voltage = chan_LDR.voltage

    LDR_reading = (3.3 - LDR_voltage) / (LDR_voltage/1000)

    # Print LDR readings
    print('Runtime\t\tLDR Reading\tLDR Resistance')
    print('{0:.0f}s\t\t{1}\t\t{2:.3f}\t Ohms'.format((currentTime - initial_LDRTime), LDR_value, LDR_reading))

def setup():
    global chan_temperature
    global chan_LDR

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # Create an analog input channel on pin 0 and 1
    chan_temperature = AnalogIn(mcp, MCP.P1)
    chan_LDR = AnalogIn(mcp, MCP.P0)

    # Setup button for interupt and input
    GPIO.setup(button_delay, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_delay, GPIO.FALLING, callback=button_delay_callback, bouncetime=250)
    
def button_delay_callback(channel):
    global delayTime

    # Cycle delay
    if (delayTime == 10):
        delayTime = 5
    elif (delayTime == 5):
        delayTime = 1
    elif (delayTime == 1):
        delayTime = 10

if __name__ == "__main__":
    setup()
    LDR_Thread()
    temp_thread()

    # Run indefinitely
    while True:
        pass

