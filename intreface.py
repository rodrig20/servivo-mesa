from tkinter import Tk, Label, Button, Listbox, Entry, BitmapImage, Toplevel, Scrollbar
from bs4 import BeautifulSoup
from threading import Thread
from flask_settings import *
import unicodedata
import webbrowser
import subprocess
import pyperclip
import pyqrcode
import tkinter
import json
import sys

class checkButton():
    def __init__(self,start_value,posx,posy,text,com='',k=''):
        self.value = bool(start_value)
        self.Botao = Button(root, text=' ',width=4,pady=4,bg=self.color(),command=lambda: self.changeValue(com,k))
        self.Botao.place(relx=posx,rely=posy)
        self.Botao_Label = Label(root,text=text, font=("Trebuche MS", 17),)
        self.Botao_Label.place(relx=posx+0.07,rely=posy)
        
    def color(self):
        if self.value == 1:    
            cor = "#27e85e"
        else: 
            cor = "#eb4034"
        return cor

    def changeValue(self,com='',k=''):
        self.value = not(self.value)
        self.Botao.config(bg=self.color())
        if com != '':
            com(self.value,**k)
        
    def destroy(self):
        self.Botao_Label.destroy()
        self.Botao.destroy()

#funcao responsavel por returnar uma string sem acentos
def removerAcentos(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

#hide_widget
def verTodos():
    root.focus()
    #esconder widgets
    defi.place_forget()
    add.place_forget() 

    #alterar configurações
    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: desverTodos([w_users]))
    users= getUsers(usersFile)
    scrollbar.pack( side = tkinter.RIGHT, fill =tkinter.Y)
    # mostrar lista com todos os utilizadores permitidos
    w_users = Listbox(root, width=47, height=20, font=("Trebuche MS", 17), yscrollcommand = scrollbar.set )
    for u in users:
        w_users.insert(tkinter.END, str(u))
    w_users.place(relx=0.02,rely=0.15)
    scrollbar.config(command = w_users.yview )
    #remover scrollbar caso não seja necessario
    if len(users)<20:
        scrollbar.pack_forget()
        
#show_widget
def desverTodos(wi):
    root.focus()
    #mostar todos os widgets principais
    defi.place(relx=0.02,rely=0.02)
    add.place(relx=0.05,rely=0.16)
    scrollbar.pack_forget()
    #destruir os que já não são mais uteis
    for w in wi:
        w.destroy()
    #repor comfigurações
    ver.configure(text="Ver utilizadores",bg="#856ff8",command=verTodos,)

#função responsavel por retornar todos os utilizadores do ficheiro especificado
def getUsers(file):
    #lista de utilizadores
    utilizadores=[]
    try:
        with open(file,"r") as f:
            #percorrer todas as linhas não vazias
            for linha in f:
                if linha.strip()!='':
                    #adicionar esse utilizador áà lista
                    utilizadores.append(linha.strip())

    #caso esse ficheiro não exista será criado em branco
    except FileNotFoundError:
        with open(file,"a+") as f:
            pass
        
    return utilizadores

def getHost(file):
    #tentar ler as configuralões de host
    try:
        with open(file,"r") as s:
            data = json.load(s)["host"]
    #se não conseguir irá colocar as mesmas em padrão
    except:
        padraoSettings(file)
        with open(file,"r") as s:
            data = json.load(s)["host"]
    
    return data


def getUrls(file):
    #tentar ler as configuralões de urls
    try:
        with open(file,"r") as s:
            data = json.load(s)["urls"]
    #se não conseguir irá colocar as mesmas em padrão
    except:
        padraoSettings(file)
        with open(file,"r") as s:
            data = json.load(s)["urls"]
    
    return data

