import cv2
vidcap = cv2.VideoCapture('vid.mp4')
success, image = vidcap.read()
count = 1
while success:
  cv2.imwrite("video_data/image_%d.jpg" % count, image)    
  success, image = vidcap.read()
  print('Saved image ', count)
  count += 1
