var r = 0;

function addRow(opcoes,preco,tipo,content) {
    document.getElementById("titulo").style.display = "table"
    var table = document.getElementById("tabela");
    var row = table.insertRow(-1);
    row.setAttribute("id",r);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    if (tipo == 'Cozinha') {
        cor = '#1ea831'
        var opcoes_tipo = opcoes[0]
        var preco_tipo = preco[0];
    } else {
        cor = '#292b94'
        var opcoes_tipo = opcoes[1]
        var preco_tipo = preco[1];
    }
    cell1.innerHTML = "<input type='number' " + (content !== undefined ? "value='" + content[0] + "'" : "") + " style='border: 3px solid " + cor + ";' id='quantity' class='quantity' min='1' oninput='validarInteiro(this), calcular_preco()'>";
    cell2.innerHTML = "<select style='border: 3px solid " + cor + ";' id='pedido' class='pedido' onchange='calcular_preco()'><option selected disabled hidden value=''></option></select>";
    cell3.innerHTML = "<input type='button' id='removerPedido' onclick='removerPedido(" + r + ")' value='&times;'>"
    cell4.innerHTML = "<input type='hidden' class='tipo' value='" + tipo + "'>"
    cell1.className = 'quantiTable';
    cell2.className = 'pedidoTable';
    // Adicionar as opções válidas ao select
    var select = cell2.getElementsByTagName("select")[0];
    for (let i = 0; i < opcoes_tipo.length; i++) {
        var option = document.createElement("option");
        option.text = opcoes_tipo[i];
        option.value = preco_tipo[i];
        select.add(option);
        if (content !== undefined && opcoes_tipo[i] === content[1]) {
            select.selectedIndex = i + 1;
          }
    }

    r++;
}

function calcular_preco(){
    var elements = document.getElementsByClassName("pedido")
    var quantidade = document.getElementsByClassName("quantity")
    var preco_text = document.getElementById("preco")
    var preco_final = 0;
    for (let i=0; i<elements.length;i++){
        preco_final+=parseFloat(quantidade[i].value*(elements[i].options[elements[i].selectedIndex].value));
    }
    preco_text.textContent = preco_final.toFixed(2)
    
    
}

function validarInteiro(input) {
    input.value = input.value.replace(/\D/g, '');
    if (input.value == "0"){
        input.value = '';
    }
}

