#Class Widgets utilizados na janela
from .Ui.ui_startWidget import *
from .Ui.ui_loadWidget import *
from .Ui.ui_endWidget import *
from .Ui.ui_tools import *
from .qt_core import *
#Funções secundarias
from typing import Literal
import webbrowser
import pyperclip
import socket
import qrcode
import json
import time
import io
import os

#Widget da janela principal e suas funcionalidades
class StartWidget(QWidget):
    def __init__(self,style_sheet: str, config: "ConfigServer") -> None:
        super().__init__()
        self.ui = Ui_StartWidget() #Widget em si
        self.ui.setupUi(self) 
        #variaveis importantes
        self.serverConfig = config
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
    
    #Função responsavel por criar os botões do tipo Switch   
    def setupCustomUI(self) -> None:
        # Botões de access
        self.enable_cozinha = QSwitchButton("Ativar Pedidos para a Cozinha",self)
        self.enable_bar = QSwitchButton("Ativar Pedidos para a Bar",self)
        self.enable_QrCode = QSwitchButton("Ativar Pedidos por QrCode",self)
        self.access_layout = QVBoxLayout(self.ui.access_frame)
        self.access_layout.addWidget(self.enable_cozinha)
        self.access_layout.addWidget(self.enable_bar)
        self.access_layout.addWidget(self.enable_QrCode)
        
        # Botões de network
        self.enable_local = QSwitchButton("Ativar Acesso dentro da Rede",self)
        self.enable_loophole = QSwitchButton("Ativar Acesso fora da Rede",self)
        
        self.enable_network_layout = QVBoxLayout(self.ui.enable_network_frame)
        self.enable_network_layout.addWidget(self.enable_local)
        self.enable_network_layout.addWidget(self.enable_loophole)
        self.ui.port_number.setValidator(QRegularExpressionValidator(QRegularExpression("[1-9]\\d*")))
        
        #Adicionar itens ao menu
        #Comida
        self.price_validator = QRegularExpressionValidator(QRegularExpression(r"^(?:\d+|\d{1,3}(?:,\d{3})+)?(?:[.,]\d+)?$"))
        self.ui.comida_price.setValidator(self.price_validator)
        self.comida_box = QVBoxLayout(self.ui.scroll_comida)
        self.comida_box.setObjectName(u"comida_box")
        self.comida_box.setContentsMargins(10, 10, 10, 10)
        self.ui.comida_list.setWidget(self.ui.scroll_comida)
        self.com_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.comida_box.addItem(self.com_spacer)
        #Bebida
        self.ui.bebida_price.setValidator(self.price_validator)
        self.bebida_box = QVBoxLayout(self.ui.scroll_bebida)
        self.bebida_box.setObjectName(u"bebida_box")
        self.bebida_box.setContentsMargins(10, 10, 10, 10)
        self.ui.bebida_list.setWidget(self.ui.scroll_bebida)
        self.beb_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.bebida_box.addItem(self.com_spacer)
    
    #Função responsavel por definir os comandos relaizados 
    def setupCommands(self) -> None:
        self.change_page(0)
        self.start_width = self.width()
        
        #SideBar
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
    
    #Carrega todos os estilos para a página
    def load_style(self) -> None:    
        #le a cor e o tema definido
        try:
            with open("interface/Ui/app.color", 'r+',encoding="utf-8") as c:
                info = c.read().split("; ")
            
        except FileNotFoundError:
            with open("interface/Ui/app.color", 'w',encoding="utf-8"): pass
        # Troca os valores da cor e do tema 
        try:
            self.ui.color_name.setCurrentText(info[0])
            self.ui.theme_name.setCurrentText(info[1])
        except:
            self.ui.color_name.setCurrentText(0)
            self.ui.theme_name.setCurrentText(0)  
        # define as cores do tema     
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
            self.sidebarHover_color = other_theme_options["sidebarHover"]
        except FileNotFoundError:
            with open("interface/themes.json", 'w',encoding="utf-8"): pass
        # Troca esse valor na StyleSheet
        style = self.style_sheet.replace("var(primary)", self.primary_color).replace("var(primary_variant)",self.primary_variant_color).replace("var(background)",self.background_color).replace("var(text)",self.text_color).replace("var(widget)",self.widget_color).replace("var(sidebar)",self.sidebar_color).replace("var(subwidget)",self.subwidget_color).replace("var(backgroundWidget)",self.backgroundWidget_color).replace("var(sidebarHover)",self.sidebarHover_color)
        # Aplicar o estilo à página
        self.ui.mainFrame.setStyleSheet(style)
        self.change_page(self.atual_page)
        self.enable_cozinha.update_style(self.text_color,self.primary_color)
        self.enable_bar.update_style(self.text_color,self.primary_color)
        self.enable_QrCode.update_style(self.text_color,self.primary_color)
        self.enable_local.update_style(self.text_color,self.primary_color)
        self.enable_loophole.update_style(self.text_color,self.primary_color)
        # Definir os icons dependendo do tema
        self.ui.Home_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/home.png"))
        self.ui.Users_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/users.png"))
        self.ui.Menu_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/menu.png"))
        self.ui.Access_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/access.png"))
        self.ui.Network_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/network.png"))
        self.ui.toggle_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/list.png"))
        self.ui.Settings_sideBar.setIcon(QIcon(u"interface/Ui/images/"+self.ui.theme_name.currentText().lower()+"/settings.png"))
        self.ui.mainFrame.update()
    
    #Mudar o tema
    def update_theme(self) -> None:
        with open("interface/Ui/app.color","w",encoding="utf-8") as c: 
            c.write(self.ui.color_name.currentText()+"; "+self.ui.theme_name.currentText())
        self.load_style()
    
    #Carregar as informações
    def load_all(self) -> None:
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
            self.enable_local.setChecked(dados["enable_local"])
            self.enable_loophole.setChecked(dados["enable_loophole"])
            if dados["domain"] != self.ui.domain_name.placeholderText():
                self.ui.domain_name.setText(dados["domain"])
            if str(dados["port"]) != self.ui.port_number.placeholderText():
                self.ui.port_number.setText(str(dados["port"]))
        except FileNotFoundError:
            with open(self.config_path+"network_access.json", 'w',encoding="utf-8"): pass
                 
    def save_all(self) -> None:
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
        
        #save network and access 
        network_access_Config = {}
        network_access_Config["enable_Cozinha"] = self.enable_cozinha.isChecked()
        network_access_Config["enable_Bar"] = self.enable_bar.isChecked()
        network_access_Config["enable_QrCode"] = self.enable_QrCode.isChecked()
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
        
        #Save server configs
        self.serverConfig.update(network_access_Config)
        self.changed = False
    
    #Função ativa sempre que há redimensionamento  
    def resizeEvent(self, event) -> None:
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
    
    #Função responsavel por mudar de página na sideBar    
    def change_page(self,page_idx: int) -> None:
        #Trocar de página
        if page_idx == None:
            page_idx = 0
        self.ui.pages.setCurrentIndex(page_idx)
        # remover a página anterior
        if self.atual_page != None:
            self.btn_list[self.atual_page].setStyleSheet("")
        #Ativar estilo da página tuak
        self.btn_list[page_idx].setStyleSheet("#"+self.btn_list[page_idx].objectName()+"{background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0.0170455 "+self.primary_color+", stop:1 "+self.background_color+"); border-left:3px solid #a1a1a1;border-bottom:1px solid "+self.background_color+";border-top:1px solid "+self.background_color+"; border-right:2px solid "+self.background_color+";}")
        self.atual_page = page_idx
        #atualizar o tamnho dos botões
        for btn in self.btn_list:
            #btn.setStyleSheet(btn.styleSheet()+"QFrame{padding-top:"+ str(height_padding) +";padding-bottom:"+ str(height_padding) +"}")
            btn.setIconSize(QSize(round(self.width() * 0.05/2+40),round(self.width() * 0.01/2+40)))
    
    #animar no estilo SideBar
    def animate_sideBar(self,animation: QPropertyAnimation ,start_size: int,end_size: int, time: int) -> None:
        animation.setStartValue(start_size)
        animation.setEndValue(end_size)
        animation.setDuration(time)
        animation.setEasingCurve(QEasingCurve.InOutCirc)
        return animation

    #Ativar sideBar
    def toggle_button(self) -> None:
        #Definir largura inincial e final        
        if self.sideBar_compressed:
            st_width=round(self.width() * 0.005/2+51)
            ed_width=round(self.width() * 0.015/2+170)
        else:
            st_width=round(self.width() * 0.015/2+170)
            ed_width=round(self.width() * 0.005/2+51)
        # fazer a animação de todos os componentes
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
        
    #Adiconar o atendente
    def add_user_name(self) -> None:
        name = self.ui.user_name.text().strip()
        if name != '':
            self.changed = True
            self.ui.user_name.clear()
            self.ui.list_users.addItem(name)
            
    #remover atendente
    def remove_user_name(self) -> None:
        selected_items = self.ui.list_users.selectedItems()
        for item in selected_items:
            self.changed = True
            self.ui.list_users.takeItem(self.ui.list_users.row(item))
    
    #Transformar o preço em um float
    def transform_price(self, price: str) -> None:
        price = price.replace(",",".")
        if "." not in price:
            price+=".00"
        inter, decim = price.split(".")
        inter = str(int(inter)) #transformar 0n em n
        while len(decim)<2:
            decim+="0"
        decim = decim[:2]
        
        return inter+"."+decim
    #Adicionar item ao menu    
    def add_menu_item(self, tipo: Literal["Comida","Bebida"]):
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
    
    # remover toda o menu     
    def remove_all_menu_items(self, tipo: Literal["Comida","Bebida"]) -> None:
        if tipo == "Comida":
            area = self.ui.scroll_comida
        else:
            area = self.ui.scroll_bebida
        children = area.findChildren(MenuLine)
        for item in children:
            self.changed = True
            item.deleteLater()

