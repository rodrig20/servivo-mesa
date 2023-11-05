from flask import render_template, jsonify, url_for, abort, redirect, send_from_directory, session, request, Response
from werkzeug.datastructures import ImmutableMultiDict
from typing import List, Tuple, Literal, Callable, Union, Optional
from flask_socketio import Namespace, emit
from datetime import datetime, timedelta
from functools import wraps
# Coisas importantes para iniciar o servidor
from app import app, socketio


# Sempre que alguem se conectar tem a página atualizada
class AtualizarPagina(Namespace):
    def on_connect(self) -> None:
        # Este evento é acionado quando um cliente se conecta ao namespace
        emit('connect')


# Estrutura de um pedido básico
class PedidoBase:
    # Elementos básicos de um Pedido
    def __init__(self, nome: str, ped_quantidades: List[str], ped_nomes: List[str], mesa: str) -> None:
        self.nome: str = nome
        self.ped_quantidades: List[str] = ped_quantidades
        self.ped_nomes: List[str] = ped_nomes
        self.mesa: str = mesa


# Estrutura de um pedido que está em Espera
class PedidoEspera(PedidoBase):
    # Elementos básicos de um Pedido em Espera
    def __init__(self, nome: str, ped_quantidades: List[str], ped_nomes: List[str], tipos: List[Literal["Cozinha", "Bar"]], mesa: str) -> None:
        super().__init__(nome, ped_quantidades, ped_nomes, mesa)
        self.tipos = tipos
    
    # verificar se o pedido contem um certo tipo
    def contemTipo(self, tipo: Literal["Cozinha", "Bar"]) -> bool:
        return tipo in self.tipos
    
    # remover o idx-esimo elemento de um certo tipo e retorna o mesmo
    def removeTipo(self, idx: int, tipo: Literal["Cozinha", "Bar"]) -> Union[None, "PedidoPronto"]:
        for t in range(len(self.tipos)):
            if self.tipos[t] == tipo:
                if idx == 0:
                    pedido = self.transformarPronto(t)
                    return pedido
                idx -= 1
        return None
    
    # remover subpedido de um certo pedido
    def removeIdx(self, idx: int) -> None:
        self.ped_quantidades.pop(idx)
        self.ped_nomes.pop(idx)
        self.tipos.pop(idx)
    
    # transformar o pedido em espera em um pedido pronto
    def transformarPronto(self, idx: int) -> "PedidoPronto":
        pedido = PedidoPronto(self.nome, [self.ped_quantidades[idx]], [self.ped_nomes[idx]], self.mesa)
        self.removeIdx(idx)
        return pedido
    
    # retornar todos os subpedidos de um certo tipo
    def listaTipo(self, tipo: Literal["Cozinha", "Bar"]) -> Optional[List[Union[str, List[str]]]]:
        quatidades = []
        nomes = []
        for i in range(len(self.tipos)):
            if self.tipos[i] == tipo:
                quatidades.append(self.ped_quantidades[i])
                nomes.append(self.ped_nomes[i])
        if quatidades == []:  # se não houver nenhum pedido
            return None
        else:
            return [self.nome, quatidades, nomes]


# Estrutura de um pedido que está em Pedido
class PedidoPronto(PedidoBase):
    # Elementos básicos de um Pedido Pronto
    def __init__(self, nome: str, ped_quantidades: List[str], ped_nomes: List[str], mesa: str) -> None:
        super().__init__(nome, ped_quantidades, ped_nomes, mesa)
        self.mesas = []
        self.mesas.append(mesa)
    
    # acrescentar um subpedido ao nome
    def mergePedidoPronto(self, pedido: "PedidoPronto") -> None:
        self.ped_quantidades.append(pedido.ped_quantidades[0])
        self.ped_nomes.append(pedido.ped_nomes[0])
        self.mesas.append(pedido.mesa)
    
    # obter parte do pedido
    def __getitem__(self, indice: int) -> List[str]:
        return self.toArray()[indice]
    
    # obter o nome de quem fez o pedido
    def getNome(self):
        return self.nome
    
    # transformar o pedido em array
    def toArray(self) -> Tuple[List[str], List[str], List[str]]:
        return (self.ped_quantidades, self.ped_nomes, self.mesas)
    

