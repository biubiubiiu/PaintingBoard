import io
import math
import os

import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice
from PyQt5.QtGui import QImage, QImageReader, QPixmap


def getSupportedImageFormats(path):
    path = os.path.dirname(path)
    formats = [f'*.{fmt.data().decode()}' for fmt in QImageReader.supportedImageFormats()]
    return formats


def readImage(filename):
    reader = QImageReader(filename)
    reader.setAutoTransform(True)  # TODO: dont know what this is doing
    return reader.read()


def length(p):
    return math.sqrt(p.x() * p.x() + p.y() * p.y())


def qpixmap2Numpy(pixmap):
    image = QImage(pixmap)
    tmp_shape = (image.height(), image.bytesPerLine()*8//image.depth())
    tmp_shape += (4,)
    ptr = image.bits()
    ptr.setsize(image.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(tmp_shape)
    result = result[..., :3]
    return result


def numpy2QPixmap(array):
    height, width, depth = array.shape
    image = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    image = QImage(image.data, width, height, width*depth, QImage.Format_RGB888)
    return QPixmap.fromImage(image)


def qpixmap2Bytes(pixmap):
    ba = QByteArray()
    buff = QBuffer(ba)
    buff.open(QIODevice.WriteOnly) 
    ok = pixmap.save(buff, "PNG")
    assert ok
    pixmap_bytes = ba.data()
    return pixmap_bytes


def bytes2QPixmap(bytes):
    image = Image.open(io.BytesIO(bytes))
    arr = np.array(image)
    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    pixmap = numpy2QPixmap(arr)
    return pixmap
