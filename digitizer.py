import cv2.cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
from copy import deepcopy


class Digitizer:
    def __init__(self):
        self.image = None
        self.image_height = None
        self.image_width = None
        self.image_size = None

    def load(self, image):
        """ Load the image to the digitizer as 2D array

        Args:
            image: 2D array

        """

        self.image = image
        self.image_height = len(image)
        self.image_width = len(image[0])
        self.image_size = self.image_width, self.image_height

    def load_by_path(self, image_path):
        """ Load the image to the digitizer by image path

        Args:
            image_path (str): image file path

        """

        image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

        self.image = image
        self.image_height = len(image)
        self.image_width = len(image[0])
        self.image_size = self.image_width, self.image_height

    def bw_filter(self):
        """ Black and white filter """

        means = []
        for x in range(len(self.image[0])):
            means.append(np.mean(self.image[:, x - 5: x + 5]))

        # min_mean = min(np.nan_to_num(means, nan=256))
        means = np.nan_to_num(means, nan=0)

        image = deepcopy(self.image)
        for row in image:
            for pixel_index in range(len(row)):
                # row[pixel_index] = 255 if row[pixel_index] < 45 - min_mean + means[pixel_index] else 0
                row[pixel_index] = 255 if row[pixel_index] < means[pixel_index] - 95 else 0
        return image

    @staticmethod
    def dilate(image):
        """ Dilate with 3x3 kernel

        Args:
            image: 2D array

        """

        kernel = np.ones((3, 3), np.uint8)
        image = cv.dilate(deepcopy(image), kernel, iterations=1)
        return image

    def find_curve(self, grid_size, show=False):
        """ Find curve on image

        Args:
            grid_size: grid size in px on input image |Not implemented|
            show (bool): Shows a digitised curve if true

        """

        curve_image = self.bw_filter()
        self.dilate(curve_image)
        contours, hierarchy = cv.findContours(curve_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # grid_image = self.grid_filter()
        # grid = Digitizer().size_the_grid(self.image) / 10
        grid = grid_size / 10

        if not contours:
            return [[], [], 10]

        curves = []

        for contour in contours:
            points = []
            for point in contour:
                x, y = point[0]
                points.append((x, y))

            points.sort(key=lambda a: a[0])
            curve = []
            while points:
                x = points[0][0]
                by_x = [point for point in points if point[0] == x]
                mean_y = round(np.mean([point[1] for point in by_x]))
                curve.append((x, mean_y))
                points = [point for point in points if point[0] != x]
            curves.append(curve)

        curves.sort(key=lambda arr: len(arr), reverse=True)
        min_length = len(curves[0]) * 2 / 110
        curve = [point for curve in curves for point in curve if len(curve) >= min_length]
        curve.sort(key=lambda a: a[0])
        x_exists = []
        for point in deepcopy(curve):
            if point[0] in x_exists:
                curve.remove(point)
            else:
                x_exists.append(point[0])

        x = [point[0] / grid for point in curve]
        y = [point[1] / grid for point in curve]
        max_y = max(y)
        y = [max_y - value for value in y]

        if show:
            plt.plot(x, y)
            plt.axis(False)
            # x_ticks = np.arange(0, max(x), 10)
            # y_ticks = np.arange(0, max(y), 10)
            # plt.xlim(0, max(x))
            # plt.xticks(x_ticks)
            # plt.yticks(y_ticks)
            # plt.grid(which='both')
            plt.show()

        return [x, y, 10]

    def crop(self, x, y, w, h):
        """ Returns a cropped copy of self.image. The self.image remains unchanged """
        return deepcopy(self.image)[self.image_height-y-h:self.image_height-y, x:x+w]

    # @staticmethod
    # def size_the_grid(image):
    #     lens = []
    #     for row in image:
    #         sizes = []
    #         size = 0
    #         for pixel in row:
    #             if pixel == 255 and size != 0:
    #                 sizes.append(size)
    #                 size = 0
    #             else:
    #                 size += 1
    #         lens.append(len(sizes))
    #     print(len(image[0]) / np.median(lens))
    #     return 9

    # def grid_filter(self):
    #     means = []
    #     for x in range(len(self.image[0])):
    #         means.append(np.mean(self.image[:, x - 5: x + 5]))
    #     means = np.nan_to_num(means, nan=0)
    #
    #     image = deepcopy(self.image)
    #     for row in image:
    #         for pixel_index in range(len(row)):
    #             row[pixel_index] = 255 if means[pixel_index] - 80 < row[pixel_index] < means[pixel_index] - 10 else 0
    #
    #     cv.imshow('gg', image)
    #     cv.waitKey(0)
    #     return image
