from ..qt_core import *


class ClickableLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
        
class Switch(QCheckBox):
    def __init__(
        self,
        width=45,
        height=23,
        border=3,
        bg_color="#3c4042",
        circLe_color="#DDDDDD",
        active_color="#8e0793",
        animation_curve=QEasingCurve.OutBounce
    ):
        QCheckBox.__init__(self)
        self.setFixedSize(width,height)
        self.setCursor(Qt.PointingHandCursor)
        self._width = self.original_w = width
        self._height= self.original_h = height
        self._border = border
        # COLORS
        self._bg_color = bg_color
        self._circle_color = circLe_color
        self._active_color = active_color
        
        #Create Animation
        
        self._circle_position = self._border
        self.animation = QPropertyAnimation(self, b"circle_position",self)
        self.animation.setEasingCurve(animation_curve)
        
        self.animation.setDuration(500)

        self.stateChanged.connect(self.start_trasition)
        
    @Property(float) # type: ignore
    def change_circle_position(self):
        return self._circle_position
    
    @change_circle_position.setter
    def circle_position(self,pos):
        self._circle_position = pos
        self.update()
    
    def start_trasition(self,val):
        
        self.animation.stop()
        if val:
            self.animation.setEndValue(self._width- self._height+self._border)
        else:
            self.animation.setEndValue(self._border)
        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
        
    def paintEvent(self,_):
        #Set Painter
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        
        rect = QRect(0,0,self._width,self._height)
        
        #If Check is Checked
        if not self.isChecked():
            #Draw Bg
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0,0,rect.width(),self._height,self._height/2,self._height/2)
            
            #Draw Circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position,self._border,self.height()-2*self._border,self._height-2*self._border)
        else:
            #Draw Bg
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0,0,rect.width(),self._height,self._height/2,self._height/2)
            
            #Draw Circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position,self._border,self._height-2*self._border,self._height-2*self._border)
        
        #End Draw
        p.end()
        
    def resize(self,size):
        self._height = self.original_h*size/14
        self._width = self.original_w*size/14
        self.setFixedSize(self._width,self._height)
        if self.isChecked():
            pos = self._width- self._height+self._border
        else:
            pos = self._border
        self._circle_position = pos
        
    def resizeEvent(self,event):
        if self.isChecked():
            pos = self._width-self._height+self._border
        else:
            pos = self._border
        self._circle_position = pos
        self.update()
        return super().resizeEvent(event)

class QSwitchButton(QFrame) :
    def __init__(self, text, mainWindow, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color:"transparent"')
        self.main = mainWindow
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        self.label = QLabel(text)
        self.label.setStyleSheet("border:none")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label.setSizePolicy(sizePolicy)
        
        self.switch = Switch()
        
        layout.addWidget(self.switch)
        layout.addWidget(self.label)
        
        self.switch.stateChanged.connect(self.change)
        
    def change(self):
        self.main.changed = True
        
    def setFont(self, font,size):
        self.label.setFont(font)
        self.switch.resize(size)
    
    def isChecked(self):
        return self.switch.isChecked()
    
    def setChecked(self,mode):
        self.switch.setChecked(mode) 
        
    def update_style(self,text_color,active_color):
        self.label.setStyleSheet('color: '+text_color+';background-color:"transparent"')
        self.switch._active_color = active_color
        self.update()

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
        self.setStyleSheet('QFrame{background-color:"transparent";}')
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
        self.setStyleSheet('color: '+text_color+';background-color:"transparent";')
        
    def resizeEvent(self, event):
        normal_font_size = 10  # Tamanho base da fonte
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

class ImageMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Resizer")
        self.setGeometry(100, 100, 800, 600)

        self.scroll_area = QScrollArea()
        self.label = QLabel()
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setObjectName("menu_image")
        self.scroll_area.setStyleSheet('QLabel{background-color:"transparent"}')
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

        self.image = None  # Store the loaded image

    def set_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        self.load_image(file_name)
                
        return file_name

    def load_image(self,file_name):
        if file_name:
            self.image = QImage(file_name)
            if not self.image.isNull():
                self.update_image()
                
        return file_name
    
    def update_image(self):
        resized_image = self.image.scaledToWidth(self.width() - 30)
        pixmap = QPixmap.fromImage(resized_image)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()

        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def remove_image(self):
        self.image = None
        self.label.clear()
        
    def resizeEvent(self, event):
        if self.image:
            self.update_image()
        return super().resizeEvent(event)
