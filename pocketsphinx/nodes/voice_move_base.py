#!/usr/bin/env python

"""
voice_cmd_vel.py is a simple demo of speech recognition.
  You can control a mobile base using commands found
  in the corpus file.
"""

import roslib; roslib.load_manifest('pocketsphinx')
import rospy
from math import sin,cos,pi
import os

from move_base_msgs.msg import MoveBaseGoal
from geometry_msgs.msg import Twist,PoseStamped
from std_msgs.msg import String

set_init = ['lamyai','lumyai']


class VoiceMoveBase:

	def __init__(self):
		self.Currentstate=[0,0]
       #	self.pub_ = rospy.Publisher('cmd_state', String)

		_xA = rospy.get_param('~xA',1.0)
		_yA = rospy.get_param('~yA',1.0)
		_thA = rospy.get_param('~thA',0.0)

#		self._init_flag = rospy.get_param('~init_flag',0.0)
#		_initX = rospy.get_param('~initX',50.0)
#		_initY = rospy.get_param('~initY',50.0)
#		_initTH = rospy.get_param('~initTH',0.0)
		
#		self._initpose = PoseWithCovarianceStamped()
#		self._initpose.header.stamp = rospy.Time.now()
#		self._initpose.header.frame_id = '/map'		
#		self._initpose.pose.position.x = _initX
#		self._initpose.pose.position.y = _initY
#		self._initpose.pose.orientation.z = sin(_initTH/2.0)
#		self._initpose.pose.orientation.w = con(_initTH/2.0)

		self._A = PoseStamped()
		self._A.header.stamp = rospy.Time.now()
		self._A.header.frame_id = '/map'
		self._A.pose.position.x = _xA
		self._A.pose.position.y = _yA
		self._A.pose.orientation.z = sin(_thA/2.0)
		self._A.pose.orientation.w = cos(_thA/2.0)
		
		
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

	#	_xB = rospy.get_param('~xB',1.0)
	#	_yB = rospy.get_param('~yB',1.0)
	#	_thB = rospy.get_param('~thB',0.0)
	#	_xC = rospy.get_param('~xC',1.0)
	#	_yC = rospy.get_param('~yC',1.0)
	#	_thC = rospy.get_param('~thC',0.0)
	#	self._B = MoveBaseGoal()
	#	self._B.target_pose.header.frame_id = "/map"
	#	self._B.target_pose.header.stamp = rospy.Time.now()
	#	self._B.target_pose.pose.position.x = _xB
	#	self._B.target_pose.pose.position.y = _yB
	#	self._B.target_pose.pose.orientation.z = sin(_thB/2.0)
	#	self._B.target_pose.pose.orientation.w = cos(_thB/2.0)
	#	self._C = MoveBaseGoal()
	#	self._C.target_pose.header.frame_id = "/map"
	#	self._C.target_pose.header.stamp = rospy.Time.now()
	#	self._C.target_pose.pose.position.x = _xC
	#	self._C.target_pose.pose.position.y = _yC
	#	self._C.target_pose.pose.orientation.z = sin(_thC/2.0)
	#	self._C.target_pose.pose.orientation.w = cos(_thC/2.0)
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		#topic state
##	self.pubNavigation = rospy.Publisher('cmd_Navigation', String)
#	self.pubWhoiswho = rospy.Publisher('cmd_Whoiswho', String)
#	self.pubFollowme = rospy.Publisher('cmd_Followme', String)
#		self.pubManipulation = rospy.Publisher('cmd_Followme', String)
		self.state = 'init'
		self.name = ''
		self._msg =''
		self._goal_state = ''
	#Subscribe
		rospy.Subscriber('recognizer/output', String, self._getMsg)
		self._GoalPublisher = rospy.Publisher('move_base_simple/goal',PoseStamped)
		self._StatePublisher = rospy.Publisher('move_base_state',String)
