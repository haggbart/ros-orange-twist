#!/usr/bin/env python

import rospy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import Twist


MULTIPLIER = 1.0
SHIFT = 0.0
SECONDS_PER_MOVE = 0.0010  # doesn't need to be accurate, will accelerate to catch up and smooth its movement


NODE_NAME = "ur5e_sin_publisher"
PUBLISHER = "/scaled_pos_joint_traj_controller/command"
SUBSCRIBER = "/test_msg"

JOINT_NAMES = ['elbow_joint', 'shoulder_lift_joint', 'shoulder_pan_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

# dont edit below pls
NSECS = SECONDS_PER_MOVE % 1 * 10000000000
SECS = int(SECONDS_PER_MOVE)


def get_publisher_msg(rotation):
    msg = JointTrajectory()
    msg.header.stamp = rospy.Time.now()
    msg.joint_names = JOINT_NAMES
    joint_trajectory_point = JointTrajectoryPoint()
    joint_trajectory_point.positions = [1.57, -1.57, -3.14, -1.57, rotation * MULTIPLIER + SHIFT, 0.0]
    joint_trajectory_point.time_from_start.secs = SECS
    joint_trajectory_point.time_from_start.nsecs = NSECS
    msg.points.append(joint_trajectory_point)
    return msg


class Spinner:
    def __init__(self):
        self.pub = rospy.Publisher(PUBLISHER, JointTrajectory, queue_size=1)
        self.sub = rospy.Subscriber(SUBSCRIBER, Twist, self.callback_rotation)

    def callback_rotation(self, msg):
        msg = get_publisher_msg(msg.angular.z)
        self.pub.publish(msg)


if __name__ == '__main__':
    rospy.init_node(NODE_NAME)
    Spinner()
    rospy.loginfo("Initialized.")
    rospy.spin()
