import pickle

class Output:
    def __init__(self, nome, device, pin):
        self.nome = nome
        self.device = device
        if device == "Wavemaker":
            self.wavemaker_mode = "Desligado"  # Modo padrão para Wavemaker
        self.pin = pin
        self.ativo = False
        self.horarios = []  # lista de dicts: {"liga": "HH:MM:SS", "desliga": "HH:MM:SS"}

    def is_active(self):
        return self.ativo

    def toggle(self):
        self.ativo = not self.ativo
    
    def on(self):
        self.ativo = True

    def off(self):
        self.ativo = False

    def adicionar_horario(self, hora_liga, hora_desliga):
        self.horarios.append({"liga": hora_liga, "desliga": hora_desliga})

    def remover_horario(self, index):
        if 0 <= index < len(self.horarios):
            del self.horarios[index]

    def limpar_horarios(self):
        self.horarios.clear()

    def __str__(self):
        return f"{self.nome} ({self.device}) - Pin {self.pin}"


class GerenciadorOutputs:
    def __init__(self):
        self.tomadas = {i: None for i in range(1, 9)}
        self.pins = {1: 2, 2: 3, 3: 4, 4: 17, 5: 27, 6: 22, 7: 10, 8: 9}

    def adicionar_output(self, nome, device, tomada, sobrescrever=False):
        if self.tomadas[tomada] is not None and not sobrescrever:
            print(f"Tomada {tomada} já está ocupada por {self.tomadas[tomada]}")
            return None
        self.tomadas[tomada] = Output(nome, device, self.pins[tomada])
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