function enviar_pedido(){
    var quantidades = document.querySelectorAll('input.quantity');
    var quant = [];
    for (let i = 0; i < quantidades.length; i++) { 
        quant.push(quantidades[i].value);
    }

    var elements = document.getElementsByClassName("pedido")
    var ped = [];
    for (let i=0; i<elements.length;i++){
        ped.push(elements[i].options[elements[i].selectedIndex].text);
    }
    var tipos = document.getElementsByClassName("tipo")
    var tip = [];
    for (let i = 0; i < tipos.length; i++) {
        tip.push(tipos[i].value);
    }
    
    if (quant.length==ped.length && ped.length == tip.length){
        if (nome){
            var mesa = (document.getElementById("mesa").value).replace(/^\s+|\s+$/g, '')
            if (mesa != ''){
                json_send = {quant: quant, ped: ped, tip:tip, mesa:mesa};
                $.post($SCRIPT_ROOT, json_send, redirect,'json');
            }
        } else {
            for(let i=0;i<tip.length;i++){
                if (quant[i]=='' || ped[i] == '')
                    return
            }
            json = {quant: quant, ped: ped, tip:tip};

            // Converter o dicionário em uma string JSON
            var jsonString = JSON.stringify(json);

            // Compactar a string JSON usando LZ77
            var compressedString = LZString.compressToBase64(jsonString).replace(/\//g, "_").replace(/\+/g, "-");

            window.location.replace($SCRIPT_ROOT + '/QrCode?pedido=' + compressedString);
        }
    }
};

function redirect(data){
    if (data['suc']){
        window.location.replace(data['redirect']);
    } 
}

function removerPedido(n){
    var row = document.getElementById(n);
    row.parentNode.removeChild(row)
    if (document.querySelectorAll('.pedido').length==0){
        document.getElementById("titulo").style.display = "none"
    }
    calcular_preco();
}

function voltar_servico(){
    window.location.replace($SCRIPT_ROOT + '/servico');
}

function voltar_cliente(){
    window.location.replace($SCRIPT_ROOT + '/pedido-automatico');
}

function verPedidos(){
    window.location.replace($SCRIPT_ROOT + '/prontos');
}

function scanQR(){
    window.location.replace($SCRIPT_ROOT + '/scanQR');
}

function pedidoPronto(botao,pedidos){
    var numero_pedido = Number($(botao).closest('table').attr('id'));
    var numero_sub_pedido = Number($(botao).closest('tr').attr('id'));

    // Verifica se existe um elemento com uma determinada tag e ID
    var todasTabelas = document.getElementsByTagName('table');
    let tabelaLadoExistente = null;
    let tabelaExistente = null;

    if (numero_pedido%2==0){
        var tabelaLado = numero_pedido+1
    
    } else if (numero_pedido%2==1){
        var tabelaLado = numero_pedido-1
    }

    for (let i=0; i<todasTabelas.length; i++) {
        if (todasTabelas[i].id == tabelaLado.toString()) {
            tabelaLadoExistente = todasTabelas[i];
            if (tabelaExistente) break;

        }else if (todasTabelas[i].id == numero_pedido.toString()){
            tabelaExistente = todasTabelas[i];
            if (tabelaLadoExistente) break;
        }

    }
    if (tabelaLadoExistente) {
        const tbodyLado = tabelaLadoExistente.querySelector('tbody');
        // Verifica o ID da última linha
        const ultimaLinhaLado = tbodyLado.lastElementChild;
        if (ultimaLinhaLado.getAttribute('id') == -1) {
            // Remove a última linha
            ultimaLinhaLado.remove();
        } else {
            // Cria uma nova linha
            const novaLinha = tabelaExistente.insertRow();

            // Define o ID da nova linha
            novaLinha.id = '-1';

            // Cria a célula da coluna
            const novaCelula = novaLinha.insertCell();

            // Define o ID da célula
            novaCelula.id = 'linhaPed';

            // Adiciona o conteúdo à célula
            novaCelula.innerHTML = '<label style="font-size:40px">&nbsp;</label>';
        }

    }
    pedidos[numero_pedido][1].splice(numero_sub_pedido-1, 1)
    pedidos[numero_pedido][2].splice(numero_sub_pedido-1, 1)
    if (pedidos.length>0){
        var ocupado = apagarRow(tabelaExistente,numero_sub_pedido);
        if (!ocupado){
            pedidos.splice(numero_pedido, 1)
            recriarDivEspera(pedidos)
            
        }
    }else{
        apagarRow(tabelaExistente,0);
    }
    const json_send = {numero_pedido:numero_pedido,numero_sub_pedido:numero_sub_pedido-1};

    const options = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json' // Define o tipo de conteúdo como JSON
        },
        body: JSON.stringify(json_send) // Converte os dados para formato JSON
    };

    fetch(window.location.href, options)
        .then(response => {
            // Verifica o status da resposta
            if (!response.ok){
              // A requisição falhou
              console.error('Erro ao enviar os dados');
            }
        })
        .catch(error => {
            // Tratar erros
            console.error(error);
        });
    
}