# Lista de pedidos em espera
class ListaTodosPedidos_Espera:
    def __init__(self) -> None:
        self.pedidos: List[PedidoEspera] = []
        
    # acrescentar pedido à lista
    def add(self, info: ImmutableMultiDict, nome: str):
        # obter a informação
        quantidade_pedido = info.getlist('quant[]')
        nome_pedido = info.getlist('ped[]')
        tipo_pedido = info.getlist('tip[]')
        mesa_pedido = info["mesa"]
        
        # verificar se é um pedido válido
        if mesa_pedido.strip() == '' or (not len(quantidade_pedido) == len(nome_pedido) == len(tipo_pedido)):
            return False
        for i in range(len(tipo_pedido)):
            if nome_pedido[i].strip() == '' or quantidade_pedido[i].strip() == '':
                return False
        
        # Criar um pedido e adiconar o mesmo à lista
        self.pedidos.append(PedidoEspera(nome, quantidade_pedido, nome_pedido, tipo_pedido, mesa_pedido))
        
        return True
    
    # tornar um pedido pronto
    def tornarPronto(self, pedido_idx: int, sub_pedido_idx: int, tipo: Literal["Cozinha", "Bar"]) -> None:
        # obter o subpedido pelo idx e tipo e trocalo de posição
        pedido = self.getPedidoTipo(pedido_idx, tipo)
        if pedido is not None:
            pedido_pronto = pedido.removeTipo(sub_pedido_idx, tipo)
            app.config["PEDIDOS_PRONTOS"].append(pedido_pronto)
    
    # função responsavel por criar uma lista com pedidos em espera
    def createList(self, tipo: Literal["Cozinha", "Bar"]):
        pedidos_area = []
        for pedido in self.pedidos:
            pedido_process = pedido.listaTipo(tipo)
            # adicionar o pedido com apenas o tipo especificado
            if pedido_process is not None:
                pedidos_area.append(pedido_process)
                
        return pedidos_area
    
    # retornar pedidos de um certo tipo
    def getPedidoTipo(self, idx: int, tipo: Literal["Cozinha", "Bar"]):
        for pedido in self.pedidos:
            if pedido.contemTipo(tipo):  # percorrer até chegar ao pedido do indice
                if idx == 0:
                    return pedido
                idx -= 1


# Lista para os pedidos que já estão prontos para entrega
class ListaTodosPedidos_Prontos:
    def __init__(self) -> None:
        self.pedidos: List[PedidoPronto] = []
    
    # adicionar de forma a juntar todos os pedidos do mesmo atendente
    def append(self, pedido: PedidoPronto):
        for ped in self.pedidos:
            if ped.nome == pedido.nome:
                ped.mergePedidoPronto(pedido)
                return
        # caso o atendente não exista é acrescentado normalmente
        self.pedidos.append(pedido)
    
    # procurar na lista pedidos pelos pedidos de um determinado nome
    def getPedidoNome(self, nome: str):
        for pedido in self.pedidos:
            if pedido.nome == nome:
                # retornar pedido sem nome
                return pedido.toArray()
        return []

    # remover pedido
    def removePedido(self, nome: str, num_sub_ped: int):
        for pedido in self.pedidos:
            # remover subpedido do nome
            if pedido.getNome() == nome:
                pedido[0].pop(num_sub_ped)
                pedido[1].pop(num_sub_ped)
                pedido[2].pop(num_sub_ped)
                return


# Colocar ficheiros em cache
def setCache(folder: str, file: str, hours: float):
    # calcular o data de expiração
    cache_time = timedelta(hours=hours)
    now = datetime.now()
    expires = now + cache_time
    # enviar o ficheiro
    response = send_from_directory(folder, file)
    response.cache_control.max_age = int(cache_time.total_seconds())
    response.expires = expires

    del response.cache_control.no_cache  # Remover o no-cache do cabeçalho Cache-Control
    
    return response


