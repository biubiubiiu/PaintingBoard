from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QPushButton

from .mainwindow import Ui_MainWindow


class Ui_MainWindow_Custom(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        sizeicon = QLabel()
        sizeicon.setPixmap(QPixmap(':/png/resources/border-weight.png'))
        self.drawingToolbar.addWidget(sizeicon)
        self.sizeselect = QSlider()
        self.sizeselect.setRange(1,20)
        self.sizeselect.setOrientation(Qt.Horizontal)
        self.drawingToolbar.addWidget(self.sizeselect)

        self.colorPicker = QPushButton()
        self.colorPicker.resize(24, 24)
        self.colorPicker.setAutoFillBackground(True)
        self.drawingToolbar.addWidget(self.colorPicker)
