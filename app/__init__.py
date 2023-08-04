import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from flask_caching import Cache
from datetime import timedelta


app = Flask(__name__)

app.config['ASYNC_MODE'] = 'threading'
app.config['SECRET_KEY'] = '_Your_Secret_Key_'
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_KEY_PREFIX'] = 'file_'  # Prefixo para chaves de cache
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['SESSION_COOKIE_HTTPONLY'] = True

cache = Cache(app)

socketio= SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

users = []
urls_info = {"cozinha":1,"bar":0,"QrCode":1}
password = "Entrar"

from app import routes
