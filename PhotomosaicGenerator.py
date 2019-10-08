import numpy as np
import cv2
import math


class PhotoMosaicGenerator:
    def __init__(self, img, img_path=None, grid_res=50):
        self.img_path = img_path
        self.grid_res = grid_res
        self.img = img
        self.average_color_grid = []

    def divide_img_into_color_grid(self):
        '''
        This function takes the initial image and divides creates an average color grid used to construct the mosaic.
        :return: a 2D list containing all the average colors
        '''
        row_colors = []
        for j in range(0, self.img.shape[0], self.grid_res):
            col_colors = []
            for i in range(0, self.img.shape[1], self.grid_res):
                avg_color = average_color(self.img[i:i + self.grid_res, j:j + self.grid_res])
                col_colors.append(avg_color)
            row_colors.append(col_colors)

        self.average_color_grid = row_colors
        return row_colors

    def create_pixel_image(self, avg_color_grid=None):
        '''
        This function creates a pixellated version of the original.
        :param avg_color_grid: a 2D array of the average color grid
        :return:
        '''
        if avg_color_grid is None:
            avg_color_grid = self.average_color_grid
        rows = []
        for i in avg_color_grid:
            cols = []
            for j in i:
                blank = np.zeros((self.grid_res, self.grid_res, 3), np.uint8)
                blank[:] = j
                cols.append(blank)

            rows.append(np.vstack(cols))

        pixellated_img = np.hstack(rows)
        return pixellated_img

    def find_closest_src_for_color(self):
        pass

    def average_color_to_image(self, src_average_colors):
        row_matches = []
        for row in self.average_color_grid:
            col_matches = []
            for col in row:
                min_delta = math.sqrt((255**2)*3)
                best_match = []
                for img_hash in src_average_colors:
                    delta = math.sqrt(
                        (col[0] - src_average_colors[img_hash][0])**2 +
                        (col[1] - src_average_colors[img_hash][1])**2 +
                        (col[2] - src_average_colors[img_hash][2])**2)

                    if delta < min_delta:
                        min_delta = delta
                        best_match = img_hash
                col_matches.append(best_match)
            row_matches.append(col_matches)

        return row_matches

    def construct_mosaic(self, img_array):
        # img_array = self.average_color_to_image()
        rows = []
        for row in img_array:
            cols = []
            for col in row:
                src_img = cv2.imread('/home/eshels/Downloads/src_img/{}.jpg'.format(col))
                src_img = cv2.resize(src_img, (self.grid_res, self.grid_res))
                cols.append(src_img)
            rows.append(np.vstack(cols))
        img = np.hstack(rows)

        return img





def average_color(img):
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
