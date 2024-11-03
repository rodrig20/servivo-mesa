from __future__ import annotations

class PedidosEsperaList:
    """Classe que contém todos os pedidos que ainda não foram atendidos pela cozinha"""

    __pedidos: list[Pedido] = []

    def __new__(cls):
        # Impede a instanciação da classe
        raise TypeError("This class cannot be instantiated")

    @staticmethod
    def add(
        username: str, subpedidos: list[str], extras: list[str], mesa: str
    ) -> list[str]:
        """Adiciona um pedido à lista de pedidos em espera

        Args:
            username (str): nome do atendente
            subpedidos (list[str]): lista com os subpedidos
            extras (list[str]): extars dos subpedidos
            mesa (str): nome da mesa

        Returns:
            list[str]: Novo pedido criado com extras
        """
        # Atualiza a interface da cozinha
        pedido = Pedido(username, subpedidos, extras, mesa)
        PedidosEsperaList.__pedidos.append(pedido)

        return pedido.get_full_pedido()

    @staticmethod
    def transfer(
        pedido_index: int,
        subpedido_index: int,
    ) -> tuple[str, str, str, str]:
        """Transfere um pedido da lista de pedidos em espera para a lista de pedidos prontos.

        Args:
            pedido_index (int): Índice do pedido a ser transferido.
            subpedido_index (int): Índice do subpedido a ser removido.

        Returns:
            (tuple[str, str, str, str]): Nome do atendente, nome do subpedido, extras e mesa.
        """
        # Acessa o pedido a ser editado
        pedido_to_edit = PedidosEsperaList.__pedidos[pedido_index]

        # Obtém o as informações do subpedido e remove da lista de pedidos em espera
        username = pedido_to_edit.get_username()
        subpedido_to_remove, extras_to_remove = pedido_to_edit.remove(subpedido_index)
        mesa = pedido_to_edit.get_mesa()

        # Adiciona o subpedido removido à lista de pedidos prontos
        PedidosProntoList.add(
            username,
            subpedido_to_remove,
            extras_to_remove,
            mesa,
        )

        # Remove o pedido se não houver mais subpedidos no pedido
        if pedido_to_edit.is_empty():
            PedidosEsperaList.__pedidos.pop(pedido_index).get_username()

        return username, subpedido_to_remove, extras_to_remove, mesa

    @staticmethod
    def simplified() -> list[list[str | list[str]]]:
        """Retorna uma representação simplificada da lista de pedidos.

        Returns:
            list[list[str]]: Lista com detalhes de cada pedido (atendente e subpedidos).
        """

        return [
            [pedido.get_username(), pedido.get_full_pedido()]
            for pedido in PedidosEsperaList.__pedidos
        ]


