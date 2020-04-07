#!/usr/bin/python3.7

import RPi.GPIO as gpio

pins = (15, 14, 18, 3, 2, 4)

#initialize pins
def init():
    
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(pins, gpio.OUT)
    gpio.output(pins, 0)
    gpio.output((3, 15), 1) #set voltage on enable pins


#turn off motors
def motors_off():

    gpio.output((14, 18, 2, 4), 0)
    

#turn on left motor to the special direction
def _left_m_on(direction):
    
    if direction == 'front':
        gpio.output((14, 18), (1, 0))
    else:
        gpio.output((14, 18), (0, 1))


#turn on rigth motor to the special direction
def _right_m_on(direction):
    
    if direction == 'front':
        gpio.output((2, 4), (1, 0))
    else:
        gpio.output((2, 4), (0, 1))
        

#move to the special direction
def move(direction):
    
    if direction == 'front':
        _left_m_on('front')
        _right_m_on('front')
        
    elif direction == 'back':
        _left_m_on('back')
        _right_m_on('back')
        
    else:
        print('Possible variants for the direction: front, back')


#turn to the special direction
def turn(direction):
    
    if direction == 'right':
        _left_m_on('front')
        _right_m_on('back')
        
    elif direction == 'left':
        _left_m_on('back')
        _right_m_on('front')
        
    else:
        print('Possible variants for the direction: right, left') 

        
#turn off pins and reset most of them to the input mode
def off_n_reset():
    
    gpio.output(pins, 0)
    gpio.cleanup((15, 14, 18, 3, 4))
