
# coding: utf-8

# In[1]:


import os
import cv2
import numpy as np
from PIL import Image


# In[2]:


path = "./meter_reading_images/"
files = [file for file in os.listdir(path) if file.endswith('.png')]
print(sorted(files))


# In[ ]:


# Desent results with this range
# roi_lower = np.array([40, 25, 0])
# roi_upper = np.array( [80, 255, 255])


# In[60]:


def meter_disp_segment(img_path):
    print(img_path)
    imgArr_o = cv2.imread(path + img_path)
    imgArr = cv2.cvtColor(imgArr_o, cv2.COLOR_BGR2HSV)
    roi_lower = np.array([40, 25, 0])
    roi_upper = np.array( [80, 255, 255])
    mask = cv2.inRange(imgArr, roi_lower, roi_upper)
    # Bitwise-AND mask and original image
    imgArr = cv2.bitwise_and(imgArr_o,imgArr_o, mask= mask)
    
    # Find contours
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        wbuffer = 0.75 * w
        hbuffer = 0.1 * h
        imgArr_ext = imgArr_o[y:y + h + int(hbuffer), x:x + w + int(wbuffer)]
        
        imgArr_ext_gray = cv2.cvtColor(imgArr_ext, cv2.COLOR_BGR2GRAY)
        imgArr_ext_pp = cv2.adaptiveThreshold(imgArr_ext_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
        imgArr_ext_pp = cv2.medianBlur(imgArr_ext_pp, 13)
        cv2.rectangle(imgArr_o, (x, y), (x + w + int(wbuffer), y + h + int(hbuffer)), (255, 0, 255), 10)
        break

    DEBUG = True
    if DEBUG:
        cv2.imwrite('./output/meter_disp_ext/' + img_path.split('.')[0] + '_ext.png', imgArr_ext)
        cv2.imwrite('./output/mask/' + img_path.split('.')[0] + '_mask.png', mask)
        cv2.imwrite('./output/meter_disp_bb/' + img_path.split('.')[0] + '_bb.png', imgArr_o)
        cv2.imwrite('./output/meter_disp_ext_pp/' + img_path.split('.')[0] + '_pp.png', imgArr_ext_pp)
    print(img_path + '--> DONE')


# In[61]:


for meter in files:
    meter_disp_segment(meter)

