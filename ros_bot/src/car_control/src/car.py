#!/usr/bin/python3.7

import RPi.GPIO as gpio
import os

pins = (15, 14, 18, 3, 2, 4)

class PWM:
    def __init__(self, pin):
        self.pin = pin

    def set(self, value):
        cmd = 'echo \"' + str(self.pin) + '=' + str(value) + '\" > /dev/pi-blaster'
        os.system(cmd)

    def release(self):
        cmd = 'echo \"release ' + str(self.pin) + '\" > /dev/pi-blaster'
        os.system(cmd)

# preparing motors enable pins vars for PWM()
pin3 = PWM(3)
pin15 = PWM(15)

# preparingright motor start moving pins vars for PWM()
pin14 = PWM(14)
pin18 = PWM(18)

# preparingleft motor start moving pins vars for PWM()
pin2 = PWM(2)
pin4 = PWM(4)

#initialize pins
def init():

    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(pins, gpio.OUT)
    pin15.set(1)
    pin14.set(0)
    pin18.set(0)
    pin3.set(1)
    pin2.set(0)
    pin4.set(0)


#turn off motors
def motors_off():

    pin14.set(0)
    pin18.set(0)
    pin2.set(0)
    pin4.set(0)


#turn on left motor to the special direction
def _left_m_on(speed):

    if speed > 0:
        pin4.set(speed)
        pin2.set(0)
    elif speed < 0:
        pin4.set(0)
        pin2.set(-speed)
    else:
        pin4.set(0)
        pin2.set(0)


#turn on rigth motor to the special direction
def _right_m_on(speed):

    if speed > 0:
        pin18.set(speed)
        pin14.set(0)
    elif speed < 0:
        pin18.set(0)
        pin14.set(-speed)
    else:
        pin18.set(0)
        pin14.set(0)


#Direct controll of both motors
def direct_controll(speed_l, speed_r):

    _left_m_on(speed_l)
    _right_m_on(speed_r)


'''
#move to the special direction
def move(direction, speed):

    if direction == 'front':
        _left_m_on('front', speed)
        _right_m_on('front', speed)

    elif direction == 'back':
        _left_m_on('back', speed)
        _right_m_on('back', speed)


#turn to the special direction
def turn(direction, speed):

    if direction == 'right':
        _left_m_on('front', speed)
        _right_m_on('back', speed)

    elif direction == 'left':
        _left_m_on('back', speed)
        _right_m_on('front', speed)
'''

#turn off pins and reset most of them to the input mode
def off_n_reset():

    pin15.set(0)
    pin14.set(0)
    pin18.set(0)
    pin3.set(0)
    pin2.set(0)
    pin4.set(0)
    gpio.cleanup((15, 14, 18, 3, 4))