###########DO NOT DELETE#########################
#cat /proc/sys/vm/overcommit_memory
#echo 1 | sudo tee /proc/sys/vm/overcommit_memory
#################################################

from tifffile import imsave
import numpy as np
import cv2
import os
import datetime
from PIL import Image 


norm = np.zeros((480,848,1))
print(norm.shape)

path, dirs, files = next(os.walk("/home/kathir/Desktop/tiff_images"))
file_count = len(files)

print(file_count)

stack = np.empty((file_count, 120, 212))

for i in range(0,file_count):
    im = Image.open(f'/home/kathir/Desktop/tiff_images/test-{i+1}.tiff')
    #print(im.shape)
    stack[i,:,:] = im

imsave('multipage.tif', stack)