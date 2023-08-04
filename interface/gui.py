from .Ui.ui_startWidget import *
from .Ui.ui_loadWidget import *
from .Ui.ui_endWidget import *
from .Ui.ui_list_ped import *
from .Ui.ui_switch import *
from .qt_core import *
import sys, os
import json

class StartWindow(QWidget):
    def __init__(self,style_sheet):
        super().__init__()
        self.ui = Ui_StartWidget()
        self.ui.setupUi(self)
        #self.setCentralWidget(self.ui.mainFrame)
        self.atual_page = None
        self.sideBar_compressed = 1
        self.btn_list = (self.ui.Home_sideBar,self.ui.Users_sideBar,self.ui.Menu_sideBar,self.ui.Access_sideBar,self.ui.Network_sideBar,self.ui.Settings_sideBar)
        self.config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\config\\"
        self.style_sheet =  style_sheet
        self.setupCustomUI()
        self.load_style()
        self.setupCommands()
        self.load_all()
        self.changed = False
        
    def setupCustomUI(self):
        #Add Access toggle Button 
        self.enable_cozinha = QSwitchButton("Ativar Pedidos para a Cozinha",self)
        self.enable_bar = QSwitchButton("Ativar Pedidos para a Bar",self)
        self.enable_QrCode = QSwitchButton("Ativar Pedidos por QrCode",self)
        self.enable_tinyurl = QSwitchButton("Ativar Acesso por TinyUrl",self)
        self.access_layout = QVBoxLayout(self.ui.access_frame)
        self.access_layout.addWidget(self.enable_cozinha)
        self.access_layout.addWidget(self.enable_bar)
        self.access_layout.addWidget(self.enable_QrCode)
        self.access_layout.addWidget(self.enable_tinyurl)
        
        #Add Network toggle Button 
        self.enable_local = QSwitchButton("Ativar Acesso dentro da Rede",self)
        self.enable_loophole = QSwitchButton("Ativar Acesso fora da Rede",self)
        
        self.enable_network_layout = QVBoxLayout(self.ui.enable_network_frame)
        self.enable_network_layout.addWidget(self.enable_local)
        self.enable_network_layout.addWidget(self.enable_loophole)
        self.ui.port_number.setValidator(QRegularExpressionValidator(QRegularExpression("[1-9]\\d*")))
        
        #Add Item to list
        self.price_validator = QRegularExpressionValidator(QRegularExpression(r"^(?:\d+|\d{1,3}(?:,\d{3})+)?(?:[.,]\d+)?$"))
        self.ui.comida_price.setValidator(self.price_validator)
        self.comida_box = QVBoxLayout(self.ui.scroll_comida)
        self.comida_box.setObjectName(u"comida_box")
        self.comida_box.setContentsMargins(10, 10, 10, 10)
        self.ui.comida_list.setWidget(self.ui.scroll_comida)
        self.com_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.comida_box.addItem(self.com_spacer)
        
        self.ui.bebida_price.setValidator(self.price_validator)
        self.bebida_box = QVBoxLayout(self.ui.scroll_bebida)
        self.bebida_box.setObjectName(u"bebida_box")
        self.bebida_box.setContentsMargins(10, 10, 10, 10)
        self.ui.bebida_list.setWidget(self.ui.scroll_bebida)
        self.beb_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.bebida_box.addItem(self.com_spacer)
        
    def setupCommands(self):
        self.change_page(0)
        self.start_width = self.width()
        
        self.ui.Home_sideBar.clicked.connect(lambda: self.change_page(0))
        self.ui.Users_sideBar.clicked.connect(lambda: self.change_page(1))
        self.ui.Menu_sideBar.clicked.connect(lambda: self.change_page(2))
        self.ui.Access_sideBar.clicked.connect(lambda: self.change_page(3))
        self.ui.Network_sideBar.clicked.connect(lambda: self.change_page(4))
        self.ui.Settings_sideBar.clicked.connect(lambda: self.change_page(5))

        #Side Bar Toggle
        self.ui.toggle_sideBar.clicked.connect(self.toggle_button)
        
        #Add User Name to Valid Users
        self.ui.add_atend.clicked.connect(self.add_user_name)
        
        #Remove User Name of Valid Users
        self.ui.remove_atend.clicked.connect(self.remove_user_name)
        
        #Remove All User Name of Valid Users
        self.ui.remove_all_atend.clicked.connect(self.ui.list_users.clear)

        self.ui.add_comida.clicked.connect(lambda: self.add_menu_item("Comida"))
        self.ui.add_bebida.clicked.connect(lambda: self.add_menu_item("Bebida"))
        
        #Remove Item of list
        self.ui.remove_comida.clicked.connect(lambda: self.remove_all_menu_items("Comida"))
        self.ui.remove_bebida.clicked.connect(lambda: self.remove_all_menu_items("Bebida"))
        
        self.ui.port_number.textChanged.connect(lambda: setattr(self, 'changed', True))
        self.ui.domain_name.textChanged.connect(lambda: setattr(self, 'changed', True))
        self.ui.theme_name.currentIndexChanged.connect(self.update_theme)
        self.ui.color_name.currentIndexChanged.connect(self.update_theme)
        
        #Action Buttons:
        self.ui.close_btn.clicked.connect(QCoreApplication.instance().quit)
        self.ui.save_all.clicked.connect(self.save_all)
    
    def load_style(self):
          
        try:
            with open("interface/Ui/app.color", 'r+',encoding="utf-8") as c:
                info = c.read().split("; ")
            
        except FileNotFoundError:
            with open("interface/Ui/app.color", 'w',encoding="utf-8"): pass
        try:
            self.ui.color_name.setCurrentText(info[0])
            self.ui.theme_name.setCurrentText(info[1])
        except:
            self.ui.color_name.setCurrentText(0)
            self.ui.theme_name.setCurrentText(0)       
        try:
            with open("interface/themes.json", 'r+',encoding="utf-8") as c:
                theme = json.load(c)
            main_theme_color = theme["colors"][self.ui.color_name.currentText().lower()][self.ui.theme_name.currentText().lower()]
            other_theme_options = theme["theme"][self.ui.theme_name.currentText().lower()]
            self.primary_color = main_theme_color["primary"]
            self.primary_variant_color = main_theme_color["primary_variant"]
            self.background_color = other_theme_options["background"]
            self.text_color = other_theme_options["text"]
            self.widget_color = other_theme_options["widget"]
            self.sidebar_color = other_theme_options["sidebar"]
            self.subwidget_color = other_theme_options["subwidget"]
            self.backgroundWidget_color = other_theme_options["backgroundWidget"]
            self.sidebarHouver_color = other_theme_options["sidebarHouver"]
        except FileNotFoundError:
            with open("interface/themes.json", 'w',encoding="utf-8"): pass
        style = self.style_sheet.replace("var(primary)", self.primary_color).replace("var(primary_variant)",self.primary_variant_color).replace("var(background)",self.background_color).replace("var(text)",self.text_color).replace("var(widget)",self.widget_color).replace("var(sidebar)",self.sidebar_color).replace("var(subwidget)",self.subwidget_color).replace("var(backgroundWidget)",self.backgroundWidget_color).replace("var(sidebarHouver)",self.sidebarHouver_color)
        self.ui.mainFrame.setStyleSheet(style)
        self.change_page(self.atual_page)
        self.enable_cozinha.update_style(self.text_color,self.primary_color)
        self.enable_bar.update_style(self.text_color,self.primary_color)
        self.enable_QrCode.update_style(self.text_color,self.primary_color)
        self.enable_tinyurl.update_style(self.text_color,self.primary_color)
        self.enable_local.update_style(self.text_color,self.primary_color)
        self.enable_loophole.update_style(self.text_color,self.primary_color)
        self.ui.Home_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/home.png"))
        self.ui.Users_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/users.png"))
        self.ui.Menu_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/menu.png"))
        self.ui.Access_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/access.png"))
        self.ui.Network_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/network.png"))
        self.ui.toggle_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/list.png"))
        self.ui.Settings_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/settings.png"))
        self.ui.mainFrame.update()
        
    def update_theme(self):
        self.changed = True
        with open("interface/Ui/app.color","w",encoding="utf-8") as c: 
            c.write(self.ui.color_name.currentText()+"; "+self.ui.theme_name.currentText())
        self.load_style()
        
    def load_all(self):
        #Load Users
        try:
            with open(self.config_path+"users.txt", 'r+',encoding="utf-8") as u:
                users = u.readlines()
            for user in users:
                self.ui.list_users.addItem(user[:-1])  
        except FileNotFoundError:
            with open(self.config_path+"users.txt", 'w',encoding="utf-8"): pass
         
        #Load Menu
        try:
            with open(self.config_path+"menu.json", 'r+',encoding="utf-8") as m:
                menu = json.load(m)
            for name, price in menu["Comida"].items():
                line = MenuLine(name,price,self)
                self.comida_box.insertWidget(0,line)
            for name, price in menu["Bebida"].items():
                line = MenuLine(name,price,self)
                self.bebida_box.insertWidget(0,line)
                
        except FileNotFoundError:
            with open(self.config_path+"menu.json", 'w',encoding="utf-8"): pass
        
        #Load Network
        try:
            with open(self.config_path+"network_access.json", 'r+',encoding="utf-8") as na:
                dados = json.load(na)
            self.enable_cozinha.setChecked(dados["enable_Cozinha"])
            self.enable_bar.setChecked(dados["enable_Bar"])
            self.enable_QrCode.setChecked(dados["enable_QrCode"])
            self.enable_tinyurl.setChecked(dados["enable_TinyUrl"])
            self.enable_local.setChecked(dados["enable_local"])
            self.enable_loophole.setChecked(dados["enable_loophole"])
            if dados["domain"] != self.ui.domain_name.placeholderText():
                self.ui.domain_name.setText(dados["domain"])
            if str(dados["port"]) != self.ui.port_number.placeholderText():
                self.ui.port_number.setText(str(dados["port"]))
        except FileNotFoundError:
            with open(self.config_path+"network_access.json", 'w',encoding="utf-8"): pass
            
    
    def closeEvent(self,event):
        if self.changed:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Guardar Alterações?")
            dlg.setText("Deseja guardar as alterações feitas para postrior utilização?\nAs alterações não guardadas serão PERDIDAS.")
            dlg.setStandardButtons(QMessageBox.Save | QMessageBox.Ignore |QMessageBox.Cancel)
            buttonS = dlg.button(QMessageBox.Save)
            buttonS.setText('Guardar')
            buttonN = dlg.button(QMessageBox.Ignore)
            buttonN.setText('Ignorar')
            buttonN = dlg.button(QMessageBox.Cancel)
            buttonN.setText('Cancelar')
            dlg.setIcon(QMessageBox.Information)
            dlg.setStyleSheet("QMessageBox{font-size:14px;margin-right:10px;margin-right:3px;}")
            button = dlg.exec()
            
            if button == QMessageBox.Save:
                self.save_all()
                event.accept()
            elif button == QMessageBox.Ignore:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
                                
            
    def save_all(self):
        #Save Users
        with open(self.config_path+"users.txt","w",encoding="utf-8") as u:
            for i in range(self.ui.list_users.count()):
                u.write((self.ui.list_users.item(i).text())+"\n")
                
        #Save Menu
        menu = {"Comida":{},"Bebida":{}}
        for line in self.ui.scroll_comida.findChildren(MenuLine):
            nome = line["name"]
            price = line["price"]
            menu["Comida"][nome] = price
        for line in self.ui.scroll_bebida.findChildren(MenuLine):
            nome = line["name"]
            price = line["price"]
            menu["Bebida"][nome] = price
        
        with open(self.config_path+"menu.json","w",encoding="utf-8") as m:
            json.dump(menu, m,indent=4)
        
        network_access_Config = {}
        network_access_Config["enable_Cozinha"] = self.enable_cozinha.isChecked()
        network_access_Config["enable_Bar"] = self.enable_bar.isChecked()
        network_access_Config["enable_QrCode"] = self.enable_QrCode.isChecked()
        network_access_Config["enable_TinyUrl"] = self.enable_tinyurl.isChecked()
        network_access_Config["enable_local"] = self.enable_local.isChecked()
        network_access_Config["enable_loophole"] = self.enable_loophole.isChecked()
        domain = self.ui.domain_name.text().strip().replace(" ","-").lower()
        if domain == '':
            domain = "dominio-de-teste"
        network_access_Config["domain"] = domain
        port = self.ui.port_number.text()
        if port == '':
            port = "8080"
        
        port = int(port)
        if port > 65535 or port < 1:
            port = 8080
        network_access_Config["port"] = int(port)
        with open(self.config_path+"network_access.json","w",encoding="utf-8") as na:
            json.dump(network_access_Config, na,indent=4)     
        
        with open("interface/Ui/app.color","w",encoding="utf-8") as c: 
            c.write(self.ui.color_name.currentText()+"; "+self.ui.theme_name.currentText())
        self.changed = False
        
    def resizeEvent(self, event):
        ###TITLES
        title_font_size = 35  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_title_font_size = int(self.width() / 100) + title_font_size
        # Configura a nova fonte
        title_font = QFont()
        title_font.setPointSize(new_title_font_size)
        self.ui.home_title.setFont(title_font)
        self.ui.users_title.setFont(title_font)
        self.ui.menu_title.setFont(title_font)
        self.ui.access_title.setFont(title_font)
        self.ui.network_title.setFont(title_font)
        self.ui.settings_title.setFont(title_font)
        
        ###NORMAL_TEXT
        normal_font_size = 4  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_normal_font_size = int(self.width() / 100) + normal_font_size
        # Configura a nova fonte
        normal_font = QFont()
        normal_font.setPointSize(new_normal_font_size)
        self.ui.user_name.setFont(normal_font)
        self.ui.add_atend.setFont(normal_font)
        self.ui.remove_atend.setFont(normal_font)
        self.ui.remove_all_atend.setFont(normal_font)
        self.ui.add_bebida.setFont(normal_font)
        self.ui.add_comida.setFont(normal_font)
        self.ui.remove_bebida.setFont(normal_font)
        self.ui.remove_comida.setFont(normal_font)
        self.ui.bebida_price.setFont(normal_font)
        self.ui.comida_price.setFont(normal_font)
        self.ui.bebida_name.setFont(normal_font)
        self.ui.comida_name.setFont(normal_font)
        
        #self.ui.tabs_page.setStyleSheet("QTabWidget{font-size:"+"50"+"px;}")

        self.ui.bebida_price.setMinimumWidth(round(self.width() * 0.03/2+62))
        self.ui.comida_price.setMinimumWidth(round(self.width() * 0.03/2+62))
        
        ###Resume Text
        cursor = QTextCursor(self.ui.resume.document())
        cursor.beginEditBlock()
        text_font = None
        # Percorre todos os blocos de texto do documento
        while not cursor.atEnd():
            cursor.select(QTextCursor.BlockUnderCursor)
            format = QTextCharFormat()
            font = cursor.charFormat().font()
            if text_font == None:
                text_font = 11
                text_atual_font = font.pointSize()
            elif font.pointSize()!= text_atual_font:
                text_font = 18
            else:
                text_font = 11
            
            # Aplica a escala de tamanho de fonte
            new_font_size = max(round(self.width()*text_font/self.start_width),11)#font.pointSize()*scale_factor)# Ajuste o valor 0.8 conforme necessário

            
            font.setPointSize(new_font_size)
            format.setFont(font)
            cursor.mergeCharFormat(format)
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.NextBlock)

        cursor.endEditBlock()

        
        ###BIG_TExT
        big_font_size = 7  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_big_font_size = int(self.width() / 100) + big_font_size
        # Configura a nova fonte
        big_font = QFont()
        big_font.setPointSize(new_big_font_size)
        self.ui.bebida_list.setFont(big_font)
        self.ui.comida_list.setFont(big_font)
        self.ui.list_users.setFont(big_font)
        
        self.enable_bar.setFont(big_font,new_big_font_size)
        self.enable_cozinha.setFont(big_font,new_big_font_size)
        self.enable_QrCode.setFont(big_font,new_big_font_size)
        self.enable_tinyurl.setFont(big_font,new_big_font_size)
        self.enable_local.setFont(big_font,new_big_font_size)
        self.enable_loophole.setFont(big_font,new_big_font_size)
        self.ui.domain_label.setFont(big_font)
        self.ui.port_label.setFont(big_font)
        self.ui.domain_name.setFont(big_font)
        self.ui.port_number.setFont(big_font)
        
        self.ui.start_btn.setFont(big_font)
        self.ui.close_btn.setFont(big_font)
        
        self.ui.colors_label.setFont(big_font)
        self.ui.themes_label.setFont(big_font)
        self.ui.color_name.setFont(big_font)
        self.ui.theme_name.setFont(big_font)
        self.ui.save_all.setFont(big_font)

        
        height_padding = round(self.width() * 0.02/2)
        for btn in self.btn_list:
            btn.setMinimumHeight(50+height_padding)
            btn.setIconSize(QSize(round(self.width() * 0.05/2+40),round(self.width() * 0.01/2+40)))
            #btn.update()

        if self.sideBar_compressed:
            width=round(self.width() * 0.005/2+51)
        else:
            width=round(self.width() * 0.015/2+170)
            
        self.ui.side_bar.setMinimumWidth(width)

        # Chama o método da classe base
        super().resizeEvent(event)
        
    def change_page(self,page_idx):
        if page_idx == None:
            page_idx = 0
        self.ui.pages.setCurrentIndex(page_idx)
        if self.atual_page != None:
            self.btn_list[self.atual_page].setStyleSheet("")
        self.btn_list[page_idx].setStyleSheet("#"+self.btn_list[page_idx].objectName()+"{background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0.0170455 "+self.primary_color+", stop:1 "+self.background_color+"); border-left:3px solid #a1a1a1;border-bottom:1px solid "+self.background_color+";border-top:1px solid "+self.background_color+"; border-right:2px solid "+self.background_color+";}")
        self.atual_page = page_idx
        #height_padding = round(self.width() * 0.01/2)
        for btn in self.btn_list:
            #btn.setStyleSheet(btn.styleSheet()+"QFrame{padding-top:"+ str(height_padding) +";padding-bottom:"+ str(height_padding) +"}")
            btn.setIconSize(QSize(round(self.width() * 0.05/2+40),round(self.width() * 0.01/2+40)))
        
    def animate_sideBar(self,animation,start_size,end_size,time):
        animation.setStartValue(start_size)
        animation.setEndValue(end_size)
        animation.setDuration(time)
        animation.setEasingCurve(QEasingCurve.InOutCirc)
        return animation
        
    def toggle_button(self):        
        if self.sideBar_compressed:
            st_width=round(self.width() * 0.005/2+51)
            ed_width=round(self.width() * 0.015/2+170)
        else:
            st_width=round(self.width() * 0.015/2+170)
            ed_width=round(self.width() * 0.005/2+51)
        
        self.animation_bar = QPropertyAnimation(self.ui.side_bar,b"minimumWidth")
        self.animation_bar=self.animate_sideBar(self.animation_bar,st_width,ed_width,200)
        self.animation_version_frame = QPropertyAnimation(self.ui.version_frame,b"minimumWidth")
        self.animation_version_frame=self.animate_sideBar(self.animation_version_frame,st_width,ed_width,200)
        self.animation_version_label = QPropertyAnimation(self.ui.version_label,b"minimumWidth")
        self.animation_version_label=self.animate_sideBar(self.animation_version_label,st_width,ed_width,200)
        self.animation_bar.start()
        self.animation_version_frame.start()
        self.animation_version_label.start()
        self.sideBar_compressed = not self.sideBar_compressed
        
        
    def add_user_name(self):
        name = self.ui.user_name.text().strip()
        if name != '':
            self.changed = True
            self.ui.user_name.clear()
            self.ui.list_users.addItem(name)
            
    def remove_user_name(self):
        selected_items = self.ui.list_users.selectedItems()
        for item in selected_items:
            self.changed = True
            self.ui.list_users.takeItem(self.ui.list_users.row(item))
            
    def transform_price(self,price):
            price = price.replace(",",".")
            if "." not in price:
                price+=".00"
            inter, decim = price.split(".")
            inter = str(int(inter))
            while len(decim)<2:
                decim+="0"
            decim = decim[:2]
            
            return inter+"."+decim
            
    def add_menu_item(self,tipo):
        if tipo == "Comida":
            name = self.ui.comida_name.text().strip()
            price = self.ui.comida_price.text().strip()
            box = self.comida_box
        else:
            name = self.ui.bebida_name.text().strip()
            price = self.ui.bebida_price.text().strip()
            box = self.bebida_box
        if name != '' and price != '':
            price = self.transform_price(price) 
            self.changed = True               
            line = MenuLine(name,price,self)
            box.insertWidget(0,line)
            if tipo == "Comida": 
                self.ui.comida_name.setText("")
                self.ui.comida_price.setText("")
            else: 
                self.ui.bebida_name.setText("")
                self.ui.bebida_price.setText("")
            
    def remove_all_menu_items(self,tipo):
        if tipo == "Comida":
            area = self.ui.scroll_comida
        else:
            area = self.ui.scroll_bebida
        children = area.findChildren(MenuLine)
        for item in children:
            self.changed = True
            item.deleteLater()

