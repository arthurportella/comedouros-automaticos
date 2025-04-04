from setup import inicializar_sistema
from balanca import setup_balanca, calibracao, calculo_peso, read_count
from motor import configurar_pwm, ativar_rele
import RPi.GPIO as GPIO
import time
import pigpio

# Inicializa o sistema, realiza a identificação do animal e controla o processo de pesagem e alimentação.

# Inicializa o pigpio, se necessário
pi = pigpio.pi()
if not pi.connected:
    print("Erro: pigpio não está conectado.")
    exit()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def processo_peso(tara1, racao):
    while True:
        peso = calculo_peso(tara1, read_count(BALANCAS[1]['DT'], BALANCAS[1]['SCK']), BALANCAS[1]['fator'])
        print(f'\nPeso atual: {peso:.2f}')
        time.sleep(0.5)

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


def identificacao(tara2):
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

        processo_peso(tara1, racao)

    except Exception as e:
        print(f"Erro: {e}")


def main():
    try:
        pi, BALANCAS = inicializar_sistema()

        print("\nCalibrando Balança 1...")
        global tara1
        tara1 = calibracao(BALANCAS[1]['DT'], BALANCAS[1]['SCK'])

        print("\nCalibrando Balança 2...")
        global tara2
        tara2 = calibracao(BALANCAS[2]['DT'], BALANCAS[2]['SCK'])

        while True:
            identificacao(tara2)

    except KeyboardInterrupt:
        print("\nEncerrando...")
        GPIO.cleanup()
        configurar_pwm(0)
        pi.stop()


if __name__ == "__main__":
    main()
