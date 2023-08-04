from flask import  render_template, jsonify, url_for,abort, redirect, send_from_directory, session, request
from flask_socketio import Namespace, emit
from datetime import datetime, timedelta
from functools import wraps

from app import app, socketio, users, urls_info, password

class AtualizarPagina(Namespace):
    def on_connect(self):
        # Este evento é acionado quando um cliente se conecta ao namespace
        emit('connect')

class ListaTodosPedidos_Base:
    def __init__(self):
        self.pedidos = []
    
    def __iter__(self):
        return iter(self.pedidos)

    def append(self,pedido):
        self.pedidos.append(pedido)

class ListaTodosPedidos_Prontos(ListaTodosPedidos_Base):
    def append(self, pedido):
        for ped in self.pedidos:
            if ped.nome == pedido.nome:
                ped.acrescentar(pedido)
                return
        super().append(pedido)
    
    def getPedidoNome(self,nome):
        for pedido in self.pedidos:
            if pedido.nome == nome:
                return pedido.toArray()[1:]
        return []

    def removePedido(self,nome,num_sub_ped):
        for pedido in self.pedidos:
            if pedido[0] == nome:
                pedido[1].pop(num_sub_ped)
                pedido[2].pop(num_sub_ped)
                pedido[3].pop(num_sub_ped)
               
class ListaTodosPedidos_Espera(ListaTodosPedidos_Base):
    def getPedidoTipo(self,idx,tipo):
        for pedido in self.pedidos:
            if pedido.contemTipo(tipo):
                if idx==0:
                    return pedido
                idx-=1

class PedidoBase:
    def __init__(self,ped_quantidades,ped_nomes,mesa):
        self.ped_quantidades = ped_quantidades
        self.ped_nomes = ped_nomes
        self.mesa = mesa
        
class PedidoEspera(PedidoBase):
    def __init__(self,nome,ped_quantidades, ped_nomes, tipos, mesa):
        super().__init__(ped_quantidades, ped_nomes, mesa)
        self.nome = nome
        self.tipos = tipos
        
    def contemTipo(self,tipo):
        return tipo in self.tipos
    
    def removeTipo(self,idx,tipo):
        for t in range(len(self.tipos)):
            if self.tipos[t] == tipo:
                if idx == 0:
                    pedido = self.transformPronto(t)
                    self.removeIdx(t)
                    return pedido
                idx-=1    
                
    def removeIdx(self,idx):
        self.ped_quantidades.pop(idx)
        self.ped_nomes.pop(idx)
        self.tipos.pop(idx)
    
    def transformPronto(self,idx):
        return PedidoPronto(self.nome,[self.ped_quantidades[idx]],[self.ped_nomes[idx]],[self.mesa])    
       
    def listaTipo(self,tipo):
        pedido = [self.nome,[],[]]
        for i in range(len(self.tipos)):
            if self.tipos[i] == tipo:
                pedido[1].append(self.ped_quantidades[i])
                pedido[2].append(self.ped_nomes[i])
        if pedido[1] == []:
            return None
        else:
            return pedido
       
class PedidoPronto(PedidoBase):
    def __init__(self,nome,ped_quantidades, ped_nomes, mesa):
        super().__init__(ped_quantidades, ped_nomes, mesa)
        self.nome = nome
        
    def acrescentar(self,pedido):
        self.ped_quantidades.append(pedido.ped_quantidades[0])
        self.ped_nomes.append(pedido.ped_nomes[0])
        self.mesa.append(pedido.mesa[0])
    
    def __getitem__(self, indice):
        return self.toArray()[indice]
    
    def toArray(self):
        return [self.nome,self.ped_quantidades,self.ped_nomes,self.mesa]

