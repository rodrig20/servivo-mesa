var r = 0;

function addRow(c,opcoes,preco) {
    document.getElementById("titulo").style.display = "table"
    var table = document.getElementById("tabela");
    var row = table.insertRow(-1);
    row.setAttribute("id",r);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var p;
    var c;
    if (c == 'c') {
        p = 'Comida';
        c = '#1ea831';
        var my_opcoes = opcoes[0];
        var my_preco = preco[0];
    } else {
        p = 'Bebida'
        c = '#292b94';
        var my_opcoes = opcoes[1];
        var my_preco = preco[1];
    }
    cell1.innerHTML = "<input type='number' style='border: 3px solid " + c + ";' id='quantity' class='quantity' min='1' oninput='calcular_preco()'>";
    cell2.innerHTML = "<select style='border: 3px solid " + c + ";' id='pedido' class='pedido' onchange='calcular_preco()'><option selected disabled hidden value=''></option></select>";
    cell3.innerHTML = "<input type='button' id='cancelar' onclick='removerPedido(" + r + ")' value=' x '>"
    cell4.innerHTML = "<input type='hidden' class='tipo' value='" + p + "'>"
    cell1.className = 'quantiNum';
    // Adicionar as opções válidas ao select
    var select = cell2.getElementsByTagName("select")[0];
    for (let i = 0; i < my_opcoes.length; i++) {
        var option = document.createElement("option");
        option.text = my_opcoes[i];
        option.value = my_preco[i];
        select.add(option);
    }

    r++;
};

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

function addPreSetRow(opcoes,preco,q,p,t){
    document.getElementById("titulo").style.display = "table"
    var table = document.getElementById("tabela");
    var row = table.insertRow(-1);
    row.setAttribute("id",r);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    if (t == 'Comida') {
        c = '#1ea831'
        var my_opcoes = opcoes[0]
        var my_preco = preco[0];
    } else {
        c = '#292b94'
        var my_opcoes = opcoes[1]
        var my_preco = preco[1];
    }
    cell1.innerHTML = "<input type='number' value="+q+" style='border: 3px solid " + c + ";' id='quantity' class='quantity' min='1' oninput='calcular_preco()'>";
    cell2.innerHTML = "<select style='border: 3px solid " + c + ";' id='pedido' class='pedido' onchange='calcular_preco()'><option selected disabled hidden value=''></option></select>";
    cell3.innerHTML = "<input type='button' id='cancelar' onclick='removerPedido(" + r + ")' value=' x '>"
    cell4.innerHTML = "<input type='hidden' class='tipo' value='" + t + "'>"
    cell1.className = 'quantiNum';
    var select = cell2.getElementsByTagName("select")[0];
    for (let i = 0; i < my_opcoes.length; i++) {
        var option = document.createElement("option");
        option.text = my_opcoes[i];
        option.value = my_preco[i];
        select.add(option);
      
        if (my_opcoes[i] === p) {
          select.selectedIndex = i + 1;
        }
    }
    
    r++;
}

function removerPedido(n){
    var row = document.getElementById(n);
    row.parentNode.removeChild(row)
    if ($('.pedido').length==0){
        document.getElementById("titulo").style.display = "none"
    }
    calcular_preco();
}

function pedidoEntregue(n){
    var tbl = document.getElementById(n);
    tbl.remove();

    json_send = {feito:n};
    nome = $('input[type="hidden"]').val();
    $.post($SCRIPT_ROOT + '/lista/'+nome, json_send, reload,'json');
}

function pedidoPronto(n,v,t){
    $('table#test tr#3').remove();
    json_send = {feito:n, ped:v};
    console.log(n)
    $.post($SCRIPT_ROOT + '/'+t , json_send, reload,'json');
}

function check(data){
    if (data['suc']='T'){
        $(location).prop('href', data['redirect']);
    } 
}

function reload(data){
    if (data['suc']='T'){
        location.reload();
    }
} 
function enviar(){
    var l1 = $('.quantity').length;
    var quant = [];
    for (i = 0; i < l1; i++) { 
        quant.push($('.quantity').eq(i).val());
    }

    var elements = document.getElementsByClassName("pedido")
    var ped = [];
    for (let i=0; i<elements.length;i++){
        ped.push(elements[i].options[elements[i].selectedIndex].text);
        console.log(ped)
    }
    var l3 = $('.tipo').length;
    var tip = [];
    for (i = 0; i < l3; i++) { 
        tip.push($('.tipo').eq(i).val());
    }

    emper = $('input[class="nome"]').val();
    mesa = $('#mesa').val();
    json_send = {emper:emper, quant: quant, ped: ped, tip:tip, mesa:mesa};
    $.post($SCRIPT_ROOT, json_send, check,'json');
}

function menu(){
    $(location).prop('href', $SCRIPT_ROOT + '/menu');
}

function voltar(){
    nome = $('input[type="hidden"]').val();
    $(location).prop('href', $SCRIPT_ROOT + '/servico/' + nome);
}

function voltar_non_user(){
    $(location).prop('href', $SCRIPT_ROOT + '/pedido-automatico');
}
function lista(){
    nome = $('.nome').val();
    $(location).prop('href', $SCRIPT_ROOT + '/lista/'+ nome);
}

function pedAuto(){
    $(location).prop('href', $SCRIPT_ROOT + "/pedido-automatico");
}

// Executar a função de decodificação de QR quando um novo frame de vídeo é exibido
function decodeQR() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    var imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    var code = jsQR(imageData.data, imageData.width, imageData.height);
    if (code) {
      // Se um código QR foi decodificado, exibir o resultado
      sendQrdata(code.data);
    } else {
      // Se nenhum código QR foi encontrado, tentar novamente no próximo frame
      requestAnimationFrame(decodeQR);
    }
}

function toQRScanner(){
    nome = $('input[type="hidden"][class="nome"]').val();
    $(location).prop('href', $SCRIPT_ROOT + '/QRScanner/' + nome);
}

function sendQrdata(data){
    json_send = {pedB64:data}
    $.post($SCRIPT_ROOT, json_send, voltaServico,'json');
}

function voltaServico(data){
    if (data.suc == "T"){
        $(location).prop('href', data['redirect']);
    }
    else{
        if ("message" in data){
            document.getElementById("password").value = "";
            document.getElementById('error-message').style.display = "block"
        }
    }
}

function makeLogin(){
    user = $('input[name="username"]').val().replace(/^\s+|\s+$/g, '');
    password = $('input[name="password"]').val();
    json_send = {user:user,pass:password}
    $.post($SCRIPT_ROOT, json_send, voltaServico,'json');
}

// Início do jQuery:
$(function() {
    $('#send').click(enviar);
    $('#menu').click(menu);
    $('#back').click(voltar);
    $('#back-non-user').click(voltar_non_user);
    $('#lista').click(lista);
    $('#prontos').click(lista);
    $('#novo').click(voltar);
    $('#voltarDoQR').click(pedAuto);
    $('#qrbotao').click(toQRScanner);
    $('#login').click(makeLogin);

});