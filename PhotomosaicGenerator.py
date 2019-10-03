import numpy as np
import cv2


def divide_img(img, grid_res=50):
    print(img.shape)
    row_colors = []
    for j in range(0, img.shape[0], grid_res):
        col_colors = []
        for i in range(0, img.shape[1], grid_res):
            avg_color = average_color(img[i:i + grid_res, j:j + grid_res])
            col_colors.append(avg_color)
        row_colors.append(col_colors)

    print(row_colors)
    return row_colors


# matrix of tuples
def create_pixel_image(mat):
    rows = []
    for i in mat:
        cols = []
        for j in i:
            blank = np.zeros((50, 50, 3), np.uint8)
            blank[:] = j
            cols.append(blank)
        rows.append(cols)

    pixellated_img = np.hstack(np.vstack(rows))
    return pixellated_img


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
