from flask import Flask, request, render_template, jsonify, url_for,abort
from pyngrok import ngrok, conf
from threading import Thread
#script da interface grafica
import intreface as inter
import socket
import os
# remover blur do ecrã
try:
    from ctypes import windll
    
    windll.shcore.SetProcessDpiAwareness(1)
except: pass

# Iniciar Falsk app
app = Flask(__name__)

#função responsavel por iniciar o ngrok
def startNgrok(port,key,url):
    #obter a pasta atual do script
    pathname = os.getcwd().replace("\\","/")     
    #defenir sitio de instalação do ngrok
    fullname = f'{pathname}/pyngrok/bin/ngrok.exe'
    #defenir algumas configurações do ngrok
    conf.set_default(conf.PyngrokConfig(region="eu", ngrok_path=fullname,auth_token=key,log_event_callback=None))
    #obter url http do ngrok
    url[0] = ngrok.connect(port).public_url


#pagina responsavel por receber os varios pedidos
@app.route("/servico/<nome>", methods=['GET', 'POST'])
def servico(nome):
    global pedidos,n,n_p
    if request.method == 'POST':
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
                #adicionar mais 1 ao nº global do pedido 
                n+=1
                #calcular o numero individual do pedido
                list_n=[]
                for j in range(len(quant)):
                    list_n.append(n_p+1+j)
                n_p+= len(quant)
                pedidos.append([nome,quant,ped,tipo,list_n,n])
                #indicar sucesso e redirecionar para a confirmação
                return jsonify({'suc':'T','redirect':url_for('confirmar',nome=nome)})
            else:
                #se não ouver nenhum pedido é indicado ao client que ouve um erro
                return jsonify({'suc':'F',})
        # se ouver algum erro ser+a endicado
        except Exception as m:
            return(jsonify(resultado=str(m)))
    #se o utilizador não for permitido será indicado
    if not nome in users:
        return "Acesso negado"
    return render_template("home.html",nome=nome,validos=[validUrls["cozinha"],validUrls["bar"]])


#pagina responsavel por indicar que os dados foram enviados com sucesso
@app.route("/confirmar/<nome>", methods=['GET', 'POST'])
def confirmar(nome):
    #se o utilizador não for permitido será indicado
    if not nome in users:
        return "Acesso negado"
    return render_template("confirmar.html",nome=nome)


#pagina resposnavel por ler todos os pedidos para a cozinha
@app.route('/listaC', methods=['GET','POST'])
def listaC():
    #verificar se os pedidos para a cozinha foi ativado atraves da interface gráfica
    if validUrls["cozinha"]:
        global pedidos
        #criar uma lista com apenas os pedidos para a cozinha 
        comidas=[]
        j=0
        print(pedidos)
        for p in pedidos:
            #copiar alguns dados para a nova lista
            ped=[p[0],[],[],[],[],p[5]]
            i=0
            existe=0
            #verificar cada sub-pedido para ver se pertence à cozinha
            for t in p[3]:
                if t=='Comida':
                    existe=1
                    #se houver esse sub-pedido é adicionado à nova lista para a cozinha
                    ped[1].append(p[1][i])
                    ped[2].append(p[2][i])
                    ped[3].append(p[3][i])
                    ped[4].append(p[-2][i])
                    
                i+=1
            if existe:
                #essa lista é adiconada à lista de todas as comidas
                comidas.append(ped)
            j+=1
            
        if request.method == 'POST':
            f = request.form["feito"] #numero do pedido global
            p = int(request.form["ped"]) #numero do sub-pedido 

            c=0
            #por cada pedido na lista de pedidos
            for i in range(len(pedidos)):
                #procurar pelo pedido na lista de comida
                if c==0:
                    #se os numeros dos pedidos globais forem iguais
                    if comidas[i][-1]==int(f):
                        c=1
                        
                        #adicionamos esse pedido à lista dos pedidos prontos
                        prontos.append([comidas[i][0],comidas[i][1][p],comidas[i][2][p],comidas[i][-2][p],comidas[i][-1]])
                        
                        #guardar o numero do sub-pedido
                        ap = comidas[i][-2][p]
                        #remover o sub-pedido da lista da comida
                        comidas[i][1].pop(p)
                        comidas[i][2].pop(p)
                        comidas[i][3].pop(p)
                        comidas[i][-2].pop(p)
                        
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
            #enviar sucesso
            return jsonify({'suc':'T','redirect':'listaC','nome':0})
        #mostrar a os pedidos
        return render_template("pedidos.html",tip='listaC',pedidos=comidas)

    #se não for permitido mostra um erro 404(Not Found)
    else:
        abort(404)
        

