# This code is taken from https://github.com/wkentaro/labelme
# and https://github.com/Jarvis-8035/PyPaint-Using-PyQt
# Modified by Raymond Wong

import random
from enum import Enum

from PyQt5.QtCore import QPoint, QPointF, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget


class cursorType(Enum):
    CURSOR_DEFAULT = Qt.ArrowCursor
    CURSOR_POINT = Qt.PointingHandCursor
    CURSOR_DRAW = Qt.CrossCursor


class CanvasMode(Enum):
    IDLE = 'idle'
    PEN = 'pen'
    ERASER = 'eraser'
    SPRAY = 'spray'
    FILL = 'fill'
    LINE = 'line'
    RECT = 'rect'
    ELLIPSE = 'ellipse'


class Canvas(QWidget):

    zoomRequest = pyqtSignal(int, QPoint)
    scrollRequest = pyqtSignal(int, int)

    SPRAY_PAINT_N = 50
    SPRAY_PAINT_MULT = 5

    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)

        self.pixmap = None
        self.pixmap_preview = None

        self._painter = QPainter()
        self._painter_config = {
            'color': QColor(0, 0, 0),
            'stroke_width': 1.
        }

        self.prev_pos = QPoint()
        self.eraser_color = QColor(Qt.white)

        self.painting_shape = False

        self.mode = CanvasMode.IDLE

        self.epsilon = 10.0
        self._scale = 1.0

    @property
    def painter_color(self):
        return self._painter_config['color']

    @painter_color.setter
    def painter_color(self, value):
        self._painter_config['color'] = value

    @property
    def stroke_width(self):
        return self._painter_config['stroke_width']

    @stroke_width.setter
    def stroke_width(self, value):
        self._painter_config['stroke_width'] = value

    def build_painter(self, eraser=False, dst=None):
        color = self.painter_color if not eraser else self.eraser_color
        painter = QPainter(self.pixmap) if not dst else QPainter(dst)
        pen = QPen(color, self.stroke_width)
        painter.setPen(pen)
        return painter

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if value < 0:
            return
        self._scale = value

    def loadPixmap(self, pixmap):
        self.pixmap = pixmap
        self.repaint()

    # These two, along with a call to adjustSize are required for the
    # scroll area.
    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        if self.pixmap:
            return self.scale * self.pixmap.size()
        return super(Canvas, self).minimumSizeHint()

    def wheelEvent(self, ev):
        mods = ev.modifiers()
        delta = ev.angleDelta()
        if Qt.ControlModifier == int(mods):
            # with Ctrl/Command key
            # zoom
            self.zoomRequest.emit(delta.y(), ev.pos())
        else:
            # scroll
            self.scrollRequest.emit(delta.x(), Qt.Horizontal)
            self.scrollRequest.emit(delta.y(), Qt.Vertical)
        ev.accept()

    def mousePressEvent(self, ev):
        if not self.pixmap:
            return

        func = getattr(self, f'{self.mode.value}_mousePressEvent', None)
        if func:
            func(ev)

    def mouseMoveEvent(self, ev):
        if not self.pixmap:
            return

        func = getattr(self, f'{self.mode.value}_mouseMoveEvent', None)
        if func:
            func(ev)

    def mouseReleaseEvent(self, ev):
        if not self.pixmap:
            return

        func = getattr(self, f'{self.mode.value}_mouseReleaseEvent', None)
        if func:
            func(ev)

    # Generic events (shared by brush-like tools)

    def generic_mousePressEvent(self, ev):
        self.prev_pos = self.transformPos(ev.localPos())

    def generic_mouseReleaseEvent(self, _):
        self.prev_pos = None

    # Mode-specific events.

    # Eraser events

    def eraser_mousePressEvent(self, ev):
        self.generic_mousePressEvent(ev)

    def eraser_mouseMoveEvent(self, ev):
        if self.prev_pos:
            pos = self.transformPos(ev.localPos())
            painter = self.build_painter(eraser=True)
            painter.drawLine(self.prev_pos, pos)

            self.prev_pos = pos
            self.update()

    def eraser_mouseReleaseEvent(self, ev):
        self.generic_mouseReleaseEvent(ev)

    # Pen events

    def pen_mousePressEvent(self, ev):
        self.generic_mousePressEvent(ev)

    def pen_mouseMoveEvent(self, ev):
        if self.prev_pos:
            pos = self.transformPos(ev.localPos())
            painter = self.build_painter(eraser=False)
            painter.drawLine(self.prev_pos, pos)

            self.prev_pos = pos
            self.update()

    def pen_mouseReleaseEvent(self, ev):
        self.generic_mouseReleaseEvent(ev)

    # Spray events

    def spray_mousePressEvent(self, ev):
        self.generic_mousePressEvent(ev)

    def spray_mouseMoveEvent(self, ev):
        if self.prev_pos:
            pos = self.transformPos(ev.localPos())
            painter = self.build_painter(eraser=False)

            for _ in range(self.SPRAY_PAINT_N):
                xo = random.gauss(0, self.stroke_width)
                yo = random.gauss(0, self.stroke_width)
                painter.drawPoint(pos.x() + xo, pos.y() + yo)

        self.update()

    def spray_mouseReleaseEvent(self, ev):
        self.generic_mouseReleaseEvent(ev)

    # Fill events

    def fill_mousePressEvent(self, ev):

        # Convert to image for pixel-by-pixel reading.
        image = self.pixmap.toImage()
        w, h = image.width(), image.height()
        s = image.bits().asstring(w * h * 4)

        pos = self.transformPos(ev.localPos())
        x, y = int(pos.x()), int(pos.y())  # Pixel location in image

        # Lookup the 3-byte value at our current location.
        i = (x + (y * w)) * 4
        target_color = s[i:i+3]

        # Convert bytestring to 1byte pp. true/false for matching colour. True values
        # will be 255, non-matching 0. Simplifies the lookup in get_pixel and
        # comparison in the main loop giving slight performance increase.
        s = b''.join(b'\xff' if s[n:n+3] == target_color else b'\x00' for n in range(0, len(s), 4))

        def get_pixel(x, y):
            i = (x + (y * w))
            return s[i]

        visited = set()
        to_fill = []
        queue = [(x, y)]

        def get_cardinal_points(have_seen, center_pos):
            points = []
            cx, cy = center_pos
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                xx, yy = cx + x, cy + y
                if (0 <= xx < w and 0 <= yy < h and (xx, yy) not in have_seen):
                    points.append((xx, yy))
                    have_seen.add((xx, yy))

            return points

        while queue:
            x, y = queue.pop()
            if get_pixel(x, y):  # 255 for a match (True) or 0 for a miss (False)
                to_fill.append((x, y))
                queue.extend(get_cardinal_points(visited, (x, y)))

        if to_fill:
            # Now we have the points, perform the fill.
            p = QPainter(self.pixmap)
            p.setPen(QPen(self.painter_color))
            p.drawPoints(*[QPoint(*xy) for xy in to_fill])
            self.update()

    # Generic shape events: Rectangle, Ellipse, Rounded-rect

    def generic_shape_mousePressEvent(self, ev):
        if not self.painting_shape:
            self.prev_pos = self.transformPos(ev.localPos())
            self.painting_shape = True
        else:
            self.painting_shape = False
            self.pixmap = self.pixmap_preview  # finish
            self.update()

    # Line events
    def line_mousePressEvent(self, ev):
        self.generic_shape_mousePressEvent(ev)

    def line_mouseMoveEvent(self, ev):
        preview = self.pixmap.copy()
        painter = self.build_painter(dst=preview)
        current_pos = self.transformPos(ev.localPos())
        painter.drawLine(self.prev_pos, current_pos)
        self.pixmap_preview = preview
        self.update()

    # Rect events
    def rect_mousePressEvent(self, ev):
        self.generic_shape_mousePressEvent(ev)

    def rect_mouseMoveEvent(self, ev):
        preview = self.pixmap.copy()
        painter = self.build_painter(dst=preview)
        current_pos = self.transformPos(ev.localPos())
        bounding_rect = QRectF(self.prev_pos, current_pos)
        painter.drawRect(bounding_rect)
        self.pixmap_preview = preview
        self.update()

    # Ellipse events
    def ellipse_mousePressEvent(self, ev):
        self.generic_shape_mousePressEvent(ev)

    def ellipse_mouseMoveEvent(self, ev):
        preview = self.pixmap.copy()
        painter = self.build_painter(dst=preview)
        current_pos = self.transformPos(ev.localPos())
        painter.drawEllipse(QRectF(self.prev_pos, current_pos))
        self.pixmap_preview = preview
        self.update()

    def paintEvent(self, event):
        if not self.pixmap:
            return super(Canvas, self).paintEvent(event)

        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        p.scale(self._scale, self._scale)
        p.translate(self.offsetToCenter())

        if self.painting_shape:
            p.drawPixmap(0, 0, self.pixmap_preview)
        else:
            p.drawPixmap(0, 0, self.pixmap)

        p.end()

    def transformPos(self, point):
        """Screen coordinate -> Image coordinate"""
        return point / self.scale - self.offsetToCenter()

    def offsetToCenter(self):
        s = self._scale
        area = super(Canvas, self).size()
        w, h = self.pixmap.width() * s, self.pixmap.height() * s
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QPointF(x, y)

    def resetState(self):
        self.pixmap = None
        self.update()