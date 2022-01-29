import cv2
import logging
from seam_carving.carver import Carver


filename = './example/image1.jpg'
carver = Carver(filename)
logging.basicConfig(level=logging.DEBUG)
logging.debug(carver.getEnergyMap())
cv2.imshow('energy', carver.getEnergyMap())
cv2.imshow('blur', carver.image)
cv2.waitKey(10000)
