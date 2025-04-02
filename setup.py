# setup.py
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import pigpio

# Inicialização
def inicializar_sistema():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    pi = pigpio.pi()
    if not pi.connected:
        exit()

    pino_pwm = 18
    frequencia_pwm = 15000
    pi.set_PWM_frequency(pino_pwm, frequencia_pwm)

    BALANCAS = {
        1: {'DT': 29, 'SCK': 31, 'fator': 0.02908},
        2: {'DT': 33, 'SCK': 35, 'fator': 0.03415}
    }

    reader = SimpleMFRC522()
    return pi, BALANCAS
