from flask import Flask, request, render_template, jsonify, url_for

app = Flask(__name__)

@app.route("/servico/<nome>", methods=['GET', 'POST'])
def servico(nome):
    global pedidos,n
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
                pedidos.append([nome,quant,ped,tipo,n])
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
    return render_template("confirmar.html",nome=nome)


@app.route('/listaC', methods=['GET','POST'])
def listaC():    
    global pedidos
    comidas=[]
    j=0
    for p in pedidos:
        ped=[p[0],[],[],[],p[4]]
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
        c=0
        for i in range(len(pedidos)):
            if c==0:
                if comidas[i][-1]==int(f):
                    c=1
                    prontos.append(comidas[i])
                    comidas.pop(i)
            if pedidos[i][-1]==int(f):  
                j=0
                apagar=[]
                for t in pedidos[i][3]:
                    if t=='Comida':
                        apagar.append(j)
                    j+=1
                apagar.reverse()
                print(pedidos)
                pedidos.pop(i)
                print(pedidos)
                break
        return jsonify({'suc':'T','redirect':'listaC','nome':0})
    return render_template("pedidos.html",tip='listaC',pedidos=comidas)


@app.route("/lista/<nome>", methods=['GET', 'POST'])
def lista_pessoa(nome):
    global prontos  
    if request.method == 'POST':
        f = request.form["feito"]
        for i in range(len(prontos)):
            if prontos[i][-1]==int(f):
                prontos.pop(i)
                break
        return jsonify({'suc':'T','redirect':'lista/'+nome,})
    return render_template("lista.html",nome=nome,pedidos=prontos)

if __name__ == "__main__":
    pedidos = []
    prontos = []
    users=['ourico','condor','pavao','cuco','gazela','pregui','orix','pavao','chita',]
    n=0
    app.run(debug=True,port=80,host='0.0.0.0')