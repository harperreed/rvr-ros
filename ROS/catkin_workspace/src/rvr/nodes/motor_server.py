#!/usr/bin/env python
# coding=utf-8

"""
This is a service node (server) to control motors on the RVR.
It controls the motors via [... tbd ...] on a Raspberry Pi.
I expects the messsages "FORWARD, BACKWARD, LEFT, RIGHT, STOP".

Author:  Markus Knapp, 2020
Website: https://direcs.de
"""


# name of the package.srv
from rvr.srv import *
import rospy

# Service nodes have to be initialised
rospy.init_node('motor_server', anonymous=False)


# getting the hostname of the underlying operating system
import socket
# showing hostname
hostname = socket.gethostname()
if hostname == 'rvr':
    rospy.loginfo("Running on host %s.", hostname)
else:
    rospy.logwarn("Running on host %s!", hostname)


# RVR stuff
if hostname == 'rvr':
    rospy.loginfo("Setting up RVR...")
    
    import os
    import sys
    # path to find the RVR lib from the SDK
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './lib/')))

    import asyncio
    from sphero_sdk import SpheroRvrAsync
    from sphero_sdk import SerialAsyncDal
    from sphero_sdk import DriveFlagsBitmask


    loop = asyncio.get_event_loop()

    rvr = SpheroRvrAsync(
        dal=SerialAsyncDal(
            loop
        )
    )
else:
    rospy.logwarn("Skipping RVR setup. This is not the robot.")


# define a clean ROS node exit
def my_exit():
    rospy.loginfo("Shutting down motor service...")
    # run some parts only on the real robot
    if hostname == 'rvr':
        # turn Off Motors()
    rospy.loginfo("...shutting down motor service complete.")


# call this method on ROS node exit
rospy.on_shutdown(my_exit)


# handle_motor is called with instances of MotorRequest and returns instances of MotorResponse
# The ROS request name comes directly from the .srv filename
async def handle_motor(req):
    """ In this function all the work is done :) """
    if hostname == 'rvr':
        # start RVR comms
        await rvr.wake()
        # Give RVR time to wake up
        await asyncio.sleep(2)
        await rvr.reset_yaw()

    # switch motors
    if (req.direction == "FORWARD"): # and speed. returns result.
        # drive
        rospy.loginfo("Driving %s @ speed %s.", req.direction, req.speed)
        if hostname == 'rvr':
            # set speed for RVR
            speed=req.speed
            # translate direction to heading for RVR
            # @to do!
            await rvr.drive_with_heading(
                speed=128,  # Valid speed values are 0-255
                heading=90,  # Valid heading values are 0-359
                flags=DriveFlagsBitmask.none.value
            )
            # Delay to allow RVR to drive
            await asyncio.sleep(1)

    if hostname == 'rvr':
        # stop RVR comms
        await rvr.close()


async def main():
    # This declares a new service named 'motor with the Motor service type.
    # All requests are passed to the 'handle_motor' function.
    # 'handle_motor' is called with instances of MotorRequest and returns instances of MotorResponse
    s = rospy.Service('motor', Motor, handle_motor)
    rospy.loginfo("Ready to switch motors.")

    # Keep our code from exiting until this service node is shutdown
    rospy.spin()


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
