from bs4 import BeautifulSoup
from threading import Thread
from tkinter import *
import unicodedata
import json
import pyperclip
import pyqrcode
import webbrowser
import subprocess
import sys


def removerAcentos(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

#hide_widget
def verTodos():
    defe.place_forget()
    add.place_forget() 

    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: desverTodos([w_users]))
    users= getUsers(usersFile)
    scrollbar.pack( side = RIGHT, fill =Y)
    w_users = Listbox(root, width=47, height=20, font=("Trebuche MS", 17), yscrollcommand = scrollbar.set )
    for u in users:
        w_users.insert(END, str(u))
    w_users.place(relx=0.02,rely=0.15)
    scrollbar.config(command = w_users.yview )
    if len(users)<20:
        scrollbar.pack_forget()
        
#show_widget
def desverTodos(wi):
    defe.place(relx=0.02,rely=0.02)
    add.place(relx=0.05,rely=0.16)
    scrollbar.pack_forget()
    for w in wi:
        w.destroy()
    ver.configure(text="Ver utilizadores",bg="#856ff8",command=verTodos,)

def getUsers(file):
    utilizadores=[]
    try:
        with open(file,"r") as f:
            for l in f:
                if l.strip()!='':
                    utilizadores.append(l.strip())

    except FileNotFoundError:
        with open(file,"a+") as f:
            pass
        
    return utilizadores

def getHost(file):
    with open(file,"r") as j:
        data = json.load(j)["host"]
    
    return data



def getTiny(original,tipo,urls,modo):
    if modo == 'n':
        c = subprocess.Popen(f'curl -s --ssl-no-revoke "https://is.gd/create.php" --data-raw "url={original}', shell=False, stdout=subprocess.PIPE).stdout.read().decode()
        html = BeautifulSoup(c, 'html.parser')
        html_line = str(html.find('input', {'id': 'short_url'}))
        link=html_line.split('value="',1)[1].rsplit('"',1)[0]
    elif modo == "h":
        link = subprocess.Popen(f"curl -s http://tinyurl.com/api-create.php?url={original}", shell=True, stdout=subprocess.PIPE).stdout.read().decode()

    urls[tipo-1] = link


def addUser():
    novo = removerAcentos(str(nome.get()).strip()).decode()
    users = getUsers(usersFile)

    if novo.find(" ") != -1:
        novo = novo.replace(" ","_")
    if novo.find("/") == -1 and novo.find("\\") == -1:
            if novo != '':
                if novo in users:
                    suc.configure(text="Nome já existe", fg="#f53b3b")
        
                else:
                    with open(usersFile, 'a+') as f:
                        f.write(f"\n{novo}")
                    nome.delete(0, END)
                    root.focus()
                    suc.configure(text="Nome adicionado com sucesso!",fg="green")
        
            else:
                suc.configure(text="Nome de utilizador inválido", fg="#f53b3b")
    
    else:
        suc.configure(text="Nome de utilizador inválido", fg="#f53b3b")

    suc.place(relx=0.35,rely=0.218)

def apagarUser():
    global w_users
    defe.place_forget()
    add.place_forget()

    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: desverTodos([w_users,atual,todos,]))
    atual = Button(root, text="Apagar Atual", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=lambda: apgOne(w_users.curselection()))
    atual.place(relx=0.37,rely=0.09)

    todos = Button(root, text="Apagar Tudo", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=lambda: apgOne(w_users.size()))
    todos.place(relx=0.69,rely=0.09)
    users= getUsers(usersFile)
    scrollbar.pack( side = RIGHT, fill =Y)
    w_users = Listbox(root, width=47,selectmode=MULTIPLE, height=20, font=("Trebuche MS", 17), yscrollcommand = scrollbar.set )
    for u in users:
        w_users.insert(END, str(u))
    w_users.place(relx=0.02,rely=0.15)
    scrollbar.config(command = w_users.yview )
    if len(users)<20:
        scrollbar.pack_forget()