class ServerConfig:
    def __init__(self):
        self.links = []
    
class Worker(QThread):
    progressChanged = Signal(int)

    def __init__(self, function, string, parent=None):
        self.function = function
        self.string = string
        super().__init__(parent)

    def run(self):
        progress_callback = self.progressChanged.emit
        self.function(self.string,progress_callback)

class ProgressBarManager(QObject):
    animationFinished = Signal()

    def __init__(self, parent, progressbar):
        super().__init__()
        self.progressbar = progressbar
        self._parent = parent
        self.animation = None

    @Slot(int)
    def update_progress_bar(self, value):
        if self.animation and self.animation.state() == QPropertyAnimation.Running:
            # Ainda há uma animação em andamento, aguarda o término
            self.animationFinished.connect(lambda: self.update_progress_bar(value))
        else:
            self.animation = QPropertyAnimation(self.progressbar, b"value")
            self.animation.setDuration(50)  # Duração da animação em milissegundos
            self.animation.setEasingCurve(QEasingCurve.InOutCirc)
            self.animation.setStartValue(self.progressbar.value())
            self.animation.setEndValue(self.progressbar.value() + value)
            self.animation.finished.connect(self.animationFinished.emit)
            self.animation.start()

            if self.progressbar.value() >= 100:
                self._parent.end_window.load_all(self._parent.server_config)
                self._parent.janelas.setCurrentIndex(2)
    
