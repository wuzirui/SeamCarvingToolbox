import cv2
import numpy as np


class Carver:
    blur_size = 5

    def __init__(self, image_filename):
        self.image = cv2.imread(image_filename)
        self.blur_image = cv2.blur(self.image, [self.blur_size, self.blur_size])
        self.x_energy, self.y_energy = self._calcImageEnergyMap()

    def getImageShape(self):
        return self.image.shape[0], self.image.shape[1]

    def getImageRow(self, row_number):
        return self.image[row_number]

    def getEnergyMap(self):
        return self.x_energy + self.y_energy

    def _calcImageEnergyMap(self):
        energy_x = np.absolute(cv2.Scharr(self.blur_image, -1, 1, 0))
        energy_y = np.absolute(cv2.Scharr(self.blur_image, -1, 0, 1))
        return np.sum(energy_x, axis=2), np.sum(energy_y, axis=2)

    def _updateImageEnergyMap(self):
        pass

    def _findVerticalSeam(self):
        return np.ones(self.image.shape[0])

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
        self._updateImageEnergyMap()
