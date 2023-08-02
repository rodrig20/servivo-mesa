from flask import Flask, request, render_template, jsonify, url_for

app = Flask(__name__)

def getUsers(file):
    utilizadores=[]
    with open(file,"r") as f:
        for l in f:
            if l.strip()!='' and l.strip()[0]!='#':
                utilizadores.append(l.strip())
    return utilizadores


@app.route("/servico/<nome>", methods=['GET', 'POST'])
def servico(nome):
    global pedidos,n,n_p
    if request.method == 'POST':
        try:
            quant = (request.form.getlist('quant[]'))
            ped = (request.form.getlist('ped[]'))
            tipo=(request.form.getlist('tip[]'))
            remove=[]
            for i in range(len(quant)):
                if quant[i].strip() == '' or ped[i].strip() == '':
                    remove.append(i)
            remove.reverse()
            for i in remove:
                tipo.pop(i)
                quant.pop(i)
                ped.pop(i)
            if len(quant) != 0:
                n+=1
                list_n=[]
                for j in range(len(quant)):
                    list_n.append(n_p+1+j)
                n_p+= len(quant)
                pedidos.append([nome,quant,ped,tipo,list_n,n])
                return jsonify({'suc':'T','redirect':url_for('confirmar',nome=nome)})
            else:
                return jsonify({'suc':'F',})
        except Exception as m:
            return(jsonify(resultado=str(m)))
    if not nome in users:
        return "Acesso negado"
    return render_template("home.html",nome=nome)

@app.route("/confirmar/<nome>", methods=['GET', 'POST'])
def confirmar(nome):
    if not nome in users:
        return "Acesso negado"
    return render_template("confirmar.html",nome=nome)


@app.route('/listaC', methods=['GET','POST'])
def listaC():    
    global pedidos
    comidas=[]
    j=0
    for p in pedidos:
        ped=[p[0],[],[],[],p[4],p[5]]
        i=0
        vp=0
        if p[3]==[]:
            pedidos.pop(j)
        for t in p[3]:
            if t=='Comida':
                vp=1
                ped[1].append(p[1][i])
                ped[2].append(p[2][i])
                ped[3].append(p[3][i])
                #if p[4]!=2:
                #    ped[4]=p[4]
            i+=1
        if vp:
            comidas.append(ped)
        j+=1
    if request.method == 'POST':
        f = request.form["feito"]
        p = int(request.form["ped"])
        c=0
        for i in range(len(pedidos)):
            if c==0:
                if comidas[i][-1]==int(f):
                    c=1
                    print(comidas)
                    prontos.append([comidas[i][0],comidas[i][1][p],comidas[i][2][p],comidas[i][-2][p],comidas[i][-1]])
                    print(prontos)
                    #comidas.pop(i)
                    comidas[i][1].pop(p)
                    comidas[i][2].pop(p)
                    comidas[i][3].pop(p)
                    comidas[i][-2].pop(p)
                    print(comidas)
                    
                    
            if pedidos[i][-1]==int(f):
                pedidos[i][1].pop(p)
                pedidos[i][2].pop(p)
                pedidos[i][3].pop(p)
                
                if pedidos [i][1]==[]:
                    pedidos.pop(i)
                    
                break
        return jsonify({'suc':'T','redirect':'listaC','nome':0})
    return render_template("pedidos.html",tip='listaC',pedidos=comidas)

@app.route("/lista/<nome>", methods=['GET', 'POST'])
def lista_pessoa(nome):
    global prontos  
    if request.method == 'POST':
        f = request.form["feito"]
        for i in range(len(prontos)):
            if prontos[i][-2]==int(f):
                prontos.pop(i)
                break
        return jsonify({'suc':'T','redirect':'lista/'+nome,})
    if not nome in users:
        return "Acesso negado"
    return render_template("lista.html",nome=nome,pedidos=prontos)

if __name__ == "__main__":
    pedidos = []
    prontos = []
    n_p=0
    n=0
    file="users.txt"
    try:
        users=getUsers(file)
        if users==[]:
            users[0]=3
    except:
        print("Não existe nenhum utilizador registado")
        exit()
    app.run(debug=True,port=8080,host='0.0.0.0')