def guardarPedido(nome):
    quantidade_pedido = (request.form.getlist('quant[]'))
    nome_pedido = (request.form.getlist('ped[]'))
    tipo_pedido =(request.form.getlist('tip[]'))
    mesa_pedido = request.form["mesa"]
    if mesa_pedido.strip() == '' or (not len(quantidade_pedido) == len(nome_pedido) == len(tipo_pedido)):
        return 0
    
    for i in range(len(tipo_pedido)):
        if nome_pedido[i].strip() == '' or quantidade_pedido[i].strip() == '':
            return 0
    
    pedido_atual = PedidoEspera(nome,quantidade_pedido,nome_pedido,tipo_pedido,mesa_pedido)
    pedidos_espera.append(pedido_atual)
    
    return 1

def createList(tipo):
    pedidos_area = []
    for pedido in pedidos_espera:
        pedido_process = pedido.listaTipo(tipo)
        if pedido_process != None:
            pedidos_area.append(pedido_process)
            
    return pedidos_area

def tornarPronto(pedido_idx,sub_pedido_idx,tip):
    pedido = pedidos_espera.getPedidoTipo(pedido_idx,tip)
    pedido_pronto = pedido.removeTipo(sub_pedido_idx,tip)
    pedidos_prontos.append(pedido_pronto)
    return pedido_pronto[0]

def setCache(folder,file,hours):
    cache_time = timedelta(hours=hours)

    now = datetime.now()
    expires = now + cache_time

    response = send_from_directory(folder, file)
    response.cache_control.max_age = cache_time.total_seconds()
    response.expires = expires

    #del response.cache_control.no_cache  # Remover o no-cache do cabeçalho Cache-Control
    
    return response
    
