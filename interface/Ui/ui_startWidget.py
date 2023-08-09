from ..qt_core import *

class Ui_StartWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.setWindowTitle(u"")
        self.verticalLayout_15 = QVBoxLayout(MainWidget)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.mainFrame = QFrame(MainWidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setStyleSheet(u"")
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.window = QFrame(self.mainFrame)
        self.window.setObjectName(u"window")
        self.window.setMaximumSize(QSize(16777215, 16777215))
        self.window.setStyleSheet(u"")
        self.window.setFrameShape(QFrame.StyledPanel)
        self.window.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.window)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.side_bar = QFrame(self.window)
        self.side_bar.setObjectName(u"side_bar")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.side_bar.sizePolicy().hasHeightForWidth())
        self.side_bar.setSizePolicy(sizePolicy)
        self.side_bar.setMinimumSize(QSize(56, 0))
        self.side_bar.setMaximumSize(QSize(56, 16777215))
        self.side_bar.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.side_bar)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.toggle_sideBar = QPushButton(self.side_bar)
        self.toggle_sideBar.setObjectName(u"toggle_sideBar")
        self.toggle_sideBar.setMinimumSize(QSize(0, 0))
        self.toggle_sideBar.setMaximumSize(QSize(16777215, 16777215))
        self.toggle_sideBar.setText(u"")

        self.verticalLayout.addWidget(self.toggle_sideBar)

        self.Home_sideBar = QPushButton(self.side_bar)
        self.Home_sideBar.setObjectName(u"Home_sideBar")
        self.Home_sideBar.setMinimumSize(QSize(0, 0))
        self.Home_sideBar.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(15)
        self.Home_sideBar.setFont(font)
        self.Home_sideBar.setStyleSheet(u"/*padding-top:5px;	padding-bottom:5px;*/")
        self.Home_sideBar.setText(u"  Princiapal")

        self.verticalLayout.addWidget(self.Home_sideBar)

        self.Users_sideBar = QPushButton(self.side_bar)
        self.Users_sideBar.setObjectName(u"Users_sideBar")
        self.Users_sideBar.setMinimumSize(QSize(0, 0))
        self.Users_sideBar.setMaximumSize(QSize(16777215, 16777215))
        self.Users_sideBar.setFont(font)
        self.Users_sideBar.setStyleSheet(u"/*padding-top:5px;	padding-bottom:5px;*/")
        self.Users_sideBar.setText(u"  Atendentes")

        self.verticalLayout.addWidget(self.Users_sideBar)

        self.Menu_sideBar = QPushButton(self.side_bar)
        self.Menu_sideBar.setObjectName(u"Menu_sideBar")
        self.Menu_sideBar.setMinimumSize(QSize(0, 0))
        self.Menu_sideBar.setMaximumSize(QSize(16777215, 16777215))
        self.Menu_sideBar.setFont(font)
        self.Menu_sideBar.setStyleSheet(u"/*padding-top:5px;	padding-bottom:5px;*/")
        self.Menu_sideBar.setText(u"  Menu")

        self.verticalLayout.addWidget(self.Menu_sideBar)

        self.Access_sideBar = QPushButton(self.side_bar)
        self.Access_sideBar.setObjectName(u"Access_sideBar")
        self.Access_sideBar.setMinimumSize(QSize(0, 0))
        self.Access_sideBar.setMaximumSize(QSize(16777215, 16777215))
        self.Access_sideBar.setFont(font)
        self.Access_sideBar.setStyleSheet(u"/*padding-top:5px;	padding-bottom:5px;*/")
        self.Access_sideBar.setText(u"  Acessos")

        self.verticalLayout.addWidget(self.Access_sideBar)

        self.Network_sideBar = QPushButton(self.side_bar)
        self.Network_sideBar.setObjectName(u"Network_sideBar")
        self.Network_sideBar.setFont(font)
        self.Network_sideBar.setStyleSheet(u"/*padding-top:5px;	padding-bottom:5px;*/")
        self.Network_sideBar.setText(u"  Rede")

        self.verticalLayout.addWidget(self.Network_sideBar)

        self.side_bar_spacing = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.side_bar_spacing)

        self.Settings_sideBar = QPushButton(self.side_bar)
        self.Settings_sideBar.setObjectName(u"Settings_sideBar")
        self.Settings_sideBar.setFont(font)
        self.Settings_sideBar.setText(u"  Defini\u00e7\u00f5es")

        self.verticalLayout.addWidget(self.Settings_sideBar)


        self.horizontalLayout.addWidget(self.side_bar)

        self.pages = QStackedWidget(self.window)
        self.pages.setObjectName(u"pages")
        sizePolicy.setHeightForWidth(self.pages.sizePolicy().hasHeightForWidth())
        self.pages.setSizePolicy(sizePolicy)
        self.pages.setStyleSheet(u"")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.home_page.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.home_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.home_title = QLabel(self.home_page)
        self.home_title.setObjectName(u"home_title")
        font1 = QFont()
        font1.setPointSize(24)
        font1.setBold(True)
        self.home_title.setFont(font1)
        self.home_title.setStyleSheet(u"")
        self.home_title.setText(u"Aplica\u00e7\u00e3o Servi\u00e7o de Mesa")
        self.home_title.setAlignment(Qt.AlignCenter)
        self.home_title.setMargin(10)

        self.verticalLayout_2.addWidget(self.home_title)

        self.resume = QTextEdit(self.home_page)
        self.resume.setObjectName(u"resume")
        font2 = QFont()
        font2.setPointSize(11)
        self.resume.setFont(font2)
        self.resume.setStyleSheet(u"")
        self.resume.setReadOnly(True)
        self.resume.setHtml(u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Esta aplica\u00e7\u00e3o foi desenvolvida com o intuito de simplificar a forma de lidar com diversos pedidos. Al\u00e9m disso, fornece algumas configura\u00e7\u00f5es para que a experiencia de todos seja a melhor.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; tex"
                        "t-indent:0px;\"><span style=\" font-size:12pt;\">Essas maravilhas s\u00e3o feitas atrav\u00e9s de um site que permite cada Atendente recolher o pedido de todos os Clientes e enviar para os pontos corretos. Posteriormente esses pedidos s\u00e3o processados pelos pontos e os respetivos Atendentes s\u00e3o informados que est\u00e1 pronto para levar aos Clientes.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Como j\u00e1 foi referido, existem algumas configura\u00e7\u00f5es simples entre elas pedidos semi-self-service (atrav\u00e9s de Qr Codes) e ativar ou desativar pontos de envio de pedidos ou configura\u00e7\u00f5es mais avan\u00e7adas como portas e hosts utilizados, mas seram melhor explicadas mais \u00e0 frente.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span s"
                        "tyle=\" font-size:12pt;\">Vamos come\u00e7ar a explica\u00e7\u00e3o mais detalhadas por Abas:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">        <span style=\" font-size:18pt;\">Atendentes</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Esta P\u00e1gina contem algumas fun\u00e7\u00f5es respons\u00e1veis por manipular quem tem acesso \u00e0 aplica\u00e7\u00e3o como Atendente. Para isso existem 3 formas de o fazer:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">-Adicionar Atendentes</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0p"
                        "x;\"><span style=\" font-size:12pt;\">-Remover Atendentes</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">-Ver Atendentes</span></p></body></html>")

        self.verticalLayout_2.addWidget(self.resume)

        self.start_stop_button_frame = QFrame(self.home_page)
        self.start_stop_button_frame.setObjectName(u"start_stop_button_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.start_stop_button_frame.sizePolicy().hasHeightForWidth())
        self.start_stop_button_frame.setSizePolicy(sizePolicy1)
        self.start_stop_button_frame.setStyleSheet(u"")
        self.start_stop_button_frame.setFrameShape(QFrame.StyledPanel)
        self.start_stop_button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.start_stop_button_frame)
        self.horizontalLayout_9.setSpacing(60)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 3, -1, 1)
        self.close_btn = QPushButton(self.start_stop_button_frame)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setFont(font2)
        self.close_btn.setStyleSheet(u"")
        self.close_btn.setText(u"Sair")

        self.horizontalLayout_9.addWidget(self.close_btn)

        self.start_btn = QPushButton(self.start_stop_button_frame)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setFont(font2)
        self.start_btn.setStyleSheet(u"")
        self.start_btn.setText(u"Come\u00e7ar")

        self.horizontalLayout_9.addWidget(self.start_btn)


        self.verticalLayout_2.addWidget(self.start_stop_button_frame)

        self.pages.addWidget(self.home_page)
        self.usesr_page = QWidget()
        self.usesr_page.setObjectName(u"usesr_page")
        self.horizontalLayout_2 = QHBoxLayout(self.usesr_page)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_2 = QFrame(self.usesr_page)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.users_title = QLabel(self.frame_2)
        self.users_title.setObjectName(u"users_title")
        self.users_title.setFont(font1)
        self.users_title.setStyleSheet(u"")
        self.users_title.setText(u"Escolher Atendentes")
        self.users_title.setAlignment(Qt.AlignCenter)
        self.users_title.setMargin(5)

        self.verticalLayout_3.addWidget(self.users_title)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.add_atend = QPushButton(self.frame_5)
        self.add_atend.setObjectName(u"add_atend")
        font3 = QFont()
        font3.setPointSize(12)
        self.add_atend.setFont(font3)
        self.add_atend.setText(u"Adicionar Atendente")

        self.horizontalLayout_3.addWidget(self.add_atend)

        self.user_name = QLineEdit(self.frame_5)
        self.user_name.setObjectName(u"user_name")
        font4 = QFont()
        font4.setPointSize(13)
        self.user_name.setFont(font4)
        self.user_name.setStyleSheet(u"")
        self.user_name.setText(u"")
        self.user_name.setPlaceholderText(u"Nome")
        self.user_name.setClearButtonEnabled(False)

        self.horizontalLayout_3.addWidget(self.user_name)


        self.verticalLayout_5.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy2)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_9 = QFrame(self.frame_4)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, -1, 0, -1)
        self.remove_atend = QPushButton(self.frame_9)
        self.remove_atend.setObjectName(u"remove_atend")
        self.remove_atend.setFont(font3)
        self.remove_atend.setText(u"Remover Atendentes Selecionados")

        self.horizontalLayout_8.addWidget(self.remove_atend)

        self.remove_all_atend = QPushButton(self.frame_9)
        self.remove_all_atend.setObjectName(u"remove_all_atend")
        self.remove_all_atend.setFont(font3)
        self.remove_all_atend.setText(u"Remover Todos os Atendentes")

        self.horizontalLayout_8.addWidget(self.remove_all_atend)


        self.verticalLayout_6.addWidget(self.frame_9)

        self.list_users = QListWidget(self.frame_4)
        self.list_users.setObjectName(u"list_users")
        self.list_users.setFont(font3)
        self.list_users.setStyleSheet(u"")
        self.list_users.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_users.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.list_users.setAlternatingRowColors(False)
        self.list_users.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_users.setSortingEnabled(True)

        self.verticalLayout_6.addWidget(self.list_users)


        self.verticalLayout_5.addWidget(self.frame_4)


        self.verticalLayout_3.addWidget(self.frame_3)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.pages.addWidget(self.usesr_page)
        self.menu_page = QWidget()
        self.menu_page.setObjectName(u"menu_page")
        self.verticalLayout_4 = QVBoxLayout(self.menu_page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.menu_title = QLabel(self.menu_page)
        self.menu_title.setObjectName(u"menu_title")
        self.menu_title.setFont(font1)
        self.menu_title.setStyleSheet(u"")
        self.menu_title.setText(u"Definir Menu")
        self.menu_title.setAlignment(Qt.AlignCenter)
        self.menu_title.setMargin(10)

        self.verticalLayout_4.addWidget(self.menu_title)

        self.tabs_page = QTabWidget(self.menu_page)
        self.tabs_page.setObjectName(u"tabs_page")
        self.tabs_page.setStyleSheet(u"")
        self.comida_tab = QWidget()
        self.comida_tab.setObjectName(u"comida_tab")
        self.verticalLayout_7 = QVBoxLayout(self.comida_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame_6 = QFrame(self.comida_tab)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy1.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy1)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 12, 0, -1)
        self.add_comida = QPushButton(self.frame_6)
        self.add_comida.setObjectName(u"add_comida")
        self.add_comida.setMinimumSize(QSize(150, 0))
        self.add_comida.setFont(font3)
        self.add_comida.setCursor(QCursor(Qt.ArrowCursor))
        self.add_comida.setText(u"Adicionar Comida")

        self.horizontalLayout_4.addWidget(self.add_comida)

        self.comida_name = QLineEdit(self.frame_6)
        self.comida_name.setObjectName(u"comida_name")
        self.comida_name.setFont(font4)
        self.comida_name.setStyleSheet(u"")
        self.comida_name.setText(u"")
        self.comida_name.setPlaceholderText(u"Comida")
        self.comida_name.setClearButtonEnabled(False)

        self.horizontalLayout_4.addWidget(self.comida_name)

        self.comida_price = QLineEdit(self.frame_6)
        self.comida_price.setObjectName(u"comida_price")
        self.comida_price.setMinimumSize(QSize(62, 0))
        self.comida_price.setMaximumSize(QSize(62, 16777215))
        self.comida_price.setFont(font4)
        self.comida_price.setStyleSheet(u"")
        self.comida_price.setInputMethodHints(Qt.ImhNone)
        self.comida_price.setText(u"")
        self.comida_price.setPlaceholderText(u"Pre\u00e7o")

        self.horizontalLayout_4.addWidget(self.comida_price)


        self.verticalLayout_7.addWidget(self.frame_6)

        self.remove_comida = QPushButton(self.comida_tab)
        self.remove_comida.setObjectName(u"remove_comida")
        self.remove_comida.setMinimumSize(QSize(150, 0))
        self.remove_comida.setFont(font3)
        self.remove_comida.setCursor(QCursor(Qt.ArrowCursor))
        self.remove_comida.setText(u"Remover Toda a Comida")

        self.verticalLayout_7.addWidget(self.remove_comida)

        self.comida_list = QScrollArea(self.comida_tab)
        self.comida_list.setObjectName(u"comida_list")
        sizePolicy.setHeightForWidth(self.comida_list.sizePolicy().hasHeightForWidth())
        self.comida_list.setSizePolicy(sizePolicy)
        self.comida_list.setStyleSheet(u"")
        self.comida_list.setWidgetResizable(True)
        self.scroll_comida = QWidget()
        self.scroll_comida.setObjectName(u"scroll_comida")
        self.scroll_comida.setGeometry(QRect(0, 0, 98, 28))
        self.comida_list.setWidget(self.scroll_comida)

        self.verticalLayout_7.addWidget(self.comida_list)

        self.tabs_page.addTab(self.comida_tab, "")
        self.tabs_page.setTabText(self.tabs_page.indexOf(self.comida_tab), u"Comida")
        self.bebida_tab = QWidget()
        self.bebida_tab.setObjectName(u"bebida_tab")
        self.verticalLayout_10 = QVBoxLayout(self.bebida_tab)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame_8 = QFrame(self.bebida_tab)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy1.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy1)
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 12, 0, -1)
        self.add_bebida = QPushButton(self.frame_8)
        self.add_bebida.setObjectName(u"add_bebida")
        self.add_bebida.setMinimumSize(QSize(150, 0))
        self.add_bebida.setFont(font3)
        self.add_bebida.setCursor(QCursor(Qt.ArrowCursor))
        self.add_bebida.setText(u"Adicionar Bebida")

        self.horizontalLayout_5.addWidget(self.add_bebida)

        self.bebida_name = QLineEdit(self.frame_8)
        self.bebida_name.setObjectName(u"bebida_name")
        self.bebida_name.setFont(font4)
        self.bebida_name.setStyleSheet(u"")
        self.bebida_name.setText(u"")
        self.bebida_name.setPlaceholderText(u"Bebida")
        self.bebida_name.setClearButtonEnabled(False)

        self.horizontalLayout_5.addWidget(self.bebida_name)

        self.bebida_price = QLineEdit(self.frame_8)
        self.bebida_price.setObjectName(u"bebida_price")
        self.bebida_price.setMinimumSize(QSize(62, 0))
        self.bebida_price.setMaximumSize(QSize(62, 16777215))
        self.bebida_price.setFont(font4)
        self.bebida_price.setStyleSheet(u"")
        self.bebida_price.setText(u"")
        self.bebida_price.setPlaceholderText(u"Pre\u00e7o")

        self.horizontalLayout_5.addWidget(self.bebida_price)


        self.verticalLayout_10.addWidget(self.frame_8)

        self.remove_bebida = QPushButton(self.bebida_tab)
        self.remove_bebida.setObjectName(u"remove_bebida")
        self.remove_bebida.setMinimumSize(QSize(150, 0))
        self.remove_bebida.setFont(font3)
        self.remove_bebida.setCursor(QCursor(Qt.ArrowCursor))
        self.remove_bebida.setText(u"Remover Toda a Bebida")

        self.verticalLayout_10.addWidget(self.remove_bebida)

        self.bebida_list = QScrollArea(self.bebida_tab)
        self.bebida_list.setObjectName(u"bebida_list")
        sizePolicy.setHeightForWidth(self.bebida_list.sizePolicy().hasHeightForWidth())
        self.bebida_list.setSizePolicy(sizePolicy)
        self.bebida_list.setStyleSheet(u"")
        self.bebida_list.setWidgetResizable(True)
        self.scroll_bebida = QWidget()
        self.scroll_bebida.setObjectName(u"scroll_bebida")
        self.scroll_bebida.setGeometry(QRect(0, 0, 98, 28))
        self.bebida_list.setWidget(self.scroll_bebida)

        self.verticalLayout_10.addWidget(self.bebida_list)

        self.tabs_page.addTab(self.bebida_tab, "")
        self.tabs_page.setTabText(self.tabs_page.indexOf(self.bebida_tab), u"Bebida")

        self.verticalLayout_4.addWidget(self.tabs_page)

        self.pages.addWidget(self.menu_page)
        self.access_page = QWidget()
        self.access_page.setObjectName(u"access_page")
        self.verticalLayout_11 = QVBoxLayout(self.access_page)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.access_title = QLabel(self.access_page)
        self.access_title.setObjectName(u"access_title")
        self.access_title.setFont(font1)
        self.access_title.setStyleSheet(u"")
        self.access_title.setText(u"Acessos do Servi\u00e7o")
        self.access_title.setAlignment(Qt.AlignCenter)
        self.access_title.setMargin(10)

        self.verticalLayout_11.addWidget(self.access_title)

        self.access_frame = QFrame(self.access_page)
        self.access_frame.setObjectName(u"access_frame")
        sizePolicy2.setHeightForWidth(self.access_frame.sizePolicy().hasHeightForWidth())
        self.access_frame.setSizePolicy(sizePolicy2)
        self.access_frame.setStyleSheet(u"")
        self.access_frame.setFrameShape(QFrame.StyledPanel)
        self.access_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_11.addWidget(self.access_frame)

        self.pages.addWidget(self.access_page)
        self.network_page = QWidget()
        self.network_page.setObjectName(u"network_page")
        self.verticalLayout_13 = QVBoxLayout(self.network_page)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.network_title = QLabel(self.network_page)
        self.network_title.setObjectName(u"network_title")
        self.network_title.setFont(font1)
        self.network_title.setStyleSheet(u"")
        self.network_title.setText(u"Rede da Aplica\u00e7\u00e3o")
        self.network_title.setAlignment(Qt.AlignCenter)
        self.network_title.setMargin(5)

        self.verticalLayout_13.addWidget(self.network_title)

        self.enable_network_frame = QFrame(self.network_page)
        self.enable_network_frame.setObjectName(u"enable_network_frame")
        sizePolicy2.setHeightForWidth(self.enable_network_frame.sizePolicy().hasHeightForWidth())
        self.enable_network_frame.setSizePolicy(sizePolicy2)
        self.enable_network_frame.setFrameShape(QFrame.StyledPanel)
        self.enable_network_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_13.addWidget(self.enable_network_frame)

        self.frame_10 = QFrame(self.network_page)
        self.frame_10.setObjectName(u"frame_10")
        sizePolicy2.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy2)
        self.frame_10.setStyleSheet(u"")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.domain_name = QLineEdit(self.frame_10)
        self.domain_name.setObjectName(u"domain_name")
        font5 = QFont()
        font5.setPointSize(14)
        self.domain_name.setFont(font5)
        self.domain_name.setStyleSheet(u"")
        self.domain_name.setText(u"")
        self.domain_name.setPlaceholderText(u"dominio-de-teste")

        self.gridLayout.addWidget(self.domain_name, 0, 1, 1, 1)

        self.domain_label = QLabel(self.frame_10)
        self.domain_label.setObjectName(u"domain_label")
        self.domain_label.setFont(font5)
        self.domain_label.setText(u"Dominio:")

        self.gridLayout.addWidget(self.domain_label, 0, 0, 1, 1)

        self.port_number = QLineEdit(self.frame_10)
        self.port_number.setObjectName(u"port_number")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.port_number.sizePolicy().hasHeightForWidth())
        self.port_number.setSizePolicy(sizePolicy3)
        self.port_number.setFont(font5)
        self.port_number.setText(u"")
        self.port_number.setPlaceholderText(u"8080")

        self.gridLayout.addWidget(self.port_number, 1, 1, 1, 1)

        self.port_label = QLabel(self.frame_10)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setFont(font5)
        self.port_label.setText(u"Porta")

        self.gridLayout.addWidget(self.port_label, 1, 0, 1, 1)


        self.verticalLayout_13.addWidget(self.frame_10)

        self.pages.addWidget(self.network_page)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_8 = QVBoxLayout(self.page)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.settings_title = QLabel(self.page)
        self.settings_title.setObjectName(u"settings_title")
        self.settings_title.setFont(font1)
        self.settings_title.setStyleSheet(u"")
        self.settings_title.setText(u"Rede da Aplica\u00e7\u00e3o")
        self.settings_title.setAlignment(Qt.AlignCenter)
        self.settings_title.setMargin(5)

        self.verticalLayout_8.addWidget(self.settings_title)

        self.frame_11 = QFrame(self.page)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy2.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy2)
        self.frame_11.setStyleSheet(u"")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_11)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.settings_frame = QFrame(self.frame_11)
        self.settings_frame.setObjectName(u"settings_frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.settings_frame.sizePolicy().hasHeightForWidth())
        self.settings_frame.setSizePolicy(sizePolicy4)
        self.settings_frame.setFrameShape(QFrame.StyledPanel)
        self.settings_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.settings_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.colors_label = QLabel(self.settings_frame)
        self.colors_label.setObjectName(u"colors_label")
        self.colors_label.setFont(font5)
        self.colors_label.setText(u"Modo")

        self.gridLayout_2.addWidget(self.colors_label, 0, 0, 1, 1)

        self.color_name = QComboBox(self.settings_frame)
        self.color_name.addItem(u"Amarelo")
        self.color_name.addItem(u"Verde")
        self.color_name.addItem(u"Azul")
        self.color_name.addItem(u"Vermelho")
        self.color_name.addItem(u"Roxo")
        self.color_name.setObjectName(u"color_name")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.color_name.sizePolicy().hasHeightForWidth())
        self.color_name.setSizePolicy(sizePolicy5)
        self.color_name.setFont(font5)
        self.color_name.setCurrentText(u"Amarelo")

        self.gridLayout_2.addWidget(self.color_name, 0, 1, 1, 1)

        self.themes_label = QLabel(self.settings_frame)
        self.themes_label.setObjectName(u"themes_label")
        self.themes_label.setFont(font5)
        self.themes_label.setText(u"Cor")

        self.gridLayout_2.addWidget(self.themes_label, 1, 0, 1, 1)

        self.theme_name = QComboBox(self.settings_frame)
        self.theme_name.addItem(u"Escuro")
        self.theme_name.addItem(u"Claro")
        self.theme_name.setObjectName(u"theme_name")
        self.theme_name.setFont(font5)
        self.theme_name.setEditable(False)
        self.theme_name.setCurrentText(u"Escuro")

        self.gridLayout_2.addWidget(self.theme_name, 1, 1, 1, 1)


        self.verticalLayout_12.addWidget(self.settings_frame)

        self.frame_13 = QFrame(self.frame_11)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy6)
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_13)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.save_all = QPushButton(self.frame_13)
        self.save_all.setObjectName(u"save_all")
        self.save_all.setFont(font4)
        self.save_all.setStyleSheet(u"")
        self.save_all.setText(u"Guardar Tudo")

        self.verticalLayout_9.addWidget(self.save_all)


        self.verticalLayout_12.addWidget(self.frame_13)


        self.verticalLayout_8.addWidget(self.frame_11)

        self.pages.addWidget(self.page)

        self.horizontalLayout.addWidget(self.pages)


        self.verticalLayout_16.addWidget(self.window)

        self.bottom_bar = QFrame(self.mainFrame)
        self.bottom_bar.setObjectName(u"bottom_bar")
        sizePolicy2.setHeightForWidth(self.bottom_bar.sizePolicy().hasHeightForWidth())
        self.bottom_bar.setSizePolicy(sizePolicy2)
        self.bottom_bar.setMaximumSize(QSize(16777215, 20))
        self.bottom_bar.setStyleSheet(u"")
        self.bottom_bar.setFrameShape(QFrame.StyledPanel)
        self.bottom_bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.bottom_bar)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.version_frame = QFrame(self.bottom_bar)
        self.version_frame.setObjectName(u"version_frame")
        sizePolicy4.setHeightForWidth(self.version_frame.sizePolicy().hasHeightForWidth())
        self.version_frame.setSizePolicy(sizePolicy4)
        self.version_frame.setMinimumSize(QSize(50, 0))
        self.version_frame.setMaximumSize(QSize(50, 20))
        self.version_frame.setStyleSheet(u"")
        self.version_frame.setFrameShape(QFrame.StyledPanel)
        self.version_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.version_frame)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.version_label = QLabel(self.version_frame)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.version_label.sizePolicy().hasHeightForWidth())
        self.version_label.setSizePolicy(sizePolicy4)
        self.version_label.setMinimumSize(QSize(54, 0))
        self.version_label.setMaximumSize(QSize(54, 16777215))
        self.version_label.setStyleSheet(u"")
        self.version_label.setText(u"v2.5")
        self.version_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.version_label)


        self.horizontalLayout_6.addWidget(self.version_frame)

        self.right_bottom_bar = QFrame(self.bottom_bar)
        self.right_bottom_bar.setObjectName(u"right_bottom_bar")
        self.right_bottom_bar.setStyleSheet(u"")
        self.right_bottom_bar.setFrameShape(QFrame.StyledPanel)
        self.right_bottom_bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.right_bottom_bar)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.horizontalLayout_6.addWidget(self.right_bottom_bar)


        self.verticalLayout_16.addWidget(self.bottom_bar)


        self.verticalLayout_15.addWidget(self.mainFrame)


        self.retranslateUi(MainWidget)

        self.pages.setCurrentIndex(1)
        self.list_users.setCurrentRow(-1)
        self.tabs_page.setCurrentIndex(0)
        self.color_name.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        pass
    # retranslateUi

