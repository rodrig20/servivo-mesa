from flask import Flask, request, render_template, jsonify, url_for,abort, redirect, session
from flask_socketio import SocketIO, emit, Namespace
from engineio.async_drivers import gevent
from threading import Thread
from flask_settings import *   # script com de defenições basicas
from login_tunnel import *     # script com o loophole
import interface as inter      # script com interface grafica
from io import BytesIO
import datetime
import requests
import string
import random
import base64
import socket
import qrcode
import ast

# remover blur do ecrã
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except: 
    pass

""" """

# Iniciar Falsk app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['ASYNC_MODE'] = 'threading'
app.config['MAX_CONTENT_LENGTH'] = 30*1024*1024   # 30 MB
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=12)
socketio= SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

class ListasNamespace(Namespace):
    def on_reload(self):
        return

#função responsavel por iniciar o loophole
def startExternalAccess(subdomain,port,proc):
    login_loophole("tunnel","log.txt")
    for _ in range(5):
        proc[0] = start_loophole(subdomain,port)
        proc[0].wait()

def createList(tipo):
    global pedidos
    #criar uma lista com apenas os pedidos para o bar 
    tipoLista=[]
    j=0
    for p in pedidos:
        #copiar alguns dados para a nova lista
        ped=[p[0],[],[],[],[],p[-3],p[-1]]
        i=0
        existe=0
        #verificar cada sub-pedido para ver se pertence à bar
        for t in p[3]:
            if t==tipo:
                existe=1
                #se houver esse sub-pedido é adicionado à nova lista para o bar
                ped[1].append(p[1][i])
                ped[2].append(p[2][i])
                ped[3].append(p[3][i])
                ped[4].append(p[-2][i])
                
            i+=1
        if existe:
            #essa lista é adiconada à lista de todas as tipoLista
            tipoLista.append(ped)
        j+=1
        
    return tipoLista

def processarPedidos(nome,request):
    global pedidos,n,n_p
    try:
        #recebem respetivamente as quantidades, o que foi pedido e o tipo dos pedidos
        quant = (request.form.getlist('quant[]'))
        ped = (request.form.getlist('ped[]'))
        tipo=(request.form.getlist('tip[]'))
        mesa = request.form["mesa"]
        remove=[]
        #ler as linhas sem pedidos
        for i in range(len(quant)):
            if quant[i].strip() == '' or ped[i].strip() == '':
                remove.append(i)
        #para remover as mesmas
        remove.reverse()
        for i in remove:
            tipo.pop(i)
            quant.pop(i)
            ped.pop(i)

        #se o pedidio não for vazio
        if len(quant) != 0 and mesa.strip() != '':
            if nome != '':
                #adicionar mais 1 ao nº global do pedido 
                n+=1
                #calcular o numero individual do pedido
                list_n=[]
                for j in range(len(quant)):
                    list_n.append(n_p+1+j)
                n_p+= len(quant)
                pedidos.append([nome,quant,ped,tipo,mesa,list_n,n])
                
                #indicar sucesso e redirecionar para a confirmação
                handle_update_page("/listaPedidos")
                return jsonify({'suc':'T','redirect':url_for('confirmar',nome=nome)})
            else:
                return [[quant,ped,tipo],1]
                
        else:
            if nome != '':
                #se não ouver nenhum pedido é indicado ao client que ouve um erro
                return jsonify({'suc':'F',})
            else:
                return [],0
    # se ouver algum erro sera endicado
    except Exception as m:
        return(jsonify(resultado=str(m)))

# função responsavel por iniciar a interface grafica parar o script
def startInterface(vars):
    try:
        public_ip = vars['public_ip']
        porta = vars['porta']
        localhost = vars['localhost']
        #por fim chamar o menu da interface gráfica
        inter.menu(public_ip,localhost,porta,"127.0.0.1")
        try:
            requests.post(f"http://127.0.0.1:{porta}/stop",data={"paragem":FRASE_DE_ENCRRAMENTO})
        except:
            pass
    except:
        pass

def randomSubdomain(tamanho):
    caracteres = string.ascii_letters + string.digits
    return str(''.join(random.choice(caracteres) for _ in range(tamanho))).lower()

def encodeQR(string):
    encoded_string = str(string).encode("utf8")
    return base64.b64encode(encoded_string).decode()

