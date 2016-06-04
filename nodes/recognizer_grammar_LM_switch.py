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

import pygtk
pygtk.require('2.0')
import gtk

import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

from std_msgs.msg import String
from speech_processing.srv import *
import sys

import actionlib
import speech_processing.msg
from include import gram_lm

class grammar_recognizer(object):
    """ GStreamer based speech recognizer. """

    def __init__(self):
        """ Initialize the speech pipelinec omponents. """
        rospy.init_node('recognizer')
        self.pub = rospy.Publisher('~output',String)
        rospy.on_shutdown(self.shutdown)

        # services to start/stop recognition
        # rospy.Service("~start", Trigger, self.start)
        # rospy.Service("~stop", Trigger, self.stop)

        # configure pipeline
        self.pipeline_gram = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
                                         + '! vader name=vad_gram auto-threshold=true '
                                         + '! pocketsphinx name=asr_gram ! fakesink')
        asr_gram = self.pipeline_gram.get_by_name('asr_gram')
        asr_gram.connect('partial_result', self.asr_partial_result)
        asr_gram.connect('result', self.asr_result)
        asr_gram.set_property('configured', True)
        asr_gram.set_property('dsratio', 1)
        self.vader_gram = self.pipeline_gram.get_by_name('vad_gram')

        self.pipeline_lm = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
                                         + '! vader name=vad_lm auto-threshold=true '
                                         + '! pocketsphinx name=asr_lm ! fakesink')
        asr_lm = self.pipeline_lm.get_by_name('asr_lm')
        asr_lm.connect('partial_result', self.asr_partial_result)
        asr_lm.connect('result', self.asr_result)
        asr_lm.set_property('configured', True)
        asr_lm.set_property('dsratio', 1)
        self.vader_lm = self.pipeline_lm.get_by_name('vad_lm')

        # parameters for lm and dic
        # try:
        #     self.grammar_ = rospy.get_param('~grammar')
        # except:
        #     rospy.logerr('Please specify a grammar file')
        #     return
        # try:
        #     self.dict_ = rospy.get_param('~dict')
        # except:
        #     rospy.logerr('Please specify a dictionary')
        #     return

        # asr.set_property('fsg',self.grammar_)
        # asr.set_property('dict',self.dict_)

        bus_gram = self.pipeline_gram.get_bus()
        bus_gram.add_signal_watch()
        bus_gram.connect('message::application', self.application_message)

        bus_lm = self.pipeline_lm.get_bus()
        bus_lm.add_signal_watch()
        bus_lm.connect('message::application', self.application_message)
        # self.start(None)

        self.ACTION_NAME = "~voice_reg"
        self.result = speech_processing.msg.VoiceRegResult()
        self.action_server = actionlib.SimpleActionServer(self.ACTION_NAME, speech_processing.msg.
            VoiceRegAction, execute_cb = self.execute_cb, auto_start = False)
        self.action_server.start()

        self.gramLm = gram_lm.GramLm
        # self.stop()
        # self.grammar_ = '/home/skuba/obsidian_workspace/src/speech_processing/dic/5questions_and_follow_New/start.fsg'
        # self.dict_ = '/home/skuba/obsidian_workspace/src/speech_processing/dic/5questions_and_follow_New/start.dic'
        # self.start(None)

        gtk.main()

    def execute_cb(self, goal):
        """ Callback function run everytime when new goal recieve """

        if goal.grammar_id == -1 :

            self.pipeline_gram.set_state(gst.STATE_NULL)
            self.pipeline_lm.set_state(gst.STATE_NULL)
            self.vader_gram.set_property('silent', True)
            self.vader_lm.set_property('silent', True)

            rospy.loginfo('%s: Succeeded Stop Both' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -2 :

            self.pipeline_gram.set_state(gst.STATE_NULL)
            self.vader_gram.set_property('silent', True)

            rospy.loginfo('%s: Succeeded Stop Gram' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -3 :

            self.pipeline_lm.set_state(gst.STATE_NULL)
            self.vader_lm.set_property('silent', True)

            rospy.loginfo('%s: Succeeded Stop LM' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -4 :

            self.pipeline_gram.set_state(gst.STATE_PAUSED)
            self.pipeline_lm.set_state(gst.STATE_PAUSED)
            self.vader_gram.set_property('silent', True)
            self.vader_lm.set_property('silent', True)

            rospy.loginfo('%s: Succeeded Stop Both' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -5 :

            self.pipeline_gram.set_state(gst.STATE_PAUSED)
            self.vader_gram.set_property('silent', True)

            rospy.loginfo('%s: Succeeded Stop Gram' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -6 :

            self.pipeline_lm.set_state(gst.STATE_PAUSED)
            self.vader_lm.set_property('silent', True)

            rospy.loginfo('%s: Succeeded Stop LM' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -7 :

            self.vader_gram.set_property('silent', False)
            self.vader_lm.set_property('silent', False)
            self.pipeline_gram.set_state(gst.STATE_PLAYING)
            self.pipeline_lm.set_state(gst.STATE_PLAYING)

            rospy.loginfo('%s: Succeeded Stop Both' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -8 :

            self.vader_lm.set_property('silent', False)
            self.pipeline_gram.set_state(gst.STATE_PLAYING)

            rospy.loginfo('%s: Succeeded Stop Gram' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        elif goal.grammar_id == -9 :

            self.vader_lm.set_property('silent', False)
            self.pipeline_lm.set_state(gst.STATE_PLAYING)

            rospy.loginfo('%s: Succeeded Stop LM' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)        

        elif goal.grammar_id < 100 :
            
            self.vader_gram.set_property('silent', True)
            self.vader_lm.set_property('silent', True)
            self.pipeline_gram.set_state(gst.STATE_NULL)
            self.pipeline_gram.set_state(gst.STATE_READY)

            self.grammar_ = self.gramLm.gram[goal.grammar_id]
            self.dict_ = self.gramLm.dic[goal.grammar_id]

            self.pipeline_gram.get_by_name('asr_gram').set_property('fsg',self.grammar_)
            self.pipeline_gram.get_by_name('asr_gram').set_property('dict',self.dict_)
            # rospy.loginfo(self.pipeline_gram.get_by_name('asr_gram').get_property('fsg'))
            # rospy.loginfo(self.pipeline_lm.get_by_name('asr_lm').get_property('lm'))
            self.pipeline_gram.set_state(gst.STATE_PLAYING)

            rospy.loginfo('%s: Succeeded Gram' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

        else :

            self.vader_gram.set_property('silent', True)
            self.vader_lm.set_property('silent', True)
            self.pipeline_lm.set_state(gst.STATE_NULL)
            self.pipeline_lm.set_state(gst.STATE_READY)

            self.grammar_ = self.gramLm.gram[goal.grammar_id]
            self.dict_ = self.gramLm.dic[goal.grammar_id-100]

            self.pipeline_lm.get_by_name('asr_lm').set_property('lm',self.grammar_)
            self.pipeline_lm.get_by_name('asr_lm').set_property('dict',self.dict_)
            # rospy.loginfo(self.pipeline_gram.get_by_name('asr_gram').get_property('fsg'))
            # rospy.loginfo(self.pipeline_lm.get_by_name('asr_lm').get_property('lm'))
            self.pipeline_lm.set_state(gst.STATE_PLAYING)

            rospy.loginfo('%s: Succeeded LM' % self.ACTION_NAME)
            self.action_server.set_succeeded(self.result)

    def shutdown(self):
        """ Shutdown the GTK thread. """
        gtk.main_quit()

    # def start(self, msg):
    #     self.pipeline.set_state(gst.STATE_PLAYING)
    #     self.pipeline.get_by_name('asr').set_property('fsg',self.grammar_)
    #     self.pipeline.get_by_name('asr').set_property('dict',self.dict_)
    #     return TriggerResponse(True, 'success')

    # def stop(self, msg, num):
    #     self.pipeline.set_state(gst.STATE_PAUSED)
    #     #self.vader = self.pipeline.get_by_name('vad')
    #     #self.vader.set_property('silent', True)
    #     return TriggerResponse(True, 'success')

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

if __name__=="__main__":
    r = grammar_recognizer()

