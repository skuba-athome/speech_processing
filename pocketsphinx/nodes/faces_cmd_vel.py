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

set_init = ['lumyai']
set_name = ['richard','philip','emma','daniel','tina','steve','henry','peter','robert','sarah','brian','thomas','britney','justin','tony','kevin','joseph','micheal','michelle','donna','pond']


class voice_cmd_vel:

    def __init__(self):
	self.Currentstate=[0,0]
       	self.pub_ = rospy.Publisher('cmd_state', String)
	
	#topic state
	self.pubNavigation = rospy.Publisher('cmd_Navigation', String)
	self.pubWhoiswho = rospy.Publisher('cmd_Whoiswho', String)
	self.pubFollowme = rospy.Publisher('cmd_Followme', String)
	self.pubManipulation = rospy.Publisher('cmd_Followme', String)
	self.state = 1
	self.name = ''
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
	os.system("espeak --stdout '" + sp + "' | aplay")

    def checkstate(self, msg):
        rospy.loginfo(msg.data+' '+str(self.state))
	#self.pub_.publish(self.Currentstate[1]*10+self.Currentstate[0])
	msg = str(msg.data)
	if(msg in set_init):
		state = 1
		self.fspeak('sir yes ir')
	if(self.state == 1):
		if(msg == 'remember me'):
			self.fspeak('command is '+msg+' yes or no')
			self.state = 2
		elif(msg == 'what is my name'):
			self.fspeak('command is '+msg+' yes or no')
			self.state = 5
		elif(msg == 'target'):
			self.fspeak('command is '+msg+' yes or no')
			self.state = 6
		else:
			self.state = 1
	elif(self.state == 5 or self.state == 6 ):
		if(msg == 'yes'):	
			self.fspeak('please wait')
			if(self.state == 5):
				self.pub_.publish('test')
			else:
				self.pub_.publish('target')
			self.state = 1
		elif(msg == 'no'):
			self.state = 1
		else:
			self.fspeak('yes or no')
	elif(self.state == 2):
		if(msg == 'yes'):
			self.fspeak('what is your name')
			self.state = 3
		elif(msg == 'no'):
			self.state = 1
		else:
			self.fspeak('yes or no')
	elif(self.state == 3):
		self.name = msg
		if not( self.name in set_name):
			self.fspeak('i dont know your name')
		else:
			self.fspeak('your name is '+msg+' yes or no')
			self.state = 4
	elif(self.state == 4):
		if(msg == 'yes'):	
			self.fspeak('please wait')
			self.pub_.publish(self.name)
			self.state = 1
		elif(msg == 'no'):
			self.fspeak('what is your name')
			self.state = 3
		else:
			self.fspeak('yes or no')
	rospy.loginfo('now state is'+str(self.state))
			
		
if __name__=="__main__":
    rospy.init_node('voice_cmd_vel')
    try:
        voice_cmd_vel()
    except:
        pass

