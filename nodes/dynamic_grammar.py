#!/usr/bin/env python

"""
"""

import roslib; roslib.load_manifest('speech_processing')
import rospy
import collections
import xml.etree.ElementTree as ET

from std_msgs.msg import String
from include.xmltojsgf import *
from subprocess import call

class dynamic_grammar(object):
	"""docstring for dynamic_grammar"""
	def __init__(self):
		rospy.init_node('dynamic_grammar')
		
		try:
			self.grammar_file = rospy.get_param('~grammar')
			self.jsgf = self.grammar_file.replace('xml','jsgf')
			self.fsg = self.grammar_file.replace('xml','fsg')
		except:
			rospy.logerr('Please specify a grammar file.')
			return

		self.word_list = get_word_list(self.grammar_file)
		self.weight = collections.OrderedDict()
		for word in self.word_list:
			self.weight.update({word:128.0})

		create_weight_grammar(self.grammar_file,self.weight)
		call(['sphinx_jsgf2fsg','-jsgf',self.jsgf,'-fsg',self.fsg])
		rospy.Subscriber('edit_grammar', String, self.edit_callback)
		rospy.Subscriber('reset_grammar', String, self.reset_callback)
		rospy.spin()

	def edit_callback(self,data):
		#print 'Decrease ' + data.data.upper() + ' weight'
		#print self.word_list
		if data.data.upper() in self.word_list:
			#print self.weight[data.data.upper()]
			self.weight[data.data.upper()] = self.weight[data.data.upper()]/128.0 
		#print self.weight
		create_weight_grammar(self.grammar_file,self.weight)
		call(['sphinx_jsgf2fsg','-jsgf',self.jsgf,'-fsg',self.fsg])

	def reset_callback(self,data):
		if data.data.lower() == 'reset':
			for word in self.word_list:
				self.weight[word] = 128.0
		create_weight_grammar(self.grammar_file,self.weight)
		call(['sphinx_jsgf2fsg','-jsgf',self.jsgf,'-fsg',self.fsg])

if __name__=="__main__":
    d = dynamic_grammar()
