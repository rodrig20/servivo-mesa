from bs4 import BeautifulSoup
from threading import Thread
from tkinter import *
import unicodedata
import webbrowser
import subprocess
import pyperclip
import pyqrcode
import json
import sys

#funcao responsavel por returnar uma string sem acentos
def removerAcentos(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

#hide_widget
def verTodos():
    root.focus()
    #esconder widgets
    defe.place_forget()
    add.place_forget() 

    #alterar configurações
    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: desverTodos([w_users]))
    users= getUsers(usersFile)
    scrollbar.pack( side = RIGHT, fill =Y)
    # mostrar lista com todos os utilizadores permitidos
    w_users = Listbox(root, width=47, height=20, font=("Trebuche MS", 17), yscrollcommand = scrollbar.set )
    for u in users:
        w_users.insert(END, str(u))
    w_users.place(relx=0.02,rely=0.15)
    scrollbar.config(command = w_users.yview )
    #remover scrollbar caso não seja necessario
    if len(users)<20:
        scrollbar.pack_forget()
        
#show_widget
def desverTodos(wi):
    root.focus()
    #mostar todos os widgets principais
    defe.place(relx=0.02,rely=0.02)
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
    #se for para encurtar link ngrok
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
                    nome.delete(0, END)
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
    defe.place_forget()
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
    scrollbar.pack( side = RIGHT, fill =Y)
    #mostar rodos os utilizadores
    w_users = Listbox(root, width=47,selectmode=MULTIPLE, height=20, font=("Trebuche MS", 17), yscrollcommand = scrollbar.set )
    for u in users:
        w_users.insert(END, str(u))
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

#função responsavel por defeniro padrao das defeniçóes
def padraoSettings(file):
    #json padrao
    json = '''{
        "host": {
            "localNetwork": 1,
            "ngrok": 0,
            "ngrok_api": "28IsPxR4UPF5SzXRBs7sW4zK6QN_3tYDqpXnTF17uyd4TNT4m",
            "port": 8080
        },

        "urls":{
            "cozinha":1,
            "bar":0
        }
    }'''
    #escrever o json no ficheiro
    with open(file,"w+") as f:
        f.write(json)

#função responsavel por ativar/desativar o url da cozinha
def enbl_coz(bt):
    global coz_var
    #se estiver ativado, destativa
    if coz_var:
        bt.configure(bg='#eb4034')
        coz_var = 0
    #se estiver desativado, ativa
    else:
        bt.configure(bg='#27e85e')
        coz_var = 1 

#função responsavel por ativar/desativar o url do bar
def enbl_bar(bt):
    global bar_var
    #se estiver ativado, destativa
    if bar_var:
        bt.configure(bg='#eb4034')
        bar_var = 0
    #se estiver desativado, ativa
    else:
        bt.configure(bg='#27e85e')
        bar_var = 1 

#função responsavel por apresentar os urls válidos
def url_validos():
    global coz_var,bar_var
    #remover todos os widgets
    root.focus()
    url_atv.place_forget()
    site.place_forget()
    defe.place_forget()
    add.place_forget()
    nome.place_forget()
    suc.place_forget()
    apg.place_forget()
    avan.place_forget()
    host.place_forget()
    quit.place_forget()
    start.place_forget()
    #alterar as configurações do botao
    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: volt([coz,cozL,bar,barL,save]))

    #tentar extrair as configurações atuais dos urls
    try:
        with open(settingsFile,"r+") as j:
            urls=json.load(j)["urls"]
    #caso haja algum erro as defenições são defenidas para padrão     
    except:
        padraoSettings(settingsFile)
        with open(settingsFile,"r+") as j:
            urls=json.load(j)["urls"]

    #colocar as cores e variaveis de acordo com a informação extraida 
    if urls["cozinha"]:
        coz_color = "#27e85e"
        coz_var = 1
    else:
        coz_color = "#eb4034"
        coz_var = 0
    
    #colocar as cores e variaveis de acordo com a informação extraida 
    if urls["bar"]:
        bar_color = "#27e85e"
        bar_var = 1
    else:
        bar_color = "#eb4034"
        bar_var = 0

    #btao de guardar
    save = Button(root,text="Guardar",bg='#27e85e', font=("Trebuche MS", 12),width=18,command=lambda: guardarUrls())
    save.place(relx=0.69,rely=0.09)

    #linha da cozinha
    coz = Button(root, text=' ',width=4,pady=4,bg=coz_color,command=lambda: enbl_coz(coz))
    coz.place(relx=0.05,rely=0.17)
    cozL = Label(root,text="Ativar envio para a cozinha", font=("Trebuche MS", 17),)
    cozL.place(relx=0.12,rely=0.17)

    #linha do bar
    bar = Button(root, text=' ',width=4,pady=4,bg=bar_color,command=lambda: enbl_bar(bar))
    bar.place(relx=0.05,rely=0.24)
    barL = Label(root,text="Ativar envio para o bar", font=("Trebuche MS", 17),)
    barL.place(relx=0.12,rely=0.24)

