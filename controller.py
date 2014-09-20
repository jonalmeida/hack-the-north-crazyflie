import os, sys, inspect, thread, time

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import hover
import scan

from threading import Thread

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "controller on_init called"
        self._x = 0;
        self._y = 0;
        self._z = 0;
        self._pitch = 0;
        self._roll = 0;
        self._yaw = 0;
        my_hover = hover.Hover(scan.getAvailable(), self);
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

        # my_hover = hover.Hover(scan.getAvailable(), self);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        i_box = frame.interaction_box
        hand_of_interest = frame.hands[0]

        normalized_hand = i_box.normalize_point(hand_of_interest.fingers[0].tip_position)

        # print "id %d, position:\t x - %s,\t y - %s,\t z - %s, " % (
        #     frame.id, 
        #     normalized_hand.x,
        #     normalized_hand.y,
        #     normalized_hand.z)

        # # Get the hand's normal vector and direction
        # normal = hand_of_interest.palm_normal
        # direction = hand_of_interest.direction

        # print "id %d position:\t p - %f,\t r - %f,\t y - %f, " % (
        #     frame.id, 
        #     direction.pitch * Leap.RAD_TO_DEG,
        #     normal.roll * Leap.RAD_TO_DEG,
        #     direction.yaw * Leap.RAD_TO_DEG)

        # Get hands
        # for hand in frame.hands:

        #     handType = "Left hand" if hand.is_left else "Right hand"

        #     print "  %s, id %d, position: %s" % (
        #         handType, hand.id, hand.palm_position)

        #     # Get the hand's normal vector and direction
        #     normal = hand.palm_normal
        #     direction = hand.direction

        #     # Calculate the hand's pitch, roll, and yaw angles
        #     print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
        #         direction.pitch * Leap.RAD_TO_DEG,
        #         normal.roll * Leap.RAD_TO_DEG,
        #         direction.yaw * Leap.RAD_TO_DEG)

        #     # Get arm bone
        #     arm = hand.arm
        #     print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
        #         arm.direction,
        #         arm.wrist_position,
        #         arm.elbow_position)

        #     # Get fingers
        #     for finger in hand.fingers:

        #         print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
        #             self.finger_names[finger.type()],
        #             finger.id,
        #             finger.length,
        #             finger.width)

        #         # Get bones
        #         for b in range(0, 4):
        #             bone = finger.bone(b)
        #             print "      Bone: %s, start: %s, end: %s, direction: %s" % (
        #                 self.bone_names[bone.type],
        #                 bone.prev_joint,
        #                 bone.next_joint,
        #                 bone.direction)

        # # Get tools
        # for tool in frame.tools:

        #     print "  Tool id: %d, position: %s, direction: %s" % (
        #         tool.id, tool.tip_position, tool.direction)

        # # Get gestures
        # for gesture in frame.gestures():
        #     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
        #         circle = CircleGesture(gesture)

        #         # Determine clock direction using the angle between the pointable and the circle normal
        #         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
        #             clockwiseness = "clockwise"
        #         else:
        #             clockwiseness = "counterclockwise"

        #         # Calculate the angle swept since the last frame
        #         swept_angle = 0
        #         if circle.state != Leap.Gesture.STATE_START:
        #             previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
        #             swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

        #         print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

        #     if gesture.type == Leap.Gesture.TYPE_SWIPE:
        #         swipe = SwipeGesture(gesture)
        #         print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 swipe.position, swipe.direction, swipe.speed)

        #     if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
        #         keytap = KeyTapGesture(gesture)
        #         print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 keytap.position, keytap.direction )

        #     if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
        #         screentap = ScreenTapGesture(gesture)
        #         print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 screentap.position, screentap.direction )

        # if not (frame.hands.is_empty and frame.gestures().is_empty):
        #     print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

    def x(self):
        return self._x;

    def y(self):
        return self._y;

    def z(self):
        return self._z;

    def pitch(self):
        return self._pitch;

    def roll(self):
        return self._roll;

    def yaw(self):
        return self._yaw;

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

# Thread(target=self._hover_this_shit).start()
    # my_hover = hover.Hover(scan.getAvailable(), listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