class LoadWindow(QWidget):
    def __init__(self,style_sheet):
        super().__init__()
        self.ui = Ui_LoadWidget()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(0) 
        self.style_sheet = style_sheet
        self.load_style()
        
    def resizeEvent(self,_):
        ###TITLES
        title_font_size = 35  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_title_font_size = int(self.width() / 100) + title_font_size
        # Configura a nova fonte
        title_font = QFont()
        title_font.setPointSize(new_title_font_size)
        self.ui.loading_label.setFont(title_font)
        
        progressBar_height = round(40+self.width()*0.05/3)
        self.ui.progressBar.setStyleSheet(f"height:{progressBar_height};margin:{progressBar_height};margin-bottom:{round(1.5*progressBar_height)};margin-top:{round(1.5*progressBar_height)}")  # Defina a altura desejada aqui
        title_font = QFont()
        title_font.setPointSize(progressBar_height-10)
        self.ui.progressBar.setFont(title_font)
        
    def load_style(self):
          
        try:
            with open("interface/Ui/app.color", 'r+',encoding="utf-8") as c:
                info = c.read().split("; ")
            
        except FileNotFoundError:
            with open("interface/Ui/app.color", 'w',encoding="utf-8"): pass   
        try:
            with open("interface/themes.json", 'r+',encoding="utf-8") as c:
                theme = json.load(c)
            main_theme_color = theme["colors"][info[0].lower()][info[1].lower()]
            other_theme_options = theme["theme"][info[1].lower()]
            self.primary_color = main_theme_color["primary"]
            self.primary_variant_color = main_theme_color["primary_variant"]
            self.background_color = other_theme_options["background"]
            self.text_color = other_theme_options["text"]
            self.widget_color = other_theme_options["widget"]
            self.sidebar_color = other_theme_options["sidebar"]
            self.subwidget_color = other_theme_options["subwidget"]
            self.backgroundWidget_color = other_theme_options["backgroundWidget"]
            self.sidebarHouver_color = other_theme_options["sidebarHouver"]
        except FileNotFoundError:
            with open("interface/themes.json", 'w',encoding="utf-8"): pass
            
        style = self.style_sheet.replace("var(primary)", self.primary_color).replace("var(primary_variant)",self.primary_variant_color).replace("var(background)",self.background_color).replace("var(text)",self.text_color).replace("var(widget)",self.widget_color).replace("var(sidebar)",self.sidebar_color).replace("var(subwidget)",self.subwidget_color).replace("var(backgroundWidget)",self.backgroundWidget_color).replace("var(sidebarHouver)",self.sidebarHouver_color)
        self.ui.mainFrame.setStyleSheet(style)
        self.ui.mainFrame.update()
        

