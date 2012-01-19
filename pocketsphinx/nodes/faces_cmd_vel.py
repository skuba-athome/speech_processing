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
set_name = ['richard','philip','emma','daniel','tina','steve','henry','peter','robert','sarah','brian','thomas','britney','justin','tony','kevin','joseph','michael','michelle','donna','pond']


class voice_cmd_vel:

    def __init__(self):
	self.Currentstate=[0,0]
       	self.pub_ = rospy.Publisher('cmd_state', String)
	
	#topic state
	self.pubNavigation = rospy.Publisher('cmd_Navigation', String)
	self.pubWhoiswho = rospy.Publisher('cmd_Whoiswho', String)
	self.pubFollowme = rospy.Publisher('cmd_Followme', String)
	self.pubManipulation = rospy.Publisher('cmd_Followme', String)
	self.state = 'init' 
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
	os.system("espeak --stdout -s 130 '" + sp + "' | aplay")

    def checkstate(self, msg):
        rospy.loginfo(msg.data+' '+str(self.state))
	#self.pub_.publish(self.Currentstate[1]*10+self.Currentstate[0])
	msg = str(msg.data)
	if( msg == 'hello' ):
		self.state = 'init'
		self.fspeak('hi')
	elif(self.state == 'init'):
		if( msg == 'what is my name' or msg == 'my name'):
			self.state = 'check'
			self.fspeak('do you want to know your name')
		msg = msg.split()
		if( len(msg)==3 ):
			if( msg[2] in set_name):
				self.fspeak('your name is '+msg[2]+" yes or no")
				self.name = msg[2]
				#self.fspeak('yes of no')
				self.state = 'remember'
	elif(self.state == 'remember'):
		if( msg == 'yes' ):
			os.system("espeak --stdout 'sirrr,yes sir' -s 260 -a 200 -p 25| aplay")
			self.pub_.publish(self.name)
			self.state = 'init'
		elif( msg == 'no'):
			self.fspeak('what is your name')
			self.state = 'init'
		else:
			self.fspeak('yes or no') 
	elif(self.state == 'check'):
		if( msg == 'yes' ):
			os.system("espeak --stdout 'sirrr,yes sir' -s 260 -a 200 -p 25| aplay")
			self.pub_.publish('test')
			self.state = 'init'
		elif( msg == 'no'):
			self.fspeak('again')
			self.state = 'init'
		else:
			self.fspeak('yes or no') 	
		


	'''if( self.state == 1):
		if(msg == 'lumyai'):
			self.fspeak("what is your name")
			state == 2
		if(msg == 'hello'):
			self.pub_.publish('test')
			
	if( self.state == 2):
		if(msg in set_name):
			self.name = msg
			self.fspeak('your name is '+msg+' yes or no')
			state = 3
	if( self.state == 3):
		if( msg == 'yes' ):
			os.system("espeak --stdout 'sirrr,yes sir' -s 260 -a 200 -p 25| aplay")
			self.pub_.publish(self.name)
		elif( msg == 'no'):
			self.fspea('what is your name')
			self.state = 2
		else:
			self.fspeak('yes or no') '''

	rospy.loginfo('now state is'+str(self.state))

			
		
if __name__=="__main__":
    rospy.init_node('voice_cmd_vel')
    try:
        voice_cmd_vel()
    except:
        pass

