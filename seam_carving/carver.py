import cv2
import numpy as np


class Carver:
    blur_size = 5

    def __init__(self, image_filename):
        self.image = cv2.imread(image_filename)
        self.blur_image = cv2.blur(self.image, [self.blur_size, self.blur_size])
        self.energy = self._calcImageEnergyMap()

    def getImageShape(self):
        return self.image.shape[0], self.image.shape[1]

    def getImageRow(self, row_number):
        return self.image[row_number]

    def getEnergyMap(self):
        return self.energy

    def _calcImageEnergyMap(self):
        b, g, r = cv2.split(self.blur_image)
        b_energy = np.absolute(cv2.Scharr(b, -1, 1, 0)) + np.absolute(cv2.Scharr(b, -1, 0, 1))
        g_energy = np.absolute(cv2.Scharr(g, -1, 1, 0)) + np.absolute(cv2.Scharr(g, -1, 0, 1))
        r_energy = np.absolute(cv2.Scharr(r, -1, 1, 0)) + np.absolute(cv2.Scharr(r, -1, 0, 1))
        return b_energy + g_energy + r_energy

    def _updateImageEnergyMap(self):
        pass

    def _findVerticalSeam(self):
        return np.zeros(self.image.shape[0])

    def widthShrink(self):
        seamIndicies = self._findVerticalSeam()
        output = np.zeros((self.image.shape[0], self.image.shape[1] - 1, 3))
        blur = np.zeros((self.image.shape[0], self.image.shape[1] - 1, 3))
        for i, index in enumerate(seamIndicies):
            index = int(index)
            output[i, :, 0] = np.delete(self.image[i, :, 0], [index])
            output[i, :, 1] = np.delete(self.image[i, :, 1], [index])
            output[i, :, 2] = np.delete(self.image[i, :, 2], [index])
            blur[i, :, 0] = np.delete(self.blur_image[i, :, 0], [index])
            blur[i, :, 1] = np.delete(self.blur_image[i, :, 1], [index])
            blur[i, :, 2] = np.delete(self.blur_image[i, :, 2], [index])
        self.image = output
        self.blur_image = blur
