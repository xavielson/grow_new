"""GPIO control helper module.

Tries to import ``gpiozero.OutputDevice`` for real hardware control. When
``gpiozero`` isn't available (e.g. running on a non-Raspberry Pi machine) a
simple fallback implementation is used so the rest of the application can run
without errors.
"""

try:
    from gpiozero import OutputDevice  # type: ignore
except Exception:
    class OutputDevice:
        """Fallback OutputDevice used when gpiozero is missing.

        It mimics the subset of the real class used by the application and
        simply prints state changes to stdout.
        """

        def __init__(self, pin, active_high=False, initial_value=False):
            self.pin = pin
            self.active_high = active_high
            self.value = initial_value

        def on(self):
            self.value = True
            print(f"[SIM] GPIO {self.pin} ON")

        def off(self):
            self.value = False
            print(f"[SIM] GPIO {self.pin} OFF")

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
        