def decodeQR(string):
    encoded_string = str(string).encode("utf8")
    return base64.b64decode(encoded_string).decode()

@socketio.on('update_page')
def handle_update_page(namspc):
    emit('reloadPedidos', broadcast=True,namespace=namspc)

@app.route("/start", methods=['GET', 'POST'])
def start():
    th = Thread(target=startInterface, args=([request.form]),daemon=True)
    th.start()
    return ''

@app.route("/stop", methods=['GET', 'POST'])
def stop():
    if request.method == "POST":
        if "paragem" in request.form:
            if request.form["paragem"] == FRASE_DE_ENCRRAMENTO:
                socketio.stop()
        return "Boa tentativa"
    
    else:
        abort(404)

@app.route("/update-files/<tipo>")
def update_files(tipo):
    if tipo == "_menu_" or tipo == "_all_":
        global todas_opcoes,preco_opcoes
        #ler todas as configurações do menu
        menu = inter.getMenu(settingsFile)
        todas_opcoes = [list(menu["cozinha"].keys()),list(menu["bar"].keys())]
        preco_opcoes = [list(menu["cozinha"].values()),list(menu["bar"].values())]
    if tipo == "_urls_" or tipo == "_all_":
        global validUrls
        #ler todas as configurações de urls
        validUrls =inter.getUrls(settingsFile)
        
    return ""        

#pagina responsavel por receber os varios pedidos
@app.route("/servico/<nome>", methods=['GET', 'POST'])
def servico(nome):
    global pedidos,n,n_p
    if 'autenticar_servico' in session and session['autenticar_servico'][1]==FRASE_DE_ENCRRAMENTO:
        if request.method == 'POST':
            return processarPedidos(nome,request)
        #se o utilizador não for permitido será indicado
        if not nome in users:
            return "Acesso negado"
        return render_template("fazerPedido.html",nome=nome,validos=[validUrls["cozinha"],validUrls["bar"],validUrls["QRCode"]],opcoes_validas=todas_opcoes,preco_opcoes=preco_opcoes,pre_def=[[],[],[]])
    
    return redirect(url_for('login'))

#pagina responsavel por indicar que os dados foram enviados com sucesso
@app.route("/confirmar/<nome>", methods=['GET', 'POST'])
def confirmar(nome):
    if 'autenticar_servico' in session and session['autenticar_servico'][1]==FRASE_DE_ENCRRAMENTO:
        return render_template("confirmar.html",nome=nome)
    return redirect(url_for('login'))

@app.route("/pedido-automatico", methods=['GET', 'POST'])
def pedidoAutomatico():
    if validUrls["QRCode"]:
        if request.method == "POST":
            pedidoQr, flag = processarPedidos('',request)
            if not flag:
                return jsonify({'suc':'F',})
            
            pedido_encode = encodeQR(str(pedidoQr)) 
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=1)
            qr.add_data(pedido_encode)
            qr.make(fit=True)
            img = qr.make_image(back_color="#f2f2f2",)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8').replace("/", "-")
            return jsonify({'suc':'T','redirect':f"QRCode/{img_str}"})

        return render_template("pedidoAutomatico.html",validos=[validUrls["cozinha"],validUrls["bar"]],opcoes_validas=todas_opcoes,preco_opcoes=preco_opcoes) 
    else:
        abort(404)  
        
@app.route("/menu", methods=['GET', 'POST'])
def menu():
    return render_template("menu.html")

@app.route("/QRCode/<string:QRbase64>", methods=['GET', 'POST'])
def QRCodeGenerate(QRbase64):
    if validUrls["QRCode"]:
        correctB64 = QRbase64.replace("-", "/")
        return render_template("mostarQR.html",correctB64=correctB64)
    else:
        abort(404)

@app.route('/QRScanner/<nome>', methods=['GET', 'POST'])
def QRScaner(nome):
    if 'autenticar_servico' in session and session['autenticar_servico'][1]==FRASE_DE_ENCRRAMENTO:
        if validUrls["QRCode"]:
            if request.method == "POST":
                try:
                    pedB64 = request.form["pedB64"]
                    str_pedido = decodeQR(pedB64)
                    lista_pedido = ast.literal_eval(str_pedido)
                    if isinstance(lista_pedido,list) and len(lista_pedido) == 3:
                        return jsonify({'suc':'T','redirect':url_for('servicoQR',nome=nome,opcoes=lista_pedido)})
                    else:
                        return jsonify({'suc':'F',})
                except:
                    return jsonify({'suc':'F',})
                
            if not nome in users:
                return "Acesso negado"
            return render_template("lerQR.html",nome=nome)
        else:
            abort(404)
    return redirect(url_for('login'))