#		self._initposePublisher = rospy.Publisher('initialpose',PoseWithCovariaceStamped)
		rospy.Subscriber('move_goal_state', String, self._getGoalState)
	#self.checkstate(_self.msg)
        #r = rospy.Rate(10.0)
        #while not rospy.is_shutdown():
        #    r.sleep()
        #self.TypeContest=enum('none','navigation','whoiswho','followme','manipulate')
	#self.Navigation=enum('none','one','two','three')
	#self.WhoIsWho=enum('none','richard','phillip','emma','daniel','tina','steve','henry','peter','robert','sarah','brian','thomas','britney','justin','tony','kevin','joseph','michael','michelle','donna')
	#self.FollowMe=enum('none','start','stop')
	def _getGoalState(self,msg):
		self._goal_state = str(msg.data)
		self.checkstate(self._msg)
	def _getMsg(self,msg):
	
		self._msg = str(msg.data)
		self.checkstate(self._msg)

	def fspeak(self,sp):
		os.system("espeak --stdout '" + sp + "' | aplay")
	def checkstate(self, msg):
   #rospy.loginfo(msg.data+' '+str(self.state))
	#self.pub_.publish(self.Currentstate[1]*10+self.Currentstate[0])
		if(msg in set_init and self.state!='Wait'):
			self.state = 'Start'
			self._StatePublisher.publish('start')
			os.system("espeak --stdout 'sirrr,yes sir' -s 260 -a 200  -p 25| aplay")
		if(self.state == 'Start'):
			if(msg == 'go'):
				self.fspeak('your command is go to target?')
				self._StatePublisher.publish('confirm')
				self.state = 'Confirm'
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,,
	#	elif(self.state == 'Where'):
	#		if(msg == 'point a'):	
	#			self.fspeak('do you want me to go to point A?')
	#			self.state = 'go A'
	#		elif(msg == 'point b'):	
	#			self.fspeak('do you want me to go to point B?')
	#			self.state = 'go B'
	#		elif(msg == 'point c'):	
	#			self.fspeak('do you want me to go to point C?')
	#			self.state = 'go C'
	#	elif(self.state == 'go A'):
	#		if(msg == 'yes'):
	#			self.fspeak('ok')
	#			self._GoalPublisher.publish(self._A)
	#			self.state = 'Wait'
	#		elif(msg == 'no'):
	#			self.state = 'Where'
	#			self.fspeak('where do you want me to go?')
	#	elif(self.state == 'go B'):
	#		if(msg == 'yes'):
	#			self.fspeak('ok')
	#			self._GoalPublisher.publish(self._B)
	#			self.state = 'Wait'
	#		elif(msg == 'no'):
	#			self.state = 'Where'
	#			self.fspeak('where do you want me to go?')
	#	elif(self.state == 'go C'):
	#		if(msg == 'yes'):
	#			self.fspeak('ok')
	#			self._GoalPublisher.publish(self._C)
	#			self.state = 'Wait'
	#		elif(msg == 'no'):
	#			self.state = 'Where'
	#			self.fspeak('where do you want me to go?')
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<,,,
		elif(self.state == 'Confirm'):
			if(msg == 'yes'):
				self.state = 'Wait'
				self.fspeak("I am going to the target")
				self._StatePublisher.publish('go')
#				if self._init_flag == 1.0 :
#					self._initposePublisher.publisher(self._initpose)
				self._GoalPublisher.publish(self._A)
			elif msg == 'no' :
				self.state = 'Start'
				self.fspeak('Please repeat your command')
		elif(self.state == 'Wait'):
			if(self._goal_state == 'SUCCEEDED'):
				self.fspeak('Target Reached')
   				self._goal_state = ''
				self.state = 'Start'
	
		#r = rospy.Rate(10)
		#while not rospy.is_shutdown():
		#Couldn't find executable named voice_cmd.launch below /home/xcerx/ros_workspace/skuba_athome_main/rharmony/pocketsphinx
		
		#	self.checkstate(self._msg)
	#		r.sleep()
if __name__=="__main__":
	rospy.init_node('voice_move_base')
	voice = VoiceMoveBase()
	try:
		rospy.spin()
	except:
		pass