function recriarDivEspera(pedidos) {
    const elementoPai = document.getElementById('main');
    const novaDiv = document.createElement('div');
    novaDiv.id = 'bigdiv';
  
    const linha = [];
    const part1 = pedidos.filter((_, index) => index % 2 === 0);
    const part2 = pedidos.filter((_, index) => index % 2 !== 0);
    const pedOrganizados = [part1, part2];
    let i = 0;
  
    part2.forEach((part) => {
      linha.push(part[2].length - part1[i][2].length);
      i++;
    });
  
    if (part1.length !== part2.length) {
      linha.push(-(part1[i][2].length));
    }
  
    const c = [1];
    const table_id = [];
    const value_id = [0];
  
    if (part1.length > 0) {
      for (const part of pedOrganizados) {
        if (c[c.length - 1] === 1) {
          var colunaDiv = document.createElement('div');
          colunaDiv.className = 'coluna';
          colunaDiv.style.borderRight = '2px solid #d3d3d3';
          c.push(2);
          table_id.push(0);
        } else if (c[c.length - 1] === 2) {
          var colunaDiv = document.createElement('div');
          colunaDiv.className = 'coluna';
          colunaDiv.style.borderLeft = '2px solid #d3d3d3';
          c.push(3);
          table_id.push(1);
        }
  
        for (let p = 0; p < part.length; p++) {
          if (part[p][1].length > 0) {
            const table = document.createElement('table');
            table.id = table_id[table_id.length - 1];
  
            const thead = document.createElement('thead');
            const tr = document.createElement('tr');
            const th = document.createElement('th');
            th.id = 'nome';
            tr.style.lineHeight = "80px"
  
            const pElement = document.createElement('p');
            pElement.style.fontSize = '70px';
            pElement.innerHTML = `<b>&nbsp;&nbsp;&nbsp;&nbsp;${part[p][0]}</b>`;
  
            th.appendChild(pElement);
            tr.appendChild(th);
            thead.appendChild(tr);
            table.appendChild(thead);
            
  
            value_id.push(1);
            const tbody = document.createElement('tbody');
            for (let i = 0; i < part[p][1].length; i++) {
              const tr = document.createElement('tr');
              tr.id = value_id[value_id.length-1];
  
              const td = document.createElement('td');
              td.id = 'linhaPed';
  
              const input = document.createElement('input');
              input.className = 'check';
              input.type = 'button';
              input.id = 'estaPronto';
              input.value = '\u2714';
              input.onclick = function () {
                pedidoPronto(this,pedidos);
              };
  
              const label1 = document.createElement('label');
              label1.style.fontSize = '35px';
              label1.innerHTML = `&nbsp;${part[p][1][i]}`;
  
              const label2 = document.createElement('label');
              label2.style.fontSize = '35px';
              label2.style.color = 'red';
              label2.innerHTML = '&nbsp;\u21d2&nbsp;';
  
              const label3 = document.createElement('label');
              label3.style.fontSize = '35px';
              label3.innerHTML = part[p][2][i];
  
              td.appendChild(input);
              td.appendChild(label1);
              td.appendChild(label2);
              td.appendChild(label3);
              tr.appendChild(td);
              tbody.appendChild(tr);
              table.appendChild(tbody);
              
  
              value_id.push(value_id[value_id.length - 1] + 1);
            }
  
            if (linha[p] > 0 && c[c.length - 1] === 2) {
              for (let i = 0; i < linha[p]; i++) {
                const tr = document.createElement('tr');
                tr.id = '-1';
  
                const td = document.createElement('td');
                td.id = 'linhaPed';
  
                const label = document.createElement('label');
                label.style.fontSize = '40px';
                label.innerHTML = '&nbsp;';
  
                td.appendChild(label);
                tr.appendChild(td);
                tbody.appendChild(tr);
                table.appendChild(tbody);

              }
            }
  
            if (linha[p] < 0 && c[c.length - 1] === 3) {
              for (let i = 0; i < -linha[p]; i++) {
                const tr = document.createElement('tr');
                tr.id = '-1';
  
                const td = document.createElement('td');
                td.id = 'linhaPed';
  
                const label = document.createElement('label');
                label.style.fontSize = '40px';
                label.innerHTML = '&nbsp;';
  
                td.appendChild(label);
                tr.appendChild(td);
                tbody.appendChild(tr);
                table.appendChild(tbody);
                
              }
            }
  
            table.appendChild(document.createElement('br'));
            table.appendChild(document.createElement('br'));
            colunaDiv.appendChild(table)
        }
        
        table_id.push(table_id[table_id.length - 1] + 2);
        }
        novaDiv.appendChild(colunaDiv);
      }
    }
  
    // Remove o conteúdo existente do elemento pai
    while (elementoPai.firstChild) {
      elementoPai.firstChild.remove();
    }
  
    // Adiciona a nova div ao elemento pai
    elementoPai.appendChild(novaDiv);
}

function removerPronto(botao,pedidos){
    var mesa = $(botao).closest('table').attr('id');
    var table_mesa = document.querySelector('table[id="'+mesa+'"]');
    var linha = $(botao).closest('tr').attr('id');
    var todasTabelas = document.getElementsByTagName('table');
    var tabela;
    for (let i=0;i<todasTabelas.length;i++){
        if(todasTabelas[i].id == mesa) {
            tabela = todasTabelas[i];
            break;}
    }

    apagarRow(tabela,linha)
    var linha_num = Number(linha)
    for(let i=0;i<pedidos[2].length;i++){
        if (pedidos[2][i]==table_mesa.dataset.mesa){
            if (linha_num==0){
                pedidos[0].splice(i,1)
                pedidos[1].splice(i,1)
                pedidos[2].splice(i,1)
                const json_send = {sub_idx:i};

                const options = {
                    method: 'DELETE',
                    headers: {
                    'Content-Type': 'application/json' // Define o tipo de conteúdo como JSON
                    },
                    body: JSON.stringify(json_send) // Converte os dados para formato JSON
                };

                fetch(window.location.href, options)
                    .then(response => {
                        // Verifica o status da resposta
                        if (!response.ok){
                            // A requisição falhou
                            console.error('Erro ao enviar os dados');
                        }
                    })
                    .catch(error => {
                        // Tratar erros
                        console.error(error);
                    });
                break;
            }
            linha_num--;
        }
    }
    if (table_mesa.rows.length==0){
        recriarDivProntos(pedidos)
    }
}

