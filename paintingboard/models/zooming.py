from enum import Enum

from .base import BaseState


class Zooming(Enum):
    FIT_WINDOW = 0
    FIT_WIDTH = 1
    MANUAL_ZOOM = 2


class ZoomingState(BaseState):

    def __init__(self) -> None:
        super().__init__()

        self.mode = Zooming.FIT_WINDOW
