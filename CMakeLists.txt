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

catkin_python_setup()

add_service_files(
  FILES
  Gram.srv
)

add_action_files(
  FILES 
  VoiceReg.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  actionlib_msgs
)

catkin_package(CATKIN_DEPENDS message_runtime)

