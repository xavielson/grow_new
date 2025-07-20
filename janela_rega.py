import tkinter as tk
from tkinter import ttk, messagebox

DIAS_SEMANA = [
    "Todos", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"
]

def abrir_janela_rega_edicao(janela_pai, salvar_callback, dia_evento=None, hora_liga=None, hora_desliga=None):
    janela = tk.Toplevel(janela_pai)
    janela.title("Horário de Rega")
    janela.resizable(False, False)
    janela.transient(janela_pai)
    janela.grab_set()
    janela.focus_force()

    frame = tk.Frame(janela, padx=8, pady=8)
    frame.grid(row=0, column=0)

    # Dia da semana
    tk.Label(frame, text="Dia da semana:", anchor="w").grid(row=0, column=0, padx=(0,8), sticky="w")
    dia_var = tk.StringVar()
    combo_dia = ttk.Combobox(frame, textvariable=dia_var, values=DIAS_SEMANA, state="readonly", width=12)
    combo_dia.grid(row=0, column=1, columnspan=6, padx=(0,8), sticky="w")
    if dia_evento in DIAS_SEMANA:
        combo_dia.set(dia_evento)
    else:
        combo_dia.current(0)

    valores_horas = [f"{i:02}" for i in range(24)]
    valores_minutos = [f"{i:02}" for i in range(60)]
    valores_segundos = [f"{i:02}" for i in range(60)]

    # Hora Liga
    tk.Label(frame, text="Hora Liga:", anchor="w").grid(row=1, column=0, padx=(0,8), sticky="w")
    liga = hora_liga if hora_liga else "00:00:00"
    h_l, m_l, s_l = [int(x) for x in liga.split(":")]
    combo_liga_h = ttk.Combobox(frame, values=valores_horas, width=2, state="normal")
    combo_liga_m = ttk.Combobox(frame, values=valores_minutos, width=2, state="normal")
    combo_liga_s = ttk.Combobox(frame, values=valores_segundos, width=2, state="normal")
    combo_liga_h.grid(row=1, column=1, padx=0, sticky="w")
    tk.Label(frame, text=":").grid(row=1, column=2, sticky="w", padx=0)
    combo_liga_m.grid(row=1, column=3, padx=0, sticky="w")
    tk.Label(frame, text=":").grid(row=1, column=4, sticky="w", padx=0)
    combo_liga_s.grid(row=1, column=5, padx=(0,8), sticky="w")
    combo_liga_h.set(f"{h_l:02}")
    combo_liga_m.set(f"{m_l:02}")
    combo_liga_s.set(f"{s_l:02}")

    # Hora Desliga
    tk.Label(frame, text="Hora Desliga:", anchor="w").grid(row=2, column=0, padx=(0,8), sticky="w")
    desliga = hora_desliga if hora_desliga else "00:00:00"
    h_d, m_d, s_d = [int(x) for x in desliga.split(":")]
    combo_desl_h = ttk.Combobox(frame, values=valores_horas, width=2, state="normal")
    combo_desl_m = ttk.Combobox(frame, values=valores_minutos, width=2, state="normal")
    combo_desl_s = ttk.Combobox(frame, values=valores_segundos, width=2, state="normal")
    combo_desl_h.grid(row=2, column=1, padx=0, sticky="w")
    tk.Label(frame, text=":").grid(row=2, column=2, sticky="w", padx=0)
    combo_desl_m.grid(row=2, column=3, padx=0, sticky="w")
    tk.Label(frame, text=":").grid(row=2, column=4, sticky="w", padx=0)
    combo_desl_s.grid(row=2, column=5, padx=(0,8), sticky="w")
    combo_desl_h.set(f"{h_d:02}")
    combo_desl_m.set(f"{m_d:02}")
    combo_desl_s.set(f"{s_d:02}")

    def salvar():
        try:
            h_l_int = int(combo_liga_h.get())
            m_l_int = int(combo_liga_m.get())
            s_l_int = int(combo_liga_s.get())
            h_d_int = int(combo_desl_h.get())
            m_d_int = int(combo_desl_m.get())
            s_d_int = int(combo_desl_s.get())
        except Exception:
            messagebox.showerror("Erro", "Todos os campos de horário devem ser preenchidos com números válidos.")
            return

        dia = dia_var.get()
        liga = f"{h_l_int:02}:{m_l_int:02}:{s_l_int:02}"
        desliga = f"{h_d_int:02}:{m_d_int:02}:{s_d_int:02}"

        salvar_callback(dia, liga, desliga)
        janela.destroy()

    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=3, column=0, columnspan=6, pady=(4,0))
    tk.Button(btn_frame, text="Salvar", command=salvar, width=16).pack()

    # Centralizar janela
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






def abrir_janela_rega_lista(janela_pai, output, salvar_callback=None):
    janela = tk.Toplevel(janela_pai)
    janela.title(f"Horários - {output.nome} (Rega)")
    janela.resizable(False, False)
    janela.transient(janela_pai)
    janela.grab_set()
    janela.focus_force()

    frame = tk.Frame(janela)
    frame.pack(padx=10, pady=10)

    lista_horarios = tk.Listbox(frame, height=8, width=32)
    lista_horarios.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")

    def atualizar_lista():
        lista_horarios.delete(0, tk.END)
        for h in output.horarios:
            dia = h.get('dia', 'Todos')
            liga = h['liga']
            desliga = h['desliga']
            lista_horarios.insert(tk.END, f"{dia:7} | Liga: {liga}   Desliga: {desliga}")

    def botao_adicionar():
        def salvar(dia, liga, desliga):
            output.horarios.append({'dia': dia, 'liga': liga, 'desliga': desliga})
            atualizar_lista()
            if salvar_callback:
                salvar_callback()
        abrir_janela_rega_edicao(janela, salvar)

    def botao_editar():
        sel = lista_horarios.curselection()
        if not sel:
            messagebox.showinfo("Selecione", "Selecione um horário para editar.")
            return
        idx = sel[0]
        horario = output.horarios[idx]
        def salvar(dia, liga, desliga):
            output.horarios[idx] = {'dia': dia, 'liga': liga, 'desliga': desliga}
            atualizar_lista()
            if salvar_callback:
                salvar_callback()
        abrir_janela_rega_edicao(janela, salvar, horario.get("dia", "Todos"), horario["liga"], horario["desliga"])

    def botao_remover():
        sel = lista_horarios.curselection()
        if not sel:
            messagebox.showinfo("Selecione", "Selecione um horário para remover.")
            return
        idx = sel[0]
        del output.horarios[idx]
        atualizar_lista()
        if salvar_callback:
            salvar_callback()

    btn_add = tk.Button(frame, text="Adicionar", command=botao_adicionar)
    btn_add.grid(row=1, column=0, padx=5, pady=5)
    btn_edit = tk.Button(frame, text="Editar", command=botao_editar)
    btn_edit.grid(row=1, column=1, padx=5, pady=5)
    btn_del = tk.Button(frame, text="Remover", command=botao_remover)
    btn_del.grid(row=1, column=2, padx=5, pady=5)

    atualizar_lista()
    # Centralizar janela
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