def getTiny(original,tipo,urls,modo):
    #se for para encurtar link loophole
    if modo == 'n':
        #criar um request, que returnará um html
        c = subprocess.Popen(f'curl -s --ssl-no-revoke "https://is.gd/create.php" --data-raw "url={original}', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        #tornar o html legivel
        html = BeautifulSoup(c, 'html.parser')
        #procurar pela tag onde é guardado o link encurtado
        html_line = str(html.find('input', {'id': 'short_url'}))
        #ler o valor dessaa tag
        link=html_line.split('value="',1)[1].rsplit('"',1)[0]
    #se for para encurtar link de um host local
    elif modo == "h":
        # criar um request que returnará apenas o link encurtado 
        link = subprocess.Popen(f"curl -s http://tinyurl.com/api-create.php?url={original}", shell=True, stdout=subprocess.PIPE).stdout.read().decode()

    #guardar o link na na posição correta da lista
    urls[tipo-1] = link

#função responsavel por adicionar um utilizador
def addUser(_=None):
    #ler o nome do utilizador pretendido
    novo = removerAcentos(str(nome.get()).strip()).decode()
    #obter todos os utilizadores já registados
    users = getUsers(usersFile)
    #trocar todos os " " por "_"
    novo = novo.replace(" ","_")
    #caso não exista nenhum "/" ou "\"
    if novo.find("/") == -1 and novo.find("\\") == -1:
            # caso o nome não for vazio
            if novo != '':
                if novo in users:
                    suc.configure(text="Nome já existe", fg="#f53b3b")

                #e caso o nome já não exista
                else:
                    #o nome é escrito no ficheiro
                    with open(usersFile, 'a+') as f:
                        f.write(f"\n{novo}")
                    #apaga a caixa de entrada
                    nome.delete(0, tkinter.END)
                    #coloca o foco na janela
                    root.focus()
                    #indica ao utilizador que o nome foi adicionado com sucesso
                    suc.configure(text="Nome adicionado com sucesso!",fg="green")
        
            else:
                #indica que ouve um erro
                suc.configure(text="Nome de utilizador inválido", fg="#f53b3b")
    
    else:
        #indica que ouve um erro
        suc.configure(text="Nome de utilizador inválido", fg="#f53b3b")

    suc.place(relx=0.35,rely=0.218)

#função responsavel por mostar o ecra para apagar utilizadores
def apagarUser():
    global w_users
    #colocar o foco na janela
    root.focus()
    #apagar alguns widgets
    defi.place_forget()
    add.place_forget()
    #altearar as configurações para poder usar com outra funcionalidade
    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: desverTodos([w_users,atual,todos,]))
    
    #botão responsavel por apagar os utilizadores selecionados
    atual = Button(root, text="Apagar Atual", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=lambda: apgOne(w_users.curselection()))
    atual.place(relx=0.37,rely=0.09)

    #botão responsavel por apagar todos os utilizadores
    todos = Button(root, text="Apagar Tudo", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=lambda: apgOne(w_users.size()))
    todos.place(relx=0.69,rely=0.09)

    #obter todos os utilizadores registados
    users= getUsers(usersFile)
    #colocar scrollbar
    scrollbar.pack( side = tkinter.RIGHT, fill =tkinter.Y)
    #mostar rodos os utilizadores
    w_users = Listbox(root, width=47,selectmode=tkinter.MULTIPLE, height=20, font=("Trebuche MS", 17), yscrollcommand = scrollbar.set )
    for u in users:
        w_users.insert(tkinter.END, str(u))
    w_users.place(relx=0.02,rely=0.15)
    scrollbar.config(command = w_users.yview )
    #remover scroolbar caso não seja necessaria
    if len(users)<20:
        scrollbar.pack_forget()

#função responsavel por remover utilizadores 
def apgOne(apg):
    global w_users
    #ler todos os utilizadores
    users=getUsers(usersFile)

    #lista com os index a apagar
    list_apg=[]
    #se for uma lista basta apenas inverter a memsma
    if type(apg) != int:
        #criar uma lista ao contrario com todos os index da lista de utilizadores
        for i in range(len(apg)-1,-1,-1):
            list_apg.append(apg[i])

    #se for passado à função um inteiro significa que que toda alista tem de ser apagada
    else:
        for i in range(apg-1,-1,-1):
            list_apg.append(i)
    apg = list_apg
    #remover os elementos pretendidos
    for a in apg:
        users.pop(a)
        w_users.delete(a)
    #escrever lista com utilizadores removidos
    with open(usersFile,"w") as f:
        for u in users:
            f.write(f"{u}\n")
    root.focus()

