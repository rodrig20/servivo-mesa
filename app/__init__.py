import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from flask_caching import Cache
from datetime import timedelta
from .loophole import *
from threading import Thread
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

def run_app(config,progress_callback):
    config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\config\\"
    progress_callback(5)
    try:
        with open(config_path+"users.txt", 'r+',encoding="utf-8") as u:
            users = u.readlines()
        for user in users:
            app.config["USERS"].append(user[:-1])  
    except FileNotFoundError:
        with open(config_path+"users.txt", 'w',encoding="utf-8"): pass
    progress_callback(10)
    app.config["USERS"].append("cozinha")
    app.config["USERS"].append("bar")
    try:
        with open(config_path+"menu.json", 'r+',encoding="utf-8") as m:
            menu = json.load(m)
        for name, price in menu["Comida"].items():
            app.config["MENU_NAME"][0].append(name)
            app.config["MENU_PRICE"][0].append(price)
        progress_callback(14)
        for name, price in menu["Bebida"].items():
            app.config["MENU_NAME"][1].append(name)
            app.config["MENU_PRICE"][1].append(price)
            
    except FileNotFoundError:
        with open(config_path+"menu.json", 'w',encoding="utf-8"): pass
    progress_callback(16)
    try:
        with open(config_path+"network_access.json", 'r+',encoding="utf-8") as u:
            acessos = json.load(u)
        app.config["URLS"]["cozinha"] = acessos["enable_Cozinha"]
        app.config["URLS"]["bar"] = acessos["enable_Bar"]
        app.config["URLS"]["QrCode"] = acessos["enable_QrCode"]
        port = acessos["port"]
        progress_callback(15)
        if acessos["enable_local"]:
            host = "0.0.0.0"
            config.links.append("0.0.0.0")
        else:
            config.links.append("127.0.0.1")
            host = "localhost"
        progress_callback(10)
        if acessos["enable_loophole"]:
            config.links.append(acessos["domain"])
            Thread(target=start_loophole, args=(config.links,port,progress_callback),daemon=True).start()
        else:
            progress_callback(15)
    except FileNotFoundError:
        with open(config_path+"network_access.json", 'w',encoding="utf-8"): pass
        app.config["URLS"]["cozinha"] = 1
        app.config["URLS"]["bar"] = 0
        app.config["URLS"]["QrCode"] = 0
        host = "localhost"
        port = 8080
    progress_callback(15)
    atualizarRotas(app.config["URLS"])
    socketio.run(app,host=host,port=port)

from app import routes