#pagina responsavel por receber os varios pedidos
@app.route("/servicoQR/<nome>/<opcoes>", methods=['GET', 'POST'])
def servicoQR(nome,opcoes):
    global pedidos,n,n_p
    if 'autenticar_servico' in session and session['autenticar_servico'][1]==FRASE_DE_ENCRRAMENTO:
        if validUrls["QRCode"]:
            if request.method == 'POST':
                return processarPedidos(nome,request)
            return render_template("fazerPedido.html",nome=nome,validos=[validUrls["cozinha"],validUrls["bar"],validUrls["QRCode"]],opcoes_validas=todas_opcoes,preco_opcoes=preco_opcoes,pre_def=ast.literal_eval(opcoes))
        else:
            abort(404)
    return redirect(url_for('login'))

@app.route('/listaC', methods=['GET', 'POST'])
@app.route('/listaB', methods=['GET', 'POST'])
def listaCeB():
    if 'autenticar_servico' in session and session['autenticar_servico'][1]==FRASE_DE_ENCRRAMENTO:
        #verificar qual é o link que está a ser acedido
        #se os link foi ativado na GUI é criado uma lista com todos os pedidos daquela area
        if request.path == "/listaC" and validUrls["cozinha"]:
            pedidos_area = createList("Comida")
        elif request.path == "/listaB" and validUrls["bar"]:
            pedidos_area = createList("Bebida")
        #se não for permitido status code 404(Not Found)
        else:
            abort(404)
        if request.method == 'POST':
            f = request.form["feito"] #numero do pedido global
            p = int(request.form["ped"]) #numero do sub-pedido 

            c=0
            #por cada pedido na lista de pedidos
            for i in range(len(pedidos)):
                #definir a varivael
                ap = None
                #procurar pelo pedido na lista de comida
                if c==0:
                    #se os numeros dos pedidos globais forem iguais
                    if pedidos_area[i][-1]==int(f):
                        c=1
                        
                        #adicionamos esse pedido à lista dos pedidos prontos
                        ins = 0
                        for j in range(len(prontos)):
                            if prontos[j][-2] == pedidos_area[i][-2]:
                                prontos.insert(j,[pedidos_area[i][0],pedidos_area[i][1][p],pedidos_area[i][2][p],pedidos_area[i][-3][p],pedidos_area[i][-2],pedidos_area[i][-1]])
                                ins = 1
                                break
                        if not ins:
                            prontos.append([pedidos_area[i][0],pedidos_area[i][1][p],pedidos_area[i][2][p],pedidos_area[i][-3][p],pedidos_area[i][-2],pedidos_area[i][-1]])
                                
                        #extarir o nome do utilizador
                        nome = pedidos_area[i][0]
                        
                        #guardar o numero do sub-pedido
                        ap = pedidos_area[i][-3][p]
                        #remover o sub-pedido da lista dos pedidos da area
                        pedidos_area[i][1].pop(p)
                        pedidos_area[i][2].pop(p)
                        pedidos_area[i][3].pop(p)
                        pedidos_area[i][-3].pop(p)
                        
                #procurar pelo pedido na lista de todos os pedidos        
                if pedidos[i][-1]==int(f):
                    for j in range(len(pedidos[i][-2])):
                        #caso os pedidos sejam iguais
                        if ap == pedidos[i][-2][j]:
                            #remover o sub-pedido
                            pedidos[i][1].pop(j)
                            pedidos[i][2].pop(j)
                            pedidos[i][3].pop(j)
                            pedidos[i][-2].pop(j)
                            break
                    #se já não houver nenhum sub-pedido dentro do pedido global, 
                    #podemos remover o mesmo
                    if pedidos[i][1]==[]:
                        pedidos.pop(i)
                    break
            
            # avisar o utilizador que fez o pedido 
            handle_update_page("/pess/"+nome)
            #enviar sucesso
            return jsonify({'suc':'T','redirect':request.path[1:]})
        #mostrar a os pedidos
        return render_template("pedidos.html",tip=request.path[1:],pedidos=pedidos_area)
    return redirect(url_for('login'))

