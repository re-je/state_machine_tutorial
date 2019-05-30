#!/usr/bin/env python2

import rospy
from qt_smach_viewer.introspection import IntrospectionServer
from smach_tutorial.BasicStateMachine import (
    BasicStateMachine_0,
    BasicStateMachine_1,
    BasicStateMachine_2,
)


def main1():

    SimpleSM = BasicStateMachine_1.FooBarStateMachine()

    introspection_server = IntrospectionServer(SimpleSM)
    introspection_server.start()

    outcome = SimpleSM.execute()
    rospy.loginfo("Result : %s", outcome)
    introspection_server.stop()


if __name__ == "__main__":
    rospy.init_node("tutorial_node")
    main1()  # Change to main1 to call your function