class PedidosProntoList:
    """Classe que contém todos os pedidos que já foram atendidos pela cozinha e que estão à espera de ser entre aos clientes"""

    __pedidos: dict[str, list[Pedido]] = dict()

    def __new__(cls):
        # Impede a instanciação da classe
        raise TypeError("This class cannot be instantiated")

    @staticmethod
    def add(username: str, subpedido: str, extras: str, mesa: str) -> None:
        """Adiciona um subpedido à lista de pedidos prontos de um atendente.

        Args:
            username (str): Nome do atendente.
            subpedido (str): Subpedido a ser adicionado.
            extras (str): Extras do subpedido a ser adicionado.
            mesa (str): Nome da mesa.
        """
        # Obtém a lista de pedidos do atendente
        pedidos_user_list = PedidosProntoList.__pedidos.get(username, None)

        # Verifica se o atendente já tem um pedido para a mesa
        if pedidos_user_list is not None:
            for pedido in pedidos_user_list:
                if pedido.get_mesa() == mesa:
                    # Adiciona o subpedido ao pedido existente
                    pedido.add(subpedido, extras)
                    break
            else:
                # Se não tiver, cria um novo pedido
                new_pedido = Pedido(username, [subpedido], [extras], mesa)
                pedidos_user_list.append(new_pedido)
        else:
            # Se o atendente não tiver nenhum pedidos , cria um novo
            new_pedido = Pedido(username, [subpedido], [extras], mesa)
            PedidosProntoList.__pedidos[username] = [new_pedido]

    @staticmethod
    def remove(name: str, mesa: int, subpedido_index: int) -> None:
        """Remove um subpedido de um pedido específico.

        Args:
            name (str): Nome do atendente.
            mesa (int): Número da mesa.
            index (int): Índice do subpedido a ser removido.
        """
        # Percorre todos os pedidos do utilizador e remove o subpedido pelo índice
        for idx, pedido in enumerate(PedidosProntoList.__pedidos[name]):
            if pedido.get_mesa() == mesa:
                pedido.remove(subpedido_index)
                # Remover pedido caso não tenha mais subpedidos
                if pedido.is_empty():
                    PedidosProntoList.__pedidos[name].pop(idx)
                break

    @staticmethod
    def simplified(username: str) -> dict[str, list[str]]:
        """Retorna uma representação simplificada dos pedidos prontos de um atendente.

        Args:
            username (str): Nome do atendente.

        Returns:
            dict[str, list[str]]: Dicionário com mesas como chaves e subpedidos como valores.
        """
        pedidos_user_list = PedidosProntoList.__pedidos.get(username, [])
        # Dicionário para armazenar a representação simplificada
        pedidos_user_json: dict[str, list[str]] = dict()

        for pedido in pedidos_user_list:
            mesa = pedido.get_mesa()
            # Cria a entrada
            pedidos_user_json[mesa] = pedido.get_full_pedido()
        return pedidos_user_json


class Pedido:
    """Classe que representa um pedido feito por um atendente."""

    def __init__(
        self, username: str, subpedidos: list[str], extras: list[str], mesa: str
    ) -> None:
        # Definir variáveis importantes do pedido
        self.__username = username
        self.__subpedidos = subpedidos
        self.__extras = extras
        self.__mesa = mesa

    def remove(self, index: int) -> list[str]:
        """Remove um subpedido pelo índice.

        Args:
            index (int): Índice do subpedido a ser removido.

        Returns:
            str: O subpedido removido.
        """
        return [self.__subpedidos.pop(index), self.__extras.pop(index)]

    def add(self, subpedido: str, extras: str) -> None:
        """Adiciona um subpedido à lista do pedido.

        Args:
            subpedido (str): Subpedido a ser adicionado.
            extras (str): Extras a serem adicionados ao subpedido.
        """
        self.__subpedidos.append(subpedido)
        self.__extras.append(extras)

    def get_list(self) -> list[str]:
        """Retorna a lista de subpedidos.

        Returns:
            list[str]: Lista de subpedidos.
        """
        return self.__subpedidos

    def get_extras(self) -> list[str]:
        """Retorna a lista de extras dos subpedidos.

        Returns:
            list[str]: Lista de extras dos subpedidos.
        """
        return self.__extras

    def get_username(self) -> str:
        """Retorna o nome do atendente.

        Returns:
            str: Nome do atendente.
        """
        return self.__username

    def get_mesa(self) -> str:
        """Retorna o nome da mesa.

        Returns:
            str: Nome da mesa.
        """
        return self.__mesa

    def get_full_pedido(self) -> list[str]:
        """Retorna a representação completa do pedido, incluindo nome simples e extras.

        Returns:
            list[str]: Lista de subpedidos com seus extras.
        """
        full_pedido = []
        for subpedido, extra in zip(self.__subpedidos, self.__extras):
            if extra != "":
                full_pedido.append(subpedido + " " + extra)
            else:
                full_pedido.append(subpedido)
        return full_pedido

    def is_empty(self) -> bool:
        """Verifica se a lista de subpedidos está vazia.

        Returns:
            bool: True se a lista estiver vazia, caso contrário, False.
        """
        return not bool(len(self.get_list()))