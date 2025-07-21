import tkinter as tk
from tkinter import ttk, messagebox
from utils_tk import centralizar_janela, gerar_lista_horas, gerar_lista_minutos, centralizar_horizontal_abaixo, posicionar_direita

def abrir_janela_runoff_edicao(janela_pai, salvar_callback, botao_modificar_horarios=None, hora_liga=None, hora_desliga=None):
    def fechar_janela():
        if botao_modificar_horarios:
            botao_modificar_horarios.config(state="normal")
        janela.destroy()

    if botao_modificar_horarios:
        botao_modificar_horarios.config(state="disabled")

    janela = tk.Toplevel(janela_pai)
    janela.title("Horários de Runoff")
    janela.resizable(False, False)
    janela.transient(janela_pai)
    janela.focus_force()
    janela.protocol("WM_DELETE_WINDOW", fechar_janela)

    frame = tk.Frame(janela, padx=8, pady=8)
    frame.grid(row=0, column=0)

    valores_horas = gerar_lista_horas()
    valores_minutos = gerar_lista_minutos()

    liga = hora_liga if hora_liga else "00:00:00"
    desliga = hora_desliga if hora_desliga else "00:00:00"
    h_l, m_l, s_l = [int(x) for x in liga.split(":")]
    h_d, m_d, s_d = [int(x) for x in desliga.split(":")]

    tk.Label(frame, text="Hora Liga:").grid(row=0, column=0, sticky="w", padx=(0, 8))
    combo_liga_h = ttk.Combobox(frame, values=valores_horas, width=2, state="normal")
    combo_liga_m = ttk.Combobox(frame, values=valores_minutos, width=2, state="normal")
    combo_liga_s = ttk.Combobox(frame, values=valores_minutos, width=2, state="normal")
    combo_liga_h.grid(row=0, column=1, sticky="w", padx=0)
    tk.Label(frame, text=":").grid(row=0, column=2, sticky="w", padx=0)
    combo_liga_m.grid(row=0, column=3, sticky="w", padx=0)
    tk.Label(frame, text=":").grid(row=0, column=4, sticky="w", padx=0)
    combo_liga_s.grid(row=0, column=5, sticky="w", padx=(0, 8))
    combo_liga_h.set(f"{h_l:02}")
    combo_liga_m.set(f"{m_l:02}")
    combo_liga_s.set(f"{s_l:02}")

    tk.Label(frame, text="Hora Desliga:").grid(row=1, column=0, sticky="w", padx=(0, 8))
    combo_desl_h = ttk.Combobox(frame, values=valores_horas, width=2, state="normal")
    combo_desl_m = ttk.Combobox(frame, values=valores_minutos, width=2, state="normal")
    combo_desl_s = ttk.Combobox(frame, values=valores_minutos, width=2, state="normal")
    combo_desl_h.grid(row=1, column=1, sticky="w", padx=0)
    tk.Label(frame, text=":").grid(row=1, column=2, sticky="w", padx=0)
    combo_desl_m.grid(row=1, column=3, sticky="w", padx=0)
    tk.Label(frame, text=":").grid(row=1, column=4, sticky="w", padx=0)
    combo_desl_s.grid(row=1, column=5, sticky="w", padx=(0, 8))
    combo_desl_h.set(f"{h_d:02}")
    combo_desl_m.set(f"{m_d:02}")
    combo_desl_s.set(f"{s_d:02}")

    def salvar():
        campos = [
            (combo_liga_h, 0, 23, "Hora Liga"),
            (combo_liga_m, 0, 59, "Minuto Liga"),
            (combo_liga_s, 0, 59, "Segundo Liga"),
            (combo_desl_h, 0, 23, "Hora Desliga"),
            (combo_desl_m, 0, 59, "Minuto Desliga"),
            (combo_desl_s, 0, 59, "Segundo Desliga"),
        ]
        valores = []
        for combo, vmin, vmax, campo_nome in campos:
            valor = combo.get()
            if not valor.isdigit():
                messagebox.showerror("Erro", f"{campo_nome} deve conter apenas números.")
                combo.focus_set()
                return
            valor_int = int(valor)
            if not (vmin <= valor_int <= vmax):
                messagebox.showerror("Erro", f"{campo_nome} deve ser entre {vmin:02} e {vmax:02}.")
                combo.focus_set()
                return
            valores.append(valor_int)

        liga = f"{valores[0]:02}:{valores[1]:02}:{valores[2]:02}"
        desliga = f"{valores[3]:02}:{valores[4]:02}:{valores[5]:02}"
        salvar_callback(liga, desliga)
        fechar_janela()

    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=2, column=0, columnspan=6, pady=(4, 0))
    tk.Button(btn_frame, text="Salvar", command=salvar, width=16).pack()

    posicionar_direita(janela, janela_pai)

def abrir_janela_runoff_lista(janela_pai, output, salvar_callback=None):
    janela = tk.Toplevel(janela_pai)    
    janela.title(f"Horários - {output.nome} (Runoff)")
    janela.resizable(False, False)
    janela.transient(janela_pai)
    janela.after(10, janela.grab_set)
    janela.focus_force()

    frame = tk.Frame(janela, padx=4, pady=8)
    frame.pack()

    list_font = ("Courier New", 10)
    texto_exemplo = "Liga: 23:59:59   Desliga: 23:59:59"
    largura_caracteres = len(texto_exemplo) + 4  # padding lateral

    lista_horarios = tk.Listbox(frame, height=8, width=largura_caracteres, font=list_font)
    lista_horarios.grid(row=0, column=0, columnspan=3, pady=(0, 4), sticky="ew")

    def atualizar_lista():
        lista_horarios.delete(0, tk.END)
        for h in output.horarios:
            liga = h['liga']
            desliga = h['desliga']
            lista_horarios.insert(
                tk.END,
                f"  Liga: {liga}   Desliga: {desliga}  "
            )

    def botao_adicionar():
        def salvar(liga, desliga):
            output.horarios.append({'liga': liga, 'desliga': desliga})
            atualizar_lista()
            if salvar_callback:
                salvar_callback()
        abrir_janela_runoff_edicao(janela, salvar)

    def botao_editar():
        sel = lista_horarios.curselection()
        if not sel:
            messagebox.showinfo("Selecione", "Selecione um horário para editar.")
            return
        idx = sel[0]
        horario = output.horarios[idx]
        def salvar(liga, desliga):
            output.horarios[idx] = {'liga': liga, 'desliga': desliga}
            atualizar_lista()
            if salvar_callback:
                salvar_callback()
        abrir_janela_runoff_edicao(janela, salvar, None, horario["liga"], horario["desliga"])

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
    btn_add.grid(row=1, column=0, padx=3, pady=3)
    btn_edit = tk.Button(frame, text="Editar", command=botao_editar)
    btn_edit.grid(row=1, column=1, padx=3, pady=3)
    btn_del = tk.Button(frame, text="Remover", command=botao_remover)
    btn_del.grid(row=1, column=2, padx=3, pady=3)

    lista_horarios.bind("<Double-1>", lambda event: botao_editar())

    atualizar_lista()

    centralizar_horizontal_abaixo(janela, janela_pai)
