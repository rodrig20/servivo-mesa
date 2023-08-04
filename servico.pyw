from flask import Flask, request, render_template, jsonify, url_for,abort
from flask_socketio import SocketIO, emit, Namespace
from engineio.async_drivers import gevent
from login_tunnel import login  #script com o login do loophole
from threading import Thread
from flask_settings import *    #script com de defenições basicas
import intreface as inter       #script da interface grafica
from io import BytesIO
import subprocess
import requests
import base64
import socket
import qrcode
import ast
# remover blur do ecrã
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except: pass
""" 
pyinstaller --noconfirm --onedir --console --add-data "C:/Users/Rodrigo/Desktop/Rodrigo/Python/Servico/Serv_12/flask_settings.py;." --add-data "C:/Users/Rodrigo/Desktop/Rodrigo/Python/Servico/Serv_12/intreface.py;." --add-data "C:/Users/Rodrigo/Desktop/Rodrigo/Python/Servico/Serv_12/settings.json;." --add-data "C:/Users/Rodrigo/Desktop/Rodrigo/Python/Servico/Serv_12/users.txt;." --add-data "C:/Users/Rodrigo/Desktop/Rodrigo/Python/Servico/Serv_12/static;static/" --add-data "C:/Users/Rodrigo/Desktop/Rodrigo/Python/Servico/Serv_12/templates;templates/" --hidden-import "engineio.async_eventlet"  "C:/Users/Rodrigo/Desktop/Rodrigo/Python/Servico/Serv_12/servico.pyw"
"""

# Iniciar Falsk app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['ASYNC_MODE'] = 'threading'
socketio= SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

class ListasNamespace(Namespace):
    def on_reload(self):
        pass

