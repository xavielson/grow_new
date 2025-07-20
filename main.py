from interface import criar_interface
from output import GerenciadorOutputs
import os



ARQUIVO = os.path.join(os.path.dirname(__file__), "dados_outputs.pkl")

def main():
    gerenciador = GerenciadorOutputs()
    try:
        gerenciador.carregar_de_arquivo(ARQUIVO)
    except Exception as e:
        print(f"Erro ao carregar dados: {e}. Iniciando com lista vazia.")

    def salvar():
        gerenciador.salvar_em_arquivo(ARQUIVO)

    criar_interface(gerenciador, salvar)

if __name__ == "__main__":
    main()