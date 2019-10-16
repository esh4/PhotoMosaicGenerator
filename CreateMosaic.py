import sys, getopt
from PhotomosaicGenerator import PhotoMosaicGenerator
from ImgaeCaching import ImageCaching
import cv2
import datetime


def main(argv):
    input_file = ''
    output_file = '{}.jpg'.format(datetime.datetime.now())
    res = 50

    img_cache = ImageCaching()
    img_cache.update_cache()

    try:
        opts, args = getopt.getopt(argv, "hi:o:ur", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt == '-u':
            img_cache.update_cache()
        elif opt == '-r':
            res = arg

    mosaic_generator = PhotoMosaicGenerator(img_path=input_file, grid_res=res)
    generated_mosaic, pixelated = mosaic_generator.run(img_cache.average_colors, img_cache.src_images_names)

    cv2.imwrite(output_file, generated_mosaic)


if __name__ == '__main__':
    main(sys.argv[1:])
