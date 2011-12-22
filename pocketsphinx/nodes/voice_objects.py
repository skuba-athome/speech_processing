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
set_cmd = ['get coke','get numtip','get coke']

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
	self.obj = ''
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
	os.system("espeak --stdout -s 130 '" + sp + "' | aplay")

    def checkstate(self, msg):
        rospy.loginfo(msg.data+' '+str(self.state))
	#self.pub_.publish(self.Currentstate[1]*10+self.Currentstate[0])
	msg = str(msg.data)
	if(self.state == 1):
		if(msg in set_cmd):
			self.obj = msg.split()[1]
			self.fspeak('your command is get '+self.obj+' yes or no')
			self.state = 2
		else :
			self.fspeak('input command again')
	elif(self.state == 2):
		if(msg == 'yes'):
			self.pub_.publish(self.obj)
			os.system("espeak --stdout 'sirrr,yes sir' -s 260 -a 200 -p 25| aplay")
			self.state = 1
		elif(msg == 'no'):
			self.state = 1
			self.fspeak('plese input command again')
		else :
			self.fspeak('yes or no please')
			
		
if __name__=="__main__":
    rospy.init_node('voice_cmd_vel')
    try:
        voice_cmd_vel()
    except:
        pass

