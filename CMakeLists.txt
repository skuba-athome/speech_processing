cmake_minimum_required(VERSION 2.8.3)
project(speech_processing)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  genmsg
  actionlib_msgs
  actionlib
)

add_service_files(
  FILES
  Gram.srv
)

add_action_files(
  DIRECTORY 
  action 
  FILES 
  VoiceReg.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  actionlib_msgs
)

catkin_package(DEPENDS)
