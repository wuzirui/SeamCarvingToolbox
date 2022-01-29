import cv2


class Carver:
    def __init__(self, image_filename):
        self.image = cv2.imread(image_filename)

    def getImageWHShape(self):
        return self.image.shape[1], self.image.shape[0]
