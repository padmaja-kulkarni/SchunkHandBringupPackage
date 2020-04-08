#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseArray
from schunk_sdh_ros.msg import ContactInfoArray
from schunk_sdh.msg import TactileSensor
from sensor_msgs.msg import JointState 
from control_msgs.msg import FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64MultiArray
from cob_srvs.srv import SetString
import math

class SDHInterface:
	
	def __init__(self, SIM=True):
		
		sub1 = rospy.Subscriber("/dsa_controller/tactile_data", TactileSensor, self.tactileSensorCB)
		sub2 = rospy.Subscriber("/dsa_controller/contact_info_array", ContactInfoArray, self.contactInfoCB)
		sub3 = rospy.Subscriber("/sdh_controller/joint_states", JointState, self.jointSateCB)
		self.cmd_joint_state_pub = rospy.Publisher("/sdh_controller/follow_joint_trajectory/goal",  FollowJointTrajectoryActionGoal, queue_size=10, latch=True)
		self.cmd_joint_vel_pub = rospy.Publisher("/sdh_controller/joint_group_velocity_controller/command",  Float64MultiArray, queue_size=10, latch=True)
		self.switch_operation_mode = rospy.ServiceProxy('/sdh_controller/set_operation_mode', SetString)
		
		self.tactile_data = None
		self.contact_info = None
		self.joint_state = None
		self.joint_names = None
		self.PI = math.pi
		self.joint_limit_lower = -0.20
		self.joint_limit_upper = 0.8
		
	def tactileSensorCB(self, msg):
		self.tactile_data = msg	
		
	def contactInfoCB(self, msg):
		self.contact_info = msg
		
	def jointSateCB(self, msg):
		if not self.joint_names and len(msg.name)>1:
			self.joint_names = msg.name
		elif len(msg.name)>1:
			self.joint_state = msg
			
	def cmdJointState(self, joint_pos, time=5.0):
		'''
		To command a joint position to the hand..
		'''
		self.switch_operation_mode('position')
		rospy.sleep(0.02)
		
		if self.joint_names is not None:
			point = JointTrajectoryPoint()
			point.positions = joint_pos
			point.time_from_start.secs = time
			
			traj = JointTrajectory()
			traj.header.stamp = rospy.Time.now()
			traj.joint_names = self.joint_names
			traj.points.append(point)
			
			action_goal = FollowJointTrajectoryActionGoal()
			action_goal.header.stamp = rospy.Time.now()
			action_goal.goal.trajectory = traj
			action_goal.goal.goal_time_tolerance.secs = time
			self.cmd_joint_state_pub.publish(action_goal)
			
		rospy.sleep(time)
		self.switch_operation_mode('velocity')
		rospy.sleep(0.02)
	
	def cmdJointVel(self, joint_vel):
		'''
		To command a velocity to the hand..
		'''
		vel_msg = Float64MultiArray()
		vel_msg.data = joint_vel
		self.cmd_joint_vel_pub.publish(vel_msg)
		
	def cmdZeroJointVel(self):
		'''
		To command zero velocity to the hand..
		'''
		joint_vel = ([0.0,])*len(self.joint_names)
		self.cmdJointVel(joint_vel)
		
		
	def cmdGoToStartPos(self):
		joint_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		self.cmdJointState(joint_pos)
		
	def get_info(self):
		return self.tactile_data, self.contact_info, self.joint_state
	
	def get_contact_info(self):
		return self.contact_info
	
	
	
	
	
	
	
	
