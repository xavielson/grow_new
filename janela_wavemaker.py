import tkinter as tk
from tkinter import ttk
from utils_tk import ajustar_estado_wavemaker_agora, centralizar_horizontal_abaixo

def abrir_janela_wavemaker_lista(janela_pai, output, salvar_callback=None):
    janela = tk.Toplevel(janela_pai)
    janela.title(f"Wavemaker - {output.nome}")
    janela.resizable(False, False)
    janela.transient(janela_pai)
    #janela.grab_set()
    janela.after(10, janela.grab_set)
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
        output.wavemaker_mode = modo_var.get()
        ajustar_estado_wavemaker_agora(output)
        if salvar_callback:
            salvar_callback()  # se quiser que a lista seja atualizada, etc        
        janela.destroy()

    tk.Button(frame, text="Salvar", command=salvar, font=("Arial", 12), width=16).pack(pady=(25,0))

    # Centraliza a janela em relação à janela pai
    centralizar_horizontal_abaixo(janela, janela_pai)
