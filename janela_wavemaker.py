import tkinter as tk
from tkinter import ttk
from utils_tk import ajustar_estado_wavemaker_agora

def abrir_janela_wavemaker_lista(janela_pai, output, salvar_callback=None):
    janela = tk.Toplevel(janela_pai)
    janela.title(f"Wavemaker - {output.nome}")
    janela.resizable(False, False)
    janela.transient(janela_pai)
    janela.grab_set()
    janela.focus_force()

    frame = tk.Frame(janela, padx=40, pady=40)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Modo de funcionamento do Wavemaker:", font=("Arial", 12)).pack(pady=(0,15))

    opcoes = [
        "Sempre ligado",
        "Liga/desliga a cada 15 minutos",
        "Liga/desliga a cada 30 minutos",
        "Liga/desliga a cada 1 hora",
        "Liga/desliga a cada 6 horas"
    ]
    modo_var = tk.StringVar()
    combo = ttk.Combobox(frame, textvariable=modo_var, values=opcoes, state="readonly", font=("Arial", 12), width=28)
    # Se já tiver salvo antes, deixa selecionado:
    if hasattr(output, "wavemaker_mode") and output.wavemaker_mode in opcoes:
        combo.set(output.wavemaker_mode)
    else:
        combo.current(0)
    combo.pack(pady=10)

    def salvar():
        print(f"Salvando modo do Wavemaker: {modo_var.get()}")
        output.wavemaker_mode = modo_var.get()
        ajustar_estado_wavemaker_agora(output)
        if salvar_callback:
            salvar_callback()  # se quiser que a lista seja atualizada, etc.
        print(f"Modo do Wavemaker salvo: {output.wavemaker_mode}")
        janela.destroy()

    tk.Button(frame, text="Salvar", command=salvar, font=("Arial", 12), width=16).pack(pady=(25,0))

    # Centraliza a janela em relação à janela pai
    janela.update_idletasks()
    w = janela.winfo_width()
    h = janela.winfo_height()
    x_pai = janela_pai.winfo_rootx()
    y_pai = janela_pai.winfo_rooty()
    w_pai = janela_pai.winfo_width()
    h_pai = janela_pai.winfo_height()
    x = x_pai + (w_pai - w) // 2
    y = y_pai + (h_pai - h) // 2
    janela.geometry(f"{w}x{h}+{x}+{y}")
