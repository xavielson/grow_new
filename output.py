import pickle

class Output:
    def __init__(self, nome, device, pin, tomada):
        self.nome = nome
        self.device = device
        self.pin = pin
        self.tomada = tomada
        self.relay_is_active = False

    def __str__(self):
        return f"{self.nome} ({self.device}) - Pin: {self.pin}"

    def is_active(self):
        return self.relay_is_active

    def toggle(self):
        self.relay_is_active = not self.relay_is_active


class GerenciadorOutputs:
    def __init__(self):
        self.tomadas = {i: None for i in range(1, 9)}
        self.pins = {1: 2, 2: 3, 3: 4, 4: 17, 5: 27, 6: 22, 7: 10, 8: 9}

    def adicionar_output(self, nome, device, tomada, sobrescrever=False):
        if self.tomadas[tomada] is not None and not sobrescrever:
            print(f"Tomada {tomada} já está ocupada por {self.tomadas[tomada]}")
            return None
        self.tomadas[tomada] = Output(nome, device, tomada, self.pins[tomada])
        return self.tomadas[tomada]

    def buscar_por_tomada(self, tomada):
        return self.tomadas.get(tomada)

    def salvar_em_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'wb') as f:
            pickle.dump(self.tomadas, f)

    def carregar_de_arquivo(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'rb') as f:
                self.tomadas = pickle.load(f)
                print("Dados carregados com sucesso!")
        except FileNotFoundError:
            print("Arquivo não encontrado. Iniciando com dados vazios.")