def login_required(required):
    def decorator(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            if bool('username' in session and session['username'] in users) == required:
                return original_function(*args, **kwargs)
            elif required:
                return redirect(url_for('login'))
            else:
                return redirect(url_for('servico'))
        return wrapper_function
    return decorator

def route_activated_factory(condition):
    def decorator(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            if isinstance(condition, dict):
                if app.config.get(condition.get(request.path, '_'),False):
                    return original_function(*args, **kwargs)
            else:
                if app.config.get(condition,False):
                    return original_function(*args, **kwargs)
            abort(404)
        return wrapper_function
    return decorator

def atualizarRotas(dicionario):
    app.config["Comida"] = dicionario.get("cozinha", False)
    app.config["Bebida"] = dicionario.get("bar", False)
    app.config["QrCode"] = dicionario.get("QrCode", False)

def createUserNamespace(basic_namespace,user_list):
    for user in user_list:
        socketio.on_namespace(AtualizarPagina(basic_namespace+"/"+user))

def createListNamespace(basic_namespace):
    if app.config["Comida"]:
        socketio.on_namespace(AtualizarPagina(basic_namespace+"/Comida"))
        print(basic_namespace+"/Comida")
    if app.config["Bebida"]:
        socketio.on_namespace(AtualizarPagina(basic_namespace+"/Bebida"))
        
"""
Problemas:
-Bruteforce login
-indicar tipos dos argumentos

"""

@socketio.on('updateProntos')
def handle_updateProntos(nome):
    print("/atualizarProntos/"+nome)
    emit('reloadPedidos', {"pedidos":pedidos_prontos.getPedidoNome(nome)}, broadcast=True, namespace="/atualizarProntos/"+nome)
    
@socketio.on('updateEspera')
def handle_updateEspera(tipo):
    print(tipo)
    emit('reloadPedidos', {"pedidos":createList(tipo)}, broadcast=True, namespace="/atualizarEspera/"+tipo)
 
@app.route('/static/<file_type>/<path:filename>')
def serve_static(file_type, filename):
    if file_type == 'js':
        static_dir = 'static/js'
        cache_duration = 6
    elif file_type == 'style':
        static_dir = 'static/style'
        cache_duration = 6
    elif file_type == 'images':
        static_dir = 'static/images'
        cache_duration = 24
    else:
        return "Tipo de arquivo inválido."

    return setCache(static_dir, filename, cache_duration)

@app.route("/servico", methods=['GET','POST'])
@login_required(True)
def servico():
    nome = session["username"]
    if request.method == "GET":
        return render_template("fazerPedido.html",nome=nome,urls_ativos=[urls_info["cozinha"],urls_info["bar"],urls_info["QrCode"]],opcoes_validas=todas_opcoes,preco_opcoes=preco_opcoes,pre_def=[[],[],[]])
    elif request.method == "POST":
        guardado = guardarPedido(nome)
        if guardado:
            if "Comida" in request.form.getlist('tip[]'):
                handle_updateEspera("Comida")
            if "Bebida" in request.form.getlist('tip[]'):
                handle_updateEspera("Bebida")
        return jsonify({'suc':guardado,'redirect':url_for('confirmar')})
    
@app.route("/confirmar", methods=['GET'])
@login_required(True)
def confirmar():
    if request.method == "GET":
        return render_template("confirmar.html")
    
@app.route("/prontos", methods=['GET', 'DELETE'])
@login_required(True)
def lista_pessoa():
    nome = session["username"]
    if request.method == "GET":
        return render_template("pedidosProntos.html",nome=nome,pedidos=pedidos_prontos.getPedidoNome(nome))
    elif request.method == "DELETE":
        dados = request.get_json()
        index = dados.get('localizacao')
        pedidos_prontos.removePedido(nome,index)
        return ''

@app.route("/scanQR", methods=['GET'])
@route_activated_factory("QrCode")
@login_required(True)
def scanQR():
    if request.method == "GET":
        return render_template("scanQR.html")

@app.route("/QrCode", methods=['GET'])
@route_activated_factory("QrCode")
def QrCode():
    if request.method == "GET":
        return render_template("mostarQR.html")

@app.route("/pedido-automatico", methods=['GET'])
@route_activated_factory("QrCode")
def pedidoAutomatico():
    if request.method == 'GET':
        return render_template("fazerPedido.html",urls_ativos=[urls_info["cozinha"],urls_info["bar"],urls_info["QrCode"]],opcoes_validas=todas_opcoes,preco_opcoes=preco_opcoes,pre_def=[[],[],[]])

@app.route('/lista/Comida', methods=['GET', 'PUT'])
@app.route('/lista/Bebida', methods=['GET', 'PUT'])
@route_activated_factory(dict([("/lista/Comida","Comida"),("/lista/Bebida","Bebida")]))
@login_required(True)
def listaCeB():
    tipo = request.path.replace("/lista/",'')
    if request.method == "GET":
        return render_template("pedidosEspera.html",pedidos=createList(tipo),tipo=tipo)
    
    elif request.method == "PUT":
        dados = request.get_json()
        numero_pedido = dados.get('numero_pedido')
        numero_sub_pedido = dados.get('numero_sub_pedido')-1 # Porque a contagem dos pedidos começa em 1 (então voltamos para 0)
        nome = tornarPronto(numero_pedido,numero_sub_pedido,tipo)
        handle_updateProntos(nome)
        return ''
            
@app.route('/login', methods=['GET', 'POST'])
@login_required(False)
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':    
        username = request.form['user']
        user_password = request.form['pass']
        if username in users and user_password == password:
            session["username"] = username
            session.permanent = True
            
            return jsonify({'suc':1,'redirect':url_for('servico')})
        return jsonify({'suc':0})

@app.route('/logout', methods=['GET', 'POST'])
@login_required(True)
def logout():
    if request.method == 'GET':
        session.pop("username")
        return redirect(url_for('login'))


pedidos_espera = ListaTodosPedidos_Espera()
pedidos_prontos = ListaTodosPedidos_Prontos()

atualizarRotas(urls_info)

createUserNamespace("/atualizarProntos",users)
createListNamespace("/atualizarEspera")


todas_opcoes = [['Cachorro sem Nada','Cachorro com Ketc. Most. Maio.', 'Cachorro com Ketc.', 'Cachorro com Maio.', 'Cachorro com Most.', 'Batata frita', 'Amendoins', 'Tremoços'], ['Água Fresca', 'Coca Cola', 'Limonada', 'Sumol']]
preco_opcoes = [[2.0, 2.0,2.0, 2.0, 2.0, 0.5, 0.5, 0.5], [0.35, 1.2, 0.5, 1.2]]


if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port=80,use_reloader=1,debug=1)
