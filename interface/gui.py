from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(200,200,300,300)
        self.setWindowTitle("Serviço")
        self.initUI()
        
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("TExto Importante")
        self.label.move(50,50)
        
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Clica me")
        self.b1.clicked.connect(self.clicked)
        self.b1.move(100,100)
        
    def clicked(self):
        self.label.setText("Parabéns Rodrigo Lopes")
        self.update()
        
    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    
    win.show()
    sys.exit(app.exec_())
    
    
window()