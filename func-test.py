from seam_carving.carver import Carver
import cv2


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
    img_w, img_h = carver.getImageWHShape()
    assert img_w == example_width and img_h == example_height


def test_width_minus_1():
    pass
