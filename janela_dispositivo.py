import tkinter as tk
from tkinter import ttk, messagebox

def abrir_janela_dispositivo(janela_pai, gerenciador, tomada, output_existente, salvar_callback, atualizar_lista):
    def confirmar():
        nome = entrada_nome.get().strip()
        device = tipo_var.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do dispositivo não pode ficar vazio.")
            return

        for t, out in gerenciador.tomadas.items():
            if out and out.nome == nome and (output_existente is None or out != output_existente):
                messagebox.showerror("Erro", f"Já existe um dispositivo com o nome '{nome}' na saída {t}.")
                return

        gerenciador.adicionar_output(nome, device, tomada, sobrescrever=True)
        salvar_callback()
        atualizar_lista()
        janela.destroy()

    janela = tk.Toplevel(janela_pai)
    acao = "Editar" if output_existente else "Novo"
    janela.title(f"{acao} Dispositivo - Saída {tomada}")

    janela.update_idletasks()
    janela_pai.update_idletasks()
    x_principal = janela_pai.winfo_x()
    y_principal = janela_pai.winfo_y()
    altura_principal = janela_pai.winfo_height()

    janela.geometry(f"+{x_principal}+{y_principal + altura_principal + 10}")

    tk.Label(janela, text="Nome do dispositivo:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entrada_nome = tk.Entry(janela, width=30)
    entrada_nome.grid(row=0, column=1, padx=10, pady=5)
    if output_existente:
        entrada_nome.insert(0, output_existente.nome)

    tk.Label(janela, text="Tipo do dispositivo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tipo_var = tk.StringVar()
    combo_tipo = ttk.Combobox(janela, textvariable=tipo_var, state="readonly")
    combo_tipo['values'] = ["Led", "Rega", "Wavemaker", "Runoff"]
    combo_tipo.grid(row=1, column=1, padx=10, pady=5)
    if output_existente:
        combo_tipo.set(output_existente.device)
    else:
        combo_tipo.current(0)

    tk.Button(janela, text="Confirmar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)