# decorador que define se é ou não necessario estar com login
def login_required(required: bool):
    def decorator(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            # verificar a condição de login
            if bool('username' in session and session['username'] in app.config["USERS"]) == required:
                return original_function(*args, **kwargs)
            # se não retornar para onde for necesidade
            elif required:
                return redirect(url_for('login'))
            else:
                return redirect(url_for('servico'))
        return wrapper_function
    return decorator


# decorador de ativação de rotas
def route_activated_factory(*args: str):
    condition = args
    
    def decorator(original_function: Callable):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            # verificar se os caminhos estão ativos
            if len(condition) > 1:
                tipo = request.path.replace("/lista/", "")
                if tipo in condition and app.config["URLS"].get(tipo, False):
                    return original_function(*args, **kwargs)
            else:
                if app.config["URLS"].get(condition[0], False):
                    return original_function(*args, **kwargs)
            abort(404)
        return wrapper_function
    return decorator


# enviar para o atendente os pedidos que já estão prontos
@socketio.on('updateProntos')
def handle_updateProntos(nome: str):
    emit('reloadPedidos', {"pedidos": app.config["PEDIDOS_PRONTOS"].getPedidoNome(nome)}, broadcast=True, namespace="/atualizarProntos/" + nome)


# enviar as informações dos pedidos de um certo tipo para os respetivos pontos
@socketio.on('updateEspera')
def handle_updateEspera(tipo: str):
    emit('reloadPedidos', {"pedidos": app.config["PEDIDOS_ESPERA"].createList(tipo)}, broadcast=True, namespace="/atualizarEspera/" + tipo)


# rota para enviar os ficheiros estaticos (js, style, images)
@app.route('/static/<file_type>/<path:filename>')
def serve_static(file_type: str, filename: str) -> Union[str, Response]:
    if file_type == 'js':
        static_dir = 'static/js'
        cache_duration = 24
    elif file_type == 'style':
        static_dir = 'static/style'
        cache_duration = 24
    elif file_type == 'images':
        static_dir = 'static/images'
        cache_duration = 24
    else:
        return "Tipo de arquivo inválido."

    return setCache(static_dir, filename, cache_duration)


# rota principal
@app.route("/servico", methods=['GET', 'POST'])
@login_required(True)
def servico():
    nome = session["username"]
    # retornar html
    if request.method == "GET":
        return render_template("fazerPedido.html", nome=nome, urls_ativos=app.config["URLS"], opcoes_validas=app.config["MENU_NAME"], preco_opcoes=app.config["MENU_PRICE"])
    elif request.method == "POST":
        # tentar guardar pedido em espera
        if guardado := app.config["PEDIDOS_ESPERA"].add(request.form, nome):
            # atulizar pontos
            if "Cozinha" in request.form.getlist('tip[]'):
                handle_updateEspera("Cozinha")
            if "Bar" in request.form.getlist('tip[]'):
                handle_updateEspera("Bar")
        return jsonify({'suc': guardado, 'redirect': url_for('confirmar')})


# rota janela confirmação de envio de pedido
@app.route("/confirmar", methods=['GET'])
@login_required(True)
def confirmar():
    # retornar html
    if request.method == "GET":
        return render_template("confirmar.html")


# rota com os pedidos prontos de cada atendente
@app.route("/prontos", methods=['GET', 'DELETE'])
@login_required(True)
def lista_pessoa():
    nome = session["username"]
    # retornar html
    if request.method == "GET":
        return render_template("pedidosProntos.html", nome=nome, pedidos=app.config["PEDIDOS_PRONTOS"].getPedidoNome(nome))
    # apagar o pedido
    elif request.method == "DELETE":
        # remover pedido
        dados = request.get_json()
        index = dados.get('sub_idx')
        app.config["PEDIDOS_PRONTOS"].removePedido(nome, index)
        return ''


# rota responsavel por scanear o QrCode
@app.route("/scanQR", methods=['GET'])
@route_activated_factory("QrCode")
@login_required(True)
def scanQR():
    # retornar html
    if request.method == "GET":
        return render_template("scanQR.html")


# rota resposnaavel por mostrar um QrCode para fazer scan
@app.route("/QrCode", methods=['GET'])
@route_activated_factory("QrCode")
def QrCode():
    # retornar html
    if request.method == "GET":
        return render_template("mostarQR.html")


# rota resposanavel por permitir os clientes gerarem um QeCode com o seu pedido
@app.route("/pedido-automatico", methods=['GET'])
@route_activated_factory("QrCode")
def pedidoAutomatico():
    return render_template("fazerPedido.html", urls_ativos=app.config["URLS"], opcoes_validas=app.config["MENU_NAME"], preco_opcoes=app.config["MENU_PRICE"])


# rota com os pontos onde são recebidos os pedidos
@app.route('/lista/Cozinha', methods=['GET', 'PUT'])
@app.route('/lista/Bar', methods=['GET', 'PUT'])
@route_activated_factory("Cozinha", "Bar")
@login_required(True)
def listaCeB():
    tipo = request.path.replace("/lista/", '')
    # retornar html
    if request.method == "GET":
        return render_template("pedidosEspera.html", pedidos=app.config["PEDIDOS_ESPERA"].createList(tipo), tipo=tipo)
    
    elif request.method == "PUT":
        # colocar o pedido como pronto
        dados = request.get_json()
        numero_pedido = dados.get('numero_pedido')
        numero_sub_pedido = dados.get('numero_sub_pedido')
        app.config["PEDIDOS_ESPERA"].tornarPronto(numero_pedido, numero_sub_pedido, tipo)
        handle_updateProntos(session["username"])
        return ''


@app.route('/menu', methods=['GET'])
@route_activated_factory("Menu_Img")
def menu():
    return render_template("menu.html")


# rota responsavel por autenticar o utilizador
@app.route('/login', methods=['GET', 'POST'])
@login_required(False)
def login():
    # retornar html
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        # obter credenciais
        username = request.form['user']
        user_password = request.form['pass']
        time = datetime.timestamp(datetime.now())
        # primeiro Login
        if username not in app.config["PASSWORD_TRIES"] or (app.config["PASSWORD_TRIES"][username] != [] and app.config["PASSWORD_TRIES"][username][-1] < 0 and -app.config["PASSWORD_TRIES"][username][-1] < time):
            app.config["PASSWORD_TRIES"][username] = []
        # verificar expiração de alguns tempos
        elif app.config["PASSWORD_TRIES"][username] != [] and app.config["PASSWORD_TRIES"][username][-1] >= 0:
            for e in range(len(app.config["PASSWORD_TRIES"][username]) - 1, 0, -1):
                if app.config["PASSWORD_TRIES"][username][e] > time:
                    app.config["PASSWORD_TRIES"][username].pop(-1)
                else:
                    break
        # verificar se o utilizador é premitido tentar fazer
        if len(app.config["PASSWORD_TRIES"][username]) < app.config["MAX_PASSWORD_TRIES_PER_MINUTE"]:
            if username in app.config["USERS"] and user_password == app.config["PASSWORD"]:
                app.config["PASSWORD_TRIES"][username] = []
                session["username"] = username
                session.permanent = True
                if username == "Cozinha" or username == "Bar":
                    return jsonify({'suc': 1, 'redirect': "/lista/" + username})
                else:
                    return jsonify({'suc': 1, 'redirect': url_for('servico')})
            # se não for permitido acrescentar o tempo
            else:
                if len(app.config["PASSWORD_TRIES"][username]) < app.config["MAX_PASSWORD_TRIES_PER_MINUTE"]:
                    app.config["PASSWORD_TRIES"][username].append(-(time + 90))
                else:
                    app.config["PASSWORD_TRIES"][username].append(time + 60)
                         
                return jsonify({'suc': 0, "erro": "nome de utilizador ou password incorreta"})

        return jsonify({'suc': 0, "erro": "numero máximo de tentativas atingidas"})


# rota responsavel por desautenticar utilizadores
@app.route('/logout', methods=['GET'])
@login_required(True)
def logout():
    session.pop("username")
    return redirect(url_for('login'))


# rota responsavel por redirecionar para o login
@app.route('/', methods=['GET'])
@login_required(True)
def redirect_to_login():
    return redirect(url_for('login'))
