import tkinter as tk
from datetime import datetime

class Relogio:
    @staticmethod
    def mostrar_em(label, agora):
        def atualizar():
            agora_alt = agora.now().strftime("%a %H:%M:%S")
            label.config(text=agora_alt)
            label.after(200, atualizar)

        atualizar()


