function verificaReload(ped,tip,page,nome='') {
    // Obtem o valor da variável 'pedidos' do template Django e remove os caracteres de escape
    ped = ped.replaceAll("&#39;",'');
    ped = ped.replaceAll('"','');
    
    // Envia uma requisição GET para o servidor Flask para verificar se há mudanças na página
    $.getJSON($SCRIPT_ROOT + '/reload', {
        tipo: tip,
        page: page,
        nome:nome,
        }, function(data) {
            document.getElementById('main').innerHTML=(data.body);
            
    });
}

function verificaReloadList(ped) {
    // Obtem o valor da variável 'pedidos' do template Django e remove os caracteres de escape
    ped = ped.replaceAll("&#39;",'');
    ped = ped.replaceAll('"','');
    // Calcula o hash SHA256 do valor da variável 'pedidos' usando a biblioteca CryptoJS
    var hashHex = String(CryptoJS.SHA256(ped));
    // Envia uma requisição GET para o servidor Flask para verificar se há mudanças na página
    $.getJSON($SCRIPT_ROOT + '/reload', {
        hash: hashHex,
        }, function(data) {
            if (data.change)
                $('body').html(data.body);
    });
}

var r = 0;

function addRow(c) {
    var table = document.getElementById("tabela");
    var row = table.insertRow(-1);
    row.setAttribute("id",r);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var p;
    var c;
    if (c=='c'){
        p= 'Comida';
        c='#1ea831'

    }else{
        p= 'Bebida'
        c='#292b94'
    }
    cell1.innerHTML = "<input type='number' style='border: 3px solid "+c+";' id='quantity' class='quantity' min='1'>";
    cell2.innerHTML = "<input type='text' style='border: 3px solid "+c+";' id='pedido' class='pedido' placeholder='"+ p +"'>";
    cell3.innerHTML = "<input type='button' id='cancelar' onclick='removerPedido("+r+")' value=' x '>"
    cell4.innerHTML = "<input type='hidden' class='tipo' value='"+ p +"'>"
    cell1.className = 'quantiNum';
    r++;
}

function removerPedido(n){
    var row = document.getElementById(n);
    row.parentNode.removeChild(row)
}

function pedidoEntregue(n){
    var tbl = document.getElementById(n);
    tbl.remove();

    json_send = {feito:n};
    nome = $('input[type="hidden"]').val();
    $.post($SCRIPT_ROOT + '/lista/'+nome, json_send, update,'json');
}

function pedidoPronto(n,v,t){
    $('table#test tr#3').remove();
    json_send = {feito:n, ped:v};
    $.post($SCRIPT_ROOT + '/'+t , json_send, update,'json');
}

function update(data){
    document.getElementById('main').innerHTML=(data.body);
}

function check(data){
    if (data['suc']='T'){
        $(location).prop('href', data['redirect']);
    }
}

function reload(data){
    if (data['suc']='T'){
        if (data['nome']==0)
            $(location).prop('href', $SCRIPT_ROOT + '/'+data['redirect']);
            //location.reload();
        else
            $(location).prop('href', $SCRIPT_ROOT + '/'+data['redirect']);  
            //location.reload();
    }
} 

function enviar(){
    var l1 = $('.quantity').length;
    var quant = [];
    for (i = 0; i < l1; i++) { 
        quant.push($('.quantity').eq(i).val());
    }

    var l2 = $('.pedido').length;
    var ped = [];
    for (i = 0; i < l2; i++) { 
        ped.push($('.pedido').eq(i).val());
    }

    var l3 = $('.tipo').length;
    var tip = [];
    for (i = 0; i < l3; i++) { 
        tip.push($('.tipo').eq(i).val());
    }

    emper = $('input[class="nome"]').val();

    json_send = {emper:emper, quant: quant, ped: ped, tip:tip};
    $.post($SCRIPT_ROOT, json_send, check,'json');
}

function voltar(){
    nome = $('input[type="hidden"]').val();
    $(location).prop('href', $SCRIPT_ROOT + '/servico/' + nome);
}
function lista(){
    nome = $('.nome').val();
    $(location).prop('href', $SCRIPT_ROOT + '/lista/'+ nome);
}

// Início do jQuery:
$(function() {
    $('#send').click(enviar);
    $('#back').click(voltar);
    $('#lista').click(lista);
    $('#prontos').click(lista);
    $('#novo').click(voltar);
});