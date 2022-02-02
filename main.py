import cv2
import numpy as np
from seam_carving.carver import Carver


filename = './example/image2.jpg'
carver = Carver(filename)
cv2.namedWindow('seam image')
cv2.startWindowThread()
while True:
    image = carver.showSeamedImage()
    image = image.astype(np.uint8)
    carver.widthShrink()
    cv2.imshow('seam image', image)
    cv2.waitKey(1)
    input('Press Enter to continue')
cv2.destroyAllWindows()
print("done")
