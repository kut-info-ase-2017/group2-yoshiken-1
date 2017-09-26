#!/usr/bin/python
###########################################################################
#Filename      :i2c1602_lcd.py
#Description   :test i2c 1602 lcd
#Author        :alan
#Website       :www.osoyoo.com
#Update        :2017/07/02
############################################################################
import smbus
import time
import sys
import RPi.GPIO as GPIO

BuzzerPin=18


# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x27
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BuzzerPin, GPIO.OUT, initial=GPIO.HIGH)
    

def main():
  # Main program block
  arg=sys.argv[1]
  # Initialise display
  lcd_init()

  while True:

    # Send some test
    lcd_string("Warning !!!     <",LCD_LINE_1)
    lcd_string("Warning !!!", LCD_LINE_2)
    # lcd_string("The rainfall over "+str(arg)+" mm",LCD_LINE_2)

    time.sleep(2)
    lcd_string("The rainfall",LCD_LINE_1)
    lcd_string("over "+str(arg)+" mm", LCD_LINE_2)
    # Send some more text
    # lcd_string("> Tutorial Url:",LCD_LINE_1)
    # lcd_string("> http://osoyoo.com",LCD_LINE_2)

    time.sleep(3)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(0.2)

def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
  setup()
  try:
    main()
  except KeyboardInterrupt:
   # pass
   destroy()
   lcd_byte(0x01, LCD_CMD)

 # finally:
 #   lcd_byte(0x01, LCD_CMD)

