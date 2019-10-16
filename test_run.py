from PhotomosaicGenerator import *
import datetime
from ImgaeCaching import ImageCaching


# Get as many images as possible from the user

img_cache = ImageCaching()
img_cache.update_cache()

# Get a "target image" from the user
test_img = cv2.imread(r'/home/eshels/Downloads/london/IMG_20190910_154200.jpg')
test_img = cv2.resize(test_img, (2000, 2000))

pmg = PhotoMosaicGenerator(test_img, grid_res=10)


cv2.imwrite('test_colage-{}.jpg'.format(datetime.datetime.now()),
            pmg.run(img_cache.average_colors, img_cache.src_images_names)[0])
# cv2.imshow('pixellated', pixellated)
# cv2.waitKey()



