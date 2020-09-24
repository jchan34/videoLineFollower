#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import CameraInfo, Image
import cv2, cv_bridge
import numpy

class Follower:

	def __init__(self):

		self.bridge = cv_bridge.CvBridge()
	
		self.image_sub = rospy.Subscriber('/camera1/image_raw', 
			Image, self.image_callback)
		self.cmd_vel_pub = rospy.Publisher('/cmd_vel',Twist, queue_size = 1)
		self.move = Twist()

	def image_callback(self,msg):

		cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding = 'bgr8')
		_, img_bin = cv2.threshold(cv_image, 100,255, cv2.THRESH_BINARY)
		small_chunk = img_bin[700:800][:]
		a = numpy.array([11,1,1])
		av = numpy.average(small_chunk, axis = 0)
		min_value = numpy.amin(av)

		if min_value == 255:
			xval = prev_xval 
		else:
			result = numpy.where(av == min_value)
			centre_min_index = numpy.average(result[0],0)

			prev_xval = centre_min_index
			xval = centre_min_index
			
		p = 0.015
		d = 0.02
		err = 400 - xval
		errd = xval - prev_xval
		gain = p*err + d*errd
		self.move.linear.x = 0.6
		self.move.angular.z = gain
		self.cmd_vel_pub.publish(self.move)


rospy.init_node("follower")
prev_xval = 400
follower = Follower()

rospy.spin()
