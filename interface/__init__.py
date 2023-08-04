import os
os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false" # remove msg ao iniciar aplicação
from .gui import *
import sys

#Abre a janela e recebe como argumento uma função a ser executada no final da mesma
def start_window(fun):
    app = QApplication(sys.argv)
    _win = MainWindow(fun)
    sys.exit(app.exec())