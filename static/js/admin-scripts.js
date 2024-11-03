// Function to add a new atendente
function addAtendente(atendenteName) {
    const atendentesListElement = document.getElementById("atendentes-list");
    const li = document.createElement("li");
    document.getElementById("saveAtendentesChanges").disabled = false;
    document.getElementById("deleteAtendentesChanges").disabled = false;
    li.className = "list-group-item d-flex justify-content-between align-items-center atendente-box";
    li.name = atendenteName;
    li.innerHTML = `
            <span class="atendente-text">${atendenteName}</span>
            <input type="text" class="form-control edit-input" style="display: none;" onblur="editAtendentesList(this.parentElement.getElementsByClassName('btn')[1])" value="${atendenteName}">
            <div class="btn-group">
                <button class="btn btn-danger btn-sm delete-btn delete-atendente" onclick="deleteAtendentesList(this)">&#x2715;</button>
                <button class="btn btn-primary btn-sm edit-btn edit-atendente" onclick="editAtendentesList(this)">&#9998;</button>
            </div>
            `;
    atendentesListElement.appendChild(li);
    atendentesUpdatedList.push(atendenteName);
}

// Function to add a new atendente
function addMenu(menuName, menuPrice) {
    const menuListElement = document.getElementById("menu-list");
    const li = document.createElement("li");

    document.getElementById("saveMenuChanges").disabled = false;
    document.getElementById("deleteMenuChanges").disabled = false;

    li.className = "list-group-item d-flex justify-content-between align-items-center menu-box";
    li.name = menuName;
    li.innerHTML = `
        <span class="menu-text">${menuName} - ${parseFloat(menuPrice).toFixed(2)}€</span>
        <input type="text" class="form-control edit-input" style="display: none;" onfocus="changeEditMenuFocus(this.parentElement.getElementsByClassName('btn')[1], 1)" onblur="changeEditMenuFocus(this.parentElement.getElementsByClassName('btn')[1], -1)" value="${menuName}">
        <input type="number" class="form-control edit-input" style="display: none;" onfocus="changeEditMenuFocus(this.parentElement.getElementsByClassName('btn')[1], 1)" onblur="changeEditMenuFocus(this.parentElement.getElementsByClassName('btn')[1], -1)" value="${menuPrice}">
        <div class="btn-group">
            <button class="btn btn-danger btn-sm delete-btn delete-menu" onclick="deleteMenuElement(this)">&#x2715;</button>
            <button class="btn btn-primary btn-sm edit-btn edit-menu" onclick="editMenuElement(this)">&#9998;</button>
        </div>
    `;

    menuListElement.appendChild(li);
    menuUpdatedList[menuName] = +menuPrice;
}


// Handle form submission
function handleFormAtendenteSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('atendentes-input');
    const name = input.value.trim();
    if (name !== "") {
        addAtendente(name);
        input.value = "";
    }
    return false;
}

// Handle form submission
function handleFormMenuSubmit(event) {
    event.preventDefault();
    const nameInput = document.getElementById('menu-input');
    const priceInput = document.getElementById('menu-price-input');
    const menuName = nameInput.value.trim();
    const menuPrice = parseFloat(priceInput.value.trim()).toFixed(2);

    if (menuName !== "" && !isNaN(menuPrice)) {
        addMenu(menuName, menuPrice);
        nameInput.value = "";
        priceInput.value = "";
    }
    return false;
}

// Function to delete a atendente
function deleteAtendentesList(button) {
    const li = button.parentElement.parentElement;
    const index = atendentesUpdatedList.indexOf(li.name);
    document.getElementById("saveAtendentesChanges").disabled = false;
    document.getElementById("deleteAtendentesChanges").disabled = false;
    if (index !== -1) {
        atendentesUpdatedList.splice(index, 1);
    }
    li.remove();
}

// Function to delete a menu
function deleteMenuElement(button) {
    const li = button.parentElement.parentElement;
    document.getElementById("saveMenuChanges").disabled = false;
    document.getElementById("deleteMenuChanges").disabled = false;
    delete menuUpdatedList[li.name];
    li.remove()

}

