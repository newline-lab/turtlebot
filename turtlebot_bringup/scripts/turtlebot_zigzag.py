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

g_range_ahead = 1.0
type(g_range_ahead)

def callback(data): 

    g_range_ahead = min(data.ranges[300:420])
    print("grange1", g_range_ahead)
    #scan_sub = rospy.Subscriber('scan', LaserScan, callback) 
    #cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

def get_g_range_ahead():
    print("grange2", g_range_ahead)
    return g_range_ahead

def DrawZgzag():
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    get_g_range_ahead()
    

    cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

    r = rospy.Rate(10);
    d = 35

    while not rospy.is_shutdown():
        g_range_ahead = get_g_range_ahead()
        move_cmd = Twist()
        move_cmd.linear.x = 0.2

        d = d * -1

        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(d); 

        turn_cmd2 = Twist()
        turn_cmd2.linear.x = 0
        turn_cmd2.angular.z = radians(45);

        if(g_range_ahead < 0.5):
            print("grange", g_range_ahead)
            rospy.loginfo("obistical")

            for x in range(0,10): 
                #cmd_vel.publish(turn_cmd2) 
                r.sleep()

        else: 
            rospy.loginfo("Going Straight")
            for x in range(0,10):
                #cmd_vel.publish(move_cmd)
                r.sleep()
        # turn 90 degrees

            rospy.loginfo("Turning")
            for x in range(0,10): 
                #cmd_vel.publish(turn_cmd) 
                r.sleep()



def shutdown():
    # stop turtlebot
    rospy.loginfo("Stop Zgzag")
    cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
    cmd_vel.publish(Twist())
    rospy.sleep(1)

if __name__ == '__main__':
    try: 
        DrawZgzag()
        rospy.loginfo("trying...")
    except: 
        shutdown()
        rospy.loginfo("shutdown")