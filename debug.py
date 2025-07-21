from datetime import datetime, timedelta

def criar_devices_de_teste(gerenciador, ciclos=100):
    agora = datetime.now()
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    dia_atual_idx = agora.weekday()
    dia_atual = dias_semana[dia_atual_idx]
    dia_errado = dias_semana[(dia_atual_idx + 1) % 7]

    tipos = ["Led", "Rega", "Runoff"]
    nomes_base = {"Led": "Led", "Rega": "Rega", "Runoff": "Runoff"}
    tomadas = list(range(1, 9))
    fase1_ciclos = 5
    fase2_blocos = 5
    tempo_inicial = 5  # segundos para o primeiro evento
    tempo_ligado = 1   # tempo em segundos de cada tomada ligada

    # Cria todos os devices e limpa horarios
    dispositivos = []
    for tomada in tomadas:
        tipo = tipos[(tomada - 1) % len(tipos)]
        nome = f"{nomes_base[tipo]} {tomada}"
        device = gerenciador.adicionar_output(nome, tipo, tomada, sobrescrever=True)
        device.horarios = []
        dispositivos.append((device, tipo))

    t = agora + timedelta(seconds=tempo_inicial)
    num_dispositivos = len(dispositivos)

    for ciclo_geral in range(ciclos):
        # ---------- PRIMEIRA FASE: alternando ----------
        for ciclo in range(fase1_ciclos):
            for idx, (device, tipo) in enumerate(dispositivos):
                liga_dt = t
                desliga_dt = liga_dt + timedelta(seconds=tempo_ligado)
                hora_liga = liga_dt.strftime("%H:%M:%S")
                hora_desliga = desliga_dt.strftime("%H:%M:%S")
                if tipo in ("Led", "Runoff"):
                    device.horarios.append({
                        "liga": hora_liga,
                        "desliga": hora_desliga
                    })
                elif tipo == "Rega":
                    if ciclo == fase1_ciclos - 1:
                        dia = dia_errado
                    else:
                        dia = "All" if ciclo % 2 == 0 else dia_atual
                    device.horarios.append({
                        "dia": dia,
                        "liga": hora_liga,
                        "desliga": hora_desliga,
                        "tempo": 5 + ciclo + ciclo_geral * (fase1_ciclos + fase2_blocos)
                    })
                t = desliga_dt  # próxima tomada liga quando anterior desliga

        # ---------- SEGUNDA FASE: todas juntas, 1s liga, 1s desliga, 5x ----------
        # Para a segunda fase, resetamos a cada ciclo para garantir alternância
        t_fase2 = t  # começa logo após a fase 1 de cada ciclo_geral
        for n in range(fase2_blocos):
            liga_dt = t_fase2 + timedelta(seconds=n * 2)        # LIGA: 0,2,4,6,8
            desliga_dt = liga_dt + timedelta(seconds=1)          # DESLIGA: 1,3,5,7,9
            hora_liga = liga_dt.strftime("%H:%M:%S")
            hora_desliga = desliga_dt.strftime("%H:%M:%S")
            for device, tipo in dispositivos:
                if tipo in ("Led", "Runoff"):
                    device.horarios.append({
                        "liga": hora_liga,
                        "desliga": hora_desliga
                    })
                elif tipo == "Rega":
                    # Alterna All/dia_atual e último evento usa dia_errado
                    if n == fase2_blocos - 1:
                        dia = dia_errado
                    else:
                        dia = "All" if n % 2 == 0 else dia_atual
                    device.horarios.append({
                        "dia": dia,
                        "liga": hora_liga,
                        "desliga": hora_desliga,
                        "tempo": 30 + n + ciclo_geral * (fase1_ciclos + fase2_blocos)
                    })
        # Agora avança t para depois da última desliga da segunda fase
        t = t_fase2 + timedelta(seconds=fase2_blocos * 2)

    print("Dispositivos de teste criados.")
