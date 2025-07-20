import tkinter as tk
from tkinter import ttk, messagebox
from output import Output
import tkinter.font as tkfont
from relogio import Relogio
from janela_led import abrir_janela_led_lista
from janela_rega import abrir_janela_rega_lista
from janela_wavemaker import abrir_janela_wavemaker_lista
from utils_tk import centralizar_horizontal_abaixo

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

    def inicializar_lista():
        # Cria cada item na Treeview uma vez só
        for tomada, output in gerenciador.tomadas.items():
            tag = "par" if tomada % 2 == 0 else "impar"
            if output:
                tree.insert("", "end", iid=tomada, values=(
                    tomada, output.nome, output.device, output.pin, ""
                ), tags=(tag,))
            else:
                tree.insert("", "end", iid=tomada, values=(
                    tomada, "Vazio", "", "", ""
                ), tags=(tag,))
        ajustar_largura_colunas()
        atualizar_botoes_status()

    def atualizar_lista():
        # Atualiza apenas os campos que mudaram, sem recriar itens!
        for tomada, output in gerenciador.tomadas.items():
            if output:
                valores = (tomada, output.nome, output.device, output.pin, "")
                tree.item(tomada, values=valores)
            else:
                valores = (tomada, "Vazio", "", "", "")
                tree.item(tomada, values=valores)
        atualizar_botoes_status()

    def atualizar_botoes_status():
        for tomada, output in gerenciador.tomadas.items():
            if output:
                estado = output.is_active()
                cor = "green" if estado else "red"
                btn = botoes_status.get(tomada)
                if btn is None:
                    btn = tk.Button(
                        tree,
                        width=2,
                        height=1,
                        bg=cor,
                        activebackground=cor,
                        relief="flat",
                        command=lambda t=tomada: toggle_status(t)
                    )
                    botoes_status[tomada] = btn
                else:
                    btn.config(bg=cor, activebackground=cor)
                tree.update_idletasks()
                bbox = tree.bbox(tomada, column=4)
                if bbox:
                    x, y, width, height = bbox
                    y_btn = y + (height - 20)//2
                    btn.place(x=x + (width - 20)//2, y=y_btn, width=20, height=20)
            else:
                btn = botoes_status.pop(tomada, None)
                if btn:
                    btn.destroy()

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

        janela = tk.Toplevel(janela_principal)
        acao = "Editar" if output_existente else "Novo"
        janela.title(f"{acao} Dispositivo - Saída {tomada}")

        # CRIE OS WIDGETS PRIMEIRO
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

        # AGORA sim, centralize!
        centralizar_horizontal_abaixo(janela, janela_principal)

        # Para debug (opcional)
        # print("Largura principal:", largura_principal)
        # print("Largura nova janela:", largura_janela)
        # print("x principal:", x_principal)
        # print("x centro:", x_centro)

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
        if not output:
            editar_dispositivo()
            return

        tipo = output.device

        def salvar_e_habilitar(*args, **kwargs):
            if salvar_callback:
                salvar_callback(*args, **kwargs)
            btn_modificar_horarios.config(state="normal")

        # Use after_idle para garantir que a janela principal está visível e prontos para abrir a nova janela
        if tipo == "Rega":
            janela_principal.after_idle(lambda: abrir_janela_rega_lista(janela_principal, output, salvar_e_habilitar))
        elif tipo == "Led":
            janela_principal.after_idle(lambda: abrir_janela_led_lista(janela_principal, output, salvar_e_habilitar))
        elif tipo == "Wavemaker":
            janela_principal.after_idle(lambda: abrir_janela_wavemaker_lista(janela_principal, output, salvar_e_habilitar))
        else:
            tk.Label(janela_principal, text=f"A personalização para '{tipo}' ainda não foi implementada.").pack(padx=10, pady=20)

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

    # ----- Nova janela para editar múltiplos horários ---------
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

        def salvar_e_habilitar(*args, **kwargs):
            if salvar_callback:
                salvar_callback(*args, **kwargs)
            btn_modificar_horarios.config(state="normal")

        if tipo == "Rega":
            abrir_janela_rega_lista(janela_principal, output, salvar_e_habilitar)
        elif tipo == "Led":
            abrir_janela_led_lista(janela_principal, output, salvar_e_habilitar)
        elif tipo == "Wavemaker":
            abrir_janela_wavemaker_lista(janela_principal, output, salvar_e_habilitar)
        else:
            tk.Label(janela_principal, text=f"A personalização para '{tipo}' ainda não foi implementada.").pack(padx=10, pady=20)

    # ----------- Automação dos horários dos relés -----------

    def checar_e_aplicar_acoes():
        agora = datetime.now()
        str_hora = agora.strftime("%H:%M:%S")
        
        dia_semana_atual = agora.weekday()
        dias_map = {
            0: "Seg",
            1: "Ter",
            2: "Qua",
            3: "Qui",
            4: "Sex",
            5: "Sab",
            6: "Dom"
        }
        dia_semana_pt = dias_map[dia_semana_atual]

        for output in gerenciador.tomadas.values():
            if not output:
                continue

            # ---------- Wavemaker -----------
            if getattr(output, "device", None) == "Wavemaker":
                modo = getattr(output, "wavemaker_mode", "Sempre ligado")
                estado_desejado = False
                if modo == "Sempre ligado":
                    estado_desejado = True
                elif modo == "Liga/desliga a cada 15 minutos":
                    estado_desejado = (agora.minute % 30) < 15
                elif modo == "Liga/desliga a cada 30 minutos":
                    estado_desejado = (agora.minute % 60) < 30
                elif modo == "Liga/desliga a cada 1 hora":
                    estado_desejado = (agora.hour % 2) == 0
                elif modo == "Liga/desliga a cada 6 horas":
                    estado_desejado = (agora.hour % 12) < 6

                if getattr(output, "relay_is_active", None) != estado_desejado:
                    if estado_desejado:
                        output.on()
                    else:
                        output.off()
                    output.relay_is_active = estado_desejado

            # ---------- Rega ----------
            if getattr(output, "device", None) == "Rega" and hasattr(output, "horarios"):
                for evento in output.horarios:
                    dia_evento = evento.get("dia", "All")
                    if dia_evento != "All" and dia_evento != dia_semana_pt:
                        continue  # só processa se for o dia certo

                    if "liga" in evento and evento["liga"] == str_hora:
                        output.on()
                    elif "desliga" in evento and evento["desliga"] == str_hora:
                        output.off()

            # ---------- Led ----------
            if getattr(output, "device", None) == "Led" and hasattr(output, "horarios"):
                for evento in output.horarios:
                    if "liga" in evento and evento["liga"] == str_hora:                        
                        output.on()
                    elif "desliga" in evento and evento["desliga"] == str_hora:                        
                        output.off()

    def loop_agendador():
        checar_e_aplicar_acoes()
        atualizar_lista()  # Agora, só status, sem piscar!
        janela_principal.after(1000, loop_agendador)

    janela_principal = tk.Tk()
    janela_principal.withdraw()
    janela_principal.title("Lista de Dispositivos")

    style = ttk.Style()
    style.configure("Treeview", rowheight=25)

    tk.Label(janela_principal, text="Dispositivos cadastrados:", font=("Arial", 12, "bold")).pack(pady=10)

    tree = ttk.Treeview(janela_principal, columns=colunas, show="headings", selectmode="browse", height=len(gerenciador.tomadas))
    tree.tag_configure("par", background="#f0f0f0")
    tree.tag_configure("impar", background="#ffffff")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=50, anchor="center")

    tree.pack(fill="both", expand=True, padx=10)
    tree.bind("<Double-1>", duplo_clique)

    frame_botoes = tk.Frame(janela_principal)
    frame_botoes.pack(pady=10)

    btn_editar = tk.Button(frame_botoes, text="Editar", command=editar_dispositivo)
    btn_editar.pack(side="left", padx=5)

    btn_remover = tk.Button(frame_botoes, text="Remover", command=remover_dispositivo)
    btn_remover.pack(side="left", padx=5)

    btn_modificar_horarios = tk.Button(frame_botoes, text="Modificar Horários", command=modificar_horarios)
    btn_modificar_horarios.pack(side="left", padx=5)

    label_relogio = tk.Label(janela_principal, text="", font=("Arial", 12))
    label_relogio.pack(pady=5)

    janela_principal.update_idletasks()
    largura = janela_principal.winfo_width()
    altura = janela_principal.winfo_height()
    largura_tela = janela_principal.winfo_screenwidth()
    altura_tela = janela_principal.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2) - 300
    y = max(0, y)
    janela_principal.geometry(f"+{x}+{y}")

    

    def ajustar_estado_inicial_wavemakers(gerenciador):
        agora_dt = datetime.now()
        for output in gerenciador.tomadas.values():
            if not output:
                continue
            if getattr(output, "device", None) == "Wavemaker":
                modo = getattr(output, "wavemaker_mode", "Sempre ligado")
                estado_desejado = False
                if modo == "Sempre ligado":
                    estado_desejado = True
                elif modo == "Liga/desliga a cada 15 minutos":
                    estado_desejado = (agora_dt.minute % 30) < 15
                elif modo == "Liga/desliga a cada 30 minutos":
                    estado_desejado = (agora_dt.minute % 60) < 30
                elif modo == "Liga/desliga a cada 1 hora":
                    estado_desejado = (agora_dt.hour % 2) == 0
                elif modo == "Liga/desliga a cada 6 horas":
                    estado_desejado = (agora_dt.hour % 12) < 6

                if estado_desejado:
                    output.on()
                else:
                    output.off()
                output.relay_is_active = estado_desejado

    Relogio.mostrar_em(label_relogio)

    botoes_status = {}

    inicializar_lista()  # Cria uma vez só!
    janela_principal.deiconify()  # Mostra a janela principal
    ajustar_estado_inicial_wavemakers(gerenciador)  # Liga os Wavemakers que estiverem no modo "Sempre ligado"
    loop_agendador()     # Atualiza só o status/cores
    
    
    janela_principal.mainloop()