#função responsavel por definiro padrao das definiçóes
def padraoSettings(file):
    #escrever o json no ficheiro
    with open(file,"w+") as f:
        f.write(DEFAUT_SETTINGS)

#função responsavel por apresentar os urls válidos
def url_validos():
    #remover todos os widgets
    root.focus()
    url_atv.place_forget()
    site.place_forget()
    menuTitle.place_forget()
    menuOpc.place_forget()
    defi.place_forget()
    add.place_forget()
    nome.place_forget()
    suc.place_forget()
    apg.place_forget()
    avan.place_forget()
    host.place_forget()
    quit.place_forget()
    start.place_forget()
    #alterar as configurações do botao
    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: volt([coz,bar,qr,save]))

    #tentar extrair as configurações atuais dos urls
    try:
        with open(settingsFile,"r+") as j:
            urls=json.load(j)["urls"]
    #caso haja algum erro as definições são definidas para padrão     
    except:
        padraoSettings(settingsFile)
        with open(settingsFile,"r+") as j:
            urls=json.load(j)["urls"]

    #linha da cozinha
    coz = checkButton(urls["cozinha"],0.05,0.17,"Ativar envio para a cozinha")
    #linha do bar
    bar = checkButton(urls["bar"],0.05,0.24,"Ativar envio para o bar")
    #linha do qrcode
    qr = checkButton(urls["QRCode"],0.05,0.31,"Ativar pedidos por QRCode")

    #botao de guardar
    save = Button(root,text="Guardar",bg='#27e85e', font=("Trebuche MS", 12),width=18,command=lambda: guardarUrls(coz,bar,qr))
    save.place(relx=0.69,rely=0.09)
    
#função resposavel por guardar os urls válidos nos ficheiros
def guardarUrls(coz,bar,qr):
    #abrir o ficheiro e ler o ficheiro
    with open(settingsFile,"r+") as j:
        data = json.load(j)
    #alterar as configurações
    data["urls"]["cozinha"] = int(coz.value)
    data["urls"]["bar"] = int(bar.value)
    data["urls"]["QRCode"] = int(qr.value)
    #atualizar o ficheiro
    with open(settingsFile, 'w') as j:
        json.dump(data, j, indent=4)

