import tkinter as tk
from tkinter import ttk, messagebox
from output import Output
import tkinter.font as tkfont
from relogio import Relogio
from datetime import datetime

def criar_interface(gerenciador, salvar_callback):

    colunas = ("Saída", "Nome", "Tipo", "Pin", "Status")

    def ajustar_largura_colunas():
        font = tkfont.Font()
        for col in colunas:
            largura_maxima = font.measure(col)
            for item in tree.get_children():
                texto = tree.set(item, col)
                largura_texto = font.measure(str(texto))
                if largura_texto > largura_maxima:
                    largura_maxima = largura_texto
            largura_final = largura_maxima + 20
            if col == "Status":
                largura_final = font.measure("Status") + 20
            tree.column(col, width=largura_final, anchor="center")

    def atualizar_lista():
        for i in tree.get_children():
            tree.delete(i)

        for tomada, output in gerenciador.tomadas.items():
            tag = "par" if tomada % 2 == 0 else "impar"

            if output:
                tree.insert("", "end", iid=tomada, values=(
                    tomada,
                    output.nome,
                    output.device,
                    output.pin,
                    ""
                ), tags=(tag,))
            else:
                tree.insert("", "end", iid=tomada, values=(
                    tomada,
                    "Vazia",
                    "",
                    "",
                    ""
                ), tags=(tag,))

        ajustar_largura_colunas()
        atualizar_botoes_status()

    def atualizar_botoes_status():
        for btn in botoes_status.values():
            btn.destroy()
        botoes_status.clear()

        for tomada, output in gerenciador.tomadas.items():
            if output:
                estado = output.is_active()
                cor = "green" if estado else "red"

                btn = tk.Button(
                    tree,
                    width=2,
                    height=1,
                    bg=cor,
                    relief="flat",
                    command=lambda t=tomada: toggle_status(t)
                )
                botoes_status[tomada] = btn

                tree.update_idletasks()
                bbox = tree.bbox(tomada, column=4)
                if bbox:
                    x, y, width, height = bbox
                    y_btn = y + (height - 20)//2
                    btn.place(x=x + (width - 20)//2, y=y_btn, width=20, height=20)

    def toggle_status(tomada):
        output = gerenciador.buscar_por_tomada(tomada)
        if output:
            output.toggle()
            salvar_callback()
            atualizar_lista()

    def abrir_janela_dispositivo(tomada, output_existente=None):
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

        janela = tk.Toplevel(janela_lista)
        acao = "Editar" if output_existente else "Novo"
        janela.title(f"{acao} Dispositivo - Saída {tomada}")

        janela.update_idletasks()
        janela_lista.update_idletasks()
        x_principal = janela_lista.winfo_x()
        y_principal = janela_lista.winfo_y()
        altura_principal = janela_lista.winfo_height()

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

    def remover_dispositivo():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um dispositivo para remover.")
            return
        tomada = int(selecionado[0])
        output = gerenciador.buscar_por_tomada(tomada)
        if not output:
            messagebox.showinfo("Info", "Saída já está vazia.")
            return
        confirmar = messagebox.askyesno("Confirmação", f"Deseja remover o dispositivo:\n{output}?")
        if confirmar:
            gerenciador.tomadas[tomada] = None
            salvar_callback()
            atualizar_lista()

    def duplo_clique(event):
        selecionado = tree.selection()
        if not selecionado:
            return
        tomada = int(selecionado[0])
        output = gerenciador.buscar_por_tomada(tomada)
        if output:
            resposta = messagebox.askyesno("Confirmação de edição", f"A saída {tomada} já está ocupada por:\n\n{output}\n\nDeseja editar este dispositivo?")
            if not resposta:
                return
            abrir_janela_dispositivo(tomada, output)
        else:
            abrir_janela_dispositivo(tomada, None)

    def editar_dispositivo():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um dispositivo para editar.")
            return
        tomada = int(selecionado[0])
        output = gerenciador.buscar_por_tomada(tomada)
        if output:
            resposta = messagebox.askyesno("Confirmação de edição", f"A saída {tomada} já está ocupada por:\n\n{output}\n\nDeseja editar este dispositivo?")
            if not resposta:
                return
            abrir_janela_dispositivo(tomada, output)
        else:
            abrir_janela_dispositivo(tomada, None)

    def modificar_horarios():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Nenhum item selecionado.")
            return
        tomada = int(selecionado[0])
        output = gerenciador.buscar_por_tomada(tomada)
        if not output:
            messagebox.showwarning("Aviso", "A linha selecionada está vazia.")
            return

        tipo = output.device

        def fechar_janela():
            btn_modificar_horarios.config(state="normal")
            janela.destroy()

        btn_modificar_horarios.config(state="disabled")
        janela = tk.Toplevel(janela_lista)
        janela.title(f"Horários - Saída {tomada} ({tipo})")
        janela.protocol("WM_DELETE_WINDOW", fechar_janela)

        janela.update_idletasks()
        janela_lista.update_idletasks()
        x_principal = janela_lista.winfo_x()
        y_principal = janela_lista.winfo_y()
        altura_principal = janela_lista.winfo_height()
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
                    btn_modificar_horarios.config(state="normal")

                except ValueError as e:
                    messagebox.showerror("Erro de validação", str(e))

            tk.Button(janela, text="Salvar", command=validar_e_salvar).pack(pady=10)




        else:
            tk.Label(janela, text=f"A personalização para '{tipo}' ainda não foi implementada.").pack(padx=10, pady=20)
            tk.Button(janela, text="Fechar", command=fechar_janela).pack(pady=10)

    janela_lista = tk.Tk()
    janela_lista.title("Lista de Dispositivos")

    style = ttk.Style()
    style.configure("Treeview", rowheight=25)

    tk.Label(janela_lista, text="Dispositivos cadastrados:", font=("Arial", 12, "bold")).pack(pady=10)

    tree = ttk.Treeview(janela_lista, columns=colunas, show="headings", selectmode="browse")
    tree.tag_configure("par", background="#f0f0f0")
    tree.tag_configure("impar", background="#ffffff")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=50, anchor="center")

    tree.pack(fill="both", expand=True, padx=10)
    tree.bind("<Double-1>", duplo_clique)

    frame_botoes = tk.Frame(janela_lista)
    frame_botoes.pack(pady=10)

    btn_editar = tk.Button(frame_botoes, text="Editar", command=editar_dispositivo)
    btn_editar.pack(side="left", padx=5)

    btn_remover = tk.Button(frame_botoes, text="Remover", command=remover_dispositivo)
    btn_remover.pack(side="left", padx=5)

    btn_modificar_horarios = tk.Button(frame_botoes, text="Modificar Horários", command=modificar_horarios)
    btn_modificar_horarios.pack(side="left", padx=5)

    janela_lista.update_idletasks()
    largura = janela_lista.winfo_width()
    altura = janela_lista.winfo_height()
    largura_tela = janela_lista.winfo_screenwidth()
    altura_tela = janela_lista.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela_lista.geometry(f"+{x}+{y}")

    label_relogio = tk.Label(janela_lista, text="", font=("Arial", 12))
    label_relogio.pack(pady=5)

    Relogio.mostrar_em(label_relogio)

    botoes_status = {}

    atualizar_lista()
    janela_lista.mainloop()
