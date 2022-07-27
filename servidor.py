import socket
import threading

# Arrays de clientes e seus respectivos nomes
CLIENTES = []
NOMES = []
host = 'localhost'
port = 65521

# Instancia o socket do servidor no host e porta
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Função que roda na thread de conexão dos clientes
# Parâmetro 'cliente' é a referência ao objeto socket do cliente, cada thread de conexão leva a referência de um socket cliente
def conexao(cliente):
    while True:
        try:
            # Recebe a mensagem de um cliente e a distribui para todos os clientes conectados (inclusive o cliente que enviou a mensagem)
            msg = cliente.recv(1024)
            enviar_mensagem(msg)
        except:
            sair_do_chat(cliente)
            break

# Transmite a mensagem para todos os clientes
def enviar_mensagem(msg):
    i = 0
    while(i < len(CLIENTES)):
        CLIENTES[i].send(msg)
        i += 1

# Desconecta um cliente do chat
def sair_do_chat(cliente):
    i = CLIENTES.index(cliente)
    CLIENTES.remove(cliente)
    cliente.close()
    nome = NOMES[i]
    enviar_mensagem(f'{nome} saiu do chat'.encode('utf-8'))
    print(f'Cliente "{nome}" se desconectou\n')
    NOMES.remove(nome)

# Função servidor, que aceita novas conexões via sockets e cria uma thread de conexão para cada cliente
def servidor():
    while True:
        cliente, endereco = server.accept()
        # Recebe o nome do cliente, logo após a conexão
        nome = cliente.recv(1024).decode('utf-8')
        # Guarda nas listas globais a referência do cliente conectado, tanto o objeto socket quanto o nome do cliente 
        NOMES.append(nome)
        CLIENTES.append(cliente)
        
        print(f'Cliente "{nome}" se conectou')
        print(f'Endereço: {str(endereco)}\n')
        # Informa a conexão de um usuário para os outros usuários conectados ao chat
        enviar_mensagem(f'{nome} entrou no chat'.encode('utf-8'))
        # Informa o cliente que o mesmo está conectado ao chat
        cliente.send('Conectado ao chat\n'.encode('utf-8'))

        # Inicia a thread de conexão do cliente
        thread_conexao = threading.Thread(target=conexao, args=(cliente,))
        thread_conexao.start()

# Inicia a função de servidor  
servidor()