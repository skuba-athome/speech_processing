#!/usr/bin/env python
import os
import rospkg

class GramLm():
	rospack = rospkg.RosPack()

	#PATH---------------------------------------
	ROS_PATH = rospack.get_path('speech_processing')
	GPSR_PATH = ['voice_recog/GPSR/GPSR.fsg', 'voice_recog/GPSR/GPSR.dic']
	FIFTY_QUESTION_PATH = ['voice_recog/50_questions_Frank/50_questions.fsg', 'voice_recog/50_questions_Frank/50_questions.dic']
	RESTAURANT_PATH = ['voice_recog/RESTAURANT/restaurant.fsg', 'voice_recog/RESTAURANT/restaurant.dic']

	GPSR_LM_PATH = 'voice_recog/GPSR/GPSR.lm'
	RESTAURANT_LM_PATH = 'voice_recog/RESTAURANT/restaurant.lm'

	#GRAMMAR------------------------------------
	GPSR_GRAMMAR = 1
	FIFTY_QUESTION_GRAMMAR = 2
	RESTAURANT_GRAMMAR = 3

	#LM-----------------------------------------
	GPSR_LM = 101
	RESTAURANT_LM = 103

	#DICTIONARY---------------------------------
	GPSR_DIC = 1
	FIFTY_QUESTION_DIC = 2
	RESTAURANT_DIC = 3

	#DICT---------------------------------------
	gram = {GPSR_GRAMMAR: os.path.join(ROS_PATH, GPSR_PATH[0]), FIFTY_QUESTION_GRAMMAR: os.path.join(ROS_PATH, FIFTY_QUESTION_PATH[0]),
			GPSR_LM: os.path.join(ROS_PATH, GPSR_LM_PATH), RESTAURANT_GRAMMAR: os.path.join(ROS_PATH, RESTAURANT_PATH[0]),
			RESTAURANT_LM: os.path.join(ROS_PATH, RESTAURANT_LM_PATH)
		}

	dic = {GPSR_DIC: os.path.join(ROS_PATH, GPSR_PATH[1]), FIFTY_QUESTION_DIC: os.path.join(ROS_PATH, FIFTY_QUESTION_PATH[1]),
		   RESTAURANT_DIC: os.path.join(ROS_PATH, RESTAURANT_PATH[1])	
		}