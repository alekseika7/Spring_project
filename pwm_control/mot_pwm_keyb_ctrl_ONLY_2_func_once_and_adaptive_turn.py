#!/usr/bin/python3.7

#NEEDS TO BE DONE:
# 1) get away from 'sudo'
# 2) try to control from virtual keyboard
# 3) set maximum PWM level instead of "1". Like for example u have a very powerful motors

# DONE:
# adaptive turn, bug fix in all directions
# there is a way from RIGHT(LEFT) back to FRONT(BACK)RIGHT(LEFT)

import keyboard
from time import *
from mot_pwm_keyb_ctrl_SUMMARY_2 import *

# Keyboard contol. Reacts on small turns not stopping the car.
def keyboard_ctrl_start(\
fullspeed_latency_time = 0.8, USER_swerve_intensity_level = 0.5, sleeptime_per_gear = 0.2, swerve_increase_level = 0.01 ):

    init()
    motors_enable()
    #motors_off()
    off_tic_start = time()
    BREAKS_needs_to_run = True
    print('Driving started, press H for help')
    sleep(fullspeed_latency_time)
    print("Press and hold SPACE to end program")

    while True:

        if keyboard.is_pressed('Space'):
            motors_off()
            off_n_reset()
            print('Done')
            break

        elif keyboard.is_pressed('h'):
            print(''' \n \
Arguements: fullspeed_latency_time, USER_swerve_intensity_level, sleeptime_per_gear, swerve_increase_level \n
Possible variants for 'fullspeed_latency_time' = 0 .. inf \n \
Stands for the amount of time passed after motors_off command perfomed in order to toggle smooth_start \n \
Recommended value is less than 0.8 second hence it is the duration of the smooth_start in current version \n
Possible variants for 'swerve_intensity_level' = 0, 0.1 ... up to 1  \n \
The less the faster turn would be. \n
Possible variants for 'sleeptime_per_gear' = 0, 0.1 and more. Recommended is 0.2. \n \
The general amount of time spent for an acceleration will be calculated as time*4 (amount of gears in pwm_list). \n
Possible variants for 'swerve_increase_level' = 0.01, 0.02 etc. The bigger number is the faster turn is . \n \
Recommended is 0.01. Keep in mind sleep time per itteration - 0.05 second by default \n \
Done. Please restart the code. \n ''')
            break

        elif keyboard.is_pressed('w'):

            W_needs_to_run = True
            BREAKS_needs_to_run = True

            if  time() - off_tic_start >= fullspeed_latency_time :
                smooth_start('front', sleeptime_per_gear)
                move('front', 1)
            else:
                move('front', 1)

            W_needs_to_run = False

            while keyboard.is_pressed('w'):
                if keyboard.is_pressed('w+a'):
                    WA_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('w+a'):
                        if swerve_intensity_level >= 0:
                            swerve('front', 'left', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            WA_needs_to_run = False
                            W_needs_to_run = True
                elif keyboard.is_pressed('w+d'):
                    WD_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('w+d'):
                        if swerve_intensity_level >= 0:
                            swerve('front', 'right', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            WD_needs_to_run = False
                            W_needs_to_run = True
                else:
                    if W_needs_to_run:
                        move('front', 1)
                        W_needs_to_run = False

        elif keyboard.is_pressed('s'):

            S_needs_to_run = True
            BREAKS_needs_to_run = True

            if  time() - off_tic_start >= fullspeed_latency_time :
                smooth_start('back', sleeptime_per_gear)
                move('back', 1)
            else:
                move('back', 1)

            S_needs_to_run = False

            while keyboard.is_pressed('s'):
                if keyboard.is_pressed('s+a'):
                    SA_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('s+a'):
                        if swerve_intensity_level >= 0:
                            swerve('back', 'left', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            SA_needs_to_run = False
                            S_needs_to_run = True
                elif keyboard.is_pressed('s+d'):
                    SD_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('s+d'):
                        if swerve_intensity_level >= 0:
                            swerve('back', 'right', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            SD_needs_to_run = False
                            S_needs_to_run = True
                else:
                    if S_needs_to_run:
                        move('back', 1)
                        S_needs_to_run = False

        elif keyboard.is_pressed('a'):
            A_needs_to_run = True
            BREAKS_needs_to_run = True
            while keyboard.is_pressed('a'):
                if keyboard.is_pressed('w+a'):
                    WA_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('w+a'):
                        if swerve_intensity_level >= 0:
                            swerve('front', 'left', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            WA_needs_to_run = False
                            A_needs_to_run = True
                elif keyboard.is_pressed('s+a'):
                    SA_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('s+a'):
                        if swerve_intensity_level >= 0:
                            swerve('back', 'left', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            SA_needs_to_run = False
                            A_needs_to_run = True
                if A_needs_to_run:
                    turn('left', 1)
                    A_needs_to_run = False

        elif keyboard.is_pressed('d'):
            D_needs_to_run = True
            BREAKS_needs_to_run = True
            while keyboard.is_pressed('d'):
                if keyboard.is_pressed('w+d'):
                    WD_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('w+d'):
                        if swerve_intensity_level >= 0:
                            swerve('front', 'right', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            WD_needs_to_run = False
                            D_needs_to_run = True
                elif keyboard.is_pressed('s+d'):
                    SD_needs_to_run = True
                    swerve_intensity_level = USER_swerve_intensity_level
                    while keyboard.is_pressed('s+d'):
                        if swerve_intensity_level >= 0:
                            swerve('back', 'right', swerve_intensity_level)
                            sleep(0.05)
                            swerve_intensity_level = swerve_intensity_level - swerve_increase_level
                            SD_needs_to_run = False
                            D_needs_to_run = True
                if D_needs_to_run:
                    turn('right', 1)
                    D_needs_to_run = False

        else:
            if BREAKS_needs_to_run:
                off_tic_start = time()
                motors_off()
                BREAKS_needs_to_run = False
#################################################################

keyboard_ctrl_start()
