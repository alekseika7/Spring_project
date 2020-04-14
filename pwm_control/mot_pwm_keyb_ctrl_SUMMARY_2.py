#!/usr/bin/python3.7

import RPi.GPIO as gpio
import os
from time import *

pins = (15, 14, 18, 3, 2, 4)

# this is a tool for an easy way to send commands to pi-blaster
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

# initialize pins
def init():

    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(pins, gpio.OUT)
    pin15.set(0)
    pin14.set(0)
    pin18.set(0)
    pin3.set(0)
    pin2.set(0)
    pin4.set(0)

# set voltage on enable pins
def motors_enable():

    pin3.set(1)
    pin15.set(1)

# turn off motors
def motors_off():

    pin14.set(0)
    pin18.set(0)
    pin2.set(0)
    pin4.set(0)

# turn on left motor to the special direction, speed from [0, 0.1 ... to 1]
def _right_m_on(direction, speed):

    if direction == 'front':
        pin14.set(speed)
        pin18.set(0)
    else:
        pin14.set(0)
        pin18.set(speed)

# turn on left motor to the special direction, speed from [0, 0.1 ... to 1]
def _left_m_on(direction, speed):

    if direction == 'front':
        pin2.set(speed)
        pin4.set(0)
    else:
        pin2.set(0)
        pin4.set(speed)

# move to the special direction, speed from [0, 0.1 ... to 1]
def move(direction, speed):

    if direction == 'front':
        _left_m_on('front', speed)
        _right_m_on('front', speed)

    elif direction == 'back':
        _left_m_on('back', speed)
        _right_m_on('back', speed)

    else:
        print('Possible variants for the direction: front, back. \
        Speed from [0, 0.1 ... to 1]')

# U - turn to the special direction, speed from [0, 0.1 ... to 1]
def turn(direction, speed):

    if direction == 'right':
        _left_m_on('front', speed)
        _right_m_on('back', speed)

    elif direction == 'left':
        _left_m_on('back', speed)
        _right_m_on('front', speed)

    else:
        print('Possible variants for the direction: right, left. \
        write them in commas \
        Speed from [0, 0.1 ... to 1]')

# turn off pins and reset most of them to the input mode
def off_n_reset():

    pin15.set(0)
    pin14.set(0)
    pin18.set(0)
    pin3.set(0)
    pin2.set(0)
    pin4.set(0)
    gpio.cleanup((15, 14, 18, 3, 4))
##############################################################

# SMOOTHLY move to the special direction
#
def smooth_start(direction, sleeptime_per_gear):

    # pwm_list = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
    pwm_list = (0.4, 0.5, 0.7, 0.9)

    if direction == 'front':
        for gear in pwm_list:
            move('front', gear)
            sleep(sleeptime_per_gear)
            gear = pwm_list[0]

    elif direction == 'back':
        for gear in pwm_list:
            move('back', gear)
            sleep(sleeptime_per_gear)
            gear = pwm_list[0]
    else:
        print('''Possible variants for 'direction': front, back \n \
Possible variants for 'sleeptime_per_gear' : 0, 0.1 and more. Recommended is 0.2 \n \
The general amount of time spent for an acceleration will be calculated as time*4 (amount of gears in pwm_list)''')

# SWERViNG to the special direction,
# swerve_intensity_level from [0, 0.1 ... to 1] the less the faster turn would be

def swerve(front_or_back, right_or_left, swerve_intensity_level):

        if front_or_back == 'front':

            if right_or_left == 'right':
                _left_m_on('front', 1)
                _right_m_on('front', swerve_intensity_level)

            elif right_or_left == 'left':
                _left_m_on('front', swerve_intensity_level)
                _right_m_on('front', 1)

        elif front_or_back == 'back':

            if right_or_left == 'right':
                _left_m_on('back', 1)
                _right_m_on('back', swerve_intensity_level)

            elif right_or_left == 'left':
                _left_m_on('back', swerve_intensity_level)
                _right_m_on('back', 1)

        else:
            print('Aruements: front_or_back, right_or_left, swerve_intensity_level \n \
Possible variants for the front_or_back = front, back \n \
Possible variants for the right_or_left = right, left \n \
Write them in commas \n \
swerve_intensity_level from [0, 0.1 ... to 1]')
# ####################################################################3
