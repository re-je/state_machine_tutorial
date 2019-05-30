#!/usr/bin/env python2

import rospy
import smach
from qt_smach_viewer.introspection import IntrospectionServer


# Exercise 2: Read a message from a userdata
# Fill this class
class MessageReader(smach.State):
    def __init__(self):
        super(MessageReader, self).__init__(
            outcomes=[""], input_keys=[], output_keys=[], io_keys=[]
        )

    def execute(self, ud):
        return ""


# This state write inside the userdata "msg", the message set as argument when created.
# For example, if you create this state with Set(msg="Hello World"), the userdate will be set to "Hello World"
class Set(smach.State):
    def __init__(self, msg=""):
        # To highlight the use of the remapping, here is an example, note that the input keys and output keys are differents
        # But it possible to still links them to the same 'userdata' by using the remapping in the State Machine
        super(Set, self).__init__(
            outcomes=["done"], input_keys=["Set_msg_in"], output_keys=["Set_msg_out"]
        )
        self.msg = msg

    def execute(self, ud):
        # print in the log at level info
        rospy.loginfo("Current userdata 'msg' : %s", ud.Set_msg_in)
        ud.Set_msg_out = self.msg
        rospy.sleep(3.0)
        return "done"


# Create the State Machine Here
def SetPrintStateMachine():
    SetPrint_sm = smach.StateMachine(outcomes=["exit"])
    # We Initialize the userdata "msg"
    SetPrint_sm.userdata.msg = "This is the initial data"

    with SetPrint_sm:
        SetPrint_sm.add(
            "Set",
            Set("Hello World"),
            transitions={"done": "Print"},
            # We set the remmaping to "msg"
            remapping={"Set_msg_in": "msg", "Set_msg_out": "msg"},
        )

        SetPrint_sm.add(
            "Print", MessageReader(), transitions={"continue": "Print_again"}
        )
        SetPrint_sm.add(
            "Print_again", MessageReader(), transitions={"continue": "exit"}
        )

    return SetPrint_sm


def main():

    SimpleSM = SetPrintStateMachine()

    introspection_server = IntrospectionServer(SimpleSM)
    introspection_server.start()
    rospy.sleep(3.0)
    outcome = SimpleSM.execute()
    rospy.loginfo("Result : %s", outcome)
    introspection_server.stop()


if __name__ == "__main__":
    rospy.init_node("tutorial_node")
    main()
