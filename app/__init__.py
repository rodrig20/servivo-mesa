from engineio.async_drivers import (gevent)
from app.password import get_secret_key, get_password
from config.config import ConfigServer
from flask_socketio import SocketIO
from typing import List, Callable
from flask_caching import Cache
from datetime import timedelta
from threading import Thread
from flask import Flask
from .loophole import start_loophole
from PIL import Image
import os


def transform_to_png(image_path):
    im = Image.open(image_path)
    im.save(r"app\static\images\Menu.png")


app = Flask(__name__)
app.config['async_mode'] = 'gevent'
app.config['SECRET_KEY'] = get_secret_key()
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_KEY_PREFIX'] = 'file_'  # Prefixo para chaves de cache
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config["MAX_PASSWORD_TRIES_PER_MINUTE"] = 10

cache = Cache(app)

socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")
# Inicializar variaveis
app.config["URLS"] = {}
app.config["USERS"] = []
app.config["PASSWORD"] = ""
app.config["PASSWORD_TRIES"] = {}
app.config["MENU_NAME"] = [[], []]
app.config["MENU_PRICE"] = [[], []]


def run_app(config_server: ConfigServer) -> Callable:
    users, menu, _ = config_server.get_info()
    
    for user in users:
        app.config["USERS"].append(user[:-1])
    
    app.config["USERS"].append("Cozinha")
    app.config["USERS"].append("Bar")
    
    for name, price in menu["Comida"].items():
        app.config["MENU_NAME"][0].append(name)
        app.config["MENU_PRICE"][0].append(price)
    for name, price in menu["Bebida"].items():
        app.config["MENU_NAME"][1].append(name)
        app.config["MENU_PRICE"][1].append(price)
    
    file_path = menu["Menu_Img_File"]
    
    if "loophole" in config_server.type:
        domain = config_server.urls[config_server.type.index("loophole")]
    else:
        domain = "pass/Word"
    
    host = config_server.host
    port = config_server.port
    loop = 0
    for i in range(len(config_server.urls)):
        if config_server.type[i] == "loophole":
            Thread(target=start_loophole, args=(config_server, port, i), daemon=True).start()
            loop = 1
    if not loop:
        config_server.final = 1
        
    app.config["URLS"] = config_server.access
    if file_path and os.path.exists(file_path):
        transform_to_png(file_path)
        app.config["URLS"]["Menu_Img"] = True
    elif os.path.exists(r"app\static\images\Menu.png"):
        os.remove(r"app\static\images\Menu.png")
        app.config["URLS"]["Menu_Img"] = False
    else:
        app.config["URLS"]["Menu_Img"] = False
    
    app.config["PASSWORD"] = get_password(domain)
    config_server.password = app.config["PASSWORD"]
    createUserNamespace("/atualizarProntos", app.config["USERS"])
    createListNamespace("/atualizarEspera")
    return lambda: socketio.run(app, host=host, port=port)


from app import routes


def createUserNamespace(basic_namespace: str, user_list: List[str]) -> None:
    for user in user_list:
        socketio.on_namespace(routes.AtualizarPagina(basic_namespace + "/" + user))


def createListNamespace(basic_namespace: str) -> None:
    if app.config["URLS"]["Cozinha"]:
        socketio.on_namespace(routes.AtualizarPagina(basic_namespace + "/Cozinha"))
    if app.config["URLS"]["Bar"]:
        socketio.on_namespace(routes.AtualizarPagina(basic_namespace + "/Bar"))


app.config["PEDIDOS_ESPERA"] = routes.ListaTodosPedidos_Espera()
app.config["PEDIDOS_PRONTOS"] = routes.ListaTodosPedidos_Prontos()
