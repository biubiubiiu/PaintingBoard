#!/bin/bash
pyrcc5 imgs.qrc -o imgs_rc.py
pyuic5 -x mainwindow.ui -o mainwindow.py
sed -i 's/import imgs_rc/from . import imgs_rc/g' mainwindow.py
sed -i 's/from canvas import Canvas/from .canvas import Canvas/g' mainwindow.py
mv imgs_rc.py ../paintingboard/ui/
mv mainwindow.py ../paintingboard/ui/