class EndWindow(QWidget):
    def __init__(self,style_sheet):
        super().__init__()
        self.style_sheet = style_sheet
        self.load_style()
        
    def load_all(self,config):
        self.uis = []
        for url in config.links[::-1]:
            ui = Ui_EndWindow()
            ui.setupUi(self)
            ui.url.setText(url)
            self.setupCommands(ui,url)
            
    def load_style(self):
          
        try:
            with open("interface/Ui/app.color", 'r+',encoding="utf-8") as c:
                info = c.read().split("; ")
            
        except FileNotFoundError:
            with open("interface/Ui/app.color", 'w',encoding="utf-8"): pass   
        try:
            with open("interface/themes.json", 'r+',encoding="utf-8") as c:
                theme = json.load(c)
            main_theme_color = theme["colors"][info[0].lower()][info[1].lower()]
            other_theme_options = theme["theme"][info[1].lower()]
            self.primary_color = main_theme_color["primary"]
            self.primary_variant_color = main_theme_color["primary_variant"]
            self.background_color = other_theme_options["background"]
            self.text_color = other_theme_options["text"]
            self.widget_color = other_theme_options["widget"]
            self.sidebar_color = other_theme_options["sidebar"]
            self.subwidget_color = other_theme_options["subwidget"]
            self.backgroundWidget_color = other_theme_options["backgroundWidget"]
            self.sidebarHouver_color = other_theme_options["sidebarHouver"]
        except FileNotFoundError:
            with open("interface/themes.json", 'w',encoding="utf-8"): pass
            
        style = self.style_sheet.replace("var(primary)", self.primary_color).replace("var(primary_variant)",self.primary_variant_color).replace("var(background)",self.background_color).replace("var(text)",self.text_color).replace("var(widget)",self.widget_color).replace("var(sidebar)",self.sidebar_color).replace("var(subwidget)",self.subwidget_color).replace("var(backgroundWidget)",self.backgroundWidget_color).replace("var(sidebarHouver)",self.sidebarHouver_color)
        self.setStyleSheet(style)
        self.update()
            
    def setupCommands(self,ui,link):
        ...
            
            

