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
import datetime

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
        self.start_record = False
        self.timestamp = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
        self.pipeline_rec = gst.parse_launch('autoaudiosrc name=audiosrc ! audioconvert ! audioresample ! wavenc ' +
                                             '! filesink name=filesink location=/home/ketamine/skuba_ws/src' +
                                             '/speech_processing/SKUBA_ShotgunMic_' +
                                             self.timestamp + '.wav')

        self.pipeline = gst.parse_launch('autoaudiosrc ! audioconvert ! audioresample '
                                         + '! pocketsphinx  name=asr ! fakesink ')

        # audiosrc = self.pipeline_rec.get_by_name('audiosrc')
        self.filesink = self.pipeline_rec.get_by_name('filesink')



        asr = self.pipeline.get_by_name('asr')

        # parameters for lm and dic
        try:
            self.grammar_ = rospy.get_param('~grammar')
        except:
            rospy.logerr('Please specify a grammar file')
            return
        try:
            self.dict_ = rospy.get_param('~dict')
        except:
            rospy.logerr('Please specify a dictionary')
            return

        asr.set_property('fsg', self.grammar_)
        asr.set_property('dict', self.dict_)


        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::element', self.element_message)


        # bus_rec = self.pipeline_rec.get_bus()
        # bus_rec.add_signal_watch()
        # bus_rec.connect('message::element', self.element_message)

        self.start(None)
        gtk.main()
        
    def shutdown(self):
        """ Shutdown the GTK thread. """
        print 'shut----------------------------------------'
        self.pipeline.set_state(gst.State.NULL)
        self.pipeline_rec.set_state(gst.State.NULL)
        gtk.main_quit()
        # sys.exit()

    def start(self, msg):
        self.pipeline.set_state(gst.State.PLAYING)
        # self.pipeline_rec.set_state(gst.State.PAUSED)
        print self.timestamp, "----------------------"
        # print self.pipeline.get_by_name('asr').get_property('decoder').get_string("-rawlogdir")
        # self.pipeline_rec.change_state(gst.StateChange.PLAYING_TO_PAUSED)
        # self.pipeline.get_by_name('asr').set_property('fsg',self.grammar_)
        # self.pipeline.get_by_name('asr').set_property('dict',self.dict_)
        return EmptyResponse()

    def stop(self):
        self.pipeline.set_state(gst.State.PAUSED)
        self.pipeline_rec.set_state(gst.State.PAUSED)
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
        print type(msg)
        msgtype = msg.get_structure().get_name()
        if msgtype != 'pocketsphinx':
            return

        if msg.get_structure().get_value('final'):
            self.final_result(msg.get_structure().get_value('hypothesis'), msg.get_structure().get_value('confidence'))
            self.pipeline_rec.change_state(gst.StateChange.PLAYING_TO_PAUSED)
            self.pipeline_rec.change_state(gst.StateChange.PAUSED_TO_READY)
            self.pipeline_rec.change_state(gst.StateChange.READY_TO_NULL)
            self.start_record = False
            # try:
            #     self.pipeline_rec.set_state(gst.State.NULL)
            # except:
            #     print 'no pipeline'
            #     return
            # self.pipeline_rec.change_state(gst.StateChange.PLAYING_TO_PAUSED)
        elif msg.get_structure().get_value('hypothesis'):
            # self.pipeline_rec = gst.parse_launch('autoaudiosrc name=audiosrc ! audioconvert ! audioresample ! wavenc ' +
            #                                      '! filesink name=filesink location=/home/ketamine/skuba_ws/src' +
            #                                      '/speech_processing/SKUBA_ShotgunMic_' +
            #                                      self.timestamp + '.wav')
            # self.pipeline.set_state(gst.State.PLAYING)
            if self.start_record == False:
                self.start_record = True
                self.record_pipeline()
            # self.pipeline_rec.change_state(gst.StateChange.PAUSED_TO_PLAYING)
            # print self.filesink.get_property('ts-offset'), "-------------------------------------"
            self.partial_result(msg.get_structure().get_value('hypothesis'))

    def record_pipeline(self):
        self.timestamp = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
        print 'record--------------', self.timestamp

        self.filesink.set_property('location', '/home/ketamine/skuba_ws/src' +
                                   '/speech_processing/SKUBA_ShotgunMic_' +
                                   self.timestamp + '.wav')

        # self.pipeline_rec = gst.parse_launch('autoaudiosrc name=audiosrc ! audioconvert ! audioresample ! wavenc ' +
        #                                      '! filesink name=filesink location=/home/ketamine/skuba_ws/src' +
        #                                      '/speech_processing/SKUBA_ShotgunMic_' +
        #                                      self.timestamp + '.wav')

        self.pipeline_rec.set_state(gst.State.NULL)

        bus_rec = self.pipeline_rec.get_bus()
        bus_rec.add_signal_watch()
        bus_rec.connect('message::element', self.element_message)

        self.pipeline_rec.change_state(gst.StateChange.NULL_TO_READY)
        self.pipeline_rec.change_state(gst.StateChange.READY_TO_PAUSED)
        self.pipeline_rec.change_state(gst.StateChange.PAUSED_TO_PLAYING)

if __name__=="__main__":
    r = grammar_recognizer()