#função resposavel por guardar os urls válidos nos ficheiros
def guardarUrls():
    global coz_var,bar_var
    #abrir o ficheiro e ler o ficheiro
    with open(settingsFile,"r+") as j:
        data = json.load(j)
    #alterar as configurações
    data["urls"]["cozinha"] = int(coz_var)
    data["urls"]["bar"] = int(bar_var)
    #atualizar o ficheiro
    with open(settingsFile, 'w') as j:
        json.dump(data, j, indent=4)

#função responsavel por mostar as alterações possiveis aos host
def mudarHost():
    global localVAR, ngrokVAR,porta,ngrokApi,errorp
    #esconder todos os widgets
    root.focus()
    url_atv.place_forget()
    site.place_forget()
    defe.place_forget()
    add.place_forget()
    nome.place_forget()
    suc.place_forget()
    apg.place_forget()
    avan.place_forget()
    host.place_forget()
    quit.place_forget()
    start.place_forget()
    #alterar as configurações para permitir a volta
    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: volt([ngrokApi,ngrokApiL,lporta,porta,check1,check2,lcheck1,lcheck2,save,errorp]))
    #tentar ler as configurações já defenidas
    try:
        with open(settingsFile,"r+") as j:
            rede=json.load(j)["host"]

    #caso não seja possivel, é colocado nas defenições padrão       
    except:
        padraoSettings(settingsFile)
        #volatar a ler
        with open(settingsFile,"r+") as j:
            rede=json.load(j)["host"]
    
    #colocar as cores e variaveis de acordo com a informação extraida 
    if rede["localNetwork"]:
        localC = "#27e85e"
        localVAR = 1
    else: 
        localC = "#eb4034"
        localVAR = 0

    #colocar as variaveis de acordo com a informação extraida 
    if rede["ngrok_api"].strip() != "":
        apiKey = rede["ngrok_api"]
    else: 
        apiKey= ''

    #caixa de entrada responsavel por ler a Api Key
    ngrokApi = Entry(root, font=("Trebuche MS", 13),width=54,highlightthickness=2)
    ngrokApi.insert(0,apiKey)

    #label da Key
    ngrokApiL = Label(root,text="Api\nKey", font=("Trebuche MS", 17))

    #caixa de entrada responsavel por ler a a porta do servidor
    porta = Entry(root, font=("Trebuche MS", 17),width=6,highlightthickness=2)
    #label da Porta
    lporta = Label(root,text="Porta", font=("Trebuche MS", 17))

    #caso haja um erro na porta
    errorp = Label(root,font=("Trebuche MS", 7))

    #colocar as cores e variaveis de acordo com a informação extraida 
    if rede["ngrok"]:
        ngrokC = "#27e85e"
        ngrokVAR=1
        ngrokApiL.place(relx=0.05,rely=0.31)
        ngrokApi.place(relx=0.165,rely=0.34)
        lporta.place(relx=0.05,rely=0.41)
        porta.place(relx=0.165,rely=0.41)
    
    else: 
        ngrokC = "#eb4034"
        ngrokVAR=0
        porta.place(relx=0.165,rely=0.31)
        lporta.place(relx=0.05,rely=0.31)
    
    #ler o valor da porta atual
    if rede["port"] != "":
        portaH = rede["port"]
        porta.insert(0,portaH)
    else: 
        portaH= ''
        

    #botao indicardor de ativação
    check1 = Button(root, text=' ',width=4,pady=4,bg=localC, command=lambda: localAcess(check1))
    check1.place(relx=0.05,rely=0.17)
    #label do indicador
    lcheck1 = Label(root,text="Acesso na rede local", font=("Trebuche MS", 17),)
    lcheck1.place(relx=0.12,rely=0.17)

    #botao indicardor de ativação
    check2 = Button(root, text=' ',width=4,pady=4,bg=ngrokC,command=lambda: ngrokAcess(check2,lporta,porta,ngrokApiL,ngrokApi,errorp))
    check2.place(relx=0.05,rely=0.24)
    #label do indicador
    lcheck2 = Label(root,text="Acesso fora da rede (Ngrok)", font=("Trebuche MS", 17))
    lcheck2.place(relx=0.12,rely=0.24)

    #botao de guardar configurações atuais
    save = Button(root,text="Guardar",bg='#27e85e', font=("Trebuche MS", 12),width=18,command=lambda: guardarHost(errorp))
    save.place(relx=0.69,rely=0.09)

    #remover a mesnagem de erro
    porta.bind("<FocusIn>", erroP)

    
#função responsavel por ativar/desativar o acesso na rede local
def localAcess(bt):
    global localVAR
    #troca dos valores das varivaeis
    if localVAR:
        bt.configure(bg='#eb4034')
        localVAR = 0
    else:
        bt.configure(bg='#27e85e')
        localVAR = 1

