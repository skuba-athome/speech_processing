#!/usr/bin/env python

"""
Node for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""

import rospy
import collections
from std_msgs.msg import String
from pocketsphinx.msg import Action,ActionContainer

names = []
objects = []
locations = []
object_categories = []
location_categories = []
verbs = []

def readFileToList(filename):
	output = []	
	file = open(filename)
	for line in file:
		output.append(line.strip().lower())
	return output

def isVerb(word):
	if word in verbs:
		return True
	else:
		return False

def isObject(word):
	if word in objects:
		return True
	elif word in locations:
		return True
	elif word in names:
		return True
	elif word in object_categories:
		return True
	elif word in location_categories:
		return True
	return False

# Extract action from command and return as tuple(s) of (verb,object,data)
def extractAction(command):
	output = []
	commands = command.split()
	for i in xrange(0,len(commands)):
		# If commands[i] is verb, then looking for object and data
		if isVerb(commands[i].lower()):
			obj = None
			data = None
			for j in xrange(i+1,len(commands)):
				if isObject(commands[j].lower()):
					if obj == None:	# If object is null assign it to obj
						obj = commands[j].lower()
					else:		# If object is not null, then assume it is a data
							data = commands[j].lower()
				if isVerb(commands[j].lower()):
					break
			# Append an action to output list
			if obj != None and data != None:
				output.append((commands[i],obj,data))
			elif obj != None:
				output.append((commands[i],obj))
			else:
				output.append((commands[i],))
	#rospy.loginfo(output)
	return output

class classify_command(object):
	def __init__(self):
		rospy.init_node('classify_command')
		self.pub = rospy.Publisher('pocketsphinx/command_category',ActionContainer)
		rospy.Subscriber('pocketsphinx/classify_command', String, self.callback)
		
		# Read config file
		global names,objects,object_categories,locations,location_categories,verbs 
		object_categories = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/object_categories.txt')
		objects = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/objects.txt')
		locations = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/locations.txt')
		names = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/names.txt')
		location_categories = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/location_categories.txt')	
		verbs = readFileToList(roslib.packages.get_pkg_dir('pocketsphinx')+'/command_config/verbs.txt')	
		
		rospy.spin()

	def callback(self,data):
		#print "I heard : %s" % (data.data)
		command = data.data.lower()
		msg = ActionContainer()
		actions = extractAction(command)
		#rospy.loginfo(action)
		index = -1
		for action in actions:
			index += 1
			if len(action) == 3:
				msg.actions[index].action = action[0]
				msg.actions[index].object = action[1]
				msg.actions[index].data = action[2]
			elif len(action) == 2:
				msg.actions[index].action = action[0]
				msg.actions[index].object = action[1]
			else:
				msg.actions[index].action = action[0]
		self.pub.publish(msg)

if __name__=="__main__":
	c = classify_command()
