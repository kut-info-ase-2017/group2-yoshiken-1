#!/usr/bin/python
###########################################################################
#Filename      :sensor.py
#Description   :Infrared alarm system
#Author        :Sasatani, Ryonai
#Update        :2017/09/25
###########################################################################
#OriginalFilename      :pirsensor.py
#Description   :Infrared alarm system
#Original Author        :alan
#Website       :www.osoyoo.com
#Original Update        :2017/07/05
############################################################################
import RPi.GPIO as GPIO
import time
import os
import pexpect # to automatically input password for scp
import getpass
from multiprocessing import Pool

# set BCM_GPIO 17(GPIO 0) as PIR pin
PIRPinIn = 17
PIRPinOut = 16
# set BCM_GPIO 18(GPIO 1) as buzzer pin
#BuzzerPin = 18

IMAGE_NUM = 0

#ryonai
#print message to ask server to upload pictures
#Reference: http://sweetme.at/2014/01/22/how-to-get-user-input-from-the-command-line-in-a-python-script/
# Reference: https://stackoverflow.com/questions/250283/how-to-scp-in-python

REMOTEHOST = raw_input("Please input server name: ")
REMOTEADDRESS = raw_input("Please input server IP address: ")
X = getpass.getpass("Server password: ")

#print message at the begining ---custom function
def print_message():
    print ('==================================')
    print ('|              Alarm             |')
    print ('|     -----------------------    |')
    print ('|     PIR connect to GPIO0       |')
    print ('|                                |')
    print ('|     Buzzer connect to GPIO1    |')
    print ('|     ------------------------   |')
    print ('|                                |')
    print ('|                          OSOYOO|')
    print ('==================================\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    #GPIO.setup(BuzzerPin,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(PIRPinIn,GPIO.IN)
    GPIO.setup(PIRPinOut,GPIO.IN)
#main function
def main():

    global IMAGE_NUM
    global REMOTEHOST
    global REMOTEADDRESS

    #print info
    print_message()
    while True:
        #read Sw520dPin's level
        if(GPIO.input(PIRPinIn)!=0):
            starttime=time.time()
            runtime = 0
            #GPIO.output(BuzzerPin,GPIO.LOW)
            #time.sleep(0.5)
            #print ('********************')
            print ('*     In Sensor!     *')
            #print ('********************')
            print ('\n')
            capture("out", IMAGE_NUM)
            while(runtime < 3):
                runtime = time.time() - starttime
                if(GPIO.input(PIRPinOut)!=0):
                    print("=============")
                    print("*    Out    *")
                    print("=============")
                    time.sleep(5)
                    setup()
                    break
            #os.system('./camera.sh')
            #print (time.time() - starttime)
            time.sleep(1)

        elif(GPIO.input(PIRPinOut)!=0):
            starttime=time.time()
            runtime = 0
            #print ('*******************')
            print ('*    Out Sensor    *')
            #print ('*******************')
            print('\n')
            while(runtime < 3):
                runtime = time.time() - starttime
                if(GPIO.input(PIRPinIn)!=0):
                    print("===============")
                    print("*     In      *")
                    print("===============")
                    capture("inn", IMAGE_NUM)
                    GPIO.setup(PIRPinOut, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                    GPIO.setup(PIRPinIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                    time.sleep(5)
                    break
            time.sleep(1)
        else:
            #GPIO.output(BuzzerPin,GPIO.HIGH)
            #print ('====================')
            print ('=     Not alarm...  =')
            #print ('====================')
            print ('\n')
        time.sleep(1)


def capture(io, filename):

    global IMAGE_NUM
    global REMOTEHOST
    global REMOTEADDRESS

    time.sleep(1)
    filename = io + str(filename)
    cmd = "fswebcam -r 528x432 ./files/" + filename + ".jpg" 
    os.system(cmd)  
    
    pool = Pool(2)
    pool.apply_async(start_scp, (filename, ))

    IMAGE_NUM += 1         

# Send picture to server by scp
# Reference: https://github.com/pexpect/pexpect/blob/master/examples/ssh_tunnel.py 
def start_scp(filename):
    tunnel_command = "scp ./files/" + str(filename) + ".jpg " + REMOTEHOST + "@" + REMOTEADDRESS + ":~/lslab/original_images/"
    
    try:
        scp_tunnel = pexpect.spawn(tunnel_command % globals())
        scp_tunnel.expect('password:')
        time.sleep(0.1)
        scp_tunnel.sendline(X)
        time.sleep(5)
        scp_tunnel.expect (pexpect.EOF)

    except Exception as e:
        print(str(e))

#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off buzzer
    #GPIO.output(BuzzerPin,GPIO.HIGH)
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
        pass

