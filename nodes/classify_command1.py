#!/usr/bin/env python

"""
Node for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""

import roslib;

roslib.load_manifest('speech_processing')
import rospy
import collections
from std_msgs.msg import String
# from speech_processing.msg  import Action,ActionContainer

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
    for i in xrange(0, len(commands)):
        # If commands[i] is verb, then looking for object and data
        if isVerb(commands[i].lower()):
            obj = None
            data = None
            for j in xrange(i + 1, len(commands)):
                if isObject(commands[j].lower()):
                    if obj == None:  # If object is null assign it to obj
                        obj = commands[j].lower()
                    else:  # If object is not null, then assume it is a data
                        data = commands[j].lower()
                if isVerb(commands[j].lower()):
                    break
            # Append an action to output list
            if obj != None and data != None:
                output.append((commands[i], obj, data))
            elif obj != None:
                output.append((commands[i], obj))
            else:
                output.append((commands[i]))
    #rospy.loginfo(output)
    return output


class classify_command(object):
    def __init__(self):
        rospy.init_node('classify_command_GPSR')
        #self.pub = rospy.Publisher('speech_processing/command_category',ActionContainer)
        rospy.Subscriber('/voice/output', String, self.callback)

        # Read config file
        global names, objects, object_categories, locations, location_categories, verbs
        object_categories = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/object_category.txt')
        objects = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/object.txt')
        locations = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/location.txt')
        names = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/name.txt')
        location_categories = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/location_category.txt')
        verbs = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/verb.txt')

        rospy.spin()

    def callback(self, data):
        print "I heard : %s" % (data.data)
        command = data.data.lower()
        #command = raw_input("command : ")
        #msg = ActionContainer()
        actions = extractAction(command)
        #rospy.loginfo(action)
        index = -1
        num_command = len(actions)
        matrix = [[0 for i in range(3)] for j in range(num_command)]
        for action in actions:
            index += 1
            if len(action) == 3:
                matrix[index][0] = action[0]
                #msg.actions[index].action = action[0]
                print ("action :" + matrix[index][0])
                matrix[index][1] = action[1]
                #msg.actions[index].object = action[1]
                print ("object :" + matrix[index][1])
                matrix[index][2] = action[2]
                #msg.actions[index].data = action[2]
                print ("data :" + matrix[index][2])
            elif len(action) == 2:
                #msg.actions[index].action = action[0]
                #print ("action :"+ msg.actions[index].action)
                #msg.actions[index].object = action[1]
                #print ("object :"+ msg.actions[index].object)
                matrix[index][0] = action[0]
                #msg.actions[index].action = action[0]
                print ("action :" + matrix[index][0])
                matrix[index][1] = action[1]
                #msg.actions[index].object = action[1]
                print ("object :" + matrix[index][1])
            else:
                #msg.actions[index].action = action[0]
                #print ("action :"+ msg.actions[index].action)
                matrix[index][0] = action[0]
                #msg.actions[index].action = action[0]
                print ("action :" + matrix[index][0])
            #self.pub.publish(msg)


if __name__ == "__main__":
    c = classify_command()

