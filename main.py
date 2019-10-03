import cv2
import numpy as np
from SourceImageHandler import SourceImageHandler
from PhotomosaicGenerator import *


# Get as many images as possible from the user
sih = SourceImageHandler(r'/home/eshels/Downloads/london/', r'/home/eshels/Downloads/src_img')

test_img = cv2.imread(r'/home/eshels/Downloads/london/IMG_20190909_135204.jpg')
test_img = cv2.resize(test_img, (2000, 2000))

pix_mat = divide_img(test_img)

pixellated_img = create_pixel_image(pix_mat)

cv2.imshow('', pixellated_img)
cv2.waitKey()
