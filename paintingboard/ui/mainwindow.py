# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.canvas = Canvas()
        self.canvas.setGeometry(QtCore.QRect(0, 0, 924, 601))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setMouseTracking(True)
        self.canvas.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.canvas.setObjectName("canvas")
        self.scrollArea.setWidget(self.canvas)
        self.verticalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuAdvanced = QtWidgets.QMenu(self.menubar)
        self.menuAdvanced.setObjectName("menuAdvanced")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.drawingToolbar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drawingToolbar.sizePolicy().hasHeightForWidth())
        self.drawingToolbar.setSizePolicy(sizePolicy)
        self.drawingToolbar.setObjectName("drawingToolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.drawingToolbar)
        self.viewToolbar = QtWidgets.QToolBar(MainWindow)
        self.viewToolbar.setObjectName("viewToolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.viewToolbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/svg/resources/open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/svg/resources/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionInvert_Color = QtWidgets.QAction(MainWindow)
        self.actionInvert_Color.setObjectName("actionInvert_Color")
        self.actionHorizontal_Flip = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/svg/resources/flip_horizontal.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHorizontal_Flip.setIcon(icon2)
        self.actionHorizontal_Flip.setObjectName("actionHorizontal_Flip")
        self.actionVertical_Flip = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/svg/resources/flip_vertical.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVertical_Flip.setIcon(icon3)
        self.actionVertical_Flip.setObjectName("actionVertical_Flip")
        self.actionFitWindow = QtWidgets.QAction(MainWindow)
        self.actionFitWindow.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/svg/resources/fit_window.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFitWindow.setIcon(icon4)
        self.actionFitWindow.setObjectName("actionFitWindow")
        self.actionFitWidth = QtWidgets.QAction(MainWindow)
        self.actionFitWidth.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/svg/resources/fit_width.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFitWidth.setIcon(icon5)
        self.actionFitWidth.setObjectName("actionFitWidth")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/svg/resources/new.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon6)
        self.actionNew.setObjectName("actionNew")
        self.actionEqualize_Hist = QtWidgets.QAction(MainWindow)
        self.actionEqualize_Hist.setObjectName("actionEqualize_Hist")
        self.actionGrayscale = QtWidgets.QAction(MainWindow)
        self.actionGrayscale.setObjectName("actionGrayscale")
        self.actionBlur = QtWidgets.QAction(MainWindow)
        self.actionBlur.setObjectName("actionBlur")
        self.actionMedian_Blur = QtWidgets.QAction(MainWindow)
        self.actionMedian_Blur.setObjectName("actionMedian_Blur")
        self.actionSharpen = QtWidgets.QAction(MainWindow)
        self.actionSharpen.setObjectName("actionSharpen")
        self.actionGaussian_Blur = QtWidgets.QAction(MainWindow)
        self.actionGaussian_Blur.setObjectName("actionGaussian_Blur")
        self.actionSepia = QtWidgets.QAction(MainWindow)
        self.actionSepia.setObjectName("actionSepia")
        self.actionPixelize = QtWidgets.QAction(MainWindow)
        self.actionPixelize.setObjectName("actionPixelize")
        self.actionDerain = QtWidgets.QAction(MainWindow)
        self.actionDerain.setObjectName("actionDerain")
        self.actionShadowRemoval = QtWidgets.QAction(MainWindow)
        self.actionShadowRemoval.setObjectName("actionShadowRemoval")
        self.GuiActions = QtWidgets.QActionGroup(MainWindow)
        self.GuiActions.setObjectName("GuiActions")
        self.actionLine = QtWidgets.QAction(self.GuiActions)
        self.actionLine.setCheckable(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/svg/resources/line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLine.setIcon(icon7)
        self.actionLine.setObjectName("actionLine")
        self.actionRectangle = QtWidgets.QAction(self.GuiActions)
        self.actionRectangle.setCheckable(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/svg/resources/rectangle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRectangle.setIcon(icon8)
        self.actionRectangle.setObjectName("actionRectangle")
        self.actionEllipse = QtWidgets.QAction(self.GuiActions)
        self.actionEllipse.setCheckable(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/svg/resources/circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEllipse.setIcon(icon9)
        self.actionEllipse.setObjectName("actionEllipse")
        self.actiondefault = QtWidgets.QAction(self.GuiActions)
        self.actiondefault.setCheckable(True)
        self.actiondefault.setChecked(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/svg/resources/Cursor.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiondefault.setIcon(icon10)
        self.actiondefault.setObjectName("actiondefault")
        self.actionErase = QtWidgets.QAction(self.GuiActions)
        self.actionErase.setCheckable(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/svg/resources/eraser.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionErase.setIcon(icon11)
        self.actionErase.setObjectName("actionErase")
        self.acitonFill = QtWidgets.QAction(self.GuiActions)
        self.acitonFill.setCheckable(True)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/svg/resources/fill.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.acitonFill.setIcon(icon12)
        self.acitonFill.setObjectName("acitonFill")
        self.actionPen = QtWidgets.QAction(self.GuiActions)
        self.actionPen.setCheckable(True)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/svg/resources/brush.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPen.setIcon(icon13)
        self.actionPen.setObjectName("actionPen")
        self.actionspray = QtWidgets.QAction(self.GuiActions)
        self.actionspray.setCheckable(True)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/svg/resources/spray.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionspray.setIcon(icon14)
        self.actionspray.setObjectName("actionspray")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionHorizontal_Flip)
        self.menuEdit.addAction(self.actionVertical_Flip)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionInvert_Color)
        self.menuEdit.addAction(self.actionGrayscale)
        self.menuEdit.addAction(self.actionEqualize_Hist)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionBlur)
        self.menuEdit.addAction(self.actionMedian_Blur)
        self.menuEdit.addAction(self.actionGaussian_Blur)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSepia)
        self.menuEdit.addAction(self.actionSharpen)
        self.menuEdit.addAction(self.actionPixelize)
        self.menuAdvanced.addAction(self.actionDerain)
        self.menuAdvanced.addAction(self.actionShadowRemoval)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAdvanced.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actiondefault)
        self.toolBar.addAction(self.actionPen)
        self.toolBar.addAction(self.actionspray)
        self.toolBar.addAction(self.actionErase)
        self.toolBar.addAction(self.acitonFill)
        self.toolBar.addAction(self.actionLine)
        self.toolBar.addAction(self.actionRectangle)
        self.toolBar.addAction(self.actionEllipse)
        self.toolBar.addSeparator()
        self.viewToolbar.addAction(self.actionFitWindow)
        self.viewToolbar.addAction(self.actionFitWidth)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Painting Board"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuAdvanced.setTitle(_translate("MainWindow", "Advanced"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.drawingToolbar.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.viewToolbar.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_as.setText(_translate("MainWindow", "Save As"))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+F4"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actionInvert_Color.setText(_translate("MainWindow", "&Invert Color"))
        self.actionInvert_Color.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionHorizontal_Flip.setText(_translate("MainWindow", "Horizontal Flip"))
        self.actionVertical_Flip.setText(_translate("MainWindow", "Vertical Flip"))
        self.actionFitWindow.setText(_translate("MainWindow", "fit window"))
        self.actionFitWidth.setText(_translate("MainWindow", "fit width"))
        self.actionNew.setText(_translate("MainWindow", "&New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionEqualize_Hist.setText(_translate("MainWindow", "Equalize Hist"))
        self.actionGrayscale.setText(_translate("MainWindow", "Grayscale"))
        self.actionBlur.setText(_translate("MainWindow", "Blur"))
        self.actionMedian_Blur.setText(_translate("MainWindow", "Median Blur"))
        self.actionSharpen.setText(_translate("MainWindow", "Sharpen"))
        self.actionGaussian_Blur.setText(_translate("MainWindow", "Gaussian Blur"))
        self.actionSepia.setText(_translate("MainWindow", "Sepia"))
        self.actionPixelize.setText(_translate("MainWindow", "Pixelize"))
        self.actionDerain.setText(_translate("MainWindow", "Derain"))
        self.actionShadowRemoval.setText(_translate("MainWindow", "Shadow Removal"))
        self.actionLine.setText(_translate("MainWindow", "Line"))
        self.actionRectangle.setText(_translate("MainWindow", "Rectangle"))
        self.actionEllipse.setText(_translate("MainWindow", "Ellipse"))
        self.actiondefault.setText(_translate("MainWindow", "default"))
        self.actionErase.setText(_translate("MainWindow", "Erase"))
        self.acitonFill.setText(_translate("MainWindow", "Fill"))
        self.actionPen.setText(_translate("MainWindow", "Pen"))
        self.actionspray.setText(_translate("MainWindow", "spray"))
from .canvas import Canvas
from . import imgs_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
