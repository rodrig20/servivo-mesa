import socket
import json
import os

#Class para configurar servidor
class ConfigServer:
    def __init__(self, widget=None):
        self.final = 0
        self.run_loophole = 1
        self.config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\config\\"
        self.menuline = widget
        
    def save_config(self,page):
        #Save Users
        with open(self.config_path+"users.txt","w",encoding="utf-8") as u:
            for i in range(page.ui.list_users.count()):
                u.write((page.ui.list_users.item(i).text())+"\n")
                
        #Save Menu
        menu = {"Comida":{},"Bebida":{}}
        for line in page.ui.scroll_comida.findChildren(self.menuline):
            nome = line["name"]
            price = line["price"]
            menu["Comida"][nome] = price
        for line in page.ui.scroll_bebida.findChildren(self.menuline):
            nome = line["name"]
            price = line["price"]
            menu["Bebida"][nome] = price
        
        with open(self.config_path+"menu.json","w",encoding="utf-8") as m:
            json.dump(menu, m,indent=4)
        
        #Save network and access 
        network_access_Config = {}
        network_access_Config["enable_Cozinha"] = page.enable_cozinha.isChecked()
        network_access_Config["enable_Bar"] = page.enable_bar.isChecked()
        network_access_Config["enable_QrCode"] = page.enable_QrCode.isChecked()
        network_access_Config["enable_local"] = page.enable_local.isChecked()
        network_access_Config["enable_loophole"] = page.enable_loophole.isChecked()
        
        domain = page.ui.domain_name.text().strip()
        network_access_Config["domain"] = domain
        
        port = page.ui.port_number.text()
        network_access_Config["port"] = port
        
        with open(page.config_path+"network_access.json","w",encoding="utf-8") as na:
            json.dump(network_access_Config, na,indent=4)
            
        self.prepare_config(network_access_Config)
    
    def prepare_config(self,network_access_Config):
        self.urls = []
        self.type = []
        self.access = {}
        #Loophole
        if network_access_Config["enable_loophole"]:
            if network_access_Config["domain"].strip() == "":
                network_access_Config["domain"] = "dominio-de-teste"
            else:
                network_access_Config["domain"] = network_access_Config["domain"].strip().replace(" ","-").lower()
            self.urls.append(network_access_Config["domain"])
            self.type.append("loophole")
            self.host = "localhost"
        #Acesso dentro da rede
        if network_access_Config["enable_local"]:
            self.urls.append(socket.gethostbyname(socket.gethostname()))
            self.type.append("same_network")
            self.host = "0.0.0.0"
            
        #Acesso apenas na maquina local     
        if not network_access_Config["enable_loophole"] and not network_access_Config["enable_local"]:
            self.urls.append("127.0.0.1")
            self.type.append("local")
            self.host = "localhost"
        
        if network_access_Config["port"].strip() == "":
            self.port = 8080
        else:
            self.port = int(network_access_Config["port"].strip())
        
        
        #Urls Acessiveis
        self.access["Cozinha"] = network_access_Config["enable_Cozinha"]
        self.access["Bar"] = network_access_Config["enable_Bar"]
        self.access["QrCode"] = network_access_Config["enable_QrCode"]
        
    def get_info(self):
         #Load Users
        try:
            with open(self.config_path+"users.txt", 'r+',encoding="utf-8") as u:
                users = u.readlines()
        except FileNotFoundError:
            with open(self.config_path+"users.txt", 'w',encoding="utf-8"): 
                users = []
                
        #Load Menu
        try:
            with open(self.config_path+"menu.json", 'r+',encoding="utf-8") as m:
                menu = json.load(m)
        
        except FileNotFoundError:
            with open(self.config_path+"menu.json", 'w',encoding="utf-8"): 
                menu = {"Comida":{"":""},"Bebida":{"":""}}
                
        
        #Load Network
        try:
            with open(self.config_path+"network_access.json", 'r+',encoding="utf-8") as na:
                network = json.load(na)
        except FileNotFoundError:
            with open(self.config_path+"network_access.json", 'w',encoding="utf-8"):
                network = {"enable_Cozinha":1, "enable_Bar":0, "enable_QrCode":0, "enable_local":0, "enable_loophole": 0, "domain":"dominio-de-teste", "port":"8080"}
        
        return users, menu, network
        
    def load_page(self,page):
        #Load Users
        (users, menu, network) = self.get_info()
        for user in users:
            page.ui.list_users.addItem(user[:-1])
         
        #Load Menu
        for name, price in menu["Comida"].items():
            line = self.menuline(name,price,page)
            page.comida_box.insertWidget(0,line)
        for name, price in menu["Bebida"].items():
            line = self.menuline(name,price,page)
            page.bebida_box.insertWidget(0,line)
        
        #Load Network
        page.enable_cozinha.setChecked(network["enable_Cozinha"])
        page.enable_bar.setChecked(network["enable_Bar"])
        page.enable_QrCode.setChecked(network["enable_QrCode"])
        page.enable_local.setChecked(network["enable_local"])
        page.enable_loophole.setChecked(network["enable_loophole"])
        if network["domain"] != page.ui.domain_name.placeholderText():
            page.ui.domain_name.setText(network["domain"])
        if str(network["port"]) != page.ui.port_number.placeholderText():
            page.ui.port_number.setText(str(network["port"]))
    
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

        