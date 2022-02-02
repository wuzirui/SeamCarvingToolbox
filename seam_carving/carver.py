import cv2
import numpy as np


class CarveImage:
    def __init__(self, image):
        self.image = image
        self.height, self.width, _ = image.shape
        self.energy_map = None

    def _calcEnergyMap(self):
        energy = np.zeros((self.height, self.width))
        for row in range(self.height):
            for col in range(self.width):
                dx = self.safe_get(row, col + 1) - self.safe_get(row, col - 1)
                dy = self.safe_get(row + 1, col) - self.safe_get(row - 1, col)
                energy[row, col] = np.sum(np.power(dx, 2)) + np.sum(np.power(dy, 2))
        self.energy_map = energy

    def get(self, row, col):
        return self.image[row, col]

    def format(self, row, col):
        row = max(row, 0)
        row = min(row, self.height - 1)
        col = max(col, 0)
        col = min(col, self.width - 1)
        return row, col

    def safe_get(self, row, col):
        row, col = self.format(row, col)
        return self.get(row, col)

    def set(self, row, col, val):
        ret = self.image.copy()
        ret[row, col] = val
        return CarveImage(ret)

    def isVerticalSeam(self, seam):
        return seam.shape[0] > 1

    def getHighlightedImage(self, seam):
        ret = self.image.copy()
        if self.isVerticalSeam(seam):
            for row, idx in enumerate(seam):
                ret[row, idx] = [0, 0, 255]
            return ret
        for col, idx in enumerate(seam):
            ret[idx, col] = [0, 0, 255]
        return ret

    def getRow(self, row):
        return self.image[row]

    def getCol(self, col):
        return self.image[:, col]

    def removeSeam(self, seam):
        if self.isVerticalSeam(seam):
            result = np.zeros((self.height, self.width - 1, 3))
            for row, idx in enumerate(seam):
                result[row, :, :] = np.delete(self.image[row, :, :], idx, axis=0)
        else:
            result = np.zeros((self.height - 1, self.width, 3))
            for col, idx in enumerate(seam[0]):
                result[:, col, :] = np.delete(self.image[:, col, :], idx, axis=0)
        return CarveImage(result)

    def getEnergyMap(self):
        if self.energy_map is None:
            self._calcEnergyMap()
        return self.energy_map

    def getEnergy(self, row, col):
        return self.getEnergyMap()[self.format(row, col)]

    def findVerticalSeam(self):
        energy = self.getEnergyMap()
        seam = np.zeros(self.height, 1)
        last_idx = np.argmin(energy[-1, :])
        seam[-1, 0] = last_idx
        for row in range(self.height - 2, -1, -1):
            new_idx = np.argmin(energy[row, last_idx - 1 : last_idx + 2]) + last_idx
            assert abs(new_idx - last_idx) <= 1
            seam[row, 0] = new_idx
            last_idx = new_idx


class Carver:
    blur_size = 5

    def __init__(self, image_filename):
        self.original = cv2.imread(image_filename)
        self.history = [self.original]
        blur_image = cv2.blur(self.image, [self.blur_size, self.blur_size])
        self.blur = CarveImage(blur_image)
        self.current = CarveImage(self.original)

    def widthShrink(self):
        pass
