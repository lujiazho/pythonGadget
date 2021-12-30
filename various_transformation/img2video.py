import cv2
import numpy as np
import glob
 
img_array = []
names = glob.glob('./video_data/*.jpg')
names.sort(key=lambda x: int(x.split('_')[2].split('.')[0]))
for filename in names:
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 21.47, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()