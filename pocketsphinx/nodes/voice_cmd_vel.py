#!/usr/bin/env python

"""
voice_cmd_vel.py is a simple demo of speech recognition.
  You can control a mobile base using commands found
  in the corpus file.
"""

import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import math
import os


from geometry_msgs.msg import Twist
from std_msgs.msg import String

class voice_cmd_vel:

    def __init__(self):
	self.Currentstate=[0,0]
       	self.pub_ = rospy.Publisher('cmd_state', String)
	
	#topic state
	self.pubNavigation = rospy.Publisher('cmd_Navigation', String)
	self.pubWhoiswho = rospy.Publisher('cmd_Whoiswho', String)
	self.pubFollowme = rospy.Publisher('cmd_Followme', String)
	self.pubManipulation = rospy.Publisher('cmd_Followme', String)

	#Subscribe
	rospy.Subscriber('recognizer/output', String, self.checkstate)

        r = rospy.Rate(10.0)
        while not rospy.is_shutdown():
            r.sleep()
        #self.TypeContest=enum('none','navigation','whoiswho','followme','manipulate')
	#self.Navigation=enum('none','one','two','three')
	#self.WhoIsWho=enum('none','richard','phillip','emma','daniel','tina','steve','henry','peter','robert','sarah','brian','thomas','britney','justin','tony','kevin','joseph','michael','michelle','donna')
	#self.FollowMe=enum('none','start','stop')

    def fspeak(self,sp):
	os.system("espeak --stdout \'" + sp + "' | aplay")

    def checkstate(self, msg):
        rospy.loginfo(msg.data)
	if msg.data.find("hello") > -1:
		self.fspeak("hello")
	if (self.Currentstate[0]==0):
		if msg.data.find("navigation test") > -1:
			self.Currentstate[0]=1
			self.fspeak("this is navigation test")
		elif msg.data.find("who is who test") > -1:
			self.Currentstate[0]=2
			self.fspeak("this is who is who test")
		elif msg.data.find("follow me test") > -1:
			self.Currentstate[0]=3
			self.fspeak("this is follow me test")
		elif msg.data.find("manipulation test") > -1:
			self.Currentstate[0]=4
			self.fspeak("this is manipulation test")
	elif (self.Currentstate[0]==1):
		if msg.data.find("target is one") > -1:
			self.Currentstate[1]=1
			self.fspeak("target is one")
		elif msg.data.find("target is two") > -1:
			self.Currentstate[1]=2
			self.fspeak("target is two")
		elif msg.data.find("target is three") > -1:
			self.Currentstate[1]=3
			self.fspeak("target is three")
		self.pubNavigation.publish(self.Currentstate[1])
	elif (self.Currentstate[0]==2):
		if msg.data.find("my name is richard") > -1:
			self.Currentstate[1]=1
			self.fspeak("my name is richard")
		elif msg.data.find("you are phillip") > -1:
			self.Currentstate[1]=2
			self.fspeak("you are is phillip")
		elif msg.data.find("my name is emma") > -1:
			self.Currentstate[1]=3
			self.fspeak("you are is emma")
		elif msg.data.find("my name is daniel") > -1:
			self.Currentstate[1]=4
			self.fspeak("you are is daniel")
		elif msg.data.find("my name is tina") > -1:
			self.Currentstate[1]=5
			self.fspeak("you are is tina")
		elif msg.data.find("my name is steve") > -1:
			self.Currentstate[1]=6
			self.fspeak("you are is steve")
		elif msg.data.find("my name is henry") > -1:
			self.Currentstate[1]=7
			self.fspeak("you are is henry")
		elif msg.data.find("my name is peter") > -1:
			self.Currentstate[1]=8
			self.fspeak("you are is peter")
		elif msg.data.find("my name is robert") > -1:
			self.Currentstate[1]=9
			self.fspeak("you are is robert")
		elif msg.data.find("my name is sarah") > -1:
			self.Currentstate[1]=10
			self.fspeak("you are is sarah")
		elif msg.data.find("my name is brian") > -1:
			self.Currentstate[1]=11
			self.fspeak("you are is brian")
		elif msg.data.find("my name is thomas") > -1:
			self.Currentstate[1]=12
			self.fspeak("you are is thomas")
		elif msg.data.find("my name is britney") > -1:
			self.Currentstate[1]=13
			self.fspeak("you are is britney")
		elif msg.data.find("my name is justin") > -1:
			self.Currentstate[1]=14
			self.fspeak("you are is justin")
		elif msg.data.find("my name is tony") > -1:
			self.Currentstate[1]=15
			self.fspeak("you are is tony")
		elif msg.data.find("my name is kevin") > -1:
			self.Currentstate[1]=16
			self.fspeak("you are is kevin")
		elif msg.data.find("my name is joseph") > -1:
			self.Currentstate[1]=17
			self.fspeak("you are is joseph")
		elif msg.data.find("my name is michael") > -1:
			self.Currentstate[1]=18
			self.fspeak("you are is michael")
		elif msg.data.find("my name is michelle") > -1:
			self.Currentstate[1]=19
			self.fspeak("you are is michelle")
		elif msg.data.find("my name is donna") > -1:
			self.Currentstate[1]=20
			self.fspeak("you are is donna")
		self.pubWhoiswho.publish(self.Currentstate[1])
	elif (self.Currentstate[0]==3):
		if msg.data.find("follow me") > -1:
			self.Currentstate[1]=1
			self.fspeak("i will follow you")
		elif msg.data.find("wait here") > -1:
			self.Currentstate[1]=2
			self.fspeak("i am waiting for you")
		self.pubFollowme.publish(self.Currentstate[1])
	elif (self.Currentstate[0]==4):
		if msg.data.find("manipulation") > -1:
			self.Currentstate[1]=1
			self.fspeak("i will manipulate")
		self.pubManipulation.publish(self.Currentstate[1])
	if msg.data.find("reset") > -1:
		self.Currentstate[1]=0
		self.Currentstate[0]=0
		self.fspeak("the state is reseted")

	#self.pub_.publish(self.Currentstate[1]*10+self.Currentstate[0])
	self.pub_.publish(msg)

  
if __name__=="__main__":
    rospy.init_node('voice_cmd_vel')
    try:
        voice_cmd_vel()
    except:
        pass