#função responsavel por mostar as alterações possiveis aos host
def mudarHost():
    global loopholeVAR,porta,subdomain,errorp
    #esconder todos os widgets
    root.focus()
    url_atv.place_forget()
    site.place_forget()
    menuTitle.place_forget()
    menuOpc.place_forget()
    defi.place_forget()
    add.place_forget()
    nome.place_forget()
    suc.place_forget()
    apg.place_forget()
    avan.place_forget()
    host.place_forget()
    quit.place_forget()
    start.place_forget()
    #alterar as configurações para permitir a volta
    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: volt([subdomain,subdomainL,lporta,porta,local_access,loophole,save,errorp]))
    #tentar ler as configurações já definidas
    try:
        with open(settingsFile,"r+") as j:
            rede=json.load(j)["host"]

    #caso não seja possivel, é colocado nas definições padrão       
    except:
        padraoSettings(settingsFile)
        #volatar a ler
        with open(settingsFile,"r+") as j:
            rede=json.load(j)["host"]

    #colocar as variaveis de acordo com a informação extraida 
    if rede["subdomain"].strip() != "":
        sub = rede["subdomain"]
    else: 
        sub= ''

    #caixa de entrada responsavel por ler a Api Key
    subdomain = Entry(root, font=("Trebuche MS", 13),width=30,highlightthickness=2)
    subdomain.insert(0,sub)

    #label da Key
    subdomainL = Label(root,text="Link", font=("Trebuche MS", 17))

    #caixa de entrada responsavel por ler a a porta do servidor
    porta = Entry(root, font=("Trebuche MS", 17),width=6,highlightthickness=2)
    #label da Porta
    lporta = Label(root,text="Porta", font=("Trebuche MS", 17))

    #caso haja um erro na porta
    errorp = Label(root,font=("Trebuche MS", 7))
    
    #colocar as cores e variaveis de acordo com a informação extraida 
    if rede["loophole"]:
        subdomainL.place(relx=0.05,rely=0.34)
        subdomain.place(relx=0.165,rely=0.34)
        lporta.place(relx=0.05,rely=0.41)
        porta.place(relx=0.165,rely=0.41)
    
    else: 
        porta.place(relx=0.165,rely=0.31)
        lporta.place(relx=0.05,rely=0.31)
    
    #ler o valor da porta atual
    if rede["port"] != "":
        portaH = rede["port"]
        porta.insert(0,portaH)
    else: 
        portaH= ''
    
    local_access = checkButton(rede["localNetwork"],0.05,0.17,"Acesso na rede local")

    
    loophole = checkButton(rede["loophole"],0.05,0.24,"Acesso fora da rede (loophole)",loopholeAcess,{"pl":lporta,"p":porta,"subdomainl":subdomainL,"subdomain":subdomain,"erro":errorp})
    
    #botao de guardar configurações atuais
    save = Button(root,text="Guardar",bg='#27e85e', font=("Trebuche MS", 12),width=18,command=lambda: guardarHost(loophole,local_access,errorp))
    save.place(relx=0.69,rely=0.09)

    #remover a mesnagem de erro
    porta.bind("<FocusIn>", erroP)

#função responsavel por ativar/desativar o acesso fora da rede
def loopholeAcess(value,pl,p,subdomainl,subdomain,erro):
    #troca dos valores das varivaeis
    if value:
        p.place(relx=0.165,rely=0.41)
        pl.place(relx=0.05,rely=0.41)
        subdomainl.place(relx=0.05,rely=0.34)
        subdomain.place(relx=0.165,rely=0.34)
        erro.place(relx=0.165,rely=0.465)
        
    else:
        p.place(relx=0.165,rely=0.31)
        pl.place(relx=0.05,rely=0.31)
        erro.place(relx=0.165,rely=0.36)
        subdomainl.place_forget()
        subdomain.place_forget()

#guardar configurações de hist no ficehirp
def guardarHost(loophole,local_access,erro):
    global porta,subdomain
    #verificar se a porta é um numeor válido
    if int(porta.get()) >= 1 and int(porta.get()) <= 65535:
        #remover mensagem de erro
        erro.place_forget()
        #ler arquivo de definições
        with open(settingsFile,"r+") as j:
            data = json.load(j)

        #alaterar as definições de acordo com o selecionado
        data["host"]["localNetwork"] = int(local_access.value)
        data["host"]["loophole"] = int(loophole.value)
        data["host"]["subdomain"] = subdomain.get().strip()
        data["host"]["port"] = int(porta.get())
        
        #carregar as novas definições 
        with open(settingsFile, 'w') as j:
            json.dump(data, j, indent=4)
    
    else:
        #mostrar erro
        erro.configure(text="Porta tem de estar entre 1-65535",fg="#eb4034")
        if int(loopholeVAR):
            erro.place(relx=0.165,rely=0.465)
        else:
            erro.place(relx=0.165,rely=0.36)
        root.focus()

