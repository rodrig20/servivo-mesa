from ..qt_core import *

class Switch(QCheckBox) :
    def __init__(
        self,
        width = 45,
        height = 23,
        border = 3,
        bg_color = "#3c4042",
        circLe_color ="#DDDDDD",
        active_color = "#8e0793",
        animation_curve = QEasingCurve.OutBounce
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
        
    @Property(float) #Get
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
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

    