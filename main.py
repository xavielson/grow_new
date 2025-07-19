from interface import criar_interface
from output import GerenciadorOutputs

ARQUIVO = "dados_outputs.pkl"

def main():
    gerenciador = GerenciadorOutputs()
    gerenciador.carregar_de_arquivo(ARQUIVO)

    def salvar():
        gerenciador.salvar_em_arquivo(ARQUIVO)

    criar_interface(gerenciador, salvar)

if __name__ == "__main__":
    main()