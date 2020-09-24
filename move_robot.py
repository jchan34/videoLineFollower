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
prev_xval = 0
#sub_cam_image = rospy.Subscriber('/camera1/image_raw',Image)
sub_cam_info = rospy.Subscriber('/camera1/camera_info',CameraInfo)



def find_center_of_line_pixel(cv_image):
	
    _, img_bin = cv2.threshold(cv_image, 100,255, cv2.THRES_BINARY)

    small_chunk = img_bin[700:800][:]
    averaged_array = [float(sum(l))/len(l) for l in zip(*small_chunk)]
    min_value = min(averaged_array)
    indices = [i for i, x in enumerate(averaged_array) if x == min_value]
    mid_index = int(len(indices) / 2) - 1	
    xval = int(indices[mid_index])
    centre_coordinates = (xval,750)      

    prev_xval = xval	
    # Case for if no line in camera feed
    if min_value == 1 and prev_xval < 400:
	xval = 0
    elif min_value == 1 and prev_xval >= 400:
	xval = 800
	
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
	


