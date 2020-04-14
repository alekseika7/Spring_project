#!/usr/bin/python3.7

import keyboard
from time import *
from mot_pwm_keyb_ctrl_SUMMARY_2 import *

# Keyboard contol. Reacts on small turns not stopping the car.
def keyboard_ctrl_start(fullspeed_latency_time, swerve_intensity_level, sleeptime_per_gear):

    stat = 'off'
    init()
    motors_enable()
    motors_off()
    off_tic_start = time()
    #tic_turn = time()
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
Arguements: fullspeed_latency_time, swerve_intensity_level, sleeptime_per_gear \n
Possible variants for 'fullspeed_latency_time' = 0 .. inf \n \
Stands for the amount of time passed after motors_off command perfomed in order to toggle smooth_start \n \
Recommended value is less than 0.8 second hence it is the duration of the smooth_start in current version \n
Possible variants for 'swerve_intensity_level' = 0, 0.1 ... up to 1  \n \
The less the faster turn would be. \n
Possible variants for 'sleeptime_per_gear' = 0, 0.1 and more. Recommended is 0.2. \n \
The general amount of time spent for an acceleration will be calculated as time*4 (amount of gears in pwm_list). \n \
Done. Please restart the code. \n ''')
            break
        elif stat == 'off':

            if keyboard.is_pressed('w'):
                stat = 'on'
                if  time() - off_tic_start >= fullspeed_latency_time :
                    #stat = 'on'
                    smooth_start('front', sleeptime_per_gear)
                    move('front', 1)
                else:
                    #stat = 'on'
                    move('front', 1)

                while keyboard.is_pressed('w'):

                    if keyboard.is_pressed('w+a'):
                        #stat = 'on'
                        swerve('front', 'left', swerve_intensity_level)

                    elif keyboard.is_pressed('w+d'):
                        #stat = 'on'
                        swerve('front','right', swerve_intensity_level)

                    else:
                        #stat = 'on'
                        move('front', 1)

            elif keyboard.is_pressed('s'):
                stat = 'on'
                if  time() - off_tic_start >= fullspeed_latency_time :
                    #stat = 'on'
                    smooth_start('back', sleeptime_per_gear)
                    move('back', 1)
                else:
                    #stat = 'on'
                    move('back', 1)

                while keyboard.is_pressed('s'):

                    if keyboard.is_pressed('s+a'):
                        #stat = 'on'
                        swerve('back', 'left', swerve_intensity_level)

                    elif keyboard.is_pressed('s+d'):
                        #stat = 'on'
                        swerve('back','right', swerve_intensity_level)

                    else:
                        #stat = 'on'
                        move('back', 1)


            elif keyboard.is_pressed('a'):
                stat = 'on'
                turn('left', 1)

            elif keyboard.is_pressed('d'):
                stat = 'on'
                turn('right', 1)

            else:
                pass

        else:
            if keyboard.is_pressed('w'):
                stat = 'on'
                #if keyboard.is_pressed('w+a'):
                    #stat = 'on'
                #elif keyboard.is_pressed('w+d'):
                    #stat = 'on'
                #else:
                    #stat = 'on'
            elif keyboard.is_pressed('s'):
                stat = 'on'
                #if keyboard.is_pressed('s+a'):
                    #stat = 'on'
                #elif keyboard.is_pressed('s+d'):
                    #stat = 'on'
                #else:
                    #stat = 'on'
            elif keyboard.is_pressed('a'):
                stat = 'on'
            elif keyboard.is_pressed('d'):
                stat = 'on'
            else:
                stat = 'off'
                off_tic_start = time()
                motors_off()

#################################################################

keyboard_ctrl_start(0.8, 0.5, 0.2)
