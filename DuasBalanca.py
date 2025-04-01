import RPi.GPIO as GPIO
import time

#Balança 1
DT1 = 29
SCK1 = 31
#Balança 2
DT2 = 33
SCK2 = 35

GPIO.setmode(GPIO.BOARD)
GPIO.setup(DT1, GPIO.IN)
GPIO.setup(SCK1, GPIO.OUT)
GPIO.setup(DT2, GPIO.IN)
GPIO.setup(SCK2, GPIO.OUT)

def read_count(DT, SCK):
    count = 0

    while GPIO.input(DT):
        pass
    
    #Le 24bits de dados
    for _ in range(24):
        #print('Entrou')
        GPIO.output(SCK, True)
        count = count << 1
        GPIO.output(SCK, False)
        if GPIO.input(DT):
            count += 1

    #Envia um pulso extra para definir o ganho para a próxima leitura
    GPIO.output(SCK, True)
    count = count ^ 0x800000
    GPIO.output(SCK, False)
    return count

#Calibra a tara
def calibracao(DT, SCK):    
    soma = 0
    for _ in range(8):
        leitura = read_count(DT, SCK)
        print("Leitura: ", leitura)
        soma += leitura
        time.sleep(0.1)
    media_tara = soma/8
    print('\nMedia: ', media_tara)
    return media_tara



#Calculo do peso
def calculo_peso1():
    leitura = read_count(DT1, SCK1)
    peso1 = (leitura - tara1) * 0.02764
    return peso1

def calculo_peso2():
    leitura = read_count(DT2, SCK2)
    peso2 = (tara2 - leitura) * 0.03415
    return peso2


    

try:
    print("\nCalibrando Balança 1...")
    tara1 = calibracao(DT1, SCK1)

    print("\nCalibrando Balança 2...")
    tara2 = calibracao(DT2,SCK2)

    while True:
        peso_balanca_1 = calculo_peso1()
        #peso2 = calculo_peso(DT2, SCK2, tara2)
        print(f'\nPeso balança 1: {peso_balanca_1:.2f} g')
        #print(f'Peso balança 2: {peso1:.2f} g')

        peso_balanca_2 = calculo_peso2()
        print(f'Peso balança 2: {peso_balanca_2:.2f} g')
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
