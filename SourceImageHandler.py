import os
import cv2


class SourceImageHandler:
    def __init__(self, src_path, dst_path):
        self.dst_path = dst_path
        self.src_path = src_path

    def find_image_paths(self, path):
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.jpg' in file:
                    files.append(os.path.join(r, file))
                    # print(os.path.join(r, file))

        return files

    def _create_source_images(self, path):
        for img_path in self.find_image_paths(path):
            source_img = cv2.imread(img_path)
            short_side = min(source_img.shape[:2])
            resized = cv2.resize(source_img, (short_side, short_side))
            cv2.imwrite(r'{}/{}'.format(self.dst_path, img_path[-10:]), resized)

    def create_sourse_img_dir(self):
        self._create_source_images(self.src_path)


if __name__ == '__main__':
    sih = SourceImageHandler(r'/home/eshels/Downloads/london/', r'/home/eshels/Downloads/src_img')

