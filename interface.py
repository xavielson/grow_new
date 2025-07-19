import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from output import Output
from relogio import Relogio

from janela_dispositivo import abrir_janela_dispositivo
from janela_horarios import abrir_janela_horarios

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

    def abrir_janela_dispositivo_local(tomada, output_existente=None):
        abrir_janela_dispositivo(janela_lista, gerenciador, tomada, output_existente, salvar_callback, atualizar_lista)

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
            resposta = messagebox.askyesno("Confirmação de edição",
                                          f"A saída {tomada} já está ocupada por:\n\n{output}\n\nDeseja editar este dispositivo?")
            if not resposta:
                return
            abrir_janela_dispositivo_local(tomada, output)
        else:
            abrir_janela_dispositivo_local(tomada, None)

    def editar_dispositivo():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um dispositivo para editar.")
            return
        tomada = int(selecionado[0])
        output = gerenciador.buscar_por_tomada(tomada)
        if output:
            resposta = messagebox.askyesno("Confirmação de edição",
                                          f"A saída {tomada} já está ocupada por:\n\n{output}\n\nDeseja editar este dispositivo?")
            if not resposta:
                return
            abrir_janela_dispositivo_local(tomada, output)
        else:
            abrir_janela_dispositivo_local(tomada, None)

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

        abrir_janela_horarios(janela_lista, gerenciador, tomada, output, salvar_callback, btn_modificar_horarios)

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
