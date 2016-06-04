#!/usr/bin/env python

"""
recognizer.py is a wrapper for speech_processing.
  parameters:
    ~lm - filename of language model
    ~dict - filename of dictionary
  publications:
    ~output (std_msgs/String) - text output
  services:
    ~start (std_srvs/Empty) - start speech recognition
    ~stop (std_srvs/Empty) - stop speech recognition
"""

import roslib; roslib.load_manifest('speech_processing')
import rospy

# import pygtk
# pygtk.require('2.0')
# import gtk

# import gobject
# import pygst
# pygst.require('0.10')
# gobject.threads_init()
# import gst

from gi import pygtkcompat
import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
GObject.threads_init()
Gst.init(None)
    
gst = Gst
    
print("Using pygtkcompat and Gst from gi")

pygtkcompat.enable() 
pygtkcompat.enable_gtk(version='3.0')

import gtk

from std_msgs.msg import String
from std_srvs.srv import *
import sys

class grammar_recognizer(object):
    """ GStreamer based speech recognizer. """

    def __init__(self):
        """ Initialize the speech pipeline components. """
        rospy.init_node('recognizer_grammar')
        self.pub = rospy.Publisher('~output',String)
        rospy.on_shutdown(self.shutdown)

        # services to start/stop recognition
        rospy.Service("~start", Empty, self.start)
        rospy.Service("~stop", Empty, self.stop)

        # configure pipeline
        self.pipeline = gst.parse_launch('autoaudiosrc ! audioconvert ! audioresample '
                                         + '! pocketsphinx name=asr ! fakesink')
        asr = self.pipeline.get_by_name('asr')
        
        # parameters for lm and dic
        try:
            self.lm_ = rospy.get_param('~lm')
        except:
            rospy.logerr('Please specify a lm file')
            return
        try:
            self.dict_ = rospy.get_param('~dict')
        except:
            rospy.logerr('Please specify a dictionary')
            return

        asr.set_property('lm',self.lm_)
        asr.set_property('dict',self.dict_)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::element', self.element_message)

        self.start(None)
        gtk.main()
        
    def shutdown(self):
        """ Shutdown the GTK thread. """
        print 'shut----------------------------------------kuy'
        self.pipeline.set_state(gst.State.NULL)
        gtk.main_quit()
        # sys.exit()

    def start(self, msg):
        self.pipeline.set_state(gst.State.PLAYING)
        # self.pipeline.get_by_name('asr').set_property('fsg',self.grammar_)
        # self.pipeline.get_by_name('asr').set_property('dict',self.dict_)
        return EmptyResponse()

    def stop(self):
        self.pipeline.set_state(gst.State.PAUSED)
        #vader = self.pipeline.get_by_name('vad')
        #vader.set_property('silent', True)
        return EmptyResponse()

    def partial_result(self, hyp):
        """ Delete any previous selection, insert text and select it. """
        print "Partial: " + hyp

    def final_result(self, hyp, uttid):
        """ Insert the final result. """
        msg = String()
        msg.data = str(hyp.lower())
        rospy.loginfo(msg.data)
        self.pub.publish(msg)

    def element_message(self, bus, msg):
        """Receive element messages from the bus."""
        msgtype = msg.get_structure().get_name()
        if msgtype != 'pocketsphinx':
            return

        if msg.get_structure().get_value('final'):
            self.final_result(msg.get_structure().get_value('hypothesis'), msg.get_structure().get_value('confidence'))
        elif msg.get_structure().get_value('hypothesis'):
            self.partial_result(msg.get_structure().get_value('hypothesis'))

if __name__=="__main__":
    r = grammar_recognizer()

