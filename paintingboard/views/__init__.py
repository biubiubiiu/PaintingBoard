from .window import *

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
            EVENT_SWITCH_TO_ERASE, EVENT_SWITCH_TO_FILL, EVENT_SWITCH_TO_DEFAULT,
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

        # zooming modes
        zoom_mode_switch = {
            EVENT_SWITCH_FIT_WIDTH: Zooming.FIT_WIDTH, 
            EVENT_SWITCH_FIT_WINDOW: Zooming.FIT_WINDOW, 
            EVENT_SWITCH_MANUAL_ZOOM: Zooming.MANUAL_ZOOM
        }
        for event, mode in zoom_mode_switch.items():
            self.window.registerListener(event, partial(self.switch_zoom_mode, mode))

        # transformations
        for event in [
            EVENT_INVERT_COLOR,
            EVENT_HORIZONTAL_FLIP,
            EVENT_VERTICAL_FLIP,
            EVENT_EQUALIZE_HIST,
            EVENT_TO_GRAYSCALE,
            EVENT_BLUR,
            EVENT_MEDIAN_BLUR,
            EVENT_GAUSSIAN_BLUR,
            EVENT_SEPIA,
            EVENT_SHARPEN,
            EVENT_PIXELIZE,
            EVENT_DERAIN,
            EVENT_SHADOW_REMOVAL
        ]:
            self.window.registerListener(event, partial(self.transform, event))

        workflow_control = {
            EVENT_UNDO: self.undo,
            EVENT_REDO: self.redo,
            EVENT_COMMIT: self.commit
        }
        for event, func in workflow_control.items():
            self.window.registerListener(event, func)


    def bind(self, viewModel):
        self.viewModel = viewModel
        if viewModel is not None:
            self.viewModel.current_img.pipe(
                ops.map(lambda img: img is not None)
            ).subscribe(self.set_actions_availability)
            self.viewModel.currentFilename.subscribe(
                on_next=self.window.show_status,
                on_error=lambda e: self.window.show_status(e.message)
            )
            self.viewModel.current_img.subscribe(self.window.display)
            self.viewModel.painter.subscribe(self.window.setup_painter)
            self.viewModel.painter.pipe(
                ops.map(lambda state: state.strokeColor),
                ops.distinct_until_changed()
            ).subscribe(self.window.show_painter_color)
            self.viewModel.zooming.pipe(
                ops.map(lambda state: state.mode),
                ops.distinct_until_changed()
            ).subscribe(self.window.change_zoom_mode)
            self.viewModel.mode.pipe(
                ops.map(lambda state: state.action),
                ops.distinct_until_changed()
            ).subscribe(self.window.switch_mode)

    def set_actions_availability(self, has_image):
        actions = [
            self.window.actionErase, self.window.acitonFill, self.window.actionPen,
            self.window.actionspray, self.window.actionLine, self.window.actionRectangle,
            self.window.actionEllipse, self.window.actionFitWidth, self.window.actionFitWindow,
            self.window.actionHorizontal_Flip, self.window.actionVertical_Flip,
            self.window.actionGrayscale, self.window.actionEqualize_Hist, self.window.actionBlur,
            self.window.actionMedian_Blur, self.window.actionGaussian_Blur,
            self.window.actionSepia, self.window.actionSharpen, self.window.actionPixelize,
            self.window.actionInvert_Color, self.window.actionSave, self.window.actionSave_as,
            self.window.actionDerain, self.window.actionShadowRemoval
        ]
        for it in actions:
            it.setEnabled(has_image)

    def new_painting(self):
        assert self.viewModel is not None
        self.clear_canvas()
        self.viewModel.new_painting()

    def open_file(self, fname):
        assert self.viewModel is not None
        self.clear_canvas()
        self.viewModel.load_file(fname)

    def clear_canvas(self):
        assert self.viewModel is not None
        self.viewModel.clear_canvas()

    def switch_mode(self, event_name):
        assert self.viewModel is not None
        mode = event_name.replace('event_switch_to_', '')
        self.viewModel.switch_mode(mode)

    def switch_zoom_mode(self, mode):
        assert self.viewModel is not None
        self.viewModel.switch_zooming_mode(mode)

    def change_color(self, color):
        assert self.viewModel is not None
        self.viewModel.update_stroke_color(color)

    def change_stroke_width(self, width):
        assert self.viewModel is not None
        self.viewModel.update_stroke_width(width)

    def transform(self, event_name):
        assert self.viewModel is not None
        trans = event_name.replace('event_', '')
        self.viewModel.transform(trans)

    def commit(self):
        assert self.viewModel is not None
        pixmap = self.window.canvas.pixmap
        self.viewModel.commit(pixmap)

    def undo(self):
        assert self.viewModel is not None
        self.viewModel.undo()

    def redo(self):
        assert self.viewModel is not None
        self.viewModel.redo()

    def show(self):
        self.window.show()


__all__ = [
    'View'
]
