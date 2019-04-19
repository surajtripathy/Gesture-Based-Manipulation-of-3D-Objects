import rotate_cube
import temp_leap
#from leap_gesture import LeapListener
import threading
import time
#import Leap , sys
#from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#from multiprocessing import Pipe
#parent , child = Pipe()

'''def main():
    print("Press enter to quit")
    listener = LeapListener()
    controller = Leap.Controller()

    controller.add_listener(listener)


    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)'''
#import os
#os.remove(temp_data)


t1 = threading.Thread(target = rotate_cube.main)
t2 = threading.Thread(target = temp_leap.main)
t1.daemon = True
t2.daemon = True
t2.start()
t1.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
