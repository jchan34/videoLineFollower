import cv2
import matplotlib.pyplot as plt
import numpy as np

video_path = '/content/drive/My Drive/ENPH 353/raw_video_feed.mp4'
cap = cv2.VideoCapture(video_path)


frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter('/content/drive/My Drive/ENPH 353/lineFollowingV4.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

threshold = 100
radius = 15
color = (0,0,255)
lineSample = 220

while (cap.isOpened()):

  

  ret, frame = cap.read()  

  if ret == True:
  
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

 
    _, img_bin = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
    

    # line = img_bin[lineSample][:]

    # logic = line < threshold

    # newline_size = line[logic].size
    # for x in range(line.size): 
    #     if line[x] < threshold:
    #           min = x;
    #           break
              
    # centre_coordinates = (min + round(newline_size/2),lineSample)
    # image = cv2.circle(frame, centre_coordinates, radius, color, -1)


    ## Should add a case where no line is detected, so make centre_coordinates 
    ## the same as previous frame until a line is detected

    small_chunk = img_bin[200:240][:]
    averaged_array = np.average(small_chunk, axis=0)
    min_value = np.amin(averaged_array)
    if min_value == 255:
      image = cv2.circle(frame, centre_coordinates, radius, color, -1)
    else:
      result = np.where( averaged_array  == min_value)
      centre_min_index = np.average(result[0],0)
      centre_coordinates = (int(centre_min_index),lineSample)
      image = cv2.circle(frame, centre_coordinates, radius, color, -1)
      
    out.write(image)

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  else:
    break
out.release()
cap.release()
cv2.destroyAllWindows()
