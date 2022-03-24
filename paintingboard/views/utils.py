from paintingboard.models import Actions
from paintingboard.ui import CanvasMode


action2canvasmode = {
    Actions.ACTION_DEFAULT: CanvasMode.IDLE,
    Actions.ACTION_ERASE: CanvasMode.ERASER,
    Actions.ACTION_FILL: CanvasMode.FILL,
    Actions.ACTION_PEN: CanvasMode.PEN,
    Actions.ACTION_SPRAY: CanvasMode.SPRAY,
    Actions.ACTION_LINE: CanvasMode.LINE,
    Actions.ACTION_RECT: CanvasMode.RECT,
    Actions.ACTION_ELLIPSE: CanvasMode.ELLIPSE
}