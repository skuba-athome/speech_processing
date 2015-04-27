#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from subprocess import call

class getDirection:

    stage = 'start'
    temp = ''
    inputArray = []
    def __init__(self):
        #rospy.init_node('listener', anonymous=True)

        rospy.Subscriber("/voice/output", String, self.callback)

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

    def callback(self,data):
        if self.stage == 'start':
            call(['espeak','robot init'])
            if data.data == 'follow me':
                call(['espeak','following master'])
                self.stage = 'following'

        elif self.stage == 'following':
            self.checkFollow(data)

        elif self.stage == 'waiting':
            self.checkFollow(data)
            self.getInput(data)

        elif self.stage == 'confirm':
            self.confirm(data)

    def checkFollow(self,data):
        if data.data == 'follow me':
            if self.stage == 'following':
                call(['espeak','I am following master'])
            elif self.stage == 'waiting':
                call(['espeak','following master'])
                self.stage = 'following'

        elif data.data == 'robot stop':
            if self.stage == 'following':
                call(['espeak','I am stopped'])
                self.stage = 'waiting'
            elif self.stage == 'waiting':
                call(['espeak','stopping'])

    def getInput(data):
        if 'location' in data.data or 'shelf' in data.data:
            self.temp = data.data
            call(['espeak','robot heard '+data.data.replace('my','your')+'yes or no'])
            sleep(1)
            print 'I heard '+data.data
            stage = 'confirm'

    def confirm(self,data):
        if data.data == 'robot yes':
            call(['espeak','confirmed '+data.data.replace('my','your')])
            self.inputArray.append(self.temp)

        elif data.data == 'robot no':
            call(['espeak','cancled'])
        else :
            return

        self.temp = ''
        self.stage = 'waiting'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        getDirection()
    except rospy.ROSInterruptException:
        pass