import RPi.GPIO as GPIO
import numpy as np
import time

GPIO.setmode(GPIO.BOARD)  # Ou GPIO.BCM, conforme sua configuração
GPIO.setwarnings(False)

# Constantes e pinos das balanças
BALANCAS = {
    1: {'DT': 29, 'SCK': 31, 'fator': 0.02908},
    2: {'DT': 33, 'SCK': 35, 'fator': 0.03415}
}

def setup_balanca(dt, sck):
    GPIO.setup(dt, GPIO.IN)
    GPIO.setup(sck, GPIO.OUT)

for balanca in BALANCAS.values():
    setup_balanca(balanca['DT'], balanca['SCK'])

def read_count(dt, sck):
    count = 0
    while GPIO.input(dt):
        pass
    for _ in range(24):
        GPIO.output(sck, True)
        count = count << 1
        GPIO.output(sck, False)
        if GPIO.input(dt):
            count += 1
    GPIO.output(sck, True)
    count = count ^ 0x800000
    GPIO.output(sck, False)
    return count

def calculo_peso(tara, leitura, fator):
    return (tara - leitura) * fator

def calibracao(dt, sck):
    leituras = [read_count(dt, sck) for _ in range(20)]
    mediana = np.median(leituras)
    desvio = np.std(leituras)
    leituras_filtradas = [v for v in leituras if abs(v - mediana) <= desvio]
    media_tara = sum(leituras_filtradas) / len(leituras_filtradas) if leituras_filtradas else mediana
    print(f'Média final (após filtragem): {media_tara}')
    return media_tara
