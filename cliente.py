import socket
import threading
import time

import tkinter as tk
from tkinter import messagebox

# Interface de usuário
# Janela inicial
janela_inicial = tk.Tk()
janela_inicial.geometry('300x80')
janela_inicial.title("Chat multiusuário")
janela_inicial.resizable(0, 0)
janela_inicial.bind("<Return>", (lambda event: entrar()))

tk.Label(janela_inicial, text = "Digite seu nome:").grid(column=0, row=2, sticky=tk.W, padx=20, pady=5)

# Input do nome
nome_input = tk.Entry(janela_inicial)
nome_input.grid(column=1, row=2, sticky=tk.E, padx=20, pady=5)

# Botão entrar
entrar_btn = tk.Button(janela_inicial, text="  Entrar  ", command = lambda : entrar())
entrar_btn.grid(column=1, row=3, sticky=tk.E, padx=20, pady=5)



# Variáveis globais
NOME = None
CLIENTE = None
JANELA_CHAT = None
FRAME_MENSAGENS = None
DISPLAY_MENSAGENS = None

# host e porta para a conexão via sockets
host = 'localhost'
port = 65521

# Função que envia mensagens ao servidor
def enviar_mensagem(mensagem):
    global mensagem_input
    mensagem = mensagem.replace('\n', '')
    # Trata a entrada para evitar mensagens vazias
    if (mensagem == ''):
        tk.messagebox.showerror(title="Erro", message="Insira uma mensagem válida")
    else: 
        mensagem = (f'{NOME}: {mensagem}')
        CLIENTE.send(mensagem.encode('utf-8'))
        mensagem_input.delete('1.0', tk.END)

# Função que recebe mensagens do servidor
def receber_mensagem():
    time.sleep(1)
    global CLIENTE, NOME, DISPLAY_MENSAGENS
    # Envia seu nome ao servidor apenas uma vez, após a conexão
    CLIENTE.send(NOME.encode('utf-8'))
    while True:
        try:
            # Recebe a mensagem do servidor e decodifica
            mensagem = CLIENTE.recv(1024).decode('utf-8')
            DISPLAY_MENSAGENS.config(state=tk.NORMAL)
            # Tratamento para exibir 'Você' ao invés do próprio nome na mensagem
            if (NOME == mensagem[0 : len(NOME)]):
                mensagem = mensagem.replace(mensagem[0 : len(NOME)], 'Você', 1)
                DISPLAY_MENSAGENS.insert(tk.END, mensagem + '\n', "cor_mensagem")
            else:
                DISPLAY_MENSAGENS.insert(tk.END, mensagem + '\n', "cor_mensagem")
            DISPLAY_MENSAGENS.config(state=tk.DISABLED)
            DISPLAY_MENSAGENS.see(tk.END)
        except:
            break
            DISPLAY_MENSAGENS.insert(tk.END, "Conexão fechada" + '\n')

    CLIENTE.close()

# Entra no chat através da janela inicial
def entrar():
    global NOME
    NOME = nome_input.get()
    # Exige que o usuário insira um nome não-vazio
    if (NOME == ''):
        tk.messagebox.showerror(title="Erro", message="Insira um nome para entrar no chat")
    else:
        # Se a conexão com o servidor ocorrer com sucesso, fecha a janela inicial e abre a janela de chat
        if (conectar_servidor()):
            janela_inicial.withdraw()
            abrir_janela_chat()

# Define a janela de chat e abre-a em mainloop      
def abrir_janela_chat():
    global JANELA_CHAT, FRAME_MENSAGENS, DISPLAY_MENSAGENS, mensagem_input
    
    # Interface de usuário
    # Janela chat
    JANELA_CHAT = tk.Tk()
    JANELA_CHAT.title("Chat multiusuário")
    JANELA_CHAT.resizable(0, 0)

    FRAME_MENSAGENS = tk.Frame(JANELA_CHAT)
    barra_rolagem = tk.Scrollbar(FRAME_MENSAGENS)
    barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)
    DISPLAY_MENSAGENS = tk.Text(FRAME_MENSAGENS, height=20, width=60)
    DISPLAY_MENSAGENS.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
    DISPLAY_MENSAGENS.tag_config("cor_mensagem", foreground="#fff", background="#2a2a2a")
    barra_rolagem.config(command=DISPLAY_MENSAGENS.yview)
    DISPLAY_MENSAGENS.config(yscrollcommand=barra_rolagem.set, background="#2a2a2a", highlightbackground="grey", state="disabled")
    FRAME_MENSAGENS.pack(side=tk.TOP)


    bottomFrame = tk.Frame(JANELA_CHAT)
    mensagem_input = tk.Text(bottomFrame, height=1, width=55)
    mensagem_input.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
    mensagem_input.config(highlightbackground="grey")
    mensagem_input.bind("<Return>", (lambda event: enviar_mensagem(mensagem_input.get("1.0", tk.END))))
    bottomFrame.pack(side=tk.BOTTOM)  

    JANELA_CHAT.protocol("WM_DELETE_WINDOW", fechar_janela_chat)
    JANELA_CHAT.mainloop()

# Fecha a janela de chat e a conexão do cliente com o servidor
def fechar_janela_chat():
    global CLIENTE
    if messagebox.askokcancel("Sair", "Deseja mesmo sair do chat?"):
        # Destroi as janelas
        JANELA_CHAT.destroy()
        janela_inicial.destroy()
        # Fecha a conexão com o servidor
        CLIENTE.close()

 # Função responsável por conectar o cliente ao servidor       
def conectar_servidor():
    global CLIENTE
    try:
        # Conecta ao servidor por meio de sockets
        CLIENTE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CLIENTE.connect((host, port))

        # Thread que recebe as mensagens do servidor
        thread_recepcao = threading.Thread(target=receber_mensagem)
        thread_recepcao.start()
        # Retorna verdadeiro caso a conexão ocorra com sucesso
        return True
    except Exception as e:
        # Retorna falso caso a aplicação não consiga se conectar com o servidor
        tk.messagebox.showerror(title="Erro", message="Servidor offline")
        return False

# Chama a janela inicial que pede o nome do usuário para prosseguir para a conexão com o chat
janela_inicial.mainloop()