#Janela de carregamento
class LoadingWidget(QFrame):
    def __init__(self,style_sheet):
        super().__init__()
        self.setObjectName(u"mainFrame")
        self.style_sheet = style_sheet
        self.initUI()
        
    #Carrega todos os estilos para a página
    def load_style(self):
        # Ler as cor e tema definido
        try:
            with open("interface/Ui/app.color", 'r+',encoding="utf-8") as c:
                info = c.read().split("; ")
            
        except FileNotFoundError:
            with open("interface/Ui/app.color", 'w',encoding="utf-8"): pass
        
        #Criar as estilo    
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
            self.sidebarHover_color = other_theme_options["sidebarHover"]
        except FileNotFoundError:
            with open("interface/themes.json", 'w',encoding="utf-8"): pass
        style = self.style_sheet.replace("var(primary)", self.primary_color).replace("var(primary_variant)",self.primary_variant_color).replace("var(background)",self.background_color).replace("var(text)",self.text_color).replace("var(widget)",self.widget_color).replace("var(sidebar)",self.sidebar_color).replace("var(subwidget)",self.subwidget_color).replace("var(backgroundWidget)",self.backgroundWidget_color).replace("var(sidebarHover)",self.sidebarHover_color)
        #colocar style sheet na página
        self.setStyleSheet(style)

    #Iniciar a UI
    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("A carregar")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateLabel)
        self.timer.start(500)

        self.dotCount = 0
    
    #função chamda sempre que houver redimensionamento    
    def resizeEvent(self, event):
        title_font_size = 45  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_title_font_size = int(self.width() / 100) + title_font_size
        # Configura a nova fonte
        title_font = QFont()
        title_font.setPointSize(new_title_font_size)
        self.label.setFont(title_font)
        return super().resizeEvent(event)

    #atulizar qunatidade de pontos
    def updateLabel(self):
        self.dotCount += 1
        dots = "." * (self.dotCount % 4)
        self.label.setText("A carregar" + dots)

