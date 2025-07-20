import tkinter as tk
from datetime import datetime

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

def ajustar_estado_wavemaker_agora(output):
    agora_dt = datetime.now()
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

def centralizar_horizontal_abaixo(janela, janela_pai, deslocamento=10):
    """
    Centraliza a janela `janela` na horizontal em relação à `janela_pai`,
    posicionando logo abaixo dela, com um deslocamento opcional em pixels.
    Deve ser chamada após todos os widgets da nova janela terem sido criados!
    """
    janela.update_idletasks()
    janela_pai.update_idletasks()
    largura_janela = janela.winfo_width()
    largura_pai = janela_pai.winfo_width()
    x_pai = janela_pai.winfo_rootx()
    y_pai = janela_pai.winfo_rooty()
    altura_pai = janela_pai.winfo_height()
    x = x_pai + (largura_pai - largura_janela) // 2
    y = y_pai + altura_pai + deslocamento
    x = max(0, x)
    y = max(0, y)
    janela.geometry(f"+{x}+{y}")


def centralizar_horizontal_acima(janela, janela_pai, deslocamento=10):
    """
    Centraliza a janela `janela` na horizontal em relação à `janela_pai`,
    posicionando logo ACIMA dela, com um deslocamento opcional em pixels.
    Deve ser chamada após todos os widgets da nova janela terem sido criados!
    """
    janela.update_idletasks()
    janela_pai.update_idletasks()
    largura_janela = janela.winfo_width()
    largura_pai = janela_pai.winfo_width()
    x_pai = janela_pai.winfo_rootx()
    y_pai = janela_pai.winfo_rooty()
    x = x_pai + (largura_pai - largura_janela) // 2
    y = y_pai - janela.winfo_height() - deslocamento
    x = max(0, x)
    y = max(0, y)
    janela.geometry(f"+{x}+{y}")

def posicionar_direita(janela, janela_pai, deslocamento=10):
    """
    Posiciona a janela `janela` logo à direita da `janela_pai`,
    alinhando pelo topo, com deslocamento opcional em pixels.
    Deve ser chamada após criar todos os widgets da nova janela!
    """
    janela.update_idletasks()
    janela_pai.update_idletasks()
    largura_pai = janela_pai.winfo_width()
    altura_pai = janela_pai.winfo_height()
    x_pai = janela_pai.winfo_rootx()
    y_pai = janela_pai.winfo_rooty()
    x = x_pai + largura_pai + deslocamento
    y = y_pai
    # Se passar do limite da tela, ajusta para caber
    largura_tela = janela.winfo_screenwidth()
    if x + janela.winfo_width() > largura_tela:
        x = largura_tela - janela.winfo_width()
        x = max(0, x)
    janela.geometry(f"+{x}+{y}")