import os
import cv2
import json
import logging
from PhotomosaicGenerator import average_color
import numpy as np


def diff_hash(image, hashSize=8):
    # resize the input image, adding a single column (width) so we
    # can compute the horizontal gradient
    resized = cv2.resize(image, (hashSize + 1, hashSize))

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff: np.ndarray = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def find_imgs_in_dir(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))
                # print(os.path.join(r, file))
    return files


def save_dict(filename, data):
    # old_data = read_dict('{}.json'.format(filename))
    # data = data.update(old_data)
    with open('{}.json'.format(filename), 'w') as outfile:
        json.dump(data, outfile)


def read_dict(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


class ImageCaching(object):
    def __init__(self, path='src_images/'):
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        self.SRC_SIZE = 500
        self.src_dir_path = path
        self.src_images_names = {}
        self.average_colors = {}
        self.indexed_averages = {}
        self.cache_files = {
            'cache_names': self.src_images_names,
            'cache_average_colors': self.average_colors,
            'cache_indexed_averages': self.indexed_averages
        }

    def check_for_new_images(self):
        self.update_cache()
        for img_path in find_imgs_in_dir(self.src_dir_path):
            if img_path not in self.src_images_names.values():
                self.add_src_img(img_path)
                logging.info('adding {}'.format(img_path))
        self.update_cache()

    def add_src_img(self, img_path):
        processed_src_img = self.process_src_img(img_path)
        cv2.imwrite(img_path, processed_src_img)
        img_hash = diff_hash(processed_src_img)
        self.src_images_names[img_hash] = img_path
        self.average_colors[img_hash] = average_color(processed_src_img)

    def process_src_img(self, img_path):
        original = cv2.imread(img_path)
        resized = cv2.resize(original, (self.SRC_SIZE, self.SRC_SIZE))
        return resized

    def update_cache(self):
        print('updating from cache...')
        for filename, data_var in self.cache_files.items():
            try:
                stored_data = read_dict('{}.json'.format(filename))
            except FileNotFoundError:
                save_dict(filename, data_var)
                stored_data = {}
            data_var.update(stored_data)
            save_dict('{}'.format(filename), data_var)


if __name__ == '__main__':
    im_cache = ImageCaching()
    im_cache.check_for_new_images()
    print(im_cache.average_colors)
