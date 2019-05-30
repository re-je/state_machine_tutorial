#!/usr/bin/env python

import qt_smach_viewer.introspection
import rospy
import smach

# Exercise 1


class WaitState(smach.State):
    def __init__(self):
        super(WaitState, self).__init__(
            outcomes=["continue"], input_keys=["sleep_time"]
        )

    def execute(self, ud):
        rospy.sleep(ud.sleep_time)
        return "continue"


# Exercise 2


class MessageReader(smach.State):
    def __init__(self):
        super(MessageReader, self).__init__(outcomes=["continue"], io_keys=["msg"])

    def execute(self, ud):
        # print to the rospy log at level info
        rospy.loginfo("Message in the userdata : %s", ud.msg)
        # rospy.loginfo(ud.msg) # alternative
        ud.msg = ""  # reset the message
        rospy.sleep(1.0)
        return "continue"


# Exercise 3


class MessageReader2(smach.State):
    def __init__(self):
        super(MessageReader2, self).__init__(
            outcomes=["continue", "empty"], input_keys=["reset"], io_keys=["msg"]
        )

    def execute(self, ud):
        rospy.sleep(1.0)
        if ud.msg:  # an empty string is considered False, non-empty True
            rospy.loginfo(ud.msg)  # print in the rospy log at level info
            if ud.reset:
                rospy.logwarn("Emptying message!")
                ud.msg = ""  # reset the message
            return "continue"
        else:
            rospy.logerr("Message empty!")
            return "empty"
