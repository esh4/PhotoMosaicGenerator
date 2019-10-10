import os
import cv2
import json
import math


class SourceImageHandler:
    def __init__(self, src_path, dst_path):
        self.dst_path = dst_path
        self.src_path = src_path

    def _create_source_images(self, path):
        average_colors = {}
        try:
            for img_path in find_image_paths(path):
                source_img = cv2.imread(img_path)
                short_side = min(source_img.shape[:2])
                resized = cv2.resize(source_img, (short_side, short_side))
                cv2.imwrite(r'{}/{}'.format(self.dst_path, str(hash(img_path))+'.jpg'), resized)
                average_colors[hash(img_path)] = average_color(resized)
        finally:
            save_dict('{}/{}'.format(self.dst_path, 'average_colors'), average_colors)

    def create_source_img_dir(self):
        self._create_source_images(self.src_path)

    def find_matching_img_for_average_color(self, target_color):
        src_colors = read_dict('{}/average_colors.json'.format(self.dst_path))
        min_delta = math.sqrt((255 ** 2) * 3)
        best_match = []

        for img_hash in src_colors:
            delta = math.sqrt(
                (target_color[0] - src_colors[img_hash][0]) ** 2 +
                (target_color[1] - src_colors[img_hash][1]) ** 2 +
                (target_color[2] - src_colors[img_hash][2]) ** 2)

            if delta < min_delta:
                min_delta = delta
                best_match = img_hash

        return best_match

    def get_src_img(self, img_hash):
        return cv2.imread('{}/{}.jpg'.format(self.dst_path, img_hash))


def find_image_paths(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))
                # print(os.path.join(r, file))
    return files


def save_dict(filename, data):
    old_data = read_dict('{}.json'.format(filename))
    data = data.update(old_data)
    with open('{}.json'.format(filename), 'a') as outfile:
        json.dump(data, outfile)


def read_dict(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def average_color(img):
    '''
    find the average color of the entire img
    :param img:
    :return: Tuple(r, g, b)
    '''
    counter = 0
    r = 0
    b = 0
    g = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            r += img[i,j,0]
            g += img[i,j,1]
            b += img[i,j,2]
            counter += 1
    return int(r/counter), int(g/counter), int(b/counter)


if __name__ == '__main__':
    sih = SourceImageHandler(r'/home/eshels/Downloads/london/', r'/home/eshels/Downloads/src_img')
    sih.create_source_img_dir()

