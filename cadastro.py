import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  

class Cadastro:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL ,
                placa TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def adicionar_usuario(self, nome, cpf, placa, tipo):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, cpf, placa, tipo) VALUES (?, ?, ?, ?)
        ''', (nome, cpf, placa, tipo))
        self.connection.commit()

    def listar_usuarios(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM usuarios')
        return cursor.fetchall()

    def fechar_conexao(self):
        self.connection.close()

import tkinter as tk
from tkinter import messagebox
import sqlite3

def abrir_janela_cadastro(cadastro):  # cadastro = instância da classe Cadastro
    janela_cadastro = tk.Tk()
    janela_cadastro.title("CADASTRO DE USUARIO E VEICULO")
    janela_cadastro.geometry("300x250")

    tk.Label(janela_cadastro, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nome = tk.Entry(janela_cadastro)
    entry_nome.grid(row=0, column=1)

    tk.Label(janela_cadastro, text="CPF:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_cpf = tk.Entry(janela_cadastro)
    entry_cpf.grid(row=1, column=1)

    tk.Label(janela_cadastro, text="Placa:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_placa = tk.Entry(janela_cadastro)
    entry_placa.grid(row=2, column=1)

    tk.Label(janela_cadastro, text="Tipo (Carro/Moto):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_tipo = tk.Entry(janela_cadastro)
    entry_tipo.grid(row=3, column=1)

    def cadastrar_usuario():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        placa = entry_placa.get()
        tipo = entry_tipo.get()

        if not (nome and cpf and placa and tipo):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            cadastro.adicionar_usuario(nome, cpf, placa, tipo)
            messagebox.showinfo("Sucesso", "Usuário e veículo cadastrados!")
            entry_nome.delete(0, tk.END)
            entry_cpf.delete(0, tk.END)
            entry_placa.delete(0, tk.END)
            entry_tipo.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF ou Placa já existe no banco.")

    tk.Button(
        janela_cadastro,
        text="Cadastrar",
        command=cadastrar_usuario,
        bg="green",
        fg="white"
    ).grid(row=4, column=0, columnspan=2, pady=15)

    janela_cadastro.mainloop()

def cadastrar_usuario():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        placa = entry_placa.get()
        tipo = entry_tipo.get()

        if nome and cpf and placa and tipo:
            try:
                cadastro.adicionar_usuario(nome, cpf, placa, tipo)
                messagebox.showinfo("Sucesso", "Usuário e veículo cadastrados!")
                janela_cadastro.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "CPF ou Placa já existe no banco.")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        btn_cadastrar = tk.Button(
        janela_cadastro, text="Cadastrar",
        command=cadastrar_usuario, bg="green", fg="white"
    )
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=20)

        btn_listar = tk.Button(
        janela_cadastro, text="Listar Usuários",
        command=lambda: abrir_janela_listagem(cadastro)
    )
        btn_listar.grid(row=5, column=0, columnspan=2)

        janela_cadastro.mainloop()


def abrir_janela_listagem(cadastro):
    janela_listagem = tk.Tk()
    janela_listagem.title("Lista de Usuários e Veículos")
    janela_listagem.geometry("400x300")


    usuarios = cadastro.listar_usuarios()
    for idx, usuario in enumerate(usuarios):
        tk.Label(
            janela_listagem,
            text=f"{usuario[1]} - {usuario[2]} - {usuario[3]} - {usuario[4]}"
        ).pack(anchor="w", padx=10, pady=2)

    janela_listagem.mainloop()


def registrar_entradas(cadastro):
    # Esta função pode ser implementada para registrar as entradas dos veículos
    pass


def registrar_saidas(cadastro):
    # Esta função pode ser implementada para registrar as saídas dos veículos
    pass


if __name__ == "__main__":
    cadastro = Cadastro("cadastro.db")
    abrir_janela_cadastro(cadastro)
    cadastro.fechar_conexao()