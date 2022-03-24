from PyQt5.QtGui import QPixmap
from rx.subject import BehaviorSubject

from paintingboard.core import utils
from paintingboard.models import ActionMode, Actions, PainterState, ZoomingState


class ViewModel(object):

    def __init__(self) -> None:

        # states
        self.canvasNotEmpty = BehaviorSubject(False)
        self.currentFilename = BehaviorSubject(None)

        self.painter = BehaviorSubject(PainterState())
        self.mode = BehaviorSubject(ActionMode())
        self.zooming = BehaviorSubject(ZoomingState())

    def new_painting(self, width=600, height=600):
        self.clear_canvas()
        self.canvasNotEmpty.on_next(True)
        return QPixmap(width, height)

    def load_file(self, fname):
        if fname is None:
            return None

        image = utils.readImage(fname)
        if image.isNull():
            self.currentFilename.on_error(ValueError(f'Fail to open {fname}'))
            return None
        else:
            self.currentFilename.on_next(fname)
            self.canvasNotEmpty.on_next(True)
            return QPixmap.fromImage(image)

    def clear_canvas(self):
        self.canvasNotEmpty.on_next(False)
        self.currentFilename.on_next(None)
        self.switch_mode('default')

    def switch_mode(self, action):
        str2Action = {
            'default': Actions.ACTION_DEFAULT,
            'pen': Actions.ACTION_PEN,
            'spray': Actions.ACTION_SPRAY,
            'erase': Actions.ACTION_ERASE,
            'fill': Actions.ACTION_FILL,
            'line': Actions.ACTION_LINE,
            'rect': Actions.ACTION_RECT,
            'ellipse': Actions.ACTION_ELLIPSE
        }
        next_action = str2Action[action]
        current_state = self.mode.value
        next_state = current_state.copy(action=next_action)
        self.mode.on_next(next_state)

    def switch_zooming_mode(self, mode):
        current_state = self.zooming.value
        next_state = current_state.copy(mode=mode)
        self.zooming.on_next(next_state)

    def update_stroke_color(self, color):
        current_painter = self.painter.value
        new_painter = current_painter.copy(strokeColor=color)
        self.painter.on_next(new_painter)

    def update_stroke_width(self, width):
        current_painter = self.painter.value
        new_painter = current_painter.copy(strokeWidth=width)
        self.painter.on_next(new_painter)
