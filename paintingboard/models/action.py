from enum import Enum
from .base import BaseState


class Actions(Enum):
    ACTION_DEFAULT = 0
    ACTION_PEN = 1
    ACTION_SPRAY = 2
    ACTION_ERASE = 3
    ACTION_FILL = 4
    ACTION_LINE = 5
    ACTION_RECT = 6
    ACTION_ELLIPSE = 7


class ActionMode(BaseState):

    def __init__(self) -> None:
        super().__init__()

        self.action = Actions.ACTION_DEFAULT
