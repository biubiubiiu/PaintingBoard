from paintingboard.core import image_ops, utils
from paintingboard.models import (ActionMode, Actions, PainterState,
                                  ZoomingState)
from PyQt5.QtGui import QPixmap
from rx.subject import BehaviorSubject


class ViewModel(object):

    max_queue_size: int = 10

    def __init__(self) -> None:

        # states
        self.currentFilename = BehaviorSubject(None)

        self.img_queue = []
        self.img_queue_idx = -1

        self.current_img = BehaviorSubject(None)

        self.painter = BehaviorSubject(PainterState())
        self.mode = BehaviorSubject(ActionMode())
        self.zooming = BehaviorSubject(ZoomingState())

    def new_painting(self, width=600, height=600):
        self.clear_canvas()
        self._enqueue_img(QPixmap(width, height))

    def load_file(self, fname):
        if fname is None:
            self.currentFilename.on_error(ValueError('Filename is None'))
            return

        image = utils.readImage(fname)
        if image.isNull():
            self.currentFilename.on_error(ValueError(f'Fail to open {fname}'))
            return

        pixmap = QPixmap.fromImage(image)
        self._enqueue_img(pixmap)
        self.currentFilename.on_next(fname)

    def clear_canvas(self):
        self._clear_img_queue()
        self.currentFilename.on_next(None)
        self.switch_mode('default')

    def switch_mode(self, action):
        next_action = {
            'default': Actions.ACTION_DEFAULT,
            'pen': Actions.ACTION_PEN,
            'spray': Actions.ACTION_SPRAY,
            'erase': Actions.ACTION_ERASE,
            'fill': Actions.ACTION_FILL,
            'line': Actions.ACTION_LINE,
            'rect': Actions.ACTION_RECT,
            'ellipse': Actions.ACTION_ELLIPSE
        }[action]
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

    def transform(self, trans):
        func = {
            'invert_color': image_ops.invert_color,
            'horizontal_flip': image_ops.horizontal_flip,
            'vertical_flip': image_ops.vertical_flip,
            'equalize_hist': image_ops.equalize_hist,
            'to_grayscale': image_ops.to_grayscale,
            'blur': image_ops.average_blur,
            'median_blur': image_ops.median_blur,
            'gaussian_blur': image_ops.gaussian_blur,
            'sepia': image_ops.sepia,
            'sharpen': image_ops.usm_sharpen,
            'pixelize': image_ops.pixelize,
            'derain': image_ops.derain,
            'shadow_removal': image_ops.remove_shadow 
        }[trans]
        current_img = self.current_img.value
        next_img = func(current_img)
        self._enqueue_img(next_img)

    def commit(self, img):
        current_img = self.current_img.value
        if img != current_img:
            self._enqueue_img(img)

    def undo(self):
        if self.img_queue_idx == 0:
            return

        self.img_queue_idx -= 1
        self._notify()

    def redo(self):
        if self.img_queue_idx == len(self.img_queue) - 1:
            return

        self.img_queue_idx += 1
        self._notify()

    def _enqueue_img(self, img):
        while len(self.img_queue) > 1 + self.img_queue_idx:
            self.img_queue.pop()

        self.img_queue.append(img)
        self.img_queue_idx += 1
        if len(self.img_queue) > self.max_queue_size:
            self.img_queue.pop(0)
            self.img_queue_idx -= 1
        self._notify()

    def _clear_img_queue(self):
        self.img_queue.clear()
        self.img_queue_idx = -1
        self._notify()

    def _notify(self):
        img = self.img_queue[self.img_queue_idx] if self.img_queue_idx >= 0 else None
        self.current_img.on_next(img)
