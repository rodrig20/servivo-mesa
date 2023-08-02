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