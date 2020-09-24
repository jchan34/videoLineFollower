#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
from sensor_msgs.msg import CameraInfo, Image
import cv2
import numpy as np

rospy.init_node('topic_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size =1)
bridge = CvBridge()
move = Twist()

sub_cam_image = rospy.Subscriber('/camera1/image_raw',Image)
sub_cam_info = rospy.Subscriber('/camera1/camera_info',CameraInfo)



def find_line(cv_image):
	
	_, img_bin = cv2.threshold(cv_image, 100,255, cv2.THRES_BINARY)

	small_chunk = img_bin[700:800][:]
    averaged_array = np.average(small_chunk, axis=0)
    min_value = np.amin(averaged_array)

    result = np.where( averaged_array  == min_value)
    centre_min_index = np.average(result[0],0)
    xval = int(centre_min_index)
    centre_coordinates = (xval,750)      


    return xval

def calculate_error(xval):
	targetX = 400
	error = targetX - xval
	
	p = 0.4
	i = 0
	d = 0
	gain = p*error

	return gain




while not rospy.is_shutdown():

	sub_cam_image = rospy.Subscriber('/camera1/image_raw',Image)
	cv_image = bridge.imgmsg_to_cv2(sub_cam_image, desired_encoding = 'CV_8UC1')
	x = find_line(cv_image)
	gain = calculate_error(x)
	move.linear.x = 0.5
	move.angular.z = gain
	pub.publish(move)
	


