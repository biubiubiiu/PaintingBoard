from PyQt5.QtGui import QColor
from .base import BaseState


class PainterState(BaseState):

    def __init__(self) -> None:
        super().__init__()

        self.strokeWidth = 1
        self.strokeColor = QColor(0, 0, 0)  # black
