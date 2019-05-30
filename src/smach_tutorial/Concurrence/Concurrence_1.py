#!/usr/bin/env python2

import random

import rospy
import smach
import smach_ros


class EmptyState(smach.State):
    def __init__(self):
        super(EmptyState, self).__init__(
            outcomes=["continue"], input_keys=[], output_keys=[], io_keys=[]
        )

    def execute(self, ud):
        rospy.sleep(2)
        return "continue"


class Ping(smach.State):
    def __init__(self):
        super(Ping, self).__init__(outcomes=["ping"], output_keys=["ping"])

    def execute(self, ud):
        rospy.sleep(3.0)
        rospy.loginfo("Pinging...")
        ud.ping = True
        return "ping"


class Pong(smach.State):
    def __init__(self):
        super(Pong, self).__init__(outcomes=["pong"], input_keys=["ping"])

    def execute(self, ud):
        while "ping" not in ud:
            rospy.loginfo("... Waiting for ping....")
            rospy.sleep(0.5)
        rospy.loginfo("Ping received")
        return "pong"


def SynchroConcurrence():
    Synchro_cc = smach.Concurrence(
        outcomes=["succeeded", "aborted"],
        default_outcome="aborted",
        outcome_map={"succeeded": {"Ping": "ping", "Pong": "pong"}},
    )

    with Synchro_cc:
        Synchro_cc.add("Ping", Ping())
        Synchro_cc.add("Pong", Pong())

    return Synchro_cc


def SimpleSM1():
    Simple_sm = smach.StateMachine(outcomes=["exit"])

    with Simple_sm:
        Simple_sm.add("Wait", EmptyState(), transitions={"continue": "Concurrence"})
        Simple_sm.add(
            "Concurrence",
            SynchroConcurrence(),
            transitions={"succeeded": "exit", "aborted": "exit"},
        )

    return Simple_sm


def main():
    Simple_sm = SimpleSM1()

    introspection_server = smach_ros.IntrospectionServer("SM", Simple_sm, "/SM_root")
    introspection_server.start()
    rospy.sleep(3.0)
    outcome = Simple_sm.execute()
    rospy.loginfo("Result : %s", outcome)
    introspection_server.stop()


##-----------------------------------------------------------------------------------

if __name__ == "__main__":
    rospy.init_node("tutorial_node")
    main()