#função responsavel por iniciar o loophole
def startExternalAccess(port,subdomain=''):
    login("tunnel","log.txt")
    if subdomain == '':
        sub = ''
    else:
        sub = f"--hostname {subdomain}"
    command = f'tunnel\\loophole.exe http {port} {sub}'.split()
    return subprocess.Popen(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def createList(tipo):
    global pedidos
    #criar uma lista com apenas os pedidos para o bar 
    tipoLista=[]
    j=0
    for p in pedidos:
        #copiar alguns dados para a nova lista
        ped=[p[0],[],[],[],[],p[5]]
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
        if len(quant) != 0:
            if nome != '':
                #adicionar mais 1 ao nº global do pedido 
                n+=1
                #calcular o numero individual do pedido
                list_n=[]
                for j in range(len(quant)):
                    list_n.append(n_p+1+j)
                n_p+= len(quant)
                pedidos.append([nome,quant,ped,tipo,list_n,n])
                
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
    public_ip = vars['public_ip']
    porta = vars['porta']
    localhost = vars['localhost']
    #por fim chamar o menu da interface gráfica
    inter.menu(public_ip,localhost,porta,"127.0.0.1")
    try:
        requests.post(f"http://127.0.0.1:{porta}/stop",data={"paragem":FRASE_DE_ENCRRAMENTO})
    except:
        pass

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

#pagina responsavel por receber os varios pedidos
@app.route("/servico/<nome>", methods=['GET', 'POST'])
def servico(nome):
    global pedidos,n,n_p
    if request.method == 'POST':
        return processarPedidos(nome,request)
    #se o utilizador não for permitido será indicado
    if not nome in users:
        return "Acesso negado"
    return render_template("fazerPedido.html",nome=nome,validos=[validUrls["cozinha"],validUrls["bar"]],opcoes_validas=todas_opcoes,pre_def=[[],[],[]])

#pagina responsavel por indicar que os dados foram enviados com sucesso
@app.route("/confirmar/<nome>", methods=['GET', 'POST'])
def confirmar(nome):
    #se o utilizador não for permitido será indicado
    if not nome in users:
        return "Acesso negado"
    return render_template("confirmar.html",nome=nome)

@app.route("/pedido-automatico", methods=['GET', 'POST'])
def pedidoAutomatico():
    if validUrls["QRCode"]:
        if request.method == "POST":
            pedidoQr, flag = processarPedidos('',request)
            if not flag:
                return jsonify({'suc':'F',})
            
            pedido_encode = encodeQR(str(pedidoQr)) 
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
            qr.add_data(pedido_encode)
            qr.make(fit=True)
            img = qr.make_image(back_color="#f2f2f2")
            
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8').replace("/", "-")
            return jsonify({'suc':'T','redirect':f"QRCode/{img_str}"})

        return render_template("pedidoAutomatico.html",validos=[validUrls["cozinha"],validUrls["bar"]],opcoes_validas=todas_opcoes)   

@app.route("/QRCode/<string:QRbase64>", methods=['GET', 'POST'])
def QRCodeGenerate(QRbase64):
    if validUrls["QRCode"]:
        correctB64 = QRbase64.replace("-", "/")
        return render_template("mostarQR.html",correctB64=correctB64)

@app.route('/QRScanner/<nome>', methods=['GET', 'POST'])
def QRScaner(nome):
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

#pagina responsavel por receber os varios pedidos
@app.route("/servicoQR/<nome>/<opcoes>", methods=['GET', 'POST'])
def servicoQR(nome,opcoes):
    global pedidos,n,n_p
    if request.method == 'POST':
        return processarPedidos(nome,request)
    #se o utilizador não for permitido será indicado
    if not nome in users:
        return "Acesso negado"
    return render_template("fazerPedido.html",nome=nome,validos=[validUrls["cozinha"],validUrls["bar"]],opcoes_validas=todas_opcoes,pre_def=ast.literal_eval(opcoes))

@app.route('/listaC', methods=['GET', 'POST'])
@app.route('/listaB', methods=['GET', 'POST'])
def listaCeB():
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
                    prontos.append([pedidos_area[i][0],pedidos_area[i][1][p],pedidos_area[i][2][p],pedidos_area[i][-2][p],pedidos_area[i][-1]])
                    #extarir o nome do utilizador
                    nome = pedidos_area[i][0]
                    
                    #guardar o numero do sub-pedido
                    ap = pedidos_area[i][-2][p]
                    #remover o sub-pedido da lista dos pedidos da area
                    pedidos_area[i][1].pop(p)
                    pedidos_area[i][2].pop(p)
                    pedidos_area[i][3].pop(p)
                    pedidos_area[i][-2].pop(p)
                    
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
                if pedidos [i][1]==[]:
                    pedidos.pop(i)
                break  
        # avisar o utilizador que fez o pedido 
        handle_update_page("/pess/"+nome)
        #enviar sucesso
        return jsonify({'suc':'T','redirect':request.path[1:]})
    #mostrar a os pedidos
    return render_template("pedidos.html",tip=request.path[1:],pedidos=pedidos_area)

#pagina responsavel por indicar quais são os pedidos prontos por cada utilizador
@app.route("/lista/<nome>", methods=['GET', 'POST'])
def lista_pessoa(nome):
    if request.method == 'POST':
        #indica qual sub-pedido foi entregue
        f = request.form["feito"]
        #procurar em todos os pedidos por aquele sub-pedido
        for i in range(len(prontos)):
            if prontos[i][-2]==int(f):
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

# pagina temporaria
@app.route("/", methods=['GET', 'POST'])
def home():
    return "Inserir Nome"

#INICIO DO SCRIPT
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
    opcoes_comida = ["Batatas Fritas", "Bife"] 
    opcoes_bebida = ["Água com gás","Coca Cola"]
    todas_opcoes = [opcoes_comida,opcoes_bebida] 
    #ler todos os utilizadores
    users = inter.getUsers(usersFile)
    #ler todas as configurações de host
    data = inter.getHost(settingsFile)
    #ler todas as configurações de urls
    validUrls =inter.getUrls(settingsFile)
    
    socketio.on_namespace(ListasNamespace('/listaPedidos'))
    for user in users:
        socketio.on_namespace(ListasNamespace('/pess/'+user))
        
    #inicializar outras variaveis importantes
    host = 'localhost'
    localhost = ''

    #ler dos dados de host se o loophole foi ativado
    if data["loophole"]:
        loophole_tunnel = startExternalAccess(data["port"],data["subdomain"])
        public_ip=data["subdomain"]+".loophole.site"
    else: public_ip = ''

    #ler dos dados de host se o localhost foi ativado
    if data["localNetwork"]:
        #defenir host e obter o ip da máquina
        host = '0.0.0.0'
        localhost = socket.gethostbyname(socket.gethostname())   
    
    Thread(target=requests.post,args=(f"http://127.0.0.1:{(data['port'])}/start",),kwargs=({"data":{'public_ip': public_ip,"localhost":localhost,"porta":data["port"]}}),).start()
    
    socketio.run(app, host=host,port=data["port"],use_reloader=False, debug=DEBUG)
    if data["loophole"]:
        loophole_tunnel.terminate()
#FIM DO SCRIPT