async function send_async_form(formData, event, success_function) {
    // Previne o envio normal do formulário
    event.preventDefault();

    const currentRoute = window.location.pathname;

    try {
        // Envia os dados via Fetch API para a rota atual
        const response = await fetch("/login", {
            method: "POST",
            body: formData
        });

        const data = await response.json(); // Converte a resposta em JSON

        if (data.success) {
            success_function();
        } else {
            console.error("Erro ao enviar o formulário.");
        }
        return data;
    } catch (error) {
        console.error('Erro:', error);
        return undefined;
    }
}

function validUsername(name) {
    if (name.length < 5) return false
    if (name.indexOf(' ') >= 0) return false
    return true
}

function validPassword(password) {
    if (password.length < 8) return false
    if (password.indexOf(' ') >= 0) return false
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/;
    if (!regex.test(password)) return false
    return true
}

function uiIsValidUsername(el) {
    if (validUsername(el.value)) {
        el.classList.remove('is-invalid');
    } else {
        el.classList.add('is-invalid');
    }
}

function uiIsValidPassword(el) {
    if (validPassword(el.value)) {
        el.classList.remove('is-invalid');
    } else {
        el.classList.add('is-invalid');
    }
}

let order = [];
let totalAmount = 0;

function addToOrder(item, price) {
    // Adicionar molho se selecionado
    let sauces = [];
    if (document.getElementById('ketchup').checked) sauces.push('Ketchup');
    if (document.getElementById('maionese').checked) sauces.push('Maionese');
    if (document.getElementById('mostarda').checked) sauces.push('Mostarda');

    resetExtras();

    // Adicionar item ao pedido
    order.push({ item: item, extras: `${sauces.length > 0 ? `com ${sauces.join(', ')}` : ''}`, "price": price });
    totalAmount += price;
    updateOrderSummary();
}

function updateOrderSummary() {
    const orderList = document.getElementById('orderList');
    const totalAmountDisplay = document.getElementById('totalAmount');
    const sendOrderButton = document.getElementById('sendOrderButton');
    const cancelOrderButton = document.getElementById('cancelOrderButton');

    // Atualiza a lista de pedidos
    orderList.innerHTML = '';
    order.forEach((orderItem, index) => {
        orderList.innerHTML += `<li class="d-flex justify-content-between align-items-center">
    ${orderItem.item} ${orderItem.extras == "" ? "" : (orderItem.extras +" ")}- €${orderItem.price.toFixed(2)}
    <span class="text-danger cursor-pointer" onclick="removeFromOrder(${index})" style="font-size: 2rem; font-weight: bold">&times;</span>
</li>`;
    });

    // Atualiza o valor total
    totalAmountDisplay.innerText = totalAmount.toFixed(2);

    // Habilita o botão de envio se houver itens no pedido
    let disabled_value = order.length === 0;
    sendOrderButton.disabled = disabled_value;
    cancelOrderButton.disabled = disabled_value;
}

function removeFromOrder(index) {
    // Remove o item do pedido e atualiza o total
    totalAmount -= order[index].price;
    order.splice(index, 1);
    updateOrderSummary();
}

function sendOrder() {
    const mesa = document.getElementById('mesaInput');

    if (mesa.value.trim() === '') {
        mesa.classList.add("is-invalid");
        return;
    }
    showLoading()

    let data = { "mesa": mesa.value, "pedido": [] , "extras": []}
    order.forEach((orderItem, _) => {
        data["pedido"].push(orderItem.item)
        data["extras"].push(orderItem.extras)
    })
    fetch('/servico', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Especifica que o corpo da requisição está em JSON
        },
        body: JSON.stringify(data), // Converte o array em uma string JSON
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede');
            }
            return response.json();
        })
        .then(data => {
            doneLoading()
            console.log('Success:', data); // Manipule a resposta do servidor
        })
        .catch((error) => {
            console.error('Error:', error); // Manipule erros
        });

    resetOrder()
}

function resetOrder() {
    order = [];
    totalAmount = 0;
    document.getElementById('mesaInput').value = ""
    // Limpar seleções de molho
    resetExtras();
    updateOrderSummary();
}


function resetExtras() {
    document.getElementById('ketchup').checked = false;
    document.getElementById('maionese').checked = false;
    document.getElementById('mostarda').checked = false;
}

function showLoading() {
    document.getElementById('loadingScreen').style.display = 'flex'; // Mostra a tela de loading
    document.getElementById('loadingTitle').innerHTML = "A Enviar o Pedido...";
    document.getElementById('loadingSpinner').style.display = 'block'; // Mostra o spinner
    document.getElementById('confirmButton').style.display = 'none'; // Esconde o botão de confirmação
}

function hideLoading() {
    document.getElementById('loadingScreen').style.display = 'none'; // Esconde a tela de loading
}

function doneLoading() {
    document.getElementById('loadingSpinner').style.display = 'none'; // Esconde o spinner
    document.getElementById('loadingTitle').innerHTML = "Enviado com Sucesso";
    document.getElementById('confirmButton').style.display = 'block';
}