#voltar depois de entrar em algum menu
def volt(w_list):
    #colocar o foco na janela
    root.focus()
    #apagar todos os widgets utilizados
    for w in w_list:
        w.destroy()
    #repor os widgets do menu principal
    ver.configure(text="Ver utilizadores",bg="#856ff8",command=verTodos,)
    defi = Label(root, text="Definições de Utilizadores", font=("Trebuche MS", 17))
    defi.place(relx=0.02,rely=0.02)
    add.place(relx=0.05,rely=0.16)
    nome.place(relx=0.35,rely=0.155)
    apg.place(relx=0.05,rely=0.23)
    menuTitle.place(relx=0.05,rely=0.32)
    menuOpc.place(relx=0.05,rely=0.39)
    site.place(relx=0.05,rely=0.48) 
    url_atv.place(relx=0.05,rely=0.55)
    avan.place(relx=0.02,rely=0.64)
    host.place(relx=0.05,rely=0.71)
    quit.place(relx=0.05,rely=0.87)
    start.place(relx=0.7,rely=0.87)

#remover mensagem de estado ao adicionar um nome
def sucesso(e):
    suc.place_forget()

#remover mensagem de estado ao escrever um a porta para o host
def erroP(e):
    global errorp
    errorp.place_forget()

#terminar processo
def close():
    sys.exit(1) 

#definir o nome dos ficehiros padrao de utilizadores e de definições
def Files(uFile,sFile):
    global usersFile,settingsFile
    usersFile=uFile
    settingsFile=sFile

# função responsavel por pegar no url e colocar no clipboard, 
#e avisar o utilizador que o link foi copiado
def copyUrl(url,win,yCord,xCord,j):
    #copiar para o clipboard
    pyperclip.copy(url)
    if j==1:
        xCord+=0.13
    #informar o utilizador
    suc = Label(win,font=("Trebuche MS", 14),text="Copiado",fg="#27e85e")
    suc.place(relx=xCord,rely=yCord)
    #remover aviso apos 5000 ms
    win.after(5000,lambda: destruir(suc))

#função responsavel por centralizar janela
def centralizaWin(win,width=0,height=0):
    #caso a janela não tenha tamanho certo
    if width == 0 and height == 0:
        #ler o tamnho da janela
        width = win.winfo_reqwidth()
        height = win.winfo_reqheight()
    #ler tamaho do ecra
    screen_width = win.winfo_screenwidth()  # Width of the screen
    screen_height = win.winfo_screenheight() # Height of the screen
    #calcular a posição do canto superior direito
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))
    #definir tamho e posição da jeanela
    win.geometry(f'{width}x{height}+{x}+{y}')
        
#função resposavel por criar uma janela com um QrCode de um link
def open_QR(url):
    global qr_win
    
    #tentar apagar qrcodes antigos
    try:
        qr_win.destroy()
    except:
        pass
    

    #criar uma janela Top Level
    qr_win = Toplevel()
    
    qr_win.title("")

    #colocar qr code gerado num Lbale como uma imagem
    img_lbl = Label(qr_win,image=generate_QR(url))
    img_lbl.pack()
    #botao para fechar a janela do qr
    sair = Button(qr_win,text="Fechar",font=("Trebuche MS", 18), bg='#f53b3b',width=12,command=qr_win.destroy)
    sair.pack()

    #mudar tamanho da janela de acordo com o tamanho do QrCode
    qr_win.update_idletasks()
    
    centralizaWin(qr_win)
    
    qr_win.mainloop()

#gerar um QrCode
def generate_QR(url):
    global qr_img
    #criar um Qrcode
    qr = pyqrcode.create(url)
    #transformar em Bitmap
    qr_img = BitmapImage(data=qr.xbm(scale=7))
    return qr_img

#função responsavel por abrir um url especificado
def redirectUrl(url):
    webbrowser.open(url)

#remover objeto
def destruir(obj):
    obj.destroy()