#Janela normal
class EndWidget(QWidget):
    def __init__(self,style_sheet,config):
        super().__init__()
        self.config = config
        self.uis = []
        #self.setObjectName("mainFrame")
        self.style_sheet =  style_sheet
        self.start = 0
        
    #Carrega todos os estilos para a página
    def load_style(self):
        # Ler as cor e tema definido
        try:
            with open("interface/Ui/app.color", 'r+',encoding="utf-8") as c:
                info = c.read().split("; ")
            
        except FileNotFoundError:
            with open("interface/Ui/app.color", 'w',encoding="utf-8"): pass
        
        #Criar o estilo    
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
            self.sidebarHover_color = other_theme_options["sidebarHover"]
        except FileNotFoundError:
            with open("interface/themes.json", 'w',encoding="utf-8"): pass
        style = self.style_sheet.replace("var(primary)", self.primary_color).replace("var(primary_variant)",self.primary_variant_color).replace("var(background)",self.background_color).replace("var(text)",self.text_color).replace("var(widget)",self.widget_color).replace("var(sidebar)",self.sidebar_color).replace("var(subwidget)",self.subwidget_color).replace("var(backgroundWidget)",self.backgroundWidget_color).replace("var(sidebarHover)",self.sidebarHover_color)

        self.setStyleSheet(style)
    
    #Definir  UI
    def startUI(self):
        layout_main = QVBoxLayout(self)
        layout_main.setSpacing(0)  # Espaçamento entre os elementos
        layout_main.setContentsMargins(0, 0, 0, 0)
        
        # Criar um novo QFrame como contêiner
        container_frame = QFrame(self)
        layout_container = QVBoxLayout(container_frame)
        layout_container.setSpacing(0)
        layout_container.setContentsMargins(0, 0, 0, 0)
        container_frame.setObjectName("container")

        self.frame_main = QFrame(self)
        layout_urls = QHBoxLayout(self.frame_main)
        layout_urls.setSpacing(0)
        layout_urls.setContentsMargins(0, 0, 0, 0)
        #Por cada URL um novo Widget é adicionado
        for u in range(len(self.config.urls)):
            widget = QWidget()  # Criar um widget para adicionar a classe gerada pelo Qt Designer
            ui = Ui_EndWindow()
            
            ui.setupUi(widget)
            real_url = self.config.getUrl(u) # obter o Url completo
            ui.url.setText(real_url)
            ui.url.setAlignment(Qt.AlignCenter)
            ui.url.update()
            # definir funções
            ui.copy_url.clicked.connect(lambda _=None,url=real_url: pyperclip.copy(url))
            ui.open_Link.clicked.connect(lambda _=None,url=real_url: webbrowser.open(url))
            ui.open_QrCode.clicked.connect(lambda _=None,url=real_url: self.openQr(url))
            self.uis.append(ui)
            layout_urls.addWidget(widget)
        #Layout de baixo
        layout_bottom = QHBoxLayout()
        layout_bottom.setObjectName("bottom")
        self.fim = QPushButton("Sair")
        self.fim.setObjectName("fim")
        self.fim.clicked.connect(QCoreApplication.instance().quit)
        self.password = ClickableLabel("Mostrar Password\n")
        self.password.setObjectName("password")
        self.password.clicked.connect(self.esconderPassword)
        self.password.setAlignment(Qt.AlignCenter)

        layout_bottom.addWidget(self.fim)
        layout_bottom.addWidget(self.password)

        # Adicionar self.frame_main e layout_bottom ao container_frame
        layout_container.addWidget(self.frame_main)
        layout_container.addLayout(layout_bottom)

        # Adicionar o container_frame ao layout principal
        layout_main.addWidget(container_frame)

        self.setLayout(layout_main)
        self.load_style()
        self.start = 1
        self.resizeEvent(None)
    
    #esconder/mostrar a password
    def esconderPassword(self):
        if self.password.text() == "Mostrar Password\n":
            self.password.setText("Password:\n" + self.config.password)
            pyperclip.copy(self.config.password)
        else:
            self.password.setText("Mostrar Password\n")
    
    #Abrir QRCode
    def openQr(self,data):
        # Criar o QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Converter a imagem do QR Code para um formato intermediário (BytesIO)
        image_stream = io.BytesIO()
        qr_img.save(image_stream, format="PNG")
        image_stream.seek(0)

        # Criar a QImage a partir do formato intermediário
        qimage = QImage.fromData(image_stream.getvalue())

        # Criar a QPixmap a partir da QImage
        pixmap = QPixmap.fromImage(qimage)

        # Criar a janela do QR Code
        self.qrcode_window = QWidget()
        layout = QVBoxLayout(self.qrcode_window)

        # Criar o QLabel para exibir o QR Code
        label = QLabel()
        label.setPixmap(pixmap)

        # Adicionar o QLabel ao layout
        layout.addWidget(label)

        # Exibir a janela
        self.qrcode_window.show()

    #Função ativada ao haver redimencionamento
    def resizeEvent(self, event):
        title_font_size = 15  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_title_font_size = int(self.width() / 100) + title_font_size
        # Configura a nova fonte
        title_font = QFont()
        title_font.setPointSize(new_title_font_size)
        button_font_size = 7  # Tamanho base da fonte
        # Calcula o novo tamanho da fonte com base na largura atual da janela
        new_button_font_size = int(self.width() / 100) + button_font_size
        # Configura a nova fonte
        button_font = QFont()
        button_font.setPointSize(new_button_font_size)
        for ui in self.uis:
            ui.url.setFont(title_font)
            ui.copy_url.setFont(button_font) 
            ui.open_Link.setFont(button_font) 
            ui.open_QrCode.setFont(button_font)
        if self.start:
            self.fim.setFont(title_font)
            self.password.setFont(title_font)
        if event != None:
            return super().resizeEvent(event)