// Function to edit a atendente
function editAtendentesList(button) {
    const li = button.parentElement.parentElement;
    const atendenteText = li.querySelector(".atendente-text");
    const editInput = li.querySelector(".edit-input");
    document.getElementById("saveAtendentesChanges").disabled = false;
    document.getElementById("deleteAtendentesChanges").disabled = false;
    if (atendenteText.style.display !== "none") {
        atendenteText.style.display = "none";
        editInput.style.display = "block";
        button.disabled = true
        editInput.focus();
    } else {
        atendenteText.textContent = editInput.value;
        atendenteText.style.display = "inline";
        editInput.style.display = "none";
        button.disabled = false
        const index = atendentesUpdatedList.indexOf(li.name);
        li.name = editInput.value;
        if (index !== -1) {
            atendentesUpdatedList[index] = editInput.value;
        }
    }
}

// Function to edit a atendente
function editMenuElement(button) {

    const li = button.parentElement.parentElement;
    const itemText = li.querySelector(".menu-text");
    const editInputs = li.querySelectorAll(".edit-input");
    const nameInput = editInputs[0];
    const priceInput = editInputs[1];
    document.getElementById("saveMenuChanges").disabled = false;
    document.getElementById("deleteMenuChanges").disabled = false;
    if (itemText.style.display !== "none") {
        itemText.style.display = "none";
        nameInput.style.display = "block";
        priceInput.style.display = "block";
        button.disabled = true;
        nameInput.focus();
    }
}

async function changeEditMenuFocus(button, count) {
    if (count < 0) {
        await new Promise(resolve => setTimeout(resolve, 1));
    }
    if (window.menuEditCount) {
        window.menuEditCount += count
    } else {
        window.menuEditCount = count
    }

    if (window.menuEditCount == 0) {
        const li = button.parentElement.parentElement;
        const editInputs = li.querySelectorAll(".edit-input");
        const nameInput = editInputs[0];
        const priceInput = editInputs[1];
        const newName = nameInput.value;
        const itemText = li.querySelector(".menu-text");
        const newPrice = parseFloat(priceInput.value).toFixed(2);
        itemText.textContent = `${newName} - ${newPrice}€`;
        itemText.style.display = "inline";
        nameInput.style.display = "none";
        priceInput.style.display = "none";
        console.log(li.name)
        delete menuUpdatedList[li.name];
        li.name = newName
        console.log(li.name)
        button.disabled = false;
        menuUpdatedList[newName] = +newPrice
    }
}