#função responsavel por manter um menu após dar executar o site 
def menu(url,localIP,p,default):
    win = Tk()

    add = 0
    height=700

    #lista com os 2 urls encortados
    tiny_urls = [None]*2

    #se as definições de acesso local e loophole estiverem ativas
    if url!='' and localIP!='':
        janela = 2
        width=900
        b_url = f"https://{url}"
        localIP = f"{localIP}:{p}"
        b_localIP = f"http://{localIP}"
        #Thread que faz request para obter o url local encurtado
        tn2_url = Thread(target=getTiny,args=(b_localIP,2,tiny_urls,'h',),daemon=True)
        tn2_url.start()
        m = 'n'
        small = 0
    #se um dos acessos estiverem arivos
    else:
        janela = 1
        width = 600
        #apenas acesso na rede
        if url=='' and localIP!='':
            url = (f"{localIP}:{p}")
            b_url = f"http://{url}"
            m = 'h' 
            small = 0
        #apenas acesso na máquina
        elif  url=='' and localIP=='':
            url = f"{default}:{p}"
            b_url = f"http://{url}"
            m = 'h' 
            small = 1
            width = 400
            height = 500
            add = 0.05
        #apenas acesso fora da rede via loophole
        else:
            b_url = f"https://{url}"
            m = 'n' 
            small = 0

    if not small:
        #Thread que faz request para obter o outro url encurtado
        tn1_url = Thread(target=getTiny,args=(b_url,1,tiny_urls,m,),daemon=True)
        tn1_url.start()

    win.title("Serviço de mesa")
    #definir tamanho e
    #centralizar janela
    centralizaWin(win,width,height)
    win.resizable(False, False)

    #botao de fechar janela
    win.protocol("WM_DELETE_WINDOW", close)

    #label do primeiro url
    link1 = Label(win,font=("Trebuche MS", 17),text=url)
    #boato de copia do primeiro url
    link1_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command=lambda: copyUrl(b_url,win,0.12+(small/10),0.29+(small/5),janela))
    #botao de redirecionamento do primeiro url
    link1_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(b_url))
    #botao de QrCode do primeiro url
    link1_QR = Button(win,font=("Trebuche MS", 17),bg="#8c8c8c",text="QR Code",width=12,command=lambda: open_QR(b_url))
    if not small:        
        #label do primeiro url encurtado
        tiny1 = Label(win,font=("Trebuche MS", 17))
        #boato de copia do primeiro url encurtado
        tn1_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command= lambda: copyUrl(tiny_urls[0],win,0.567,0.29,janela))
        #botao de redirecionamento do primeiro url encurtado
        tn1_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(tiny_urls[0]))

    #colocação dos widgets
    link1.place(relx=0.05,rely=0.03+add)
    link1_cop.place(relx=0.05,rely=0.1+add*2)
    link1_red.place(relx=0.05,rely=0.2+add*3)
    link1_QR.place(relx=0.05,rely=0.3+add*4)

    if not small:
        tiny1.place(relx=0.05,rely=0.48)
        tn1_cop.place(relx=0.05,rely=0.55)
        tn1_red.place(relx=0.05,rely=0.65)

    if janela == 2:
        #repetir os wisgets acima, mas com o segundo url
        link2 = Label(win,font=("Trebuche MS", 17),text=localIP)
        link2_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command=lambda: copyUrl(b_localIP,win,0.12,0.79,0))
        link2_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(b_localIP))
        link2_QR = Button(win,font=("Trebuche MS", 17),bg="#8c8c8c",text="QR Code",width=12,command=lambda: open_QR(b_localIP))
        tiny2 = Label(win,font=("Trebuche MS", 17))
        tn2_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command= lambda: copyUrl(tiny_urls[1],win,0.565,0.79,0))
        tn2_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(tiny_urls[1]))

        link2.place(relx=0.55,rely=0.03)
        link2_cop.place(relx=0.55,rely=0.1)
        link2_red.place(relx=0.55,rely=0.2)
        link2_QR.place(relx=0.55,rely=0.3)
        tiny2.place(relx=0.55,rely=0.48)
        tn2_cop.place(relx=0.55,rely=0.55)
        tn2_red.place(relx=0.55,rely=0.65)

    #botao para terminar script
    quit = Button(win,font=("Trebuche MS", 17),text="Terminar",bg="#f53b3b",command=lambda: destruir(win))
    quit.place(relx=0.5,rely=0.91,anchor=tkinter.CENTER)

    #receber o primeiro url encurtado
    if not small:
        tn1_url.join()
        tiny1.configure(text=str(tiny_urls[0]))
        
    #receber o segundo url encurtado
    if janela == 2:
        tn2_url.join()
        tiny2.configure(text=str(tiny_urls[1]))

    # Execute Tkinter
    win.mainloop()