#Class para configurar servidor
class ConfigServer:
    def __init__(self):
        self.final = 0
        self.run_loophole = 1
    
    #Atulizar as configurações
    def update(self,config):
        self.urls = []
        self.type = []
        self.access = {}
        #Loophole
        if config["enable_loophole"]:
            self.urls.append(config["domain"])
            self.type.append("loophole")
            self.host = "localhost"
        #Acesso dentro da rede
        if config["enable_local"]:
            self.urls.append(socket.gethostbyname(socket.gethostname()))
            self.type.append("same_network")
            self.host = "0.0.0.0"
        
        #Acesso apenas na maquina local     
        if not config["enable_loophole"] and not config["enable_local"]:
            self.urls.append("127.0.0.1")
            self.type.append("local")
            self.host = "localhost"
        self.port = config["port"]

        #Urls Acessiveis
        self.access["Cozinha"] = config["enable_Cozinha"]
        self.access["Bar"] = config["enable_Bar"]
        self.access["QrCode"] = config["enable_QrCode"]
    
    #Obter Full Url
    def getUrl(self,idx):
        url = self.urls[idx]
        type = self.type[idx]
        
        if type == "loophole":
            url = f"https://{url}.loophole.site"
        elif type == "same_network":
            url = f"http://{url}"
            if self.port != 80:
                url += ":"+str(self.port)     
        else:
            url = f"http://127.0.0.1"
            if self.port != 80:
                url += ":"+str(self.port)
        return url

        
