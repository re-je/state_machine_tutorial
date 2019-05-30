#!/usr/bin/env python2

import rospy
import smach
from std_msgs.msg import Bool, Empty, String


class WaitForMessage(smach.State):
    def __init__(self, timeout=10):
        super(WaitForMessage, self).__init__(
            outcomes=["timeout", "message_received", "preempted"], output_keys=["msg"]
        )  # all outcomes and user data are defined
        # initialise the subscriber
        self.sub = rospy.Subscriber("/message", String, self.message_received_cb)
        # where we will put the content of the message
        self.msg = None
        # the timeout float
        self.timeout = timeout

    # callback of the subscriber
    def message_received_cb(self, msg):
        # we copy the content of the message inside our place holder
        self.msg = msg.data

    def execute(self, ud):
        # compute the timeout with rostime
        ros_timeout_ = rospy.Time().now() + rospy.Duration(self.timeout)
        while not self.msg:  # an empty string is considered False, non-empty True
            # check if we are over the timeout rostime
            if rospy.Time.now() > ros_timeout_:
                rospy.logwarn("Timed Out")  # warning message
                return "timeout"  # timeout
            # check if we are preempted or if ctrl+c
            elif self.preempt_requested() or rospy.is_shutdown():
                rospy.logwarn("Preempted ! (or shutdown)")  # waning message
                return "preempted"  # preempted
                rospy.sleep(0.1)  # free the thread for callback checking
        rospy.loginfo("Message received : '%s'", self.msg)  # information message
        ud.msg = self.msg  # copy the message content inside the userdata
        return "message_received"  # message received
