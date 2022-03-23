from enum import Enum
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QMainWindow

from paintingboard.core import utils
from paintingboard.models import Actions
from paintingboard.ui import CanvasMode, Ui_MainWindow_Custom

EVENT_NEW_PAINTING = 'event_new_painting'
EVENT_LOAD_FILE = 'event_load_file'
EVENT_SAVE_FILE = 'event_save_file'
EVENT_CLEAR_CANVAS = 'event_clear_canvas'

EVENT_SWITCH_TO_ERASE = 'event_switch_to_erase'
EVENT_SWITCH_TO_FILL = 'event_switch_to_fill'
EVENT_SWITCH_TO_DEFALT = 'event_switch_to_default'
EVENT_SWITCH_TO_PEN = 'event_switch_to_pen'
EVENT_SWITCH_TO_SPRAY = 'event_switch_to_spray'
EVENT_SWITCH_TO_LINE = 'event_switch_to_line'
EVENT_SWITCH_TO_RECT = 'event_switch_to_rect'
EVENT_SWITCH_TO_ELLIPSE = 'event_switch_to_ellipse'

EVENT_UPDATE_STROKE_WIDTH = 'event_update_stroke_width'
EVENT_UPDATE_STROKE_COLOR = 'event_update_stroke_color'

EVENT_INVERT_COLOR = 'event_invert_color'
EVENT_HORIZONTAL_FLIP = 'event_horizontal_flip'
EVENT_VERTICAL_FLIP = 'event_vertical_flip'
EVENT_EQUALIZE_HIST = 'event_equalize_hist'
EVENT_TO_GRAYSCALE = 'event_to_grayscale'
EVENT_BLUR = 'event_blur'
EVENT_MEDIAN_BLUR = 'event_median_blur'
EVENT_GAUSSIAN_BLUR = 'event_gaussian_blur'
EVENT_SEPIA = 'event_sepia'
EVENT_SHARPEN = 'event_sharpen'
EVENT_PIXELIZE = 'event_pixelize'


class Zooming(Enum):
    FIT_WINDOW = 0
    FIT_WIDTH = 1
    MANUAL_ZOOM = 2


