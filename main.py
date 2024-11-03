import json
import os
import sqlite3
from functools import wraps
from hashlib import sha256

import pandas as pd
from flask import (
    Flask,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from flask_socketio import SocketIO

from pedidos import PedidosEsperaList, PedidosProntoList


class Data:
    """Classe que contém métodos estáticos para manipulação de dados de menu e usuários"""

    db_path = "./data/vendas.db"
    excel_path = "./data/vendas.xlsx"
    users_path = "./data/users.json"
    menu_path = "./data/menu.json"

    def __new__(cls):
        # Impede a instanciação da classe
        raise TypeError("This class cannot be instantiated")

    @staticmethod
    def ensure_file(file_name: str) -> None:
        """Verifica se o arquivo existe, caso contrário, cria um arquivo vazio.

        Args:
            file_name (str): Caminho do arquivo a ser verificado.
        """
        if not os.path.isfile(file_name):
            with open(file_name, "w"):
                pass

    @staticmethod
    def load_json(file_name: str):
        """Carrega o conteúdo de um arquivo JSON.

        Args:
            file_name (str): Caminho do arquivo JSON.

        """

        Data.ensure_file(file_name)
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                # Retorna o conteúdo do arquivo JSON
                return json.load(file)
            except json.decoder.JSONDecodeError:
                # Caso haja algum erro, retorna None
                return None

    @staticmethod
    def start_data_base() -> None:
        """Inicializa o banco de dados criando o arquivo se não existir e a tabela de pedidos."""
        # Cria o ficheiro se não existir
        Data.ensure_file(Data.db_path)

        conn = sqlite3.connect(Data.db_path)
        cursor = conn.cursor()

        # Criar a tabela
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_nome TEXT NOT NULL,
                extras TEXT NOT NULL,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        # Apaga os dados da tabela
        Data.clear_data_base(cursor)
        conn.commit()
        conn.close()

    @staticmethod
    def clear_data_base(cursor: sqlite3.Cursor = None) -> None:
        """Limpa todos os registros da tabela de pedidos.

        Args:
            cursor (sqlite3.Cursor, optional): Cursor da conexão com o banco de dados. Se None, uma nova conexão será criada.
        """
        if cursor is None:
            conn = sqlite3.connect(Data.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedidos")
            conn.commit()
            conn.close()
        else:
            cursor.execute("DELETE FROM pedidos")

    @staticmethod
    def send_vendas_file() -> Response:
        """Gera um arquivo com as vendas e o envia como anexo.

        Returns:
            Response: Resposta da requisição com o arquivo enviado como anexo.
        """
        conn = sqlite3.connect(Data.db_path)
        df = pd.read_sql_query(
            "SELECT pedido_nome AS 'Nome do Pedido', extras AS 'Extras', data_hora AS Data FROM pedidos",
            conn,
        )

        df.to_excel(Data.excel_path, index=False)
        conn.close()

        return send_file(Data.excel_path, as_attachment=True)

    @staticmethod
    def load_menu() -> dict[str, float]:
        """Carrega o menu de um arquivo JSON.

        Returns:
            dict[str, float]: Dicionário com itens do menu e seus preços.
        """

        return Data.load_json(Data.menu_path) or {}

    @staticmethod
    def load_users() -> set[str]:
        """Carrega um set de usuários de um arquivo JSON.

        Returns:
            set[str]: Set com nomes de usuários.
        """
        users = Data.load_json(Data.users_path)
        return set(users) if users is not None else set()

    @staticmethod
    def load_vendas() -> list[list[str]]:
        """Carrega todas as vendas registradas no banco de dados.

        Returns:
            list[list[str]]: Lista de vendas, cada uma representada por uma lista contendo nome do pedido, extras e data/hora.
        """
        conn = sqlite3.connect(Data.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos")

        vendas = []
        # Recuperar todas as linhas
        while True:
            linha = cursor.fetchone()
            # Sai do loop quando não há mais linhas
            if linha is None:
                break
            vendas.append([linha[1], linha[2], linha[3]])

        conn.close()

        return vendas

    @staticmethod
    def update_menu(menu: dict[str, float]) -> None:
        """Atualiza o menu em um arquivo JSON e na configuração do site.

        Args:
            menu (dict[str, float]): Dicionário com itens do menu e seus preços.
        """
        with open(Data.menu_path, "w", encoding="utf-8") as file:
            # Atualiza o menu no arquivo JSON
            json.dump(menu, file, ensure_ascii=False, indent=4)

        # Atualiza a configuração do site
        app.config["MENU"] = menu

    @staticmethod
    def update_usernames(usernames: list[str]) -> None:
        """Atualiza a lista de usuários em um arquivo JSON e na configuração do site.

        Args:
            usernames (list[str]): Lista de nomes de usuários.
        """
        with open(Data.users_path, "w", encoding="utf-8") as file:
            # Atualiza os usuários no arquivo JSON
            json.dump(usernames, file, ensure_ascii=False, indent=4)

        # Atualiza a configuração do site
        app.config["USER_NAMES"] = set(usernames)

    @staticmethod
    def update_vendas(
        subpedido: str, extras: str, return_timestamp: bool = False
    ) -> str | None:
        """Insere um novo pedido no banco de dados.

        Args:
            subpedido (str): Nome do pedido.
            extras (str): Extras do pedido.
            return_timestamp (bool): Se True, retorna o timestamp da inserção.

        Returns:
            (str | None): Timestamp do pedido inserido se `return_timestamp` for True, senão None.
        """
        conn = sqlite3.connect(Data.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO pedidos (pedido_nome, extras) VALUES (?, ?)
        """,
            (subpedido, extras),
        )
        if return_timestamp:
            last_id = cursor.lastrowid

            # Consultar a data e hora do pedido inserido
            cursor.execute(
                """
                SELECT data_hora FROM pedidos WHERE id = ?
                """,
                (last_id,),
            )

            # Obtém o timestamp
            data_hora = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        if return_timestamp:
            return data_hora


class SocketUi(SocketIO):
    def update_cozinha(self, content: list[str | list[str]] | None = None) -> None:
        """Atualiza a interface da cozinha com os pedidos em espera.

        Args:
            content (list[str | list[str]] | None, optional): Dados a serem enviados para a cozinha.
                Se None, utiliza a lista de pedidos inteira da configuração.
        """
        # Calcula quais dados devem ser enviados para a cozinha
        data = content if content is not None else PedidosEsperaList.simplified()
        # Emite os dados para a cozinha
        self.emit("update_cozinha", {"data": data})

    def update_admin(self, content: list[str] | None = None):
        """Atualiza a interface do administrador com o total de pedidos prontos.

        Args:
            content (list[str] | None, optional): Dados a serem enviados ao administrador.
                Se None, utiliza a lista de vendas carregadas do banco de dados.
        """
        # Calcula quais dados devem ser enviados para a página de admin
        data = content if content is not None else Data.load_vendas()
        # Emite os dados para o admin
        self.emit("update_admin", {"data": data})

    def update_prontos(
        self, name: str, content: tuple[str, dict[str, str]] | None = None
    ) -> None:
        """Atualiza a interface dos pedidos prontos para um atendente específico.

        Args:
            name (str): Nome do atendente para quem os pedidos prontos estão sendo atualizados.
            content (tuple[str, dict[str, str]] | None, optional): Dados a serem enviados.
                Se None, utiliza a lista de pedidos prontos do atendente correspondente.
        """
        # Calcula quais dados devem ser enviados para os pedidos prontos do atendetente
        data = content if content is not None else PedidosProntoList.simplified(name)
        # Emite os dados para os pedidos prontos do atendente
        self.emit("update_prontos_" + name, {"data": data})


class Login:
    def __new__(cls):
        # Impede a instanciação da classe
        raise TypeError("This class cannot be instantiated")

    @staticmethod
    def required(func):
        """Decorador que verifica se o usuário está autenticado."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            #  Verifica se o utilizador está autenticado e em caso afirmativo executa a rora
            if session.get("auth", False):
                return func(*args, **kwargs)
            # Caso contrário redireciona para a página de login
            return redirect(url_for("login"))

        return wrapper

    @staticmethod
    def required_as_user(username: str):
        """Decorador que verifica se o usuário está autenticado e se o nome de usuário é o esperado."""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Verifica se o utilizador está autenticado e tem um determinado username
                if session.get("auth", False) == username:
                    return func(*args, **kwargs)
                # Caso contrário, redireciona para a página de login
                return redirect(url_for("login"))

            return wrapper

        return decorator


app = Flask(__name__)
socketio = SocketUi(app)

# Carrega usuários e o menu guardado na pasta './data'
Data.start_data_base()
app.config["USER_NAMES"] = Data.load_users()
app.config["SPECIAL_USER_NAMES"] = {"cozinha": "cozinha", "admin": "admin"}
app.config["MENU"] = Data.load_menu()
# Hash da senha dos usuários
app.config["USER_PASSWORD_HASH"] = (
    "4e9600e62f0a1eac60f74fa8ef8552c96247dee51ba68b8e9a6fffdd6a4ad1b8"
)
# Chave secreta para sessões
app.secret_key = "oSZZM6dToiLQ1Sgkw4ERrPp13ZHYi23nubTdwBD5XcbsXsY6tznzVDhDziZM1jM9"


@socketio.on("cozinha_connect")
def handle_cozinha_connect() -> None:
    """Lida com a conexão da cozinha, atualizando a sua interface."""
    socketio.update_cozinha()


@socketio.on("prontos_connect")
def handle_prontos_connect(name: str) -> None:
    """Lida com conexão dos pedidos prontos, atualizando a sua interface.

    Args:
        name (str): Nome do atendente.
    """
    socketio.update_prontos(name)


@socketio.on("admin_connect")
def handle_admin_connect() -> None:
    """Lida com a conexão de admin, atualizando a sua interface."""
    socketio.update_admin()


@socketio.on("cozinha_remove")
def handle_cozinha_remove(data: list[int]) -> None:
    """Lida com a remoção de um subpedido na cozinha.

    Args:
        data (list[int]): Lista contendo o índice do pedido e o índice do subpedido a ser removido.
    """
    # Transferência do pedido de em espera para pronto
    username, subpedido, extras, mesa = PedidosEsperaList.transfer(data[0], data[1])
    # Atualiza a interface com a lista de pedidos prontos
    socketio.update_prontos(
        username,
        {"mesa": mesa, "subpedido": subpedido + (f" {extras}" if extras else "")},
    )
    timestamp = Data.update_vendas(subpedido, extras, return_timestamp=True)
    socketio.update_admin([subpedido, extras, timestamp])


@socketio.on("prontos_remove")
def handle_prontos_remove(data: list[int]) -> None:
    """Lida com a remoção de um pedido pronto.

    Args:
        data (list[int]): Lista contendo o nome do atendente, número da mesa e índice do subpedido a ser removido.
    """
    # Remove o subpedido
    PedidosProntoList.remove(data[0], data[1], data[2])


@app.route("/", methods=["GET"])
def home():
    # Redireciona para o serviço se autenticado
    if username := session.get("auth", False):
        location = url_for(app.config["SPECIAL_USER_NAMES"].get(username, "servico"))
        return redirect(location)

    # Redireciona para a página de login se não autenticado
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Retorna a página de login
        return render_template("login.html")

    else:
        # Obtém nome de usuário e senha do form
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Calcula a hash da senha
        password_hash = sha256(password.encode("utf-8")).hexdigest()

        # Compara com as informações de login
        if password_hash == app.config["USER_PASSWORD_HASH"] and (
            username in app.config["USER_NAMES"]
            or username in app.config["SPECIAL_USER_NAMES"]
        ):
            # Armazena nome de usuário na sessão
            session["auth"] = username
            location = url_for(
                app.config["SPECIAL_USER_NAMES"].get(username, "servico")
            )
            # Retorna JSON de sucesso
            return jsonify(success=True, auth=True, location=location)

        # Retorna JSON de falha na autenticação
        return jsonify(success=True, auth=False)


@app.route("/servico", methods=["GET", "POST"])
@Login.required
def servico():
    if request.method == "GET":
        # Retorna a página para fazer os pedidos
        return render_template("fazer_pedido.html", menu=app.config["MENU"])
    else:
        # Obtém dados do pedido em formato JSON
        data = request.get_json()
        # Extrai o pedido
        pedido = data["pedido"]
        extras = data["extras"]
        # Adiciona o pedido à lista de espera
        full_pedido = PedidosEsperaList.add(
            session["auth"], pedido, extras, data["mesa"]
        )
        socketio.update_cozinha([session["auth"], full_pedido])
        # Retorna JSON de sucesso
        return jsonify(success=True)


@app.route("/cozinha", methods=["GET"])
@Login.required_as_user("cozinha")
def cozinha():
    # Retorna a interface da cozinha
    return render_template("cozinha.html")


@app.route("/prontos", methods=["GET"])
@Login.required
def prontos():
    # Retorna a interface dos pedidos prontos
    return render_template("prontos.html", name=session["auth"])


@app.route("/admin", methods=["GET", "POST"])
@Login.required_as_user("admin")
def admin():
    if request.method == "GET":
        # Retorna a interface de administração
        return render_template(
            "admin.html",
            atendetes=app.config["USER_NAMES"],
            menu=app.config["MENU"],
            vendas=Data.load_vendas(),
        )
    else:
        # Obtém os dados enviados no formato JSON
        data = request.get_json()

        # Obtém as todas as variaveis das opções disponiveis
        usernames = data.get("atendentes", None)
        menu = data.get("menu", None)
        history_delete = data.get("history_delete", None)
        get_excel = data.get("get_excel", None)

        # Caso necessario atualiza a lista de usuários
        if usernames is not None:
            Data.update_usernames(usernames)

        # Caso necessario atualiza o menu
        elif menu is not None:
            Data.update_menu(menu)

        # Caso necessario apagar a data base
        elif history_delete:
            Data.clear_data_base()

        # Caso necessario enviar o ficehiro que contem as vendas feitas
        elif get_excel:
            return Data.send_vendas_file()

        # Retorna JSON de sucesso
        return jsonify(success=True)


if __name__ == "__main__":
    # Inicia o Flask
    app.run(debug=True, port=80)
