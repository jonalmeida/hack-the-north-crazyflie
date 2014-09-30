
import time, sys
from threading import Thread

#FIXME: Has to be launched from within the example folder
sys.path.append("/home/jonathan/cfclient-2014.01.0/lib")
import cflib
from cflib.crazyflie import Crazyflie

from controller import SampleListener

import logging
logging.basicConfig(level=logging.ERROR)

class Hover:
    def __init__(self, link_uri, control_listener):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie()

        self._control_listener = control_listener

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print "Connecting to %s" % link_uri

    def _connected(self, link_uri):
        print "Connected to %s" % link_uri
        Thread(target=self._hover_this_shit).start()
        # self._hover_this_shit()

    def _disconnected(self, link_uri):
        print "disconnected from %s" % link_uri

    def _connection_failed(self, link_uri, msg):
        print "Connection to %s failed: %s" % (link_uri, msg)

    def _connection_lost(self, link_uri, msg):
        print "Connection to %s lost: %s" % (link_uri, msg)

    # def _hover_this_shit(self):
    #     print "Hovering this shit"
    #     thrust_mult = 1.5
    #     thrust_step = 500
    #     thrust = 20000
    #     pitch = -6
    #     roll = -2
    #     yawrate = 0
    #     while thrust >= 20000:
    #         self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
    #         time.sleep(0.1)
    #         if thrust >=47000:
    #             thrust_mult = -1
    #         thrust += thrust_step * thrust_mult
    #     self._cf.commander.send_setpoint(0, 0, 0, 0)
    #     # Make sure that the last packet leaves before the link is closed
    #     # since the message queue is not flushed before closing
    #     time.sleep(0.1)
    #     self._cf.close_link()

    def _hover_this_shit(self):
        print "Hovering this shit"
        # try:
        while True:
            print "asdasd %s %s %s %d" % (
                int(self._control_listener.roll()*10),
                int(self._control_listener.pitch()*10),
                int(self._control_listener.yaw()*100), 
                int(self._control_listener.y() * 40000))

            self._cf.commander.send_setpoint(
                int(self._control_listener.roll()*10),
                int(self._control_listener.pitch()*10),
                int(self._control_listener.yaw()*100), 
                int(self._control_listener.y() * 40000))
            time.sleep(0.1)
        # except (KeyboardInterrupt):
        #     self._cf.commander.send_setpoint(0, 0, 0, 0)
        #     self._cf.close_link()
        #     exit