def apgOne(apg):
    global w_users
    users=getUsers(usersFile)
    list_apg=[]
    if type(apg) != int:
        for i in range(len(apg)-1,-1,-1):
            list_apg.append(apg[i])

    else:
        for i in range(apg-1,-1,-1):
            list_apg.append(i)
    apg = list_apg
    for a in apg:
        users.pop(a)
        w_users.delete(a)
    with open(usersFile,"w") as f:
        for u in users:
            f.write(f"{u}\n")

def padraoSettings(file):
    json = '''{
    "host": {
        "localNetwork": 0,
        "ngrok": 0,
        "ngrok_api": "YOUR_API_KEY",
        "port": 8080
    }
}'''
    with open(file,"a+") as f:
        f.write(json)

def mudarHost():
    global localVAR, ngrokVAR,porta,ngrokApi,errorp
    #global w_users
    defe.place_forget()
    add.place_forget()
    nome.place_forget()
    suc.place_forget()
    apg.place_forget()
    avan.place_forget()
    host.place_forget()
    quit.place_forget()
    start.place_forget()

    ver.configure(text="Voltar", bg='#f53b3b', command= lambda: sairHost([ngrokApi,ngrokApiL,lporta,porta,check1,check2,lcheck1,lcheck2,save,errorp]))
    try:
        with open(settingsFile,"r+") as j:
            #try:
            rede=json.load(j)["host"]
            #except:
                
    except:
        padraoSettings(settingsFile)
        with open(settingsFile,"r+") as j:
            rede=json.load(j)["host"]
    
    if rede["localNetwork"]:
        localC = "#27e85e"
        localVAR = 1
    else: 
        localC = "#eb4034"
        localVAR = 0

    if rede["ngrok_api"].strip() != "":
        apiKey = rede["ngrok_api"]
    else: apiKey= ''

    ngrokApi = Entry(root, font=("Trebuche MS", 13),width=54,highlightthickness=2)
    ngrokApi.insert(0,apiKey)

    ngrokApiL = Label(root,text="Api\nKey", font=("Trebuche MS", 17))

    lporta = Label(root,text="Porta", font=("Trebuche MS", 17))

    porta = Entry(root, font=("Trebuche MS", 17),width=6,highlightthickness=2)
    errorp = Label(root,font=("Trebuche MS", 7))

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
    
    if rede["port"] != "":
        portaH = rede["port"]
        porta.insert(0,portaH)
    else: 
        portaH= ''
        


    check1 = Button(root, text=' ',width=4,pady=4,bg=localC, command=lambda: localAcess(localVAR,check1))
    check1.place(relx=0.05,rely=0.17)
    lcheck1 = Label(root,text="Acesso na rede local", font=("Trebuche MS", 17),)
    lcheck1.place(relx=0.12,rely=0.17)

    check2 = Button(root, text=' ',width=4,pady=4,bg=ngrokC,command=lambda: ngrokAcess(ngrokVAR,check2,lporta,porta,ngrokApiL,ngrokApi,errorp))
    check2.place(relx=0.05,rely=0.24)
    lcheck2 = Label(root,text="Acesso fora da rede (Ngrok)", font=("Trebuche MS", 17))
    lcheck2.place(relx=0.12,rely=0.24)

    save = Button(root,text="Guardar",bg='#27e85e', font=("Trebuche MS", 12),width=18,command=lambda: guardarHost(errorp))
    save.place(relx=0.69,rely=0.09)

    porta.bind("<FocusIn>", erroP)

    

def localAcess(state, bt):
    global localVAR
    if state:
        bt.configure(bg='#eb4034')
        localVAR = 0
    else:
        bt.configure(bg='#27e85e')
        localVAR = 1

def ngrokAcess(state,bt,pl,p,apil,api,erro):
    global ngrokVAR
    if state:
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


def guardarHost(erro):
    global localVAR, ngrokVAR,porta,ngrokApi
    if int(porta.get()) >= 1 and int(porta.get()) <= 65535:
        erro.place_forget()
        with open(settingsFile,"r+") as j:
            data = json.load(j)
            data["host"]["localNetwork"] = int(localVAR)
            data["host"]["ngrok"] = int(ngrokVAR)
            data["host"]["ngrok_api"] = ngrokApi.get().strip()
            data["host"]["port"] = int(porta.get())

        with open(settingsFile, 'w') as j:
            json.dump(data, j, indent=4)
    
    else:
        erro.configure(text="Porta tem de estar entre 1-65535",fg="#eb4034")
        if int(ngrokVAR):
            erro.place(relx=0.165,rely=0.465)
        else:
            erro.place(relx=0.165,rely=0.36)
        root.focus()

