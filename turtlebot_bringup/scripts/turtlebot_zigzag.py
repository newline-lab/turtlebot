#!/usr/bin/env python

import rospy

from std_msgs.msg import Int32

from geometry_msgs.msg import Twist

from math import radians

from sensor_msgs.msg import LaserScan

import tf

from std_msgs.msg import Empty

from time import sleep

from statistics import mean


g_range_ahead = []
for i in range(0,725):  
    g_range_ahead.append(i)

#list_true = []

def callback(data): 
    for i in range(0,725):  
        g_range_ahead[i] = data.ranges[i]

def get_g_range_ahead():
    global list_true 
    list_true = []
    for i in range(100,650): 
        if g_range_ahead[i] > 0.02:
            list_true.append(g_range_ahead[i])
    min_grange = min(list_true)
    print("min ranges", min_grange)

    return min_grange



def main():
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, callback)

    cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

    r = rospy.Rate(10);
    d = 35

    while not rospy.is_shutdown():
        min_grange = get_g_range_ahead()
        move_cmd = Twist()
        move_cmd.linear.x = -0.1

        d = d * -1

        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(d); 

        turn_cmd2 = Twist()
        turn_cmd2.linear.x = 0
        turn_cmd2.angular.z = radians(35);

        if(min_grange < 0.3):
            print("Obst")
            rospy.loginfo("obistical")
            rospy.loginfo("Turning")
            cmd_vel.publish(turn_cmd2) 
            r.sleep()

        else: 
            rospy.loginfo("Going Straight")
            cmd_vel.publish(move_cmd)
            r.sleep()
        

def shutdown():
    # stop turtlebot
    rospy.loginfo("Stop Zgzag")
    cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
    cmd_vel.publish(Twist())
    rospy.sleep(1)

if __name__ == '__main__':
    try: 
        main()
        rospy.loginfo("trying...")
    except: 
        main()
        rospy.loginfo("trying...")