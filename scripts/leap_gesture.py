import Leap , sys , os, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#sys.stdout = open('temp_data','w')
#f = open('temp_data', 'w', os.O_NONBLOCK)
class LeapListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pink']
    bones_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Disto']
    state_names = ['STATE_INVALID', 'STATE_START', ' STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print("Initialised")

    def on_connect(self, controller):
        print("Motion Sensor Connected")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);

    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        '''print("frame id:" + str(frame.id) \
        + "Timestamp" + str(frame.timestamp) \
        + "No of hands" + str(len(frame.hands)) \
        + "No of fingers" + str(len(frame.fingers)) \
        + "No of tools" + str(len(frame.tools)) \
        + "No of gestures" + str(len(frame.gestures()))) '''
        f = open('temp_data','a')
        for hand in frame.hands:
            handType = "Left Hand" if hand.is_left else "Right Hand"
            #print(handType + "Hand ID:" + str(hand.id) + "    " + str(hand.palm_position))
            #print(handType)
            f.write(handType + '\n')
            f.flush()
            time.sleep(0.1)
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

#if __name__ == "__main__":
#    on_leap_start()