#pagina responsavel por indicar quais são os pedidos prontos por cada utilizador
@app.route("/lista/<nome>", methods=['GET', 'POST'])
def lista_pessoa(nome):
    if 'autenticar_servico' in session and session['autenticar_servico'][1]==FRASE_DE_ENCRRAMENTO:
        if request.method == 'POST':
            #indica qual sub-pedido foi entregue
            f = request.form["feito"]
            #procurar em todos os pedidos por aquele sub-pedido
            for i in range(len(prontos)):
                if prontos[i][-3]==int(f):
                    #se for encontrado é removido
                    prontos.pop(i)
                    break
            #returnar sucesso
            return jsonify({'suc':'T','redirect':'lista/'+nome,})
        #se o utilizador não for permitido será indicado
        if not nome in users:
            return "Acesso negado"
        #mostar resultados
        return render_template("lista.html",nome=nome,pedidos=prontos)
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["pass"]
        if user in users and password == f"{my_sub}:{PASS_NUM}":
            session.permanent = True
            session['autenticar_servico'] = [user,FRASE_DE_ENCRRAMENTO]
            return jsonify({"suc":"T","redirect":"/servico/"+user})
        else:
            return jsonify({"suc":"F","message":"Senha incorreta"})        
    if 'autenticar_servico' in session and session['autenticar_servico'][1]==FRASE_DE_ENCRRAMENTO:
        return redirect(url_for("servico",nome=session['autenticar_servico'][0]))
    return render_template("login.html")

# pagina temporaria
@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for("login"))

#-#-INICIO DO SCRIPT-#-#
if __name__ == "__main__":
    #inicilaizar variaveis imporatntes
    pedidos = []        #Lista com todos os pedidos por fazer
    prontos = []        #Lista com todos os pedidos prontos
    
    n_p=0               #Guarda o proximo numero de sub pedido
    n=0                 #Guarda o valor do pedido global

    #nomes dos ficheiros importantes
    usersFile="users.txt"
    settingsFile = "settings.json"
    
    #responsavel por fazer os ficheiros acessiveis em todo o código
    inter.Files(usersFile,settingsFile)
    
    #chamar a interface gráfica para configuração do site
    inter.main() 
    #ler todos os utilizadores
    users = inter.getUsers(usersFile)
    #ler todas as configurações de host
    data = inter.getHost(settingsFile)
    #ler todas as configurações de urls
    validUrls =inter.getUrls(settingsFile)
    #ler todas as configurações do menu
    menu = inter.getMenu(settingsFile)
    
    todas_opcoes = [list(menu["cozinha"].keys()),list(menu["bar"].keys())]
    preco_opcoes = [list(menu["cozinha"].values()),list(menu["bar"].values())]
    
    socketio.on_namespace(ListasNamespace('/listaPedidos'))
    for user in users:
        socketio.on_namespace(ListasNamespace('/pess/'+user))
        
    #inicializar outras variaveis importantes
    host = 'localhost'
    localhost = ''

    #ler dos dados de host se o loophole foi ativado
    if data["loophole"]:
        my_sub= data["subdomain"]
        if my_sub.strip() == '':
            my_sub = randomSubdomain(10)
        lh = ['']
        loophole_tunnel = Thread(target=startExternalAccess, args=(my_sub,data["port"],lh,),daemon=True)
        loophole_tunnel.start()
        public_ip=my_sub+".loophole.site"
    else: 
        public_ip = ''
        my_sub = ''


    #ler dos dados de host se o localhost foi ativado
    if data["localNetwork"]:
        #defenir host e obter o ip da máquina
        host = '0.0.0.0'
        localhost = socket.gethostbyname(socket.gethostname())
        
    
    Thread(target=requests.post,args=(f"http://127.0.0.1:{(data['port'])}/start",),kwargs=({"data":{'public_ip': public_ip,"localhost":localhost,"porta":data["port"]}}),).start()
    
    socketio.run(app, host=host,port=data["port"],use_reloader=False, debug=DEBUG)
    if data["loophole"]:
        lh[0].kill()
#-#-FIM DO SCRIPT-#-#