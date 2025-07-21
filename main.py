from interface import criar_interface
from output import GerenciadorOutputs
import os
from debug import criar_devices_de_teste
from gpio_control import inicializar_todos_os_pinos



ARQUIVO = os.path.join(os.path.dirname(__file__), "dados_outputs.pkl")

def main():

    inicializar_todos_os_pinos()
    
    gerenciador = GerenciadorOutputs()
    #criar_devices_de_teste(gerenciador)  # Cria dispositivos de teste
    
    try:
        gerenciador.carregar_de_arquivo(ARQUIVO)
    except Exception as e:
        print(f"Erro ao carregar dados: {e}. Iniciando com lista vazia.")

    def salvar():
        gerenciador.salvar_em_arquivo(ARQUIVO)
    
    criar_interface(gerenciador, salvar)

if __name__ == "__main__":
    main()