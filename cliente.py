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

# login button
entrar_btn = tk.Button(janela_inicial, text="  Entrar  ", command = lambda : entrar())
entrar_btn.grid(column=1, row=3, sticky=tk.E, padx=20, pady=5)



# Variáveis globais
nome = None
cliente = None
window = None
displayFrame = None
tkDisplay = None
sair = False

host = 'localhost'
port = 65521

# Função que envia mensagens ao servidor
def enviar_mensagem(mensagem):
    global tkMessage
    mensagem = mensagem.replace('\n', '')
    if (mensagem == ''):
        tk.messagebox.showerror(title="Erro", message="Insira uma mensagem válida")
    else: 
        mensagem = (f'{nome}: {mensagem}')
        cliente.send(mensagem.encode('utf-8'))
        tkMessage.delete('1.0', tk.END)

# Função que recebe mensagens do servidor
def receber_mensagem():
    time.sleep(1)
    global cliente, nome, tkDisplay
    # Envia seu nome ao servidor apenas uma vez, após a conexão
    cliente.send(nome.encode('utf-8'))
    while True:
        try:
            # Recebe a mensagem do servidor e decodifica
            mensagem = cliente.recv(1024).decode('utf-8')
            # Tratamento para exibir 'Você' ao invés do próprio nome na mensagem
            tkDisplay.config(state=tk.NORMAL)
            if (nome == mensagem[0 : len(nome)]):
                mensagem = mensagem.replace(mensagem[0 : len(nome)], 'Você', 1)
                #print(mensagem)
                tkDisplay.insert(tk.END, mensagem + '\n', "cor_mensagem")
            else:
                tkDisplay.insert(tk.END, mensagem + '\n', "cor_mensagem")
                #print(mensagem)
            tkDisplay.config(state=tk.DISABLED)
            tkDisplay.see(tk.END)
        except:
            break
            tkDisplay.insert(tk.END, "Conexão fechada" + '\n')
            #print("Conexão fechada")
    cliente.close()

def entrar():
    global nome
    nome = nome_input.get()
    if (nome == ''):
        tk.messagebox.showerror(title="Erro", message="Insira um nome para entrar no chat")
    else:
        if (conectar_servidor()):
            janela_inicial.withdraw()
            abrir_janela_chat()
        
def abrir_janela_chat():
    global window, displayFrame, tkDisplay, tkMessage
    
    # Janela chat
    window = tk.Tk()
    window.title("Chat multiusuário")
    window.resizable(0, 0)
    displayFrame = tk.Frame(window)
    scrollBar = tk.Scrollbar(displayFrame)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
    tkDisplay = tk.Text(displayFrame, height=20, width=55)
    tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
    tkDisplay.tag_config("cor_mensagem", foreground="#fff", background="#2a2a2a")
    scrollBar.config(command=tkDisplay.yview)
    tkDisplay.config(yscrollcommand=scrollBar.set, background="#2a2a2a", highlightbackground="grey", state="disabled")
    displayFrame.pack(side=tk.TOP)


    bottomFrame = tk.Frame(window)
    tkMessage = tk.Text(bottomFrame, height=1, width=55)
    tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
    tkMessage.config(highlightbackground="grey")
    tkMessage.bind("<Return>", (lambda event: enviar_mensagem(tkMessage.get("1.0", tk.END))))
    bottomFrame.pack(side=tk.BOTTOM)  

    window.protocol("WM_DELETE_WINDOW", fechar_janela_chat)
    window.mainloop()

def fechar_janela_chat():
    global cliente, sair
    if messagebox.askokcancel("Sair", "Deseja mesmo sair do chat?"):
        window.destroy()
        janela_inicial.destroy()
        cliente.close()
        sair = True

        
def conectar_servidor():
    global cliente
    try:
        # Conecta ao servidor por meio de sockets
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((host, port))

        # Threads para envio e recepção de mensagens 
        thread_recepcao = threading.Thread(target=receber_mensagem)
        thread_recepcao.start()

        return True
    except Exception as e:
        tk.messagebox.showerror(title="Erro", message="Servidor offline")
        return False

janela_inicial.mainloop()
