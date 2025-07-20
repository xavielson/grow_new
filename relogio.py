import tkinter as tk
from datetime import datetime

class Relogio:
    @staticmethod
    def mostrar_em(label):
        def atualizar():
            agora = datetime.now().strftime("%a %H:%M:%S")
            label.config(text=agora)
            label.after(1000, atualizar)

        atualizar()


def checar_e_aplicar_acoes(lista_de_outputs):
    agora = datetime.now().strftime("%H:%M:%S")
    for output in lista_de_outputs:
        for evento in output.horarios:
            if "liga" in evento and evento["liga"] == agora:
                output.relay_is_active = True
            elif "desliga" in evento and evento["desliga"] == agora:
                output.relay_is_active = False