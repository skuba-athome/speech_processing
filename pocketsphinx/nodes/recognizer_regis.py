#!/usr/bin/env python

"""
recognizer.py is a wrapper for pocketsphinx.
  parameters:
    ~lm - filename of language model
    ~dict - filename of dictionary
  publications:
    ~output (std_msgs/String) - text output
  services:
    ~start (std_srvs/Empty) - start speech recognition
    ~stop (std_srvs/Empty) - stop speech recognition
"""

import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import os
import pygtk
pygtk.require('2.0')
import gtk
import sys
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

from std_msgs.msg import String
from std_srvs.srv import *


filepath = '/home/xcerx/ros_workspace/'
class recognizer(object):
    """ GStreamer based speech recognizer. """

    def __init__(self):
        """ Initialize the speech pipeline components. """
        rospy.init_node('recognizer')
        self.pub = rospy.Publisher('~output',String)
        self.pubSound = rospy.Publisher('~sound',String)
        rospy.on_shutdown(self.shutdown)

        # services to start/stop recognition
        rospy.Service("~start", Empty, self.start)
        rospy.Service("~stop", Empty, self.stop)

        # configure pipeline
        self.pipeline = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
                                         + '! vader name=vad auto-threshold=true '
                                         + '! pocketsphinx name=asr ! fakesink')
        asr = self.pipeline.get_by_name('asr')
        asr.connect('partial_result', self.asr_partial_result)
        asr.connect('result', self.asr_result)
        asr.set_property('configured', True)
        asr.set_property('dsratio', 1)

        # parameters for lm and dic
        try:
	#		rospy.set_param('~lm',filepath+'skuba_athome_main/rharmony/pocketsphinx/demo/'+ filename +'.lm')
			lm_ = rospy.get_param('~lm')
 			print lm_
        except:
			
            rospy.logerr('Please specify a language model file')
            return
        try:
	#		rospy.set_param('~dict',filepath+'skuba_athome_main/rharmony/pocketsphinx/demo/'+ filename +'.dic')
			dict_ = rospy.get_param('~dict')
        except:
            rospy.logerr('Please specify a dictionary')
            return
 #       print lm_
        asr.set_property('lm',lm_)
        asr.set_property('dict',dict_)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.application_message)
        self.start(None)
        gtk.main()
        
    def shutdown(self):
        """ Shutdown the GTK thread. """
        gtk.main_quit()

    def start(self, msg):
        self.pipeline.set_state(gst.STATE_PLAYING)
        return EmptyResponse()

    def stop(self):
        self.pipeline.set_state(gst.STATE_PAUSED)
        #vader = self.pipeline.get_by_name('vad')
        #vader.set_property('silent', True)
        return EmptyResponse()

    def asr_partial_result(self, asr, text, uttid):
        """ Forward partial result signals on the bus to the main thread. """
        struct = gst.Structure('partial_result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def asr_result(self, asr, text, uttid):
        """ Forward result signals on the bus to the main thread. """
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def application_message(self, bus, msg):
        """ Receive application messages from the bus. """
        msgtype = msg.structure.get_name()
        if msgtype == 'partial_result':
            self.partial_result(msg.structure['hyp'], msg.structure['uttid'])
        if msgtype == 'result':
            self.final_result(msg.structure['hyp'], msg.structure['uttid'])

    def partial_result(self, hyp, uttid):
        """ Delete any previous selection, insert text and select it. """
        print "Partial: " + hyp

    def final_result(self, hyp, uttid):
        """ Insert the final result. """
        msg = String()
        msg.data = str(hyp.lower())
        rospy.loginfo(msg.data)
        self.pub.publish(msg)        
        self.pubSound.publish(msg)
        #self.os.system("espeak --stdout \'" + msg.data + "' | aplay")
if __name__=="__main__":
    r = recognizer()