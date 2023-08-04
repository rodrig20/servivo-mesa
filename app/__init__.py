import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from flask_caching import Cache
from datetime import timedelta
from .loophole import *
from multiprocessing import Process, Array
import os.path
import json

def atualizarRotas(dicionario):
    app.config["Comida"] = dicionario.get("cozinha", False)
    app.config["Bebida"] = dicionario.get("bar", False)
    app.config["QrCode"] = dicionario.get("QrCode", False)



app = Flask(__name__)

app.config['ASYNC_MODE'] = 'threading'
app.config['SECRET_KEY'] = 'Rio_'
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_KEY_PREFIX'] = 'file_'  # Prefixo para chaves de cache
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['SESSION_COOKIE_HTTPONLY'] = True

cache = Cache(app)

socketio= SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

app.config["USERS"] = []
app.config["MENU_NAME"] = [[],[]]
app.config["MENU_PRICE"] = [[],[]]
app.config["URLS"] = {}

password = "Entrar"

def run_app():
    config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\config\\"
    try:
        with open(config_path+"users.txt", 'r+',encoding="utf-8") as u:
            users = u.readlines()
        for user in users:
            app.config["USERS"].append(user[:-1])  
    except FileNotFoundError:
        with open(config_path+"users.txt", 'w',encoding="utf-8"): pass
    
    app.config["USERS"].append("cozinha")
    app.config["USERS"].append("bar")
    try:
        with open(config_path+"menu.json", 'r+',encoding="utf-8") as m:
            menu = json.load(m)
        for name, price in menu["Comida"].items():
            app.config["MENU_NAME"][0].append(name)
            app.config["MENU_PRICE"][0].append(price)
        for name, price in menu["Bebida"].items():
            app.config["MENU_NAME"][1].append(name)
            app.config["MENU_PRICE"][1].append(price)
            
    except FileNotFoundError:
        with open(config_path+"menu.json", 'w',encoding="utf-8"): pass
    try:
        with open(config_path+"network_access.json", 'r+',encoding="utf-8") as u:
            acessos = json.load(u)
        app.config["URLS"]["cozinha"] = acessos["enable_Cozinha"]
        app.config["URLS"]["bar"] = acessos["enable_Bar"]
        app.config["URLS"]["QrCode"] = acessos["enable_QrCode"]
        port = acessos["port"]
        if acessos["enable_local"]:
            host = "0.0.0.0"
        else:
            host = "localhost"
            
        domain = Array("c", acessos["domain"].encode()+b"__________")
        domain.value = acessos["domain"].encode()
        if acessos["enable_loophole"]:
            Process(target=start_loophole, args=(domain,port),daemon=True).start()
    except FileNotFoundError:
        with open(config_path+"network_access.json", 'w',encoding="utf-8"): pass
        app.config["URLS"]["cozinha"] = 1
        app.config["URLS"]["bar"] = 0
        app.config["URLS"]["QrCode"] = 0
        host = "localhost"
        port = 8080

    atualizarRotas(app.config["URLS"])
    
    socketio.run(app,host=host,port=port)

from app import routes