#função responsavel por ativar/desativar o acesso fora da rede
def ngrokAcess(bt,pl,p,apil,api,erro):
    global ngrokVAR
    #troca dos valores das varivaeis
    if ngrokVAR:
        bt.configure(bg='#eb4034')
        ngrokVAR = 0
        p.place(relx=0.165,rely=0.31)
        pl.place(relx=0.05,rely=0.31)
        erro.place(relx=0.165,rely=0.36)
        apil.place_forget()
        api.place_forget()
        

    else:
        bt.configure(bg='#27e85e')
        ngrokVAR = 1
        p.place(relx=0.165,rely=0.41)
        pl.place(relx=0.05,rely=0.41)
        apil.place(relx=0.05,rely=0.31)
        api.place(relx=0.165,rely=0.34)
        erro.place(relx=0.165,rely=0.465)

#guardar configurações de hist no ficehirp
def guardarHost(erro):
    global localVAR, ngrokVAR,porta,ngrokApi
    #verificar se a porta é um numeor válido
    if int(porta.get()) >= 1 and int(porta.get()) <= 65535:
        #remover mensagem de erro
        erro.place_forget()
        #ler arquivo de defenições
        with open(settingsFile,"r+") as j:
            data = json.load(j)

        #alaterar as defenições de acordo com o selecionado
        data["host"]["localNetwork"] = int(localVAR)
        data["host"]["ngrok"] = int(ngrokVAR)
        data["host"]["ngrok_api"] = ngrokApi.get().strip()
        data["host"]["port"] = int(porta.get())
        
        #carregar as novas defenições 
        with open(settingsFile, 'w') as j:
            json.dump(data, j, indent=4)
    
    else:
        #mostrar erro
        erro.configure(text="Porta tem de estar entre 1-65535",fg="#eb4034")
        if int(ngrokVAR):
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
    defe = Label(root, text="Defenições de Utilizadores", font=("Trebuche MS", 17))
    defe.place(relx=0.02,rely=0.02)
    add.place(relx=0.05,rely=0.16)
    nome.place(relx=0.35,rely=0.155)
    apg.place(relx=0.05,rely=0.23)
    site.place(relx=0.02,rely=0.34) 
    url_atv.place(relx=0.05,rely=0.41)
    avan.place(relx=0.02,rely=0.52)
    host.place(relx=0.05,rely=0.59)
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

#defenir o nome dos ficehiros padrao de utilizadores e de defenições
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
    root.after(5000,lambda: destruir(suc))

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
    #defenir tamho e posição da jeanela
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
    
    #lista com os 2 urls encortados
    tiny_urls = [None]*2
    
    #se as defenições de acesso local e ngrok estiverem ativas
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
    #se um dos acessos estiverem arivos
    else:
        janela = 1
        width = 600
        height = 700
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
        #apenas acesso fora da rede via ngrok
        else:
            b_url = f"https://{url}"
            m = 'n' 
            small = 0

    if not small:
        #Thread que faz request para obter o outro url encurtado
        tn1_url = Thread(target=getTiny,args=(b_url,1,tiny_urls,m,),daemon=True)
        tn1_url.start()

    win.title("Serviço de mesa")
    #defenir tamanho e
    #centralizar janela
    centralizaWin(win,width,height)
    win.resizable(False, False)

    #botao de fechar janela
    win.protocol("WM_DELETE_WINDOW", close)

    #label do primeiro url
    link1 = Label(win,font=("Trebuche MS", 17),text=url)
    #boato de copia do primeiro url
    link1_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command=lambda: copyUrl(b_url,win,0.12,0.29,janela))
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
    quit.place(relx=0.5,rely=0.91,anchor=CENTER)

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
    global root, defe, ver,add,nome,suc,apg,scrollbar,url_atv,site,host,avan,quit,start
    root = Tk()
    #defenir tamanho da janela
    width = 800
    height = 800
    

    #titulo da janela
    root.title("Serviço de mesa")
    #centralizar janela
    centralizaWin(root,width,height)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", close)
    scrollbar = Scrollbar()

    #colocar titulo das defeniçoes dos utilizadores
    defe = Label(root, text="Defenições de Utilizadores", font=("Trebuche MS", 17))
    defe.place(relx=0.02,rely=0.02)

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

    #colocar titulo das defeniçoes de site
    site = Label(root, text="Defenições do site", font=("Trebuche MS", 17))
    site.place(relx=0.02,rely=0.34)

    #colocar botao para alterar urls permitidos
    url_atv = Button(root, text="Urls Permitidos", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=url_validos)
    url_atv.place(relx=0.05,rely=0.41)

    #colocar titulo para defenições avançadas
    avan = Label(root, text="Defenições Avançadas", font=("Trebuche MS", 17))
    avan.place(relx=0.02,rely=0.52)

    #colocar botao para alterar configurações de host
    host = Button(root, text="Mudar Host", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=mudarHost)
    host.place(relx=0.05,rely=0.59)

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
