from .window import *

from paintingboard.core import image_ops
from rx import operators as ops


class View(object):

    def __init__(self, viewModel=None) -> None:
        self.window = MainWindow()

        self.bind(viewModel)
        self.init_actions()

    def init_actions(self):
        self.window.registerListener(EVENT_NEW_PAINTING, self.new_painting)
        self.window.registerListener(EVENT_LOAD_FILE, self.open_file)
        self.window.registerListener(EVENT_CLEAR_CANVAS, self.clear_canvas)

        # painting modes
        mode_switch = [
            EVENT_SWITCH_TO_ERASE, EVENT_SWITCH_TO_FILL, EVENT_SWITCH_TO_DEFALT,
            EVENT_SWITCH_TO_PEN, EVENT_SWITCH_TO_SPRAY, EVENT_SWITCH_TO_LINE,
            EVENT_SWITCH_TO_RECT, EVENT_SWITCH_TO_ELLIPSE
        ]
        for mode in mode_switch:
            self.window.registerListener(mode, self.switch_mode)

        # painting setups
        attr_update = {
            EVENT_UPDATE_STROKE_COLOR: self.change_color,
            EVENT_UPDATE_STROKE_WIDTH: self.change_stroke_width
        }
        for event, callfunc in attr_update.items():
            self.window.registerListener(event, callfunc)

        # transformations
        transforms = {
            EVENT_INVERT_COLOR: image_ops.invert_color,
            EVENT_HORIZONTAL_FLIP: image_ops.horizontal_flip,
            EVENT_VERTICAL_FLIP: image_ops.vertical_flip,
            EVENT_EQUALIZE_HIST: image_ops.equalize_hist,
            EVENT_TO_GRAYSCALE: image_ops.to_grayscale,
            EVENT_BLUR: image_ops.average_blur,
            EVENT_MEDIAN_BLUR: image_ops.median_blur,
            EVENT_GAUSSIAN_BLUR: image_ops.gaussian_blur,
            EVENT_SEPIA: image_ops.sepia,
            EVENT_SHARPEN: image_ops.usm_sharpen,
            EVENT_PIXELIZE: image_ops.pixelize,
        }
        for event, op in transforms.items():
            self.window.registerListener(event, partial(self.transform, op))

    def bind(self, viewModel):
        self.viewModel = viewModel
        if viewModel is not None:
            self.viewModel.canvasNotEmpty.subscribe(self.set_actions_availability)
            self.viewModel.currentFilename.subscribe(
                on_next=self.window.show_status,
                on_error=lambda e: self.window.show_status(e.message)
            )
            self.viewModel.painter.subscribe(self.window.setup_painter)
            self.viewModel.painter.pipe(
                ops.map(lambda state: state.strokeColor),
                ops.distinct_until_changed()
            ).subscribe(self.window.show_painter_color)
            self.viewModel.mode.subscribe(self.window.switch_mode)

    def set_actions_availability(self, has_image):
        actions = [
            self.window.actionErase, self.window.acitonFill, self.window.actionPen,
            self.window.actionspray, self.window.actionLine, self.window.actionRectangle,
            self.window.actionEllipse, self.window.actionFitWidth, self.window.actionFitWindow,
            self.window.actionHorizontal_Flip, self.window.actionVertical_Flip,
            self.window.actionGrayscale, self.window.actionEqualize_Hist, self.window.actionBlur,
            self.window.actionMedian_Blur, self.window.actionGaussian_Blur,
            self.window.actionSepia, self.window.actionSharpen, self.window.actionPixelize,
            self.window.actionInvert_Color, self.window.actionSave, self.window.actionSave_as
        ]
        for it in actions:
            it.setEnabled(has_image)

    def new_painting(self):
        assert self.viewModel is not None
        self.clear_canvas()
        image = self.viewModel.new_painting()
        self.window.display(image)

    def open_file(self, fname):
        assert self.viewModel is not None
        self.clear_canvas()
        image = self.viewModel.load_file(fname)
        self.window.display(image)

    def clear_canvas(self):
        assert self.viewModel is not None
        self.viewModel.clear_canvas()
        self.window.display(None)

    def switch_mode(self, event_name):
        assert self.viewModel is not None
        mode = event_name.replace('event_switch_to_', '')
        self.viewModel.switch_mode(mode)

    def change_color(self, color):
        assert self.viewModel is not None
        self.viewModel.update_stroke_color(color)

    def change_stroke_width(self, width):
        assert self.viewModel is not None
        self.viewModel.update_stroke_width(width)

    def transform(self, trans):
        pixmap = self.window.canvas.pixmap
        pixmap_trans = trans(pixmap)
        self.window.display(pixmap_trans)

    def show(self):
        self.window.show()


__all__ = [
    'View'
]