function recriarDivProntos(pedidos){
    const elementoPai = document.getElementById('main');
    //const novaDiv = document.createElement('div');
    //novaDiv.id = 'main';
    var pedidos_mesa = [];
    var pedidos_organizados = [];
    var idx;
    while (elementoPai.firstChild) {
        elementoPai.firstChild.remove();
    }
    
    if (pedidos && pedidos.length!==0 && pedidos[0].length!==0){
        for (let m=0;m<pedidos[2].length;m++){
            idx = pedidos_mesa.indexOf(pedidos[2][m])

            if (idx != -1){
                pedidos_organizados[idx].push([pedidos[0][m],pedidos[1][m]])
            } else {
                pedidos_mesa.push(pedidos[2][m])
                pedidos_organizados.push([[pedidos[0][m],pedidos[1][m]]])
            }
        }
        for (let i=0;i<pedidos_mesa.length;i++){
            // Remove o conteúdo existente do elemento pai
            const h2 = document.createElement('h2');
            h2.style.fontSize = '60px'
            h2.innerHTML = '&emsp;'+pedidos_mesa[i]
            elementoPai.appendChild(h2)
            const table = document.createElement('table');
            const tbody = document.createElement('tbody');
            table.id = i;
            table.dataset.mesa = pedidos_mesa[i];
            for (let j=0;j<pedidos_organizados[i].length;j++){
                const tr  = document.createElement('tr')
                const td1  = document.createElement('td')
                const input = document.createElement('input');
                input.setAttribute('type', 'button');
                input.setAttribute('class','check');
                input.setAttribute('id', 'removerPronto');
                input.onclick = function(){
                    removerPronto(this,pedidos);
                };
                input.value = '✓';

                const td2  = document.createElement('td')
                // Criar o primeiro label
                const label1 = document.createElement('label');
                label1.style.fontSize = '50px';
                label1.textContent = pedidos_organizados[i][j][0];

                // Criar o segundo label
                const label2 = document.createElement('label');
                label2.style.fontSize = '50px';
                label2.style.color = 'red';
                label2.textContent = '➜';

                // Criar o terceiro label
                const label3 = document.createElement('label');
                label3.style.fontSize = '50px';
                label3.textContent = pedidos_organizados[i][j][1];
                
                tr.id = j;

                td1.appendChild(input);
                td2.appendChild(label1);
                td2.appendChild(label2);
                td2.appendChild(label3);
                tr.appendChild(td1);
                tr.appendChild(td2);
                tbody.appendChild(tr);
            }
            table.appendChild(tbody);
            elementoPai.appendChild(table);

            
        }
    }
    
}

function apagarRow(tabela,idx){
    tabela.deleteRow(idx);
    for (let i=idx; i<tabela.rows.length; i++){
        if (tabela.rows[i].id == "-1"){
            break
        }
        tabela.rows[i].id = i.toString();
    }
    return (tabela.rows.length>1 && tabela.rows[1].id != "-1")
    
}

function makeLogin(){
    var user = document.querySelector('input[name="username"]').value.trim();
    var password = document.querySelector('input[name="password"]').value;
    if (user!='' && password!=''){
        json_send = {user:user,pass:password};
        $.post($SCRIPT_ROOT, json_send, loginValidation,'json');
    } else {
        erro = document.getElementById('error-message');
        if (erro.innerText == "");
            erro.innerText = "*nome de utilizador ou password incorreta";
        erro.style.display = "block";
    }
}

function loginValidation(data){
    if (data["suc"])
        window.location.replace(data['redirect']);
    else{
        var campo = document.querySelector('input[name="password"]');
        campo.select();
        erro = document.getElementById('error-message');
        erro.style.display = "block";
        erro.innerText = "*"+data["erro"]
    }
}

function makeLogout(){
    window.location.replace($SCRIPT_ROOT + '/logout');
}

function ver_menu(){
    if (nome)
        window.location.replace($SCRIPT_ROOT + '/menu?page=servico');
    else
        window.location.replace($SCRIPT_ROOT + '/menu?page=cliente');
}

function voltar_menu() {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);

    const pageValue = params.get('page');

    if (pageValue === "servico") {
        window.location.replace($SCRIPT_ROOT + '/servico');
    } else {
        window.location.replace($SCRIPT_ROOT + '/pedido-automatico');
    }
    
}

$(function() {
    $('#send').click(enviar_pedido);
    $('#voltar_servico').click(voltar_servico);
    $('#voltar_cliente').click(voltar_cliente);
    $('#verPedidos').click(verPedidos);
    $('#scanQR').click(scanQR);
    $('#login').click(makeLogin);
    $('#logout').click(makeLogout);
    $('#menu').click(ver_menu);
    $('#voltar_menu').click(voltar_menu);
});