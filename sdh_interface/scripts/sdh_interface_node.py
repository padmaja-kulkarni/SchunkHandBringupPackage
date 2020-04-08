#!/usr/bin/env python

import rospy
from sdh_interface import SDHInterface
import math

def shutdownRos():
  print ("shutdown time!")


if __name__ == '__main__':
	rospy.init_node('sdh_interface')
	frequency = 1.0 #Change this to 30 when using the velocity interface as controller needs faster velocity rate.
	rate = rospy.Rate(frequency)
	hand_interface = SDHInterface()
	'''
	To command an arbitrary joint position.
	Arguments are Joint pose and time needed to complete the trajectory. 
	In ideal case scenario, take the joint pose difference between current and future position 
	and devide it by velocity to get the time. Choose the time curresponding to the farthest joint.
	%TODO: Integrate this function if the node works.
	'''
	PI = math.pi
	joint_pos = [PI/2 - 0.01, -PI/3, PI/3, -PI/3, 0.0, -PI/3, 0.0] #arbitrary pose
	hand_interface.cmdJointState(joint_pos, time=5.0)
	while not rospy.is_shutdown():
		print ("Printing hand information because why not")
		hand_interface.get_contact_info() ## Also can be used for all information, hand_interface.get_info()
		rate.sleep()
	    
        
        
	
	
	
	
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
