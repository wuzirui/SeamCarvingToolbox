from seam_carving.carver import Carver
import cv2
import logging


filename = './example/image1.jpg'
example_width, example_height = 959, 960


# smoke test
def test_carver_smoke():
    assert Carver is not None


def test_load_exmaple_image():
    w, h = 959, 960
    bgr_image = cv2.imread(filename)
    img_h, img_w, _ = bgr_image.shape
    assert h == img_h and w == img_w


def test_carver_load():
    carver = Carver(filename)
    img_h, img_w = carver.getImageShape()
    assert img_w == example_width and img_h == example_height


def test_get_image_row():
    carver = Carver(filename)
    assert carver.getImageRow(0).shape == (959, 3)


def test_get_energy_map():
    carver = Carver(filename)
    emap = carver.getEnergyMap()
    assert emap.shape == (960, 959)
    logging.info(emap)


def test_width_shrink():
    carver = Carver(filename)
    carver.widthShrink()
    img_h, img_w = carver.getImageShape()
    assert img_w == example_width - 1 and img_h == example_height
