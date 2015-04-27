#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from subprocess import call

class question:
	stage = 'start'
	def __init__(self):
        # spin() simply keeps python from exiting until this node is stopped
        rospy.Subscriber("/voice/output", String, self.callback)
        rospy.spin()
    def callback(self,data):
    	print (data.data)
    	if ('capital city ' and 'thailand') in data.data: #what is the capital city of thailand
    		call(['espeak','the capital city of thailand is bangkok'])
    	elif ('come from') in data.data: #whare are you come from
    		call(['espeak','I come from thailand'])
    	elif ('your name') in data.data: #what is your name
    		call(['espeak','my name is lumyai'])

if __name__ == '__main__':
    try:
        rospy.init_node('question')
        question()
    except rospy.ROSInterruptException:
        pass