from seam_carving.carver import Carver
from seam_carving.carver import CarveImage
import numpy as np
import cv2
import logging
import random


filename = './example/image1.jpg'
example_width, example_height = 32, 32


def test_load_exmaple_image():
    bgr_image = cv2.imread(filename)
    img_h, img_w, _ = bgr_image.shape
    assert example_height == img_h and example_width == img_w


def test_carver_load():
    imdata = cv2.imread(filename)
    cimg = CarveImage(imdata)
    assert (cimg.height, cimg.width) == (example_height, example_width)


def test_get_image_row():
    imdata = cv2.imread(filename)
    cimg = CarveImage(imdata)
    assert cimg.getRow(0).shape == (example_width, 3)


def test_get_image_col():
    imdata = cv2.imread(filename)
    cimg = CarveImage(imdata)
    assert cimg.getCol(0).shape == (example_height, 3)


def test_image_remove_seam():
    imdata = cv2.imread(filename)
    cimg = CarveImage(imdata)
    seam = [[random.randint(0, example_width  - 1)] for i in range(example_height)]
    seam = np.array(seam)
    cimg = cimg.removeSeam(seam)
    assert cimg.width == example_width - 1 and cimg.height == example_height
    seam = [[random.randint(0, example_height - 1) for i in range(example_width - 1)]]
    cimg = cimg.removeSeam(np.array(seam))
    assert cimg.width == example_width - 1 and cimg.height == example_height - 1


def test_get_energy_map():
    imdata = cv2.imread(filename)
    cimg = CarveImage(imdata)
    energy = cimg.getEnergyMap()
    assert energy.shape == (example_height, example_width)


def test_width_shrink():
    pass