class MainWindow(QMainWindow):
    def __init__(self,start_function):
        super().__init__()
        self.setGeometry(200,200,1000,500)
        self.setMinimumSize(910,450)
        self.setWindowTitle("Serviço")
        self.style_sheet = self.getStyleSheet()
        self.server_config = ServerConfig()
        self.worker = Worker(start_function,self.server_config)
        self.janelas = QStackedWidget(self)
        self.start_window = StartWindow(self.style_sheet)
        self.end_window = EndWindow(self.style_sheet)
        self.load_window = LoadWindow(self.style_sheet)
        self.janelas.addWidget(self.start_window)
        self.janelas.addWidget(self.load_window)
        self.janelas.addWidget(self.end_window)
        self.setupCommands()
        self.setCentralWidget(self.janelas)
        self.show()
    
    def getStyleSheet(self):
        with open("interface/Ui/styles.qss", "r") as f:
            default_style = f.read() 
        return default_style
    
    def start_function(self):
        self.janelas.setCurrentIndex(1)
        self.worker.start()
    
    def setupCommands(self):
        self.start_window.ui.start_btn.clicked.connect(lambda: self.start_function())
        manager = ProgressBarManager(self,self.load_window.ui.progressBar)
        self.worker.progressChanged.connect(lambda v: manager.update_progress_bar(v))

        

app = QApplication(sys.argv)