def sairHost(w_list):
    for w in w_list:
        w.destroy()
    ver.configure(text="Ver utilizadores",bg="#856ff8",command=verTodos,)
    defe = Label(root, text="Defenições de Utilizadores", font=("Trebuche MS", 17))
    defe.place(relx=0.02,rely=0.02)
    add.place(relx=0.05,rely=0.16)
    nome.place(relx=0.35,rely=0.155)
    apg.place(relx=0.05,rely=0.23)
    avan.place(relx=0.02,rely=0.34)
    host.place(relx=0.05,rely=0.41)
    quit.place(relx=0.05,rely=0.87)
    start.place(relx=0.7,rely=0.87)

def sucesso(e):
    suc.place_forget()

def erroP(e):
    global errorp
    errorp.place_forget()
    
def close():
    sys.exit()

def Files(uFile,sFile):
    global usersFile,settingsFile
    usersFile=uFile
    settingsFile=sFile


def copyUrl(url,win,yCord,xCord,j):
    pyperclip.copy(url)
    if j==1:
        xCord+=0.1
    suc = Label(win,font=("Trebuche MS", 14),text="Copiado",fg="#27e85e")
    suc.place(relx=xCord,rely=yCord)
    root.after(5000,lambda: labelRemover(suc))

def open_QR(url):
    global qr_win
    try:
        qr_win.destroy()
    except:
        pass
    qr_win = Toplevel()
    
    qr_win.title("")

    img_lbl = Label(qr_win,image=generate_QR(url))
    img_lbl.pack()
    sair = Button(qr_win,text="Fechar",font=("Trebuche MS", 18), bg='#f53b3b',width=12,command=qr_win.destroy)
    sair.pack()

    qr_win.update_idletasks()  # Update "requested size" from geometry manager

    x = (qr_win.winfo_screenwidth() - qr_win.winfo_reqwidth()) / 2
    y = (qr_win.winfo_screenheight() - qr_win.winfo_reqheight()) / 2
    qr_win.geometry("+%d+%d" % (x, y))
    
    qr_win.mainloop()

def generate_QR(url):
    global qr_img
    qr = pyqrcode.create(url)
    qr_img = BitmapImage(data=qr.xbm(scale=7))
    return qr_img


def redirectUrl(url):
    webbrowser.open(url)

def labelRemover(label):
    label.destroy()


def finalizar(win):
    win.destroy()



