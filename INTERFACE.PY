import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk

from cliente import Clientes
from movimentacao import Movimentacao
from relatorio import Relatorio
from database import criar_tabelas, conectar
from pdf_utils import gerar_cupom_pdf


def iniciar_sistema():
    criar_tabelas()

    janela = tk.Tk()
    janela.title("Sistema de Estacionamento")
    janela.geometry("700x500")

    try:
        janela.iconbitmap("estacionamento.ico")
    except Exception:
        pass

    # ===== TOPO =====
    topo = tk.Frame(janela, bg="#0d6efd", height=30)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="ESTACIONAMENTO J J",
        bg="#0d6efd",
        fg="white",
        font=("Arial", 20, "bold"),
    ).pack(expand=True)

    # ===== NOTEBOOK =====
    style = ttk.Style(janela)
    style.theme_use("default")
    style.configure("TNotebook.Tab", background="#c0c0c0")
    style.map("TNotebook.Tab", background=[("selected", "#ffffff")])

    abas = ttk.Notebook(janela)
    abas.pack(expand=True, fill="both")

    # ================= ABA CLIENTES =================
    aba_clientes = tk.Frame(abas, bg="#c5ddcc")
    abas.add(aba_clientes, text="Clientes")

    try:
        img = Image.open("bg_clientes.png").resize((700, 470))
        bg_img = ImageTk.PhotoImage(img)
        lbl_bg = tk.Label(aba_clientes, image=bg_img)
        lbl_bg.image = bg_img
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception:
        pass

    tk.Label(aba_clientes, text="Nome", bg="#c5ddcc").pack()
    entry_nome = tk.Entry(aba_clientes)
    entry_nome.pack()

    tk.Label(aba_clientes, text="CPF", bg="#c5ddcc").pack()
    entry_cpf = tk.Entry(aba_clientes)
    entry_cpf.pack()

    tk.Label(aba_clientes, text="Placa", bg="#c5ddcc").pack()
    entry_placa = tk.Entry(aba_clientes)
    entry_placa.pack()

    tk.Label(aba_clientes, text="Tipo (carro/moto)", bg="#c5ddcc").pack()
    entry_tipo = tk.Entry(aba_clientes)
    entry_tipo.pack()

    def cadastrar():
        try:
            Clientes.cadastrar(
                entry_nome.get(),
                entry_cpf.get(),
                entry_placa.get(),
                entry_tipo.get(),
            )
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            entry_nome.delete(0, tk.END)
            entry_cpf.delete(0, tk.END)
            entry_placa.delete(0, tk.END)
            entry_tipo.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    tk.Button(aba_clientes, text="Cadastrar", command=cadastrar).pack(pady=10)

    # ================= ABA MOVIMENTAÇÃO =================
    aba_mov = tk.Frame(abas, bg="#C0C0C0")
    abas.add(aba_mov, text="Movimentação")

    tk.Label(aba_mov, text="Placa", bg="#C0C0C0").pack(pady=5)
    entry_mov = tk.Entry(aba_mov)
    entry_mov.pack(pady=5)

    def entrada():
        try:
            placa = entry_mov.get()
            Movimentacao.registrar_entrada(placa)

            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, entrada FROM movimentacoes
                WHERE placa = ?
                ORDER BY id DESC LIMIT 1
            """, (placa,))
            mov = cur.fetchone()
            conn.close()

            if mov:
                mov_id, entrada_iso = mov
                entrada_br = datetime.fromisoformat(entrada_iso).strftime("%d/%m/%Y %H:%M:%S")
                messagebox.showinfo(
                    "Ticket",
                    f"ID: {mov_id}\nPlaca: {placa}\nEntrada: {entrada_br}"
                )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def saida():
        try:
            placa = entry_mov.get()
            valor = Movimentacao.registrar_saida(placa)
            if valor is None:
                messagebox.showwarning("Aviso", "Nenhuma entrada aberta.")
                return

            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, entrada, saida, valor FROM movimentacoes
                WHERE placa = ?
                ORDER BY id DESC LIMIT 1
            """, (placa,))
            mov = cur.fetchone()
            conn.close()

            if mov:
                mov_id, ent, sai, val = mov
                caminho = gerar_cupom_pdf(
                    mov_id,
                    placa,
                    datetime.fromisoformat(ent).strftime("%d/%m/%Y %H:%M:%S"),
                    datetime.fromisoformat(sai).strftime("%d/%m/%Y %H:%M:%S"),
                    val
                )
                messagebox.showinfo("Cupom", f"Cupom gerado:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    tk.Button(aba_mov, text="Registrar Entrada", command=entrada).pack(pady=5)
    tk.Button(aba_mov, text="Registrar Saída", command=saida).pack(pady=5)

    # ================= ABA RELATÓRIOS =================
    aba_rel = ttk.Frame(abas)
    abas.add(aba_rel, text="Relatórios")

    texto = tk.Text(aba_rel)
    texto.pack(expand=True, fill="both")

    def mostrar_clientes():
        texto.delete("1.0", tk.END)
        rows = Relatorio.clientes()

        if not rows:
            texto.insert(tk.END, "Nenhum cliente cadastrado.\n")
            return

        for (cid, nome, cpf, placa, tipo, valor) in rows:
            linha = (
                f"ID: {cid}\n"
                f"Nome: {nome}\n"
                f"CPF: {cpf}\n"
                f"Placa: {placa}\n"
                f"Tipo: {tipo}\n"
                f"Valor: R$ {valor:.2f}\n"
                "-----------------------------\n"
            )
            texto.insert(tk.END, linha)

    tk.Button(aba_rel, text="Clientes", command=mostrar_clientes).pack(pady=5)

    janela.mainloop()


if __name__ == "__main__":
    iniciar_sistema()
