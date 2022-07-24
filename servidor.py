import socket
import threading

# Arrays de clientes e seus respectivos nomes
clientes = []
nomes = []
host = 'localhost'
port = 65521

# Inicia o servidor no host e porta
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Função que roda na thread de conexão dos clientes
def conexao(cliente):
    while True:
        try:
            msg = cliente.recv(1024)
            if (msg == 'sair'):
                sair_do_chat(cliente)
                break
            enviar_mensagem(msg)
        except:
            sair_do_chat(cliente)
            break

# Transmite a mensagem para todos os clientes
def enviar_mensagem(msg):
    i = 0
    while(i < len(clientes)):
        clientes[i].send(msg)
        i += 1

def sair_do_chat(cliente):
    i = clientes.index(cliente)
    clientes.remove(cliente)
    cliente.close()
    nome = nomes[i]
    enviar_mensagem(f'{nome} saiu do chat'.encode('utf-8'))
    print(f'Cliente "{nome}" se desconectou\n')
    nomes.remove(nome)

# Função servidor, que aceita novas conexões via socket e cria uma thread de conexão para cada cliente
def servidor():
    while True:
        cliente, endereco = server.accept()
        # Recebe o nome do cliente, logo após a conexão
        nome = cliente.recv(1024).decode('utf-8')
        nomes.append(nome)
        clientes.append(cliente)
        
        print(f'Cliente "{nome}" se conectou')
        print(f'Endereço: {str(endereco)}\n')
        # Informa a conexão de um usuário para os outros usuários
        enviar_mensagem(f'{nome} entrou no chat'.encode('utf-8'))
        cliente.send('Conectado ao chat\n'.encode('utf-8'))

        # Inicia a thread de conexão do cliente
        thread_conexao = threading.Thread(target=conexao, args=(cliente,))
        thread_conexao.start()
  
servidor()