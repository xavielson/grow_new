from gpiozero import OutputDevice

pins_usados = [2, 3, 4, 17, 27, 22, 10, 9]

gpio_devices = {}

def inicializar_todos_os_pinos():
    """
    Inicializa todos os 8 GPIOs (1 a 8) e adiciona ao dicionário global gpio_devices.
    """
    for pin in pins_usados:
        if pin not in gpio_devices:
            try:
                gpio_devices[pin] = OutputDevice(pin, active_high=False, initial_value=False)
                #print(f"GPIO {pin} inicializado.")
            except Exception as e:
                print(f"Erro ao inicializar GPIO {pin}: {e}")
        else:
            print(f"GPIO {pin} já estava inicializado.")

def desligar_todos_os_pinos():
    """
    Desliga todos os OutputDevice registrados no dicionário global gpio_devices.
    """
    for pin, device in gpio_devices.items():
        try:
            device.off()
            print(f"GPIO {pin} desligado.")
        except Exception as e:
            print(f"Erro ao desligar GPIO {pin}: {e}")



def ligar_output(output):
    output.ativo = True
    if output.pin in gpio_devices:
        print("Ativando pin " + str(output.pin))
        gpio_devices[output.pin].on()
        if gpio_devices[output.pin].value == 1:
            print("Ligado")
        
        

def desligar_output(output):
    output.ativo = False
    if output.pin in gpio_devices:
        print("Desativando pin " + str(output.pin))
        gpio_devices[output.pin].off()
        if gpio_devices[output.pin].value == 0:
            print("Desligado")
        
