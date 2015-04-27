#!/usr/bin/env python
import sys
import find
from datetime import datetime
from pymongo import Connection
from pymongo.errors import ConnectionFailure

#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from subprocess import call

import roslib; roslib.load_manifest('speech_processing')
import collections


stage = 'start'
temp = ''
obj = ''
cat= ''
fea = []
fea_data = []
obj_value=''
obj_recog=''
data_fea =''
ans_fea=''
inputArray = []
objects=[]
categories = []
value=[]
greeting=[]
features=[]
date=[]
choose=[]

def readFileToList(filename):
    output = [] 
    file = open(filename)
    for line in file:
        output.append(line.strip().lower())
    return output


class getDirection:
    def __init__(self):
        #rospy.init_node('listener', anonymous=True)
        global obj,cat,fea,obj_recog,obj_value,ans_fea,i,fea_data,stage,temp,objects,categories,value,greeting,features,date,data_fea,choose
        objects = readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/project/objects_conver.txt')
        categories = readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/project/categories_conver.txt')
        value = readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/project/value_conver.txt')
        greeting = readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/project/greeting_conver.txt')
        features = readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/project/features_conver.txt')
        date= readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/project/date_conver.txt')


        # spin() simply keeps python from exiting until this node is stopped
        rospy.Subscriber("/voice/output", String, self.callback)
        rospy.spin()
    def callback(self,data):
        global obj,cat,fea,obj_recog,obj_value,ans_fea,i,fea_data,stage,temp,objects,categories,value,greeting,date,data_fea,choose
    	print(data.data)
        if stage == 'start':
            x=0
            fea_data = ['','','','','','','','','','','','']
            for x in range(12):
                fea_data[x] = 'no'
            i=-1
            if data.data in greeting:
                call(['espeak',data.data+' sweety! Nice to meet you   My name is Antonio  I come to help your shopping life easier   So  What is the object do you want '])
               	choose = readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/choose.txt')
                obj_recog = choose[0]
                #obj_recog = 'green tea'
                call(['espeak','It is'+obj_recog+ ' is not it ?'])
                stage = 'check_ans'
            elif data.data == 'no':
                call(['espeak','sorry I do not understand what do you want, can you repeat?'])
                stage = 'start'

        elif stage == 'check_ans':
            if 'robot no' in data.data :
                call(['espeak','I do not know what is this, Do you want me to recognize?'])
                stage = 'learning'
            elif 'robot yes' in data.data:
                #call(['espeak','Wow , Why am I so genious , Do you want to know anything else?'])
                call(['espeak','Wow , Why am I so genious , Do you want to know anything else?'])
                stage = 'question'
            elif 'robot cancel' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'start'

        
        elif stage == 'question':
            if 'robot no' in data.data :
                call(['espeak','Ok , see you next time sweety. bye'])
                stage = 'start'
            elif 'robot yes' in data.data:
                call(['espeak','What feature do you want to know?'])
                stage = 'answering'
            elif 'robot cancel' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'start'

        elif stage == 'answering':
            #ans_fea = data.data
            #obj_value = query data from db
            if data.data in features:
                ans_fea =  data.data
                obj_value = str(find.FindDB(obj_recog,ans_fea))
                if (obj_value == 'Not Found'):
                #    print('Not Found')
                #    call(['espeak','Sorry ,  I do not know  the  value of this feature   ,   Have '])
                #    stage = 'question'
                    call(['espeak','Sorry , I do not know the value of this feature , can you give me the data ?'])
                    stage = 'ask_for_learning_fea'
                else :
                    print(obj_value)
                    call(['espeak',' the '+ans_fea+ ' of '+obj_recog+' is '+obj_value+'  ,  Have any feature do you want to know more?'])
                    stage = 'question'
        
        elif stage == 'ask_for_learning_fea':
            if 'robot no' in data.data:
               call(['espeak','So have another feature do you want to know?'])
               stage = 'question'
            elif 'robot yes' in data.data:
                call(['espeak','What is the' +ans_fea+' of the'+obj_recog])  
                stage = 'learning_fea'

        elif stage == 'learning_fea':
            if data.data in value:
                data_fea = data.data
                call(['espeak','Did you tell me  the'+ans_fea+'  of   the'+obj_recog+' is' + data_fea+ ', right?'])
                stage = 'ask_for_sure'

        elif stage == 'ask_for_sure' :
            if 'robot no' in data.data:
                call(['espeak','Oh Sorry , Can you repeat it?'])
                stage = 'learning_fea'
            elif 'robot yes' in data.data:
                call(['espeak','Ok , I will remember ,   Thank you for your information  , Have any feature do you want to know more?'])
                find.AddData(obj_recog,ans_fea,data_fea)
                stage = 'question'

        elif stage == 'learning':
            if 'robot no' in data.data:
            	call(['espeak','Ok  see you next time sweety. bye'])
                stage = 'start'
            elif 'robot yes' in data.data:
                call(['espeak','So what is this?'])
                stage = 'store_data'
            elif 'robot cancel' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'start'

        elif stage == 'store_data':
            if data.data in objects:
                obj = data.data
                call(['espeak','Did you tell me' +obj+'  right'])
                stage = 'confirm_obj'
            #obj = data.data

        elif stage  == 'confirm_obj' :
            if 'robot yes' in data.data:
        		call(['espeak','what is the category of the'+obj])
        		stage = 'category'
            elif 'robot no' in data.data:
                call(['espeak','If it not , can you repeat?'])
                stage = 'store_data'
            elif 'robot cancel' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'start'

        elif stage == 'category':
            if data.data in categories :
                cat =  data.data
                call(['espeak','Did you tell me' +cat+' right'])
                stage = 'confirm_cat'

        elif stage  == 'confirm_cat' :
            if 'robot yes' in data.data:
                call(['espeak','Do you know its feature?'])
                stage = 'ask_data'
            elif 'robot no' in data.data:
                call(['espeak','If it not , can you repeat?'])
                stage = 'category'
            elif 'robot cancel' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'start'


        elif stage == 'ask_data':
            if  'robot yes' in data.data:
                i=i+1
                if(cat == 'food' or cat == 'drink' or cat == 'fruit' or cat == 'snack' or cat == 'vegetable' or cat == 'bakery'):
                    fea = ['price  in  baht','location', 'calories  in  kilo calories','volumn  in  millilitre', 'flavor',
                    'production date' , 'expired date']
                    if ( i <= 5):
                        print(fea[i])
                        call(['espeak','what is the'+ fea[i] +' of the'+obj])
                        stage = 'insert'
                    else:  
                        stage = 'finish'

                elif (cat =='blank'):
                    #fea = 'price'
                    fea = ['price  in  baht','location', 'calories  in  kilo calories','volumn  in  milli litre', 'flavor',
                    'production date' , 'expired date' , 'color', 'width  in  centimeter' , 'height  in  centimeter' , 'long  in  centimeter']
                    if ( i <= 2):
                        print(fea[i])
                        call(['espeak','what is the'+ fea[i] +' of the'+obj])
                        stage = 'insert'
                    else:  
                        stage = 'finish'

                else:
                    fea = ['price' , 'location' , 'color' , 'width  in  centimeter' , 'height  in  centimeter' , 'long  in  centimeter']
                    if ( i <= 2):
                        print(fea[i])
                        call(['espeak','what is the'+ fea[i] +' of the  '+obj])
                        stage = 'insert'
                    else:  
                        stage = 'finish'

            elif 'robot no' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'finish'
            elif 'robot cancel' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'start'

        elif stage == 'insert':
            if data.data == 'blank' :
                fea_data[i] = 'no'
                print(fea_data[i])
                call(['espeak','You do not know the' + fea[i]+'of   the'+obj+' , right?'])
                stage = 'check_fea'
            else :
                if 'in' in fea[i]:
                    if ( data.data not in value and data.data not in objects and data.data not in features and data.data not in categories and data.data not in greeting and data.data not in date):
                        fea_data[i] = data.data
                        print(fea_data[i])
                        call(['espeak','Did you tell me the'+fea[i]+'  of   the'+obj+' is' + fea_data[i]+ ', right?'])
                        stage = 'check_fea'
                elif 'date' in fea[i]:
                    if (data.data not in value and data.data not in objects and data.data not in features and data.data not in categories and data.data not in greeting):
                        fea_data[i] = data.data
                        print(fea_data[i])
                        call(['espeak','Did you tell me the'+fea[i]+'  of   the'+obj+' is' + fea_data[i]+ ', right?'])
                        stage = 'check_fea'
                else:
                    if data.data in value :
                        fea_data[i] = data.data
                        print(fea_data[i])
                        call(['espeak','Did you tell me the'+fea[i]+'  of   the'+obj+' is' + fea_data[i]+ ', right?'])
                        stage = 'check_fea'

        elif stage == 'check_fea':
            if 'robot no' in data.data:
                call(['espeak','Oh Sorry , Can you repeat it?'])
                stage = 'insert'
            elif 'robot yes' in data.data:
                if (i == 2) :
                    call(['espeak','Ok , I will remember ,   Thank you for your information  see you next time ,  bye'])
                    stage = 'finish'
                else :
                    call(['espeak','Ok , I will remember ,   Ready for next question?'])
                    stage = 'ask_data'
            elif 'robot cancel' in data.data:
                call(['espeak','Ok ,   no problem honey    see you next time  bye'])
                stage = 'start'


        elif stage == 'finish':
            if (cat == 'food' or cat == 'drink' or cat == 'fruit' or cat == 'snack' or cat == 'vegetable' or cat == 'bakery'  ):
                doc = {
                    "name" : obj,
                    "category" : cat,
                    "price" : fea_data[0],
                    "location" : fea_data[1],
                    "calories" : fea_data[2],
                    "volumn" : fea_data[3],
                    "flavor" : fea_data[4],
                    "production date" : fea_data[5],
                    "expiration date" : fea_data[6]
                }
            elif (cat == 'blank'):
                doc = {
                    "name" : obj,
                    "category" : cat,
                    "price" : fea_data[0],
                    "location" : fea_data[1],
                    "calories" : fea_data[2],
                    "volumn" : fea_data[3],
                    "flavor" : fea_data[4],
                    "production date" : fea_data[5],
                    "expiration date" : fea_data[6],
                    "color" : fea_data[7],
                    "width" : fea_data[8],
                    "height" : fea_data[9],
                    "long" : fea_data[10],
                    "shape" : fea_data[11]
                }
            else :
                doc = {
                    "name" : obj,
                    "category" : cat,
                    "price" : fea_data[0],
                    "location" : fea_data[1],
                    "color" : fea_data[2],
                    "width" : fea_data[3],
                    "height" : fea_data[4],
                    "long" : fea_data[5],
                    "shape" : fea_data[6]
                }
            print(doc)
            find.InsertDB(doc)
            find.RemoveBlank()
            stage = 'start'

if __name__ == '__main__':
    try:
        rospy.init_node('conversation')
        getDirection()
    except rospy.ROSInterruptException:
        pass

"""
import rospy
import time
from subprocess import call
from std_msgs.msg import String

def callback(data):
	print(data.data)
	if "no" in data.data:
		call(["espeak","What do you want from me?"])
	elif "yes" in data.data:
		call(["espeak","Ok , sweety"])


def listener():
	rospy.init_node('listener',anonymous=False)
	rospy.Subscriber("/voice/output",String,callback)
	rospy.spin()
if __name__ == '__main__':
	listener()
	"""