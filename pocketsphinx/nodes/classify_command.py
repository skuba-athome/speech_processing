#!/usr/bin/env python

"""
Node for classify command categories of EGPSR
"""

import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import collections
from std_msgs.msg import String

names = []
objects = []
locations = []
object_categories = []
location_categories = []

def readFileToList(filename):
	output = []	
	file = open(filename)
	for line in file:
		output.append(line.strip())
	return output

class classify_command(object):
	def __init__(self):
		rospy.init_node('classify_command')
		self.pub = rospy.Publisher('pocketsphinx/command_category',String)
		rospy.Subscriber('pocketsphinx/classify_command', String, self.callback)
		global names,objects,object_categories,locations,location_categories 
		object_categories = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/object_categories.txt')
		objects = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/objects.txt')
		locations = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/locations.txt')
		names = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/names.txt')
		location_categories = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/location_categories.txt')	
		rospy.spin()

	def callback(self,data):
		print "I heard : %s" % (data.data)
		command = data.data
		msg = String()

		#Check category 1

		#Check category 2
		isObjectIncomplete = False
		isLocationIncomplete = False
		for category in object_categories:
			if category in command:
				isObjectIncomplete = True
				object_category = category
				break

		for category in location_categories:
			if category in command:
				isLocationIncomplete = True
				location_category = category
				break

		verb = command.split()[0].lower()

		if isObjectIncomplete and isLocationIncomplete:
			msg.data = '%d:%s %s %s' % (2,verb,object_category,location_category)
			self.pub.publish(msg)
			return
		elif isObjectIncomplete:
			msg.data = '%d:%s %s' % (2,verb,object_category)
			self.pub.publish(msg)
			return

if __name__=="__main__":
	c = classify_command()
