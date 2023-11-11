# Aplicação de Serviço às Mesas

Esta é uma aplicação web Flask desenvolvida para simplificar o serviço às mesas por pequenos grupos, permitindo que os clientes façam pedidos, gerem códigos QR para seus pedidos e permitindo que a equipa do estabelecimento visualize e atenda os pedidos. A aplicação também oferece uma interface de login para gerenciar o acesso.

## Funcionalidades Principais

- Fazer pedidos através de uma interface amigável.
- Gerar códigos QR para pedidos automatizados.
- Visualizar e atender pedidos pendentes.
- Autenticação de usuário para acessar funcionalidades específicas.

## Pré-requisitos

Antes de executar a aplicação, deve ter o seguinte instalado em sua máquina:

- **Python 3.x**: A linguagem de programação utilizada para desenvolver a aplicação.

- Todas as bibliotecas e dependências necessárias estão listadas no arquivo `requirements.txt`. Pode instalá-las executando o seguinte comando na raiz do projeto:

    ```bash
    pip install -r requirements.txt
    ```

Para executar a aplicação, precisará fornecer as credenciais de acesso, como o Username (nome de usuário) e Password (senha). Essas credenciais serão armazenadas em um arquivo `.env` localizado na pasta `./config`.

Siga estas etapas para configurar as credenciais:

1. Navegue até a pasta raiz do projeto, caso ainda não esteja lá.
2. Dentro da pasta `./config`, edite o arquivo chamado `.env`.
3. Abra o arquivo `.env` em um editor de texto.
4. Dentro do arquivo `.env`, adicione suas credenciais da seguinte maneira:

    ```plaintext
    USERNAME=__YOUR_EMAIL__
    PASSWORD=__YOUR_PASSWORD__
    ```
Substitua `__YOUR_EMAIL__` pelo nome de usuário desejado e `__YOUR_PASSWORD__` pela senha escolhida.

5. Guarde o arquivo `.env`. A aplicação usará essas credenciais para autenticação durante o processo de login. Certifique-se de manter essas informações em segurança e não compartilhar com terceiros.

## Executando a aplicação

- Tenha certeza de ter todos [Pré-Requisitos](#Pré-requisitos) cumpridos.

É possivel executar a aplicação de diferentes maneiras, dependendo das suas necessidades. A seguir, são apresentadas as opções disponíveis:

### Opção 1: Modo Padrão (com GUI)

1. Abra um terminal e navegue até a pasta raiz do projeto.
2. Execute a aplicação com o seguinte comando:

    ```bash
    python main.py
    ```
3. Configure as opções da aplicação, como URLs ativas, menu e credenciais de usuário, na interface que aparecerá
4. Abra um navegador e acesse o endereço do host definido durante a configuração ou então use os botões da interface.


### Opção 2: Modo Rápido (Sem GUI)
Se deseja iniciar a aplicação sem a interface gráfica (GUI), pode usar a flag `--fast-start`. Isto iniciará a aplicação com as configurações atuais sem a necessidade da interface gráfica.

Para executar a aplicação no modo rápido, siga estas etapas:

1. Abra um terminal e navegue até a pasta raiz do projeto.
2. Configure as opções da aplicação, como URLs ativas, menu e credenciais de usuário diretamente nos arquivos contidos em `./config/`.
3. Execute a aplicação com o seguinte comando:

    ```bash
    python main.py --fast-start
    ```
Lembre-se de que a flag `--fast-start` é opcional e destinada a cenários de uso em que a interface gráfica não é necessária.

## Estrutura do Projeto

- `app/`: Contém os módulos relacionados à lógica de rotas e de inicio da app.
- `config/`: Contém arquivos de configuração, como URLs ativas, menu e usuários.
- `interface/`: Contém a interface gráfica da aplicação.

## Páginas da aplicação

- `/login`: Página de login para autenticar os usuários.
- `/servico`: Página principal para fazer pedidos.
- `/lista/Cozinha` e `/lista/Bar`: Páginas para visualizar e atender pedidos pendentes.
- `/scanQR`: Página para escanear um QR Code.
- `/QrCode`: Página para gerar um QR Code com o pedido.

### Transformando a aplicação em Executável (Windows)

Se deseja distribuir a sua aplicação como um executável para sistemas Windows, pode utilizar o arquivo `to_exe.py` fornecido neste repositório. Ele utiliza a biblioteca `pyinstaller` para criar um executável a partir do seu código Python.

#### Passos para Transformar em Executável:

1. Certifique-se de ter todas as dependências instaladas, conforme listado no arquivo `requirements.txt`. Se não tiver feito isso ainda, execute o seguinte comando:

    ```bash
    pip install -r requirements.txt
    ```
2. Abra um terminal e navegue até a pasta raiz do projeto.

3. Execute o seguinte comando para transformar a aplicação em um executável:

    ```bash
    python to_exe.py
    ```
4. O script `to_exe.py` utilizará o `pyinstaller` para criar uma pasta chamada `dist` que conterá o executável e outros arquivos necessários.

5. Na pasta `dist`, encontrará o executável da aplicação. Execute-o clicando duas vezes para iniciar a aplicação.

Lembre-se de que o processo de criação de executáveis pode variar dependendo do sistema operacional e das configurações específicas. Certifique-se de testar o executável gerado em diferentes ambientes para garantir que ele funcione conforme o esperado.

### Observação

Caso deseje criar executáveis para outros sistemas operacionais ou configurar opções específicas do `pyinstaller`, pode ajustar o arquivo `to_exe.py` de acordo com suas necessidades.

**Nota:** Lembre-se de que a criação de executáveis pode envolver considerações de segurança e de compatibilidade entre diferentes sistemas. Certifique-se de rever a documentação do `pyinstaller` para mais informações e diretrizes sobre criação de executáveis.

## Contribuindo

Se quiser contribuir para este projeto, sinta-se à vontade para abrir um problema ou enviar um pull request.