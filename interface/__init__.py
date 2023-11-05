import os
from .gui import QApplication, MainWindow
import sys
os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false"  # remove msg ao iniciar aplicação


# Abre a janela e recebe como argumento uma função a ser executada no final da mesma
def start_window(fun):
    app = QApplication(sys.argv)
    MainWindow(app, fun)
    sys.exit(app.exec())
