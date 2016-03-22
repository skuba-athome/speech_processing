#!/usr/bin/env python
import os
import rospkg

class GramLm():
	rospack = rospkg.RosPack()

	#PATH---------------------------------------
	ROS_PATH = rospack.get_path('speech_processing')

	NAVIGATION_PATH = ['voice_recog/Navigate_Jap2016/NavJap.fsg', 'voice_recog/Navigate_Jap2016/NavJap.dic']
	RESTAURANT_PATH = ['voice_recog/Restaurant_Jap2016/RestaurantJap.fsg', 'voice_recog/Restaurant_Jap2016/RestaurantJap.dic']
	GPSR_PATH = ['voice_recog/GPSR_Jap2016/GPSRJap.fsg', 'voice_recog/GPSR_Jap2016/GPSRJap.dic']
	NURSE_PATH = ['voice_recog/RoboNurse_Jap2016/NurseJap.fsg', 'voice_recog/RoboNurse_Jap2016/NurseJap.dic']
	GPSR2_PATH = ['voice_recog/GPSR_2_Jap2016/GPSR2Jap.fsg', 'voice_recog/GPSR_2_Jap2016/GPSR2Jap.dic']

	NAVIGATION_LM_PATH = 'voice_recog/Navigate_Jap2016/NavJap.lm'
	RESTAURANT_LM_PATH = 'voice_recog/Restaurant_Jap2016/RestaurantJap.lm'
	GPSR_LM_PATH = 'voice_recog/GPSR_Jap2016/GPSRJap.lm'
	NURSE_LM_PATH = 'voice_recog/RoboNurse_Jap2016/NurseJap.dic'
	GPSR2_LM_PATH = 'voice_recog/GPSR_2_Jap2016/GPSR2Jap.lm'

	#GRAMMAR------------------------------------
	NAVIGATION_GRAMMAR = 1
	RESTAURANT_GRAMMAR = 2
	GPSR_GRAMMAR = 3
	NURSE_GRAMMAR = 4
	GPSR2_GRAMMAR = 5

	#LM-----------------------------------------
	NAVIGATION_LM = 101
	RESTAURANT_LM = 102
	GPSR_LM = 103
	NURSE_LM = 104
	GPSR2_LM = 105

	#DICTIONARY---------------------------------
	NAVIGATION_DIC = 1
	RESTAURANT_DIC = 2
	GPSR_DIC = 3
	NURSE_DIC = 4
	GPSR2_DIC = 5

	#DICT---------------------------------------
	gram = {NAVIGATION_GRAMMAR: os.path.join(ROS_PATH, NAVIGATION_PATH[0]), 
			NAVIGATION_LM: os.path.join(ROS_PATH, NAVIGATION_LM_PATH),
			RESTAURANT_GRAMMAR: os.path.join(ROS_PATH, RESTAURANT_PATH[0]),
			RESTAURANT_LM: os.path.join(ROS_PATH, RESTAURANT_LM_PATH),
			GPSR_GRAMMAR: os.path.join(ROS_PATH, GPSR_PATH[0]),
			GPSR_LM: os.path.join(ROS_PATH, GPSR_LM_PATH),
			NURSE_GRAMMAR: os.path.join(ROS_PATH, NURSE_PATH[0]),
			NURSE_LM: os.path.join(ROS_PATH, NURSE_LM_PATH),
			GPSR2_GRAMMAR: os.path.join(ROS_PATH, GPSR2_PATH[0]),
			GPSR2_LM: os.path.join(ROS_PATH, GPSR2_LM_PATH)
		}

	dic = {	NAVIGATION_DIC: os.path.join(ROS_PATH, NAVIGATION_PATH[1]),
			RESTAURANT_DIC: os.path.join(ROS_PATH, RESTAURANT_PATH[1]),
			GPSR_DIC: os.path.join(ROS_PATH, GPSR_PATH[1]),
			NURSE_DIC: os.path.join(ROS_PATH, NURSE_PATH[1]),
			GPSR2_DIC: os.path.join(ROS_PATH, GPSR2_PATH[1])
		}