// Function to save changes (you can customize this function)
function saveAtendentesListChanges() {
    fetch('/admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ atendentes: atendentesUpdatedList })
    })
        .then(response => response.json()) // Espera a resposta do servidor em JSON
        .then(data => {
            console.log('Success:', data);
            atendentesOriginalList = [...atendentesUpdatedList]
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Function to save changes (you can customize this function)
function saveMenuListChanges() {
    fetch('/admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ menu: menuUpdatedList })
    })
        .then(response => response.json()) // Espera a resposta do servidor em JSON
        .then(data => {
            console.log('Success:', data);
            menuOriginalList = { ...menuUpdatedList }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Function to delete changes (you can customize this function)
function deleteAtendentesListChanges() {
    atendentesUpdatedList = []
    // Implement deletion logic here
    const deleteBtns = document.querySelectorAll('.delete-atendente');

    // Adicionando um evento de clique a cada botão
    deleteBtns.forEach(element => {
        element.click()
    });
    atendentesLoad()
}

// Function to delete changes (you can customize this function)
function deleteMenuListChanges() {
    menuUpdatedList = []
    // Implement deletion logic here
    const deleteBtns = document.querySelectorAll('.delete-menu');

    // Adicionando um evento de clique a cada botão
    deleteBtns.forEach(element => {
        element.click()
    });
    menuLoad()
}

function atendentesLoad() {
    for (let atendenteName of atendentesOriginalList) {
        addAtendente(atendenteName);
    }
    document.getElementById("saveAtendentesChanges").disabled = true;
    document.getElementById("deleteAtendentesChanges").disabled = true;
}

function menuLoad() {
    for (let menuName in menuOriginalList) {
        addMenu(menuName, menuOriginalList[menuName]);
    }
    document.getElementById("saveMenuChanges").disabled = true;
    document.getElementById("deleteMenuChanges").disabled = true;
}


function removeAllHistory() {
    vendas = []
    document.getElementById('pedidoTabela').innerHTML = '';
    historyLoad()
    fetch('/admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ history_delete: true })
    })
        .then(response => response.json()) // Espera a resposta do servidor em JSON
        .then(data => {
            console.log('Success:', data);
            menuOriginalList = { ...menuUpdatedList }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function calcTotalHistory(pedidoName) {
    let total = 0;
    if (!pedidoName){
        vendas.forEach(pedido => total += (menuOriginalList[pedido[0]] || 0));
    } else{
        total += parseFloat(document.getElementById('totalDinheiro').innerText) + (menuOriginalList[pedidoName] || 0)
    }
    document.getElementById('quantidadePedidos').innerText = vendas.length;
    document.getElementById('totalDinheiro').innerText = total.toFixed(2);
}

function listHistory(pedido) {
    const tabela = document.getElementById('pedidoTabela');
    if (!pedido) {
        vendas.forEach(pedido => {
            const row = `<tr>
                    <td>${pedido[0] + (pedido[1] !== "" ? (" " + pedido[1]) : "")}</td>
                    <td>${(menuOriginalList[pedido[0]] || 0).toFixed(2)} €</td>
                    <td>${pedido[2]}</td>
                 </tr>`;
            tabela.innerHTML += row;
        });
    } else {
        const row = `<tr>
                    <td>${pedido[0] + (pedido[1] !== "" ? (" " + pedido[1]) : "")}</td>
                    <td>${(menuOriginalList[pedido[0]] || 0).toFixed(2)} €</td>
                    <td>${pedido[2]}</td>
                 </tr>`;
        tabela.innerHTML += row;
    }
}

function historyLoad(content) {
    listHistory(content)
    calcTotalHistory(content ? content[0]: undefined)
}

function downloadExcel() {
    fetch('/admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ get_excel: true })
    })
        .then(response => {
            if (response.ok) {
                return response.blob(); // Converte a resposta em um Blob
            }
            throw new Error('Erro ao baixar o arquivo');
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob); // Cria um URL para o Blob
            const a = document.createElement('a'); // Cria um elemento <a>
            a.style.display = 'none';
            a.href = url; // Define o href para o Blob
            a.download = 'vendas.xlsx'; // Define o nome do arquivo para download
            document.body.appendChild(a); // Adiciona o <a> ao DOM
            a.click(); // Simula um clique no <a>
            window.URL.revokeObjectURL(url); // Libera o URL
        })
        .catch(error => console.error('Erro:', error));

}


function loadAll() {
    atendentesLoad()
    menuLoad()
    historyLoad()
}

function showSection(index) {
    // Seleciona todas as seções
    const sections = document.querySelectorAll('.content-section');

    // Oculta todas as seções
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Mostra a seção desejada
    sections[index].classList.add('active');

    // Atualiza o estado ativo da navegação
    const navLinks = document.querySelectorAll('.nav-item.nav-link');
    navLinks.forEach((link, i) => {
        link.classList.remove('active');
        if (i === index) {
            link.classList.add('active');
        }
    });
    closeNavbar()
}

function closeNavbar() {
    const navbarToggle = document.getElementById('navbarToggle');
    const navbarCollapse = document.getElementById('navbarNavAltMarkup');

    // Verifica se o menu está aberto e fecha se necessário
    if (navbarCollapse.classList.contains('show')) {
        navbarToggle.click(); // Simula um clique para fechar
    }
}