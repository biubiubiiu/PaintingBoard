from enum import Enum
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QMainWindow

from .utils import action2canvasmode

from paintingboard.core import utils
from paintingboard.models import Actions, Zooming
from paintingboard.ui import Ui_MainWindow_Custom

EVENT_NEW_PAINTING = 'event_new_painting'
EVENT_LOAD_FILE = 'event_load_file'
EVENT_SAVE_FILE = 'event_save_file'
EVENT_CLEAR_CANVAS = 'event_clear_canvas'

EVENT_UNDO = 'event_undo'
EVENT_REDO = 'event_redo'

EVENT_COMMIT = 'event_commit'

EVENT_SWITCH_TO_ERASE = 'event_switch_to_erase'
EVENT_SWITCH_TO_FILL = 'event_switch_to_fill'
EVENT_SWITCH_TO_DEFAULT = 'event_switch_to_default'
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

EVENT_DERAIN = 'event_derain'
EVENT_SHADOW_REMOVAL = 'event_shadow_removal'

EVENT_SWITCH_FIT_WINDOW = 'event_switch_fit_window'
EVENT_SWITCH_FIT_WIDTH = 'event_switch_fit_width'
EVENT_SWITCH_MANUAL_ZOOM = 'event_switch_manual_zoom'


class MainWindow(QMainWindow, Ui_MainWindow_Custom):

    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.canvas.commitRequest.connect(self._commit)

        painting_mode_switch = {
            self.actionErase: EVENT_SWITCH_TO_ERASE,
            self.acitonFill: EVENT_SWITCH_TO_FILL,
            self.actiondefault: EVENT_SWITCH_TO_DEFAULT,
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
            self.actionDerain: EVENT_DERAIN,
            self.actionShadowRemoval: EVENT_SHADOW_REMOVAL
        }
        for signal, event in image_editing.items():
            signal.triggered.connect(partial(self._transform_image, event))

        workflow_control = {
            self.actionUndo: EVENT_UNDO,
            self.actionRedo: EVENT_REDO
        }
        for signal, event in workflow_control.items():
            signal.triggered.connect(partial(self._workflow_control, event))

        zooming_mode_switch = {
            self.actionFitWindow: EVENT_SWITCH_FIT_WINDOW,
            self.actionFitWidth: EVENT_SWITCH_FIT_WIDTH,
        }
        for signal, event in zooming_mode_switch.items():
            signal.triggered.connect(partial(self._switch_zoom_mode, event))

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

    def _workflow_control(self, name):
        self.notifyListener(name)

    def _transform_image(self, name):
        self.notifyListener(name)

    def _switch_zoom_mode(self, name):
        self.notifyListener(name)

    def _update_stroke_width(self, value):
        self.notifyListener(EVENT_UPDATE_STROKE_WIDTH, width=value)

    def _commit(self):
        self.notifyListener(EVENT_COMMIT)

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

    def switch_mode(self, action):
        self.canvas.mode = action2canvasmode[action]
        self.update_action_mode_hint(action)

    def update_action_mode_hint(self, action):
        # TODO: refactoring
        self.actionErase.setChecked(action == Actions.ACTION_ERASE)
        self.acitonFill.setChecked(action == Actions.ACTION_FILL)
        self.actiondefault.setChecked(action == Actions.ACTION_DEFAULT)
        self.actionPen.setChecked(action == Actions.ACTION_PEN)
        self.actionspray.setChecked(action == Actions.ACTION_SPRAY)
        self.actionLine.setChecked(action == Actions.ACTION_LINE)
        self.actionRectangle.setChecked(action == Actions.ACTION_RECT)
        self.actionEllipse.setChecked(action == Actions.ACTION_ELLIPSE)

    def show_painter_color(self, color):
        if color is int:
            color = QColor(color)
        palette = self.colorPicker.palette()
        palette.setColor(self.colorPicker.backgroundRole(), color)
        self.colorPicker.setPalette(palette)

    def show_status(self, message):
        self.statusbar.showMessage(message)

    def computeScale(self, image, zoomMode):
        if zoomMode == Zooming.FIT_WINDOW:
            e = 2.0
            w1 = self.centralWidget().width() - e
            h1 = self.centralWidget().height() - e
            a1 = w1 / h1

            w2 = image.width()
            h2 = image.height()
            a2 = w2 / h2
            return w1 / w2 if a2 >= a1 else h1 / h2
        elif zoomMode == Zooming.FIT_WIDTH:
            w = self.centralWidget().width() - 2.0
            return w / image.width()
        elif zoomMode == Zooming.MANUAL_ZOOM:
            return self.canvas.scale

    def handle_zoom_request(self, delta, pos):
        canvas_width_old = self.canvas.width()

        self._zoom(isZoomIn=True if delta > 0 else False)

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

    def _zoom(self, isZoomIn):
        self._switch_zoom_mode(EVENT_SWITCH_MANUAL_ZOOM)
        self.canvas.scale += 0.1 * (1 if isZoomIn else -1)
        self.canvas.updateGeometry()
        self.canvas.adjustSize()
        self.canvas.repaint()

    def change_zoom_mode(self, mode):
        self.updateZoomBtn(mode)
        if self.canvas.pixmap:
            self.adjustScale(mode)
            self.canvas.repaint()

    def updateZoomBtn(self, mode):
        self.actionFitWidth.setChecked(mode == Zooming.FIT_WIDTH)
        self.actionFitWindow.setChecked(mode == Zooming.FIT_WINDOW)

    def adjustScale(self, mode):
        value = self.computeScale(self.canvas.pixmap, mode)
        self.canvas.scale = value

    def paintCanvas(self):
        self.canvas.scale = 0.01 * self.spinbox_scale.value()
        self.canvas.repaint()

    def dragEnterEvent(self, event):
        self.handle_drag_drop_event(event, 'enter')

    def dragMoveEvent(self, event):
        self.handle_drag_drop_event(event, 'move')

    def dropEvent(self, event):
        self.handle_drag_drop_event(event, 'drop')