def menu(url,localIP,p,default):
    win = Tk()
    tiny_urls = [None]*2
    if url!='' and localIP!='':
        janela = 2
        width=900
        b_url = f"https://{url}"
        localIP = f"{localIP}:{p}"
        b_localIP = f"http://{localIP}"
        tn2_url = Thread(target=getTiny,args=(b_localIP,2,tiny_urls,'h',),daemon=True)
        tn2_url.start()
    else:
        janela = 1
        width = 600
        if url=='' and localIP!='':
            url = (f"{localIP}:{p}")
            b_url = f"http://{url}"
        elif  url=='' and localIP=='':
            url = default
            b_url = f"http://{url}"
        else:
            b_url = f"https://{url}"

    #tiny1_url = getTiny(b_url)
    tn1_url = Thread(target=getTiny,args=(b_url,1,tiny_urls,'n',),daemon=True)
    tn1_url.start()


    height = 700
    screen_width = win.winfo_screenwidth()  # Width of the screen
    screen_height = win.winfo_screenheight() # Height of the screen
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    # win window title and dimension
    win.title("Serviço de mesa")
    # Set geometry(widthxheight)
    win.geometry(f'{width}x{height}+{x}+{y}')
    win.resizable(False, False)

    win.protocol("WM_DELETE_WINDOW", lambda: finalizar(win))

    link1 = Label(win,font=("Trebuche MS", 17),text=url)

    link1_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command=lambda: copyUrl(b_url,win,0.12,0.29,janela))

    link1_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(b_url))

    link1_QR = Button(win,font=("Trebuche MS", 17),bg="#8c8c8c",text="QR Code",width=12,command=lambda: open_QR(b_url))

    tiny1 = Label(win,font=("Trebuche MS", 17))

    tn1_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command= lambda: copyUrl(tiny_urls[0],win,0.567,0.29,janela))

    tn1_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(tiny_urls[0]))

    link1.place(relx=0.05,rely=0.03)
    link1_cop.place(relx=0.05,rely=0.1)
    link1_red.place(relx=0.05,rely=0.2)
    link1_QR.place(relx=0.05,rely=0.3)
    tiny1.place(relx=0.05,rely=0.48)
    tn1_cop.place(relx=0.05,rely=0.55)
    tn1_red.place(relx=0.05,rely=0.65)
    
    if janela == 2:

        link2 = Label(win,font=("Trebuche MS", 17),text=localIP)

        link2_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command=lambda: copyUrl(b_localIP,win,0.12,0.85,0))

        link2_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(b_localIP))

        link2_QR = Button(win,font=("Trebuche MS", 17),bg="#8c8c8c",text="QR Code",width=12,command=lambda: open_QR(b_localIP))
        
        tiny2 = Label(win,font=("Trebuche MS", 17))

        tn2_cop = Button(win,font=("Trebuche MS", 17),bg="#856ff8",text="Copiar Link",width=12,command= lambda: copyUrl(tiny_urls[1],win,0.565,0.85,0))

        tn2_red = Button(win,font=("Trebuche MS", 17),bg="#27e85e",text="Abrir Link",width=12,command= lambda: redirectUrl(tiny_urls[1]))

        link2.place(relx=0.55,rely=0.03)
        link2_cop.place(relx=0.55,rely=0.1)
        link2_red.place(relx=0.55,rely=0.2)
        link2_QR.place(relx=0.55,rely=0.3)
        tiny2.place(relx=0.55,rely=0.48)
        tn2_cop.place(relx=0.55,rely=0.55)
        tn2_red.place(relx=0.55,rely=0.65)
        
            

    quit = Button(win,font=("Trebuche MS", 17),text="Terminar",bg="#f53b3b",command=lambda: finalizar(win))
    quit.place(relx=0.5,rely=0.91,anchor=CENTER)

    tn1_url.join()
    tiny1.configure(text=tiny_urls[0])
    tn2_url.join()
    tiny2.configure(text=tiny_urls[1])

    # Execute Tkinter
    root.mainloop()


# create root window
def main():
    global root, defe, ver,add,nome,suc,apg,scrollbar,host,avan,quit,start
    root = Tk()
    width = 800
    height = 800


    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight() # Height of the screen

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    scrollbar = Scrollbar(root)

    # root window title and dimension
    root.title("Serviço de mesa")
    # Set geometry(widthxheight)
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", close)

    # adding a label to the root window
    defe = Label(root, text="Defenições de Utilizadores", font=("Trebuche MS", 17))
    defe.place(relx=0.02,rely=0.02)

    ver = Button(root, text="Ver Utilizadores", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=verTodos)
    ver.place(relx=0.05,rely=0.09)

    add = Button(root, text="Adicionar Utilizador", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=addUser)
    add.place(relx=0.05,rely=0.16)

    nome = Entry(root, font=("Trebuche MS", 20),width=20,highlightthickness=2)
    nome.place(relx=0.35,rely=0.155)

    suc = Label(root, text="Nome adicionado com sucesso!",font=("Trebuche MS", 6),fg="green")
    nome.bind("<FocusIn>", sucesso)

    apg = Button(root, text="Apagar Utilizador", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=apagarUser)
    apg.place(relx=0.05,rely=0.23)

    avan = Label(root, text="Defenições Avançadas", font=("Trebuche MS", 17))
    avan.place(relx=0.02,rely=0.34)

    host = Button(root, text="Mudar Host", font=("Trebuche MS", 12),width=18,bg="#856ff8", command=mudarHost)
    host.place(relx=0.05,rely=0.41)

    quit = Button(root, text="SAIR", font=("Trebuche MS", 18),width=10,pady=5,bg="#eb4034", command=close)
    quit.place(relx=0.05,rely=0.87)

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