# create root window
def main():
    global root, defi, ver,add,nome,suc,apg,menuTitle,menuOpc,scrollbar,url_atv,site,host,avan,quit,start
    root = Tk()
    #definir tamanho da janela
    width = 800
    height = 800

    #titulo da janela
    root.title("Serviço de mesa")
    #centralizar janela
    centralizaWin(root,width,height)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", close)
    scrollbar = Scrollbar()
    
    #colocar titulo das definiçoes dos utilizadores
    defi = Label(root, text="Definições de Utilizadores", font=("Trebuche MS", 17))
    defi.place(relx=0.02,rely=0.02)

    #colocar botao para visualizar os utilizadores válidos
    ver = Button(root, text="Ver Utilizadores", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=verTodos)
    ver.place(relx=0.05,rely=0.09)

    #colocar botao para adicionar novos utilizadores
    add = Button(root, text="Adicionar Utilizador", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=addUser)
    add.place(relx=0.05,rely=0.16)

    #colocar caixa de texto que recebe o nome a adicionar
    nome = Entry(root, font=("Trebuche MS", 20),width=20,highlightthickness=2)
    nome.place(relx=0.35,rely=0.155)

    #Se for clicar no enter adiciona esse nome
    nome.bind('<Return>',addUser)

    #mostar mensagem de estado
    suc = Label(root, text="Nome adicionado com sucesso!",font=("Trebuche MS", 6),fg="green")
    #se a caixa de texto voltar a estar em foco a mensage, remove a mensagem de estado
    nome.bind("<FocusIn>", sucesso)

    #colocar botao para remover utilizadores
    apg = Button(root, text="Apagar Utilizador", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=apagarUser)
    apg.place(relx=0.05,rely=0.23)
    
    menuTitle = Label(root, text="Definições do Menu", font=("Trebuche MS", 17))
    menuTitle.place(relx=0.02,rely=0.32)
    
    menuOpc = Button(root, text="Esolher Menu", font=("Trebuche MS", 12),width=18,bg="#856ff8", )#command=)
    menuOpc.place(relx=0.05,rely=0.39)

    #colocar titulo das definiçoes de site
    site = Label(root, text="Definições do site", font=("Trebuche MS", 17))
    site.place(relx=0.02,rely=0.48)
    
    #colocar botao para alterar urls permitidos
    url_atv = Button(root, text="Urls Permitidos", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=url_validos)
    url_atv.place(relx=0.05,rely=0.55)

    #colocar titulo para definições avançadas
    avan = Label(root, text="Definições Avançadas", font=("Trebuche MS", 17))
    avan.place(relx=0.02,rely=0.64)

    #colocar botao para alterar configurações de host
    host = Button(root, text="Mudar Host", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=mudarHost)
    host.place(relx=0.05,rely=0.71)

    #colocar botao para cancelar operação
    quit = Button(root, text="SAIR", font=("Trebuche MS", 18),width=10,pady=5,bg="#eb4034", command=close)
    quit.place(relx=0.05,rely=0.87)

    #colocar botao para começar o site
    start = Button(root, text="Começar", font=("Trebuche MS", 18),width=10,pady=5,bg="#27e85e", command=root.destroy)
    start.place(relx=0.7,rely=0.87)

    # Execute Tkinter
    root.mainloop()

if __name__ == "__main__":
    usersFile = "users.txt"
    settingsFile = "settings.json"
    main()

    print("Utilizadores: ")
    for u in getUsers(usersFile):
        print(u)
    print()

    data = getHost(settingsFile)
    for info in data:
        print(f"{info:<13}: {data[info]}")
        
    print()
    print()
