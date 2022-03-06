from PyQt5.QtWidgets import QApplication

from .models import *
from .viewModel import ViewModel
from .views import View


def init_app(argv):
    app = QApplication(argv)

    viewModel = ViewModel()
    view = View()
    view.bind(viewModel)
    view.show()

    return app
