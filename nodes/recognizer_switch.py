#!/usr/bin/env python

# Copyright (c) 2008 Carnegie Mellon University.
#
# You may modify and redistribute this file under the same terms as
# the CMU Sphinx system. See LICENSE for more information.

import roslib; roslib.load_manifest('speech_processing')
import rospy

from std_msgs.msg import String
from speech_processing.srv import *
import sys

import actionlib
import speech_processing.msg
from include import gram_lm

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

class grammar_recognizer(object):
    """GStreamer/PocketSphinx Demo Application"""

    def __init__(self):
        """ Initialize the speech pipelinec omponents. """
        rospy.init_node('recognizer')
        self.pub = rospy.Publisher('~output',String)
        rospy.on_shutdown(self.shutdown)

        self.init_gst()

    def init_gst(self):
        """Initialize the speech components"""

        self.ACTION_NAME = "~voice_reg"
        self.result = speech_processing.msg.VoiceRegResult()
        self.action_server = actionlib.SimpleActionServer(self.ACTION_NAME, speech_processing.msg.
            VoiceRegAction, execute_cb = self.execute_cb, auto_start = False)
        self.action_server.start()
        self.gramLm = gram_lm.GramLm

        gtk.main()
        print "pass main-----------------------------------"

    def element_message(self, bus, msg):
        """Receive element messages from the bus."""
        msgtype = msg.get_structure().get_name()
        if msgtype != 'pocketsphinx':
            return

        if msg.get_structure().get_value('final'):
            self.final_result(msg.get_structure().get_value('hypothesis'), msg.get_structure().get_value('confidence'))
        elif msg.get_structure().get_value('hypothesis'):
            self.partial_result(msg.get_structure().get_value('hypothesis'))

    def execute_cb(self, goal):
        """ Callback function run everytime when new goal recieve """
        if goal.grammar_id == -1 :

            self.volume_gram.set_property('mute', True)
            self.volume_lm.set_property('mute', True)
            self.pipeline_gram.change_state(gst.StateChange.PLAYING_TO_PAUSED)
            self.pipeline_gram.change_state(gst.StateChange.PAUSED_TO_READY)
            self.pipeline_gram.change_state(gst.StateChange.READY_TO_NULL)

            self.pipeline_lm.change_state(gst.StateChange.PLAYING_TO_PAUSED)
            self.pipeline_lm.change_state(gst.StateChange.PAUSED_TO_READY)
            self.pipeline_lm.change_state(gst.StateChange.READY_TO_NULL)

            rospy.loginfo('%s: Succeeded Stop Both' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -2 :

            self.volume_gram.set_property('mute', True)
            self.pipeline_gram.change_state(gst.StateChange.PLAYING_TO_PAUSED)
            self.pipeline_gram.change_state(gst.StateChange.PAUSED_TO_READY)
            self.pipeline_gram.change_state(gst.StateChange.READY_TO_NULL)

            rospy.loginfo('%s: Succeeded Stop Gram' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -3 :

            self.volume_lm.set_property('mute', True)
            self.pipeline_lm.change_state(gst.StateChange.PLAYING_TO_PAUSED)
            self.pipeline_lm.change_state(gst.StateChange.PAUSED_TO_READY)
            self.pipeline_lm.change_state(gst.StateChange.READY_TO_NULL)

            rospy.loginfo('%s: Succeeded Stop LM' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)      

        elif goal.grammar_id < 100 :
            self.pipeline_gram = gst.parse_launch('autoaudiosrc ! audioconvert ! audioresample ! volume name=volume_gram '
                                         + '! pocketsphinx name=asr_gram ! fakesink name=sink_gram')
        
            asr_gram = self.pipeline_gram.get_by_name('asr_gram')
            self.volume_gram = self.pipeline_gram.get_by_name('volume_gram')
            self.volume_gram.set_property('mute', False)
            self.sink_gram = self.pipeline_gram.get_by_name('sink_gram')

            bus_gram = self.pipeline_gram.get_bus()
            bus_gram.add_signal_watch()
            bus_gram.connect('message::element', self.element_message)

            self.grammar_ = self.gramLm.gram[goal.grammar_id]
            self.dict_ = self.gramLm.dic[goal.grammar_id]

            self.pipeline_gram.get_by_name('asr_gram').set_property('fsg',self.grammar_)
            self.pipeline_gram.get_by_name('asr_gram').set_property('dict',self.dict_)
            # rospy.loginfo(self.pipeline_gram.get_by_name('asr_gram').get_property('fsg'))
            # rospy.loginfo(self.pipeline_lm.get_by_name('asr_lm').get_property('lm'))
            self.pipeline_gram.change_state(gst.StateChange.NULL_TO_READY)
            self.pipeline_gram.change_state(gst.StateChange.READY_TO_PAUSED)
            self.pipeline_gram.change_state(gst.StateChange.PAUSED_TO_PLAYING)
            self.volume_gram.set_property('mute', False)

            rospy.loginfo('%s: Succeeded Gram' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        else :
            # this is for lm use id >= 101
            self.pipeline_lm = gst.parse_launch('autoaudiosrc ! audioconvert ! audioresample ! volume name=volume_lm '
                                         + '! pocketsphinx name=asr_lm ! fakesink')
        
            asr_lm = self.pipeline_lm.get_by_name('asr_lm')
            self.volume_lm = self.pipeline_lm.get_by_name('volume_lm')
            self.volume_lm.set_property('mute', False)

            bus_lm = self.pipeline_lm.get_bus()
            bus_lm.add_signal_watch()
            bus_lm.connect('message::element', self.element_message)

            self.lm_ = self.gramLm.gram[goal.grammar_id]
            self.dict_ = self.gramLm.dic[goal.grammar_id-100]

            self.pipeline_lm.get_by_name('asr_lm').set_property('lm',self.lm_)
            self.pipeline_lm.get_by_name('asr_lm').set_property('dict',self.dict_)
            # rospy.loginfo(self.pipeline_gram.get_by_name('asr_gram').get_property('fsg'))
            # rospy.loginfo(self.pipeline_lm.get_by_name('asr_lm').get_property('lm'))
            self.volume_gram.set_property('mute', False)
            self.pipeline_lm.change_state(gst.StateChange.NULL_TO_READY)
            self.pipeline_lm.change_state(gst.StateChange.READY_TO_PAUSED)
            self.pipeline_lm.change_state(gst.StateChange.PAUSED_TO_PLAYING)

            rospy.loginfo('%s: Succeeded LM' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

    def partial_result(self, hyp):
        """ Delete any previous selection, insert text and select it. """
        print "Partial: " + hyp

    def final_result(self, hyp, uttid):
        """ Insert the final result. """
        msg = String()
        msg.data = str(hyp.lower())
        rospy.loginfo(msg.data)
        self.pub.publish(msg)

    def shutdown(self):
        """ Shutdown the GTK thread. """
        print "shutdown----------------------------------------"
        gtk.main_quit()

if __name__=="__main__":
    r = grammar_recognizer()