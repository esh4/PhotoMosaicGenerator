import cv2
import numpy as np
from PhotomosaicGenerator import *
import datetime
from ImgaeCaching import ImageCaching


# Get as many images as possible from the user

img_cache = ImageCaching()

# Get a "target image" from the user
test_img = cv2.imread(r'/home/eshels/Downloads/london/IMG_20190903_182746.jpg')
test_img = cv2.resize(test_img, (2000, 2000))


pmg = PhotoMosaicGenerator(test_img)

pix_mat = pmg.divide_img_into_color_grid()

pixellated = pmg.create_pixel_image(pix_mat)

src_array =[]# pmg.average_color_to_image()


cv2.imwrite('test_colage-{}.jpg'.format(datetime.datetime.now()), pmg.construct_mosaic())
# cv2.imshow('pixellated', pixellated)
cv2.waitKey()



