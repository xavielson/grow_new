import tkinter as tk

def centralizar_janela(janela, janela_pai=None):
    janela.update_idletasks()
    if janela_pai:
        x_pai = janela_pai.winfo_rootx()
        y_pai = janela_pai.winfo_rooty()
        w_pai = janela_pai.winfo_width()
        h_pai = janela_pai.winfo_height()
        w = janela.winfo_width()
        h = janela.winfo_height()
        x = x_pai + (w_pai - w) // 2
        y = y_pai + (h_pai - h) // 2
        janela.geometry(f"{w}x{h}+{x}+{y}")
    else:
        w = janela.winfo_width()
        h = janela.winfo_height()
        ws = janela.winfo_screenwidth()
        hs = janela.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        janela.geometry(f'{w}x{h}+{x}+{y}')

def gerar_lista_horas():
    return [f"{i:02}" for i in range(24)]

def gerar_lista_minutos():
    return [f"{i:02}" for i in range(60)]
