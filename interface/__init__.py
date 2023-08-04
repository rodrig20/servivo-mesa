from .gui import *
import sys


def start_window(fun):
    _win = MainWindow(fun)
    sys.exit(app.exec())