#pagina resposnavel por ler todos os pedidos para o bar
@app.route('/listaB', methods=['GET','POST'])
def listaB():
    #verificar se os pedidos para o bar foi ativado atraves da interface gráfica
    if validUrls["bar"]:
        global pedidos
        #criar uma lista com apenas os pedidos para o bar 
        bebidas=[]
        j=0
        print(pedidos)
        for p in pedidos:
            #copiar alguns dados para a nova lista
            ped=[p[0],[],[],[],[],p[5]]
            i=0
            existe=0
            #verificar cada sub-pedido para ver se pertence à bar
            for t in p[3]:
                if t=='Bebida':
                    existe=1
                    #se houver esse sub-pedido é adicionado à nova lista para o bar
                    ped[1].append(p[1][i])
                    ped[2].append(p[2][i])
                    ped[3].append(p[3][i])
                    ped[4].append(p[-2][i])
                    
                i+=1
            if existe:
                #essa lista é adiconada à lista de todas as bebidas
                bebidas.append(ped)
            j+=1
            
        if request.method == 'POST':
            f = request.form["feito"] #numero do pedido global
            p = int(request.form["ped"]) #numero do sub-pedido 

            c=0
            #por cada pedido na lista de pedidos
            for i in range(len(pedidos)):
                #procurar pelo pedido na lista de bebida
                if c==0:
                    #se os numeros dos pedidos globais forem iguais
                    if bebidas[i][-1]==int(f):
                        c=1
                        
                        #adicionamos esse pedido à lista dos pedidos prontos
                        prontos.append([bebidas[i][0],bebidas[i][1][p],bebidas[i][2][p],bebidas[i][-2][p],bebidas[i][-1]])
                        
                        #guardar o numero do sub-pedido
                        ap = bebidas[i][-2][p]
                        #remover o sub-pedido da lista da bebida
                        bebidas[i][1].pop(p)
                        bebidas[i][2].pop(p)
                        bebidas[i][3].pop(p)
                        bebidas[i][-2].pop(p)
                        
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
            #enviar sucesso
            return jsonify({'suc':'T','redirect':'listaB','nome':0})
        #mostrar a os pedidos
        return render_template("pedidos.html",tip='listaB',pedidos=bebidas)

    #se não for permitido mostra um erro 404(Not Found)
    else:
        abort(404)


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


#pagina temporaria
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
    
    #ler todos os utilizadores
    users = inter.getUsers(usersFile)
    #ler todas as configurações de host
    data = inter.getHost(settingsFile)
    #ler todas as configurações de urls
    validUrls =inter.getUrls(settingsFile)
    
    #inicializar outras variaveis importantes
    public_ip = ['']*1
    host = 'localhost'
    localhost = ''

    #ler dos dados de host se o ngrok foi ativado
    if data["ngrok"]:
        #iniciar o ngrok por uma Thread
        ngrok_tunnel = Thread(target=startNgrok,args=(data["port"],data["ngrok_api"],public_ip,),daemon=True,)
        ngrok_tunnel.start()

    #ler dos dados de host se o localhost foi ativado
    if data["localNetwork"]:
        #defenir host e obter o ip da máquina
        host = '0.0.0.0'
        localhost = socket.gethostbyname(socket.gethostname())

    #importar a production WSGI server em vez do Flask
    from waitress import serve
    
    #executar a aplicação flask com o serve
    th = Thread(target=serve, args=(app,),kwargs={'host':host,'port':data["port"]},daemon=True)
    th.start()
    
    #caso o ngrok esteja ativo esperar pelo resultado da Thread
    if data["ngrok"]:
        ngrok_tunnel.join()

    #remover o http do ngrok
    public_ip=public_ip[0].replace("http://",'')

    #por fim chamar o menu da interface gráfica
    inter.menu(public_ip,localhost,data["port"],"127.0.0.1")

#FIM DO SCIPT
