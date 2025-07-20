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


