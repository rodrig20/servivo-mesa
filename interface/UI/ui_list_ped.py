from ..qt_core import *

class CrossButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(parent)
        self.setStyleSheet("QPushButton{border-radius:3px;background-color:red;margin-bottom:2px;}QPushButton::pressed {margin-top:2px;margin-bottom:0px;}")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.white, 2)
        painter.setPen(pen)

        # Desenha a cruz
        painter.drawLine(1/4*self.width(), 1/4*self.height(), 3/4*self.width(), 3/4*self.height())
        painter.drawLine(1/4*self.width(), 3/4*self.height(), 3/4*self.width(), 1/4*self.height())
        
    def resize(self,parent):
        self.setFixedSize(round(parent.width() * 0.03/2+15),round(parent.width() * 0.03/2+15))
        
        
class MenuLine(QFrame):
    def __init__(self, name, price, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.setStyleSheet('QFrame{background-color:"transparent";border-bottom:2px solid #888888;}')
        #font = QFont()
        #font.setPointSize(15)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        self.ped_name = QLabel(name)
        self.ped_name.setStyleSheet("border:none")
        self.preco_name = QLabel(price)
        self.preco_name.setStyleSheet("border:none")
        self.del_btn = CrossButton(self)
        self.del_btn.clicked.connect(self.remove_line)
        
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.ped_name.setSizePolicy(sizePolicy)

        layout.addWidget(self.ped_name)
        layout.addWidget(self.preco_name)
        layout.addWidget(self.del_btn)
        
        self.del_btn.clicked.connect(self.click)
        
    def click(self):
       if self._parent != None:
           self._parent.changed = True
        
    def remove_line(self):
        self.deleteLater()
        
    def update_style(self,text_color):
        self.setStyleSheet('color: '+text_color+';background-color:"transparent";border-bottom:2px solid #888888')
        
    def resizeEvent(self, event):
        normal_font_size = 5  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_normal_font_size = int(self.width() / 100) + normal_font_size
        # Configura a nova fonte
        normal_font = QFont()
        normal_font.setPointSize(new_normal_font_size)
        self.ped_name.setFont(normal_font)
        self.preco_name.setFont(normal_font)
        
        self.del_btn.resize(self)
        return super().resizeEvent(event)
    
    def __getitem__(self,key):
        if key == "nome" or key == "name":
            return self.ped_name.text()
        if key == "preco" or key == "price":
            return self.preco_name.text()