function renderizarPedidosEspera() {
    const pedidoTableBody = document.getElementById('pedidoTableBody');
    pedidoTableBody.innerHTML = ''; // Limpa a tabela existente

    const totalPedidos = pedidos.length;
    const maxRows = Math.ceil(totalPedidos / 2); // Calcula o número máximo de linhas necessárias

    for (let i = 0; i < maxRows; i++) {
        const row = document.createElement('tr');

        // Primeira coluna
        const cell1 = document.createElement('td');
        if (pedidos[i * 2]) {
            cell1.appendChild(criarPedidoEsperaCell(i * 2));
        }
        row.appendChild(cell1);

        // Segunda coluna
        const cell2 = document.createElement('td');
        if (pedidos[i * 2 + 1]) {
            cell2.appendChild(criarPedidoEsperaCell(i * 2 + 1));
        }
        row.appendChild(cell2);

        pedidoTableBody.appendChild(row);
    }
}

function criarPedidoEsperaCell(index) {
    const div = document.createElement('div');
    const pedidoUsername = pedidos[index][0];
    const pedidoGroup = pedidos[index][1];

    // Cabeçalho fixo do nome de usuário com <h2>
    const usernameHeader = document.createElement('div');
    usernameHeader.className = 'sticky-header';

    const usernameTitle = document.createElement('h2');
    usernameTitle.innerHTML = pedidoUsername;
    usernameHeader.appendChild(usernameTitle);

    div.appendChild(usernameHeader);

    pedidoGroup.forEach((pedido, pedidoIndex) => {
        const pedidoDiv = document.createElement('div');
        pedidoDiv.className = 'pedido';
        pedidoDiv.innerHTML = pedido;

        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-btn btn btn-sm';
        removeBtn.innerHTML = 'X';
        removeBtn.onclick = () => removerPedidoEspera(index, pedidoIndex);

        pedidoDiv.appendChild(removeBtn);
        div.appendChild(pedidoDiv);
    });

    return div;
}

function adicionarPedidoEspera(username, pedido) {
    // Adiciona o pedido como um novo grupo
    pedidos.push([username, pedido]);
    renderizarPedidosEspera(); // Atualiza a tabela
}

function removerPedidoEspera(index, pedidoIndex) {
    // Remove o pedido do grupo
    pedidos[index][1].splice(pedidoIndex, 1);
    socket.emit('cozinha_remove', [index, pedidoIndex])

    // Se não houver mais pedidos no grupo, remove o grupo
    if (pedidos[index][1].length === 0) {
        pedidos.splice(index, 1);
    }

    renderizarPedidosEspera(); // Atualiza a tabela
}

function renderizarPedidosProntos(name) {
    const pedidoTableBody = document.getElementById('pedidoTableBody');
    pedidoTableBody.innerHTML = ''; // Limpa a tabela existente

    for (const mesa in pedidos) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.setAttribute('id', `mesa-${mesa}`);

        // Cabeçalho fixo do nome da mesa
        const mesaHeader = document.createElement('div');
        mesaHeader.className = 'sticky-header';

        const mesaTitle = document.createElement('h2');
        mesaTitle.innerText = mesa;
        mesaHeader.appendChild(mesaTitle);

        cell.appendChild(mesaHeader);
        cell.appendChild(criarPedidoProntoCell(name, mesa));
        row.appendChild(cell);
        pedidoTableBody.appendChild(row);
    }
}

function criarPedidoProntoCell(name, mesa) {
    const div = document.createElement('div');
    pedidos[mesa].forEach((pedido, index) => {
        const pedidoDiv = document.createElement('div');
        pedidoDiv.className = 'pedido';
        pedidoDiv.innerHTML = pedido;

        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-btn btn btn-sm';
        removeBtn.innerHTML = 'X';
        removeBtn.onclick = () => removerPedidoPronto(name, mesa, index);

        pedidoDiv.appendChild(removeBtn);
        div.appendChild(pedidoDiv);
    });

    return div;
}

function removerPedidoPronto(name, mesa, index) {
    // Remove o pedido da mesa
    pedidos[mesa].splice(index, 1);
    socket.emit('prontos_remove', [name, mesa, index]);

    // Se não houver mais pedidos na mesa, removê-la
    if (pedidos[mesa].length === 0) {
        delete pedidos[mesa];
    }
    renderizarPedidosProntos(name); // Atualiza a tabela
}


document.addEventListener("DOMContentLoaded", function () {
    // Verifica se o formulário "loginForm" existe na página antes de adicionar o event listener
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            // Coleta os dados do formulário
            const formData = new FormData(this);

            const username = formData.get("username")
            const password = formData.get("password")
            if (!validUsername(username)) {
                this.username.classList.add("is-invalid")
            }
            if (!validPassword(password)) {
                this.password.classList.add("is-invalid")
            }
            if (validUsername(username) && validPassword(password)) {
                const data = await send_async_form(formData, event, function () { });
                if (data) {
                    if (data.auth) {
                        window.location.href = data.location
                        formError.classList.add('d-none')
                    } else {
                        formError.classList.remove('d-none')
                    }
                }
            }

        });
    }
});