#Class Worker
class Worker(QThread):
    finished = Signal()  # Sinal para indicar que a tarefa foi concluída
    def __init__(self,function,config):
        super().__init__()
        self.function = function
        self.config = config
        self.stop_loophole = 0
    @Slot()
    def run(self):
        # Executa a função
        run_app = self.function(self.config)
        while not self.config.final:
            time.sleep(0.5)
        time.sleep(3)
        self.finished.emit()
        run_app()# iniciar servidor
    

# Janela principal
class MainWindow(QMainWindow):
    def __init__(self, function):
        super().__init__()
        # Configuração da janela
        self.setGeometry(200, 200, 1000, 500)
        self.setMinimumSize(910, 450)
        self.setWindowTitle("Serviço")
        self.setWindowIcon(QIcon(".\\interface\\Ui\\images\\icon.ico"))
        self.style_sheet = self.getStyleSheet()
        self.function = function
        self.config = ConfigServer()
        self.janelas = QStackedWidget(self)
        self.start_window = StartWidget(self.style_sheet, self.config)
        self.load_window = LoadingWidget(self.style_sheet)
        self.end_window = EndWidget(self.style_sheet, self.config)
        self.setupCommands()
        self.janelas.addWidget(self.start_window)
        self.janelas.addWidget(self.load_window)
        self.janelas.addWidget(self.end_window)
        self.setCentralWidget(self.janelas)
        self.show()
        
    def closeEvent(self, event: QCloseEvent):
        if self.janelas.currentWidget() == self.start_window:
            if self.start_window.changed:
                # Diálogo de confirmação para salvar alterações
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Guardar Alterações?")
                dlg.setText("Deseja guardar as alterações feitas para posterior utilização?\nAs alterações não guardadas serão PERDIDAS.")
                dlg.setStandardButtons(QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel)
                dlg.setIcon(QMessageBox.Information)
                dlg.setStyleSheet("QMessageBox{font-size:14px;margin-right:10px;margin-right:3px;}")
                button = dlg.exec()
                if button == QMessageBox.Save:
                    self.start_window.save_all()
                    event.accept()
                elif button == QMessageBox.Ignore:
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()
        elif self.janelas.currentWidget() == self.load_window or self.janelas.currentWidget() == self.end_window:
            # Tratamento de fechamento para as outras janelas
            self.hide()
            if "loophole" in self.config.type:
                self.config.run_loophole = 0
                while self.config.run_loophole != 2:
                    time.sleep(0.1)
            self.worker.terminate()
        else:
            return super().closeEvent(event)        
    
    # Obtém a folha de estilo para a interface a partir de um arquivo
    def getStyleSheet(self):
        with open("interface/Ui/styles.qss", "r") as f:
            default_style = f.read() 
        return default_style
    
    # Configuração de comandos e sinais
    def setupCommands(self):
        self.worker = Worker(self.function, self.config)
        self.worker.finished.connect(self.service_window_setup)
        self.start_window.ui.start_btn.clicked.connect(self.load_window_setup)
    
    # Configuração da janela de carregamento e início do worker
    def load_window_setup(self):
        self.start_window.save_all()
        self.load_window.load_style()
        self.janelas.setCurrentIndex(1)
        self.worker.start()
        
    # Configuração da janela de término
    def service_window_setup(self):
        self.janelas.setCurrentIndex(2)
        self.end_window.startUI()