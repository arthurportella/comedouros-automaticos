import RPi.GPIO as GPIO
import time

# Balança 1
DT1 = 33
SCK1 = 35

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DT1, GPIO.IN)
GPIO.setup(SCK1, GPIO.OUT)

def read_count():
    count = 0
    while GPIO.input(DT1):
        pass
    for _ in range(24):
        GPIO.output(SCK1, True)
        count = count << 1
        GPIO.output(SCK1, False)
        if GPIO.input(DT1):
            count += 1
    GPIO.output(SCK1, True)
    count = count ^ 0x800000
    GPIO.output(SCK1, False)
    return count

try:
    print("Iniciando leitura da balança...")
    while True:
        valor = read_count()
        print(f"Leitura da balança: {valor}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Programa encerrado!")
finally:
    GPIO.cleanup()
