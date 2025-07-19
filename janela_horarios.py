import tkinter as tk
from tkinter import ttk, messagebox

def abrir_janela_horarios(janela_pai, gerenciador, tomada, output, salvar_callback, botao_modificar_horarios):
    tipo = output.device

    def fechar_janela():
        botao_modificar_horarios.config(state="normal")
        janela.destroy()

    botao_modificar_horarios.config(state="disabled")
    janela = tk.Toplevel(janela_pai)
    janela.title(f"Horários - Saída {tomada} ({tipo})")
    janela.protocol("WM_DELETE_WINDOW", fechar_janela)

    janela.update_idletasks()
    janela_pai.update_idletasks()
    x_principal = janela_pai.winfo_x()
    y_principal = janela_pai.winfo_y()
    altura_principal = janela_pai.winfo_height()
    janela.geometry(f"+{x_principal}+{y_principal + altura_principal + 10}")

    if tipo == "Led":
        frame = tk.Frame(janela)
        frame.pack(padx=10, pady=10)

        # Labels acima dos campos
        tk.Label(frame, text="").grid(row=0, column=0)
        tk.Label(frame, text="Hora").grid(row=0, column=1)
        tk.Label(frame, text="Minuto").grid(row=0, column=2)
        tk.Label(frame, text="Segundo").grid(row=0, column=3)

        # Linha Hora Liga
        tk.Label(frame, text="Hora Liga:").grid(row=1, column=0, padx=(0, 5), sticky="e")

        hora_var = tk.StringVar()
        entrada_hora = ttk.Combobox(
            frame,
            textvariable=hora_var,
            width=4,
            justify="center",
            values=[f"{i:02d}" for i in range(24)]
        )
        entrada_hora.set("00")
        entrada_hora.grid(row=1, column=1, padx=2)

        minuto_var = tk.StringVar()
        entrada_minuto = ttk.Combobox(
            frame,
            textvariable=minuto_var,
            width=4,
            justify="center",
            values=[f"{i:02d}" for i in range(60)]
        )
        entrada_minuto.set("00")
        entrada_minuto.grid(row=1, column=2, padx=2)

        segundo_var = tk.StringVar()
        entrada_segundo = ttk.Combobox(
            frame,
            textvariable=segundo_var,
            width=4,
            justify="center",
            values=[f"{i:02d}" for i in range(60)]
        )
        entrada_segundo.set("00")
        entrada_segundo.grid(row=1, column=3, padx=2)

        # Linha Hora Desliga
        tk.Label(frame, text="Hora Desliga:").grid(row=2, column=0, padx=(0, 5), pady=(5, 0), sticky="e")

        hora_desliga_var = tk.StringVar()
        entrada_hora_desliga = ttk.Combobox(
            frame,
            textvariable=hora_desliga_var,
            width=4,
            justify="center",
            values=[f"{i:02d}" for i in range(24)]
        )
        entrada_hora_desliga.set("00")
        entrada_hora_desliga.grid(row=2, column=1, padx=2, pady=(5, 0))

        minuto_desliga_var = tk.StringVar()
        entrada_minuto_desliga = ttk.Combobox(
            frame,
            textvariable=minuto_desliga_var,
            width=4,
            justify="center",
            values=[f"{i:02d}" for i in range(60)]
        )
        entrada_minuto_desliga.set("00")
        entrada_minuto_desliga.grid(row=2, column=2, padx=2, pady=(5, 0))

        segundo_desliga_var = tk.StringVar()
        entrada_segundo_desliga = ttk.Combobox(
            frame,
            textvariable=segundo_desliga_var,
            width=4,
            justify="center",
            values=[f"{i:02d}" for i in range(60)]
        )
        entrada_segundo_desliga.set("00")
        entrada_segundo_desliga.grid(row=2, column=3, padx=2, pady=(5, 0))

        def validar_e_salvar():
            try:
                h1 = int(hora_var.get())
                m1 = int(minuto_var.get())
                s1 = int(segundo_var.get())
                h2 = int(hora_desliga_var.get())
                m2 = int(minuto_desliga_var.get())
                s2 = int(segundo_desliga_var.get())

                if not (0 <= h1 <= 23 and 0 <= m1 <= 59 and 0 <= s1 <= 59):
                    raise ValueError("Hora Liga contém valores inválidos.")
                if not (0 <= h2 <= 23 and 0 <= m2 <= 59 and 0 <= s2 <= 59):
                    raise ValueError("Hora Desliga contém valores inválidos.")

                hora_liga = f"{h1:02d}:{m1:02d}:{s1:02d}"
                hora_desliga = f"{h2:02d}:{m2:02d}:{s2:02d}"

                messagebox.showinfo("Horários válidos", f"Hora Liga: {hora_liga}\nHora Desliga: {hora_desliga}")
                janela.destroy()
                botao_modificar_horarios.config(state="normal")

            except ValueError as e:
                messagebox.showerror("Erro de validação", str(e))

        tk.Button(janela, text="Salvar", command=validar_e_salvar).pack(pady=10)

    else:
        tk.Label(janela, text=f"A personalização para '{tipo}' ainda não foi implementada.").pack(padx=10, pady=20)
        tk.Button(janela, text="Fechar", command=fechar_janela).pack(pady=10)
