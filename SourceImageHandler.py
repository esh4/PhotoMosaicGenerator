import os
import cv2
import json
from PhotomosaicGenerator import average_color


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

    def find_matching_img_for_average_color(self, average_color):
        pass


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


if __name__ == '__main__':
    sih = SourceImageHandler(r'/home/eshels/Downloads/london/', r'/home/eshels/Downloads/src_img')
    sih.create_source_img_dir()

