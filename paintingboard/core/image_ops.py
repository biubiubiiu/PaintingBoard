import cv2
import numpy as np
import requests
from PyQt5.QtGui import QImage, QPixmap, QTransform

from . import utils


def invert_color(pixmap):
    image = QImage(pixmap)
    image.invertPixels()
    return QPixmap.fromImage(image)


def horizontal_flip(pixmap):
    ret = pixmap.transformed(QTransform().scale(-1, 1))
    return ret


def vertical_flip(pixmap):
    ret = pixmap.transformed(QTransform().scale(1, -1))
    return ret


def equalize_hist(pixmap):
    img = utils.qpixmap2Numpy(pixmap)
    n_channel = img.shape[-1]
    if n_channel > 1:
        # convert from RGB color-space to YCrCb
        ycrcb_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

        # equalize the histogram of the Y channel
        ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])

        # convert back to RGB color-space from YCrCb
        ret = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)
    else:
        ret = cv2.equalizeHist(img)
    ret = utils.numpy2QPixmap(ret)
    return ret


def to_grayscale(pixmap):
    image = QImage(pixmap)
    grayscale = image.convertToFormat(QImage.Format_Grayscale8)
    return QPixmap.fromImage(grayscale)


def average_blur(pixmap, kernel_size=5):
    img = utils.qpixmap2Numpy(pixmap)
    kernel = np.ones((kernel_size, kernel_size), np.float32) / kernel_size**2
    ret = cv2.filter2D(img, -1, kernel)
    ret = utils.numpy2QPixmap(ret)
    return ret


def median_blur(pixmap, kernel_size=5):
    img = utils.qpixmap2Numpy(pixmap)
    ret = cv2.medianBlur(img, kernel_size)
    ret = utils.numpy2QPixmap(ret)
    return ret


def gaussian_blur(pixmap, kernel_size=5):
    img = utils.qpixmap2Numpy(pixmap)
    ret = cv2.GaussianBlur(img, (kernel_size, kernel_size), cv2.BORDER_DEFAULT)
    ret = utils.numpy2QPixmap(ret)
    return ret


def usm_sharpen(pixmap, kernel_size=5):
    img = utils.qpixmap2Numpy(pixmap)
    blur_img = cv2.GaussianBlur(img, (0, 0), kernel_size)
    usm = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)
    ret = utils.numpy2QPixmap(usm)
    return ret


def sepia(pixmap):
    """
    Taken from: https://gist.github.com/FilipeChagasDev/bb63f46278ecb4ffe5429a84926ff812
    """
    img = utils.qpixmap2Numpy(pixmap)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32)/255
    # solid color
    ret = np.ones(img.shape)
    ret[:, :, 0] *= 153  # B
    ret[:, :, 1] *= 204  # G
    ret[:, :, 2] *= 255  # R
    # hadamard
    ret[:, :, 0] *= normalized_gray  # B
    ret[:, :, 1] *= normalized_gray  # G
    ret[:, :, 2] *= normalized_gray  # R
    ret = np.array(ret, np.uint8)
    ret = utils.numpy2QPixmap(ret)
    return ret


def pixelize(pixmap, pixelated_factor=4):
    img = utils.qpixmap2Numpy(pixmap)
    height, width = img.shape[:2]
    short = min(height, width)
    pixelated_size = (short//pixelated_factor, short//pixelated_factor)

    # Resize input to "pixelated" size
    temp = cv2.resize(img, pixelated_size, fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)

    # Initialize output image
    ret = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    ret = utils.numpy2QPixmap(ret)
    return ret


def derain(pixmap):
    # TODO: move to view model, call from coroutine

    url = 'http://localhost:5000/derain'
    resp = requests.post(url, files={"file": utils.qpixmap2Bytes(pixmap)})
    if resp.status_code == 200:
        ret = utils.bytes2QPixmap(resp.content)
    else:
        ret = None
    return ret


def remove_shadow(pixmap):
    # TODO: move to view model, call from coroutine

    url = 'http://localhost:5000/shadow'
    resp = requests.post(url, files={"file": utils.qpixmap2Bytes(pixmap)})
    if resp.status_code == 200:
        ret = utils.bytes2QPixmap(resp.content)
    else:
        ret = None
    return ret
