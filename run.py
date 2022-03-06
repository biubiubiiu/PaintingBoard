# -*- coding: utf-8 -*-

import sys

import paintingboard

if __name__ == '__main__':
    app = paintingboard.init_app(sys.argv)
    sys.exit(app.exec_())