class MainWindow(QMainWindow, Ui_MainWindow_Custom):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.zoomMode = Zooming.FIT_WINDOW

        self.setAcceptDrops(True)  # TODO: set this property in mainwindow.ui

        self.setupUi(self)
        self.initListeners()
        self.establishConnections()

    @property
    def actions(self):
        return {k: v for k, v in self.__dict__.items() if k.startswith('action')}

    def establishConnections(self):
        self.actionNew.triggered.connect(self._new_painting)
        self.actionOpen.triggered.connect(self._open_file)
        self.actionSave.triggered.connect(self._saveFile)
        self.actionQuit.triggered.connect(self.close)
        self.actionClose.triggered.connect(self._clearCanvas)

        self.canvas.scrollRequest.connect(self.handle_scroll_request)
        self.canvas.zoomRequest.connect(self.handle_zoom_request)

        painting_mode_switch = {
            self.actionErase: EVENT_SWITCH_TO_ERASE,
            self.acitonFill: EVENT_SWITCH_TO_FILL,
            self.actiondefault: EVENT_SWITCH_TO_DEFALT,
            self.actionPen: EVENT_SWITCH_TO_PEN,
            self.actionspray: EVENT_SWITCH_TO_SPRAY,
            self.actionLine: EVENT_SWITCH_TO_LINE,
            self.actionRectangle: EVENT_SWITCH_TO_RECT,
            self.actionEllipse: EVENT_SWITCH_TO_ELLIPSE
        }
        for signal, event in painting_mode_switch.items():
            signal.triggered.connect(partial(self._switch_painting_mode, event))

        image_editing = {
            self.actionHorizontal_Flip: EVENT_HORIZONTAL_FLIP,
            self.actionVertical_Flip: EVENT_VERTICAL_FLIP,
            self.actionInvert_Color: EVENT_INVERT_COLOR,
            self.actionEqualize_Hist: EVENT_EQUALIZE_HIST,
            self.actionGrayscale: EVENT_TO_GRAYSCALE,
            self.actionBlur: EVENT_BLUR,
            self.actionMedian_Blur: EVENT_MEDIAN_BLUR,
            self.actionGaussian_Blur: EVENT_GAUSSIAN_BLUR,
            self.actionSepia: EVENT_SEPIA,
            self.actionSharpen: EVENT_SHARPEN,
            self.actionPixelize: EVENT_PIXELIZE,
        }
        for signal, event in image_editing.items():
            signal.triggered.connect(partial(self._transform_image, event))

        zooming_mode_switch = {
            self.actionFitWindow: Zooming.FIT_WINDOW,
            self.actionFitWidth: Zooming.FIT_WIDTH
        }
        for signal, mode in zooming_mode_switch.items():
            signal.triggered.connect(partial(self.change_zoom_mode, mode))

        self.sizeselect.valueChanged.connect(self._update_stroke_width)
        self.colorPicker.clicked.connect(self._pick_color)

    def initListeners(self):
        self.listeners = dict()

    def registerListener(self, name, func):
        listeners = self.listeners.get(name, [])
        listeners.append(func)
        self.listeners[name] = listeners

    def notifyListener(self, name, **kwargs):
        for func in self.listeners.get(name, []):
            func(**kwargs)

    def _new_painting(self):
        self.notifyListener(EVENT_NEW_PAINTING)

    def _open_file(self):
        path = '.'
        supportedFmts = utils.getSupportedImageFormats(path)
        filters = f'Image files ({" ".join(supportedFmts)})'
        filename, _ = QFileDialog.getOpenFileName(self, 'Choose Image', path, filters)
        if filename:
            if isinstance(filename, (tuple, list)):
                filename = filename[0]
            self._load_file(filename)

    def _load_file(self, filename):
        self.notifyListener(EVENT_LOAD_FILE, fname=filename)

    def _saveFile(self):
        path = '.'
        supportedFmts = utils.getSupportedImageFormats(path)
        filters = f'Image files ({" ".join(supportedFmts)})'
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save file', path, filters)
        if save_path:
            pixmap = self.canvas.pixmap
            pixmap.save(save_path, 'png')
            self.notifyListener(EVENT_SAVE_FILE, save_path=save_path)

    def _clearCanvas(self):
        self.notifyListener(EVENT_CLEAR_CANVAS)

    def _switch_painting_mode(self, name):
        self.notifyListener(name, event_name=name)

    def _transform_image(self, name):
        self.notifyListener(name)

    def _update_stroke_width(self, value):
        self.notifyListener(EVENT_UPDATE_STROKE_WIDTH, width=value)

    def _pick_color(self):
        dlg = QColorDialog()
        if dlg.exec():
            self.notifyListener(EVENT_UPDATE_STROKE_COLOR, color=dlg.selectedColor())

    def display(self, pixmap):
        if pixmap is None:
            self.canvas.resetState()
        else:
            self.canvas.loadPixmap(pixmap)

    def setup_painter(self, state):
        self.canvas.painter_color = state.strokeColor
        self.canvas.stroke_width = state.strokeWidth

    def switch_mode(self, state):
        action2canvasmode = {
            Actions.ACTION_DEFALT: CanvasMode.IDLE,
            Actions.ACTION_ERASE: CanvasMode.ERASER,
            Actions.ACTION_FILL: CanvasMode.FILL,
            Actions.ACTION_PEN: CanvasMode.PEN,
            Actions.ACTION_SPRAY: CanvasMode.SPRAY,
            Actions.ACTION_LINE: CanvasMode.LINE,
            Actions.ACTION_RECT: CanvasMode.RECT,
            Actions.ACTION_ELLIPSE: CanvasMode.ELLIPSE
        }
        self.canvas.mode = action2canvasmode[state.action]

    def show_painter_color(self, color):
        if color is int:
            color = QColor(color)
        palette = self.colorPicker.palette()
        palette.setColor(self.colorPicker.backgroundRole(), color)
        self.colorPicker.setPalette(palette)

    def show_status(self, message):
        self.statusbar.showMessage(message)

    def computeScale(self, image):
        if self.zoomMode == Zooming.FIT_WINDOW:
            e = 2.0
            w1 = self.centralWidget().width() - e
            h1 = self.centralWidget().height() - e
            a1 = w1 / h1

            w2 = image.width()
            h2 = image.height()
            a2 = w2 / h2
            return w1 / w2 if a2 >= a1 else h1 / h2
        elif self.zoomMode == Zooming.FIT_WIDTH:
            w = self.centralWidget().width() - 2.0
            return w / image.width()
        elif self.zoomMode == Zooming.MANUAL_ZOOM:
            return 1.0

    def handle_zoom_request(self, delta, pos):
        canvas_width_old = self.canvas.width()

        self.zoom(True if delta > 0 else False)

        canvas_width_new = self.canvas.width()
        if canvas_width_old != canvas_width_new:
            canvas_scale_factor = canvas_width_new / canvas_width_old

            x_shift = round(pos.x() * canvas_scale_factor) - pos.x()
            y_shift = round(pos.y() * canvas_scale_factor) - pos.y()

            hScrollBar = self.scrollArea.horizontalScrollBar()
            vScrollBar = self.scrollArea.verticalScrollBar()

            hScrollBar.setValue(hScrollBar.value() + x_shift)
            vScrollBar.setValue(vScrollBar.value() + y_shift)

    def handle_scroll_request(self, delta, orientation):
        units = - delta * 0.1
        scrollBar = self.scrollArea.verticalScrollBar() \
            if orientation == Qt.Vertical \
            else self.scrollArea.horizontalScrollBar()
        scrollBar.setValue(scrollBar.value() + scrollBar.singleStep() * units)

    def handle_drag_drop_event(self, event, type):
        if not event.mimeData().hasImage:
            event.ignore()
            return
        
        if type == 'drop':
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self._load_file(file_path)

        event.accept()

    def zoom(self, isZoomIn=True):
        self.canvas.scale += 0.1 * (1 if isZoomIn else -1)
        self.zoomMode = Zooming.MANUAL_ZOOM
        self.canvas.updateGeometry()
        self.canvas.adjustSize()
        self.canvas.repaint()

    def adjustScale(self):
        value = self.computeScale(self.canvas.pixmap)
        self.canvas.scale = value

    def paintCanvas(self):
        self.canvas.scale = 0.01 * self.spinbox_scale.value()
        self.canvas.repaint()

    def change_zoom_mode(self, mode):
        if not isinstance(mode, Zooming) or mode == self.zoomMode:
            return
        self.zoomMode = mode
        self.updateZoomBtn()
        self.adjustScale()
        self.canvas.repaint()

    def updateZoomBtn(self):
        actions = (self.actionFitWidth, self.actionFitWindow)
        modes = (Zooming.FIT_WIDTH, Zooming.FIT_WINDOW)
        for action, mode in zip(actions, modes):
            action.setChecked(True if mode == self.zoomMode else False)

    def dragEnterEvent(self, event):
        self.handle_drag_drop_event(event, 'enter')

    def dragMoveEvent(self, event):
        self.handle_drag_drop_event(event, 'move')

    def dropEvent(self, event):
        self.handle_drag_drop_event(event, 'drop')
