#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from subprocess import call

global obj,fea

class getDirection:

    stage = 'start'
    temp = ''
    obj = ''
    fea = ''
    inputArray = []
    def __init__(self):
        #rospy.init_node('listener', anonymous=True)

        rospy.Subscriber("/voice/output", String, self.callback)

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

    def callback(self,data):
        if self.stage == 'start':
            if data.data == 'What is this':
                call(['espeak','It is cola , is not it'])
                self.stage = 'check_ans'
            else :
                call(['espeak','sorry I do not understand what do you want, can you repeat?'])
                self.stage = 'start'

        elif self.stage == 'check_ans':
            if 'no' in data.data :
                call(['espeak','I do not know what is this, Do you want me to recognize?'])
                self.stage = 'learning'
            if 'yes' in data.data:
                call(['espeak','Wow , Why I am so genious, Do you want to know anything else about it?'])
                self.stage = 'question'
        
        elif self.stage == 'question':
            if 'no' in data.data :
                call(['espeak','Ok , see you next time sweety. bye'])
                self.stage = 'start'
            elif 'yes' in data.data:
                call(['espeak','What is the feature which you want to know?'])
                self.stage = 'answering'

        elif self.stage == 'answering':
            ans_fea =  data.data
            call(['espeak','the'+ans_fea+ 'of cola is ten baht. Have any feature do you want to know more?'])
            self.stage == 'more_ques'

        elif self.stage == 'more_ques':
            if 'no' in data.data:
                call(['espeak','Ok , see you next time sweety. bye'])
                self.stage = 'start'
            elif 'yes' in data.data:
                call(['espeak','So what is the feature which you want to know next?'])
                self.stage = 'answering'

        elif self.stage == 'learning':
            if 'no' in data.data:
                self.stage = 'start'
            elif 'yes' in data.data:
                call(['espeak','So what is this?'])
                self.stage = 'store_data'

        elif self.stage == 'store_data':
            obj = data.data
            call(['espeak','what is the category of the'+obj])
            self.stage = 'feature'

        elif self.stage == 'feature':
            cat = data.data
            call(['espeak','Do you know other feature about it?'])
            self.stage = 'ask_data'


        elif self.stage = 'ask_data'
            if  'yes' in data.data:
                if cat == 'food' or cat == 'drink':
                    fea = 'volumn'
                    call(['espeak','what is the'+ fea +' of the'+obj])
                    self.stage = 'insert'
                elif cat =='no':
                    fea = 'price'
                    call(['espeak','what is the '+fea+' of the'+obj])
                    self.stage = 'insert'
                else:
                    fea = 'width'
                    call(['espeak','what is the '+fea+' of the'+obj])
                    self.stage = 'insert'
            elif 'no' in data.data:
                call(['espeak','Ok , no problem honey. see you next time.  bye'])
                self.stage = 'start'


        elif self.stage = 'insert':
            check = data.data
            call(['espeak','Did you tell me that the'+fea+'of the'+obj+'is' + check ', right?'])
            self.stage = 'check_fea'

        elif self.stage == 'check_fea':
            if 'no' in data.data:
                call(['espeak','Oh Sorry , Can you repeat it?'])
                self.stage = 'insert'
            elif 'yes' in data.data:
                call(['espeak','Ok , I will remember , Can you give me more information?'])
                self.stage = 'ask_data'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        getDirection()
    except rospy.ROSInterruptException:
        pass