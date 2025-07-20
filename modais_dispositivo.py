import tkinter as tk
from tkinter import ttk, messagebox

# LED
def abrir_janela_led_lista(janela_pai, output_led, salvar_callback):
    def salvar():
        dia = combo_dia.get()
        h_liga = ent_h_liga.get().zfill(2)
        m_liga = ent_m_liga.get().zfill(2)
        s_liga = ent_s_liga.get().zfill(2)
        h_desliga = ent_h_desliga.get().zfill(2)
        m_desliga = ent_m_desliga.get().zfill(2)
        s_desliga = ent_s_desliga.get().zfill(2)

        if not (h_liga.isdigit() and m_liga.isdigit() and s_liga.isdigit() and
                h_desliga.isdigit() and m_desliga.isdigit() and s_desliga.isdigit()):
            messagebox.showerror("Erro", "Horário inválido.")
            return

        horario = {
            "dia": dia,
            "liga": f"{h_liga}:{m_liga}:{s_liga}",
            "desliga": f"{h_desliga}:{m_desliga}:{s_desliga}"
        }
        output_led.horarios.append(horario)
        salvar_callback()
        janela.destroy()

    janela = tk.Toplevel(janela_pai)
    janela.title("Adicionar Horário LED")
    janela.resizable(False, False)
    frame = tk.Frame(janela, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Dia da semana:").grid(row=0, column=0, sticky="w")
    combo_dia = ttk.Combobox(frame, values=["Todos", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"], state="readonly", width=10)
    combo_dia.current(0)
    combo_dia.grid(row=0, column=1)

    # Hora liga
    tk.Label(frame, text="Hora Liga:").grid(row=1, column=0, sticky="w")
    ent_h_liga = tk.Entry(frame, width=2)
    ent_m_liga = tk.Entry(frame, width=2)
    ent_s_liga = tk.Entry(frame, width=2)
    ent_h_liga.grid(row=1, column=1, sticky="w")
    tk.Label(frame, text=":").grid(row=1, column=2)
    ent_m_liga.grid(row=1, column=3, sticky="w")
    tk.Label(frame, text=":").grid(row=1, column=4)
    ent_s_liga.grid(row=1, column=5, sticky="w")

    # Hora desliga
    tk.Label(frame, text="Hora Desliga:").grid(row=2, column=0, sticky="w")
    ent_h_desliga = tk.Entry(frame, width=2)
    ent_m_desliga = tk.Entry(frame, width=2)
    ent_s_desliga = tk.Entry(frame, width=2)
    ent_h_desliga.grid(row=2, column=1, sticky="w")
    tk.Label(frame, text=":").grid(row=2, column=2)
    ent_m_desliga.grid(row=2, column=3, sticky="w")
    tk.Label(frame, text=":").grid(row=2, column=4)
    ent_s_desliga.grid(row=2, column=5, sticky="w")

    btn = tk.Button(frame, text="Salvar", command=salvar, width=10)
    btn.grid(row=3, column=0, columnspan=6, pady=(8, 2))

    janela.transient(janela_pai)
    janela.grab_set()
    janela.focus_force()
    janela.wait_window(janela)

# REGA
def abrir_janela_rega_lista(janela_pai, output_rega, salvar_callback):
    def salvar():
        dia = combo_dia.get()
        h_liga = ent_h_liga.get().zfill(2)
        m_liga = ent_m_liga.get().zfill(2)
        s_liga = ent_s_liga.get().zfill(2)
        h_desliga = ent_h_desliga.get().zfill(2)
        m_desliga = ent_m_desliga.get().zfill(2)
        s_desliga = ent_s_desliga.get().zfill(2)

        tempo = ent_tempo.get()
        if not tempo.isdigit():
            messagebox.showerror("Erro", "Tempo de rega inválido.")
            return

        horario = {
            "dia": dia,
            "liga": f"{h_liga}:{m_liga}:{s_liga}",
            "desliga": f"{h_desliga}:{m_desliga}:{s_desliga}",
            "tempo": int(tempo)
        }
        output_rega.horarios.append(horario)
        salvar_callback()
        janela.destroy()

    janela = tk.Toplevel(janela_pai)
    janela.title("Adicionar Horário REGA")
    janela.resizable(False, False)
    frame = tk.Frame(janela, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Dia da semana:").grid(row=0, column=0, sticky="w")
    combo_dia = ttk.Combobox(frame, values=["Todos", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"], state="readonly", width=10)
    combo_dia.current(0)
    combo_dia.grid(row=0, column=1)

    tk.Label(frame, text="Hora Liga:").grid(row=1, column=0, sticky="w")
    ent_h_liga = tk.Entry(frame, width=2)
    ent_m_liga = tk.Entry(frame, width=2)
    ent_s_liga = tk.Entry(frame, width=2)
    ent_h_liga.grid(row=1, column=1, sticky="w")
    tk.Label(frame, text=":").grid(row=1, column=2)
    ent_m_liga.grid(row=1, column=3, sticky="w")
    tk.Label(frame, text=":").grid(row=1, column=4)
    ent_s_liga.grid(row=1, column=5, sticky="w")

    tk.Label(frame, text="Hora Desliga:").grid(row=2, column=0, sticky="w")
    ent_h_desliga = tk.Entry(frame, width=2)
    ent_m_desliga = tk.Entry(frame, width=2)
    ent_s_desliga = tk.Entry(frame, width=2)
    ent_h_desliga.grid(row=2, column=1, sticky="w")
    tk.Label(frame, text=":").grid(row=2, column=2)
    ent_m_desliga.grid(row=2, column=3, sticky="w")
    tk.Label(frame, text=":").grid(row=2, column=4)
    ent_s_desliga.grid(row=2, column=5, sticky="w")

    tk.Label(frame, text="Tempo de rega (s):").grid(row=3, column=0, sticky="w")
    ent_tempo = tk.Entry(frame, width=4)
    ent_tempo.insert(0, "10")
    ent_tempo.grid(row=3, column=1, sticky="w")

    btn = tk.Button(frame, text="Salvar", command=salvar, width=10)
    btn.grid(row=4, column=0, columnspan=6, pady=(8, 2))

    janela.transient(janela_pai)
    janela.grab_set()
    janela.focus_force()
    janela.wait_window(janela)

# WAVEMAKER
def abrir_janela_wavemaker_lista(janela_pai, output_wavemaker, salvar_callback):
    def salvar():
        try:
            intervalo_liga = int(ent_liga.get())
            intervalo_desliga = int(ent_desliga.get())
        except ValueError:
            messagebox.showerror("Erro", "Intervalo inválido.")
            return
        output_wavemaker.horarios.append({
            "intervalo_liga": intervalo_liga,
            "intervalo_desliga": intervalo_desliga,
        })
        salvar_callback()
        janela.destroy()

    janela = tk.Toplevel(janela_pai)
    janela.title("Intervalo Wavemaker")
    janela.resizable(False, False)
    frame = tk.Frame(janela, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Intervalo Liga (s):").grid(row=0, column=0, sticky="w")
    ent_liga = tk.Entry(frame, width=5)
    ent_liga.insert(0, "10")
    ent_liga.grid(row=0, column=1, sticky="w")

    tk.Label(frame, text="Intervalo Desliga (s):").grid(row=1, column=0, sticky="w")
    ent_desliga = tk.Entry(frame, width=5)
    ent_desliga.insert(0, "10")
    ent_desliga.grid(row=1, column=1, sticky="w")

    btn = tk.Button(frame, text="Salvar", command=salvar, width=10)
    btn.grid(row=2, column=0, columnspan=2, pady=(8, 2))

    janela.transient(janela_pai)
    janela.grab_set()
    janela.focus_force()
    janela.wait_window(janela)
