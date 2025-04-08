from datetime import datetime
from mfrc522 import SimpleMFRC522
from rfid_reader import obter_tag, definir_percentual
from balanca import calibracao, calculo_peso, read_count, BALANCAS
from motor import configurar_pwm, ativar_rele, destravar_motor
from detector_movimento import detectar_movimento
import RPi.GPIO as GPIO
import pigpio
import time

# Inicialização
pi = pigpio.pi()
if not pi.connected:
    exit()

# Faz a calibração dasi duas balanças
#tara1 = calibracao(BALANCAS[1]['DT'], BALANCAS[1]['SCK'])
#tara2 = calibracao(BALANCAS[2]['DT'], BALANCAS[2]['SCK'])

# Constantes e pinos
pino_pwm = 18
pino_rele = 11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pino_rele, GPIO.OUT)

configurar_pwm(0)  # Desliga o PWM inicialmente

def obter_hora_atual():
    return datetime.now().strftime("\nDia: %d-%m-%Y \nHora: %H:%M:%S")

def processo_peso(racao):
    ultimo_peso = 0
    tempo_ultimo_peso = time.time()

    while True:
        peso = calculo_peso(tara1, read_count(BALANCAS[1]['DT'], BALANCAS[1]['SCK']), BALANCAS[1]['fator'])
        print(f'\nPeso atual: {peso:.2f}')
        time.sleep(0.5)

        # Verifica se o peso ficou travado por mais de 30 segundos
        if abs(peso - ultimo_peso) < 1:  # Variação pequena considerada como travamento
            if time.time() - tempo_ultimo_peso > 30:
                print('Travamento detectado! Tentando destravar o motor...')
                destravar_motor()
                tempo_ultimo_peso = time.time()
        else:
            ultimo_peso = peso
            tempo_ultimo_peso = time.time()

        if peso >= racao:
            print('Peso atingido')
            configurar_pwm(0)
            ativar_rele()
            break
        elif peso > (racao * 0.5):
            print('Tá quase')
            configurar_pwm(100)
        elif peso < (racao * 0.1):
            configurar_pwm(255)


def identificacao():
    try:
        print("Aguardando... CTRL+C para parar o programa")
        nome_animal = obter_tag()
        percentual = definir_percentual(nome_animal)
        if percentual is None:
            print("Animal não registrado!")
            return

        hora = obter_hora_atual()
        print(f"Data e hora atual: {hora}")

        for _ in range(10):
            peso_animal = calculo_peso(tara2, read_count(BALANCAS[2]['DT'], BALANCAS[2]['SCK']), BALANCAS[2]['fator'])
            racao = peso_animal * percentual
            print(f"Peso {nome_animal}: {peso_animal}")
            time.sleep(1)

        print(f"\nPeso da ração definido em: {racao:.2f} g")
        time.sleep(3)

        processo_peso(racao)

    except Exception as e:
        print(f"Erro: {e}")

def main():
    try:
        print("\nCalibrando Balança 1...")
        global tara1
        tara1 = calibracao(BALANCAS[1]['DT'], BALANCAS[1]['SCK'])

        print("\nCalibrando Balança 2...")
        global tara2
        tara2 = calibracao(BALANCAS[2]['DT'], BALANCAS[2]['SCK'])

        while True:
            identificacao()
            print("Aguardando movimento para iniciar identificação...")
            detectar_movimento()

    except KeyboardInterrupt:
        print("\nEncerrando...")
        GPIO.cleanup()
        configurar_pwm(0)
        pi.stop()


if __name__ == "__main__":
    main()
