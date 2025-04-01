from datetime import datetime
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import pigpio
import time

reader = SimpleMFRC522()

pi = pigpio.pi()
if not pi.connected:
    exit()

pino_pwm = 18
#configurar PWM no pino com uma frequÊncia de 1k5Hz e 0% de duty
frequencia_pwm = 15000

pi.set_PWM_frequency(pino_pwm, frequencia_pwm)
#pi.set_PWM_dutycycle(pino_pwm, 175) #0 a 255 para variar o PWM 

#Balança 1
DT1 =  29
SCK1 = 31

#Balança 2
DT2 = 33
SCK2 = 35

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DT1, GPIO.IN)
GPIO.setup(SCK1, GPIO.OUT)
GPIO.setup(DT2, GPIO.IN)
GPIO.setup(SCK2, GPIO.OUT)

#Função que configura o driver da balança
def read_count(DT, SCK):
    count = 0
    while GPIO.input(DT):
        pass
    #Le 24 bits de dados
    for _ in range(24):
        #print('entrou')
        GPIO.output(SCK, True)
        count = count << 1
        GPIO.output(SCK, False)
        if GPIO.input(DT):
            count +=1
    #Envia um pulso extra para definir o ganho para a proxima leitura
    GPIO.output(SCK, True)
    count = count ^ 0x800000
    GPIO.output(SCK, False)
    return count


'''
#Função para calcular a média do peso atual em cima da balança
def calculo_peso():
    peso = (media_tara - read_count()) * 0.02925
    return peso
'''

#Calculo do peso
def calculo_peso1():
    leitura = read_count(DT1, SCK1)
    peso1 = (tara1 - leitura) * 0.02925
    return peso1

def calculo_peso2():
    leitura = read_count(DT2, SCK2)
    peso2 = (tara2 - leitura) * 0.03415
    return peso2


#Função que retorna a hora atual do sistema
def obter_hora_atual():
    return datetime.now().strftime("\nDia: %d-%m-%Y \nHora: %H:%M:%S")

#Identificação de TAGS
def identificacao(tags):
    if tags == 1045638617204:
        print('\nBovino 1')
        hora = obter_hora_atual()
        print("\nData e hora atual:", hora,"\n")   
        for _ in range(10):
            peso_animal = calculo_peso2()
            print("Peso Bovino 1: ", peso_animal)
            time.sleep(1)

        racao = 500
        print("\nPeso da ração definido em:" , racao, "g")
        time.sleep(3)
        
        #Criar uma função para rodar após a identificação     
        while True:
            peso = calculo_peso1()
            #peso = (media_tara - read_count()) * 0.02925
            print('\nPeso atual:{: .2f}'.format(peso))
            time.sleep(0.5)

            if peso >= (racao):
                print('Peso atingido')
                pi.set_PWM_dutycycle(pino_pwm, 0)
                time.sleep(2)
                rele()
                time.sleep(2)
                break #Sai do Loop e volta para leitura de TAG
            elif peso > (racao*0.8):
                print('Ta quase')
                pi.set_PWM_dutycycle(pino_pwm, 100)

            if peso < (racao*0.1):
                pi.set_PWM_dutycycle(pino_pwm, 255)
        
    if tags == 445860857856:
        print('\nOvino 1')
        hora = obter_hora_atual()
        print("\nData e hora atual: ", hora)
        for _ in range(10):
            peso_animal = calculo_peso2()
            print("Peso Ovino: ", peso_animal)
            time.sleep(1)

        racao = 300
        print("\nPeso da ração definido em:", racao, "g")
        time.sleep(3)

        #Criar uma função para rodar após a identificação     
        while True:
            peso = calculo_peso1()
            #peso = (media_tara - read_count()) * 0.02925
            print('\nPeso atual:{: .2f}'.format(peso))
            time.sleep(0.5)

            if peso >= (racao):
                print('Peso atingido')
                pi.set_PWM_dutycycle(pino_pwm, 0)
                time.sleep(2)
                rele()
                time.sleep(2)
                break #Sai do Loop e volta para leitura de TAG
            elif peso > (racao*0.8):
                print('Ta quase')
                pi.set_PWM_dutycycle(pino_pwm, 100)

            if peso < (racao*0.1):
                pi.set_PWM_dutycycle(pino_pwm, 255)
            
def rele():
    pino_rele = 11
    GPIO.setup(pino_rele, GPIO.OUT)
    GPIO.output(pino_rele, GPIO.HIGH)
    print("\nPrimeiro motor ativado, liberando ração!")
    time.sleep(10)

    GPIO.output(pino_rele, GPIO.LOW)
    print("\nDesligou")

    return

'''
#identificação de animais utilizando MathCase
def ident_animal(tag_id):
    match tag_id:
        case 1045638617204:
            print("Ovino identificado!")
            print("Data e Hora de entrada: ", obter_hora_atual())
        case _:
            print("Animal não identificado")                

'''
#Calibração da NOVA 
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
   
'''
#Calibração da ANTIGA tara
def calibracao():
    
    x = 0 
    for n in range(8):
        print('Valor atual em gramas: ', read_count())
        x = x + read_count()
                
    media_tara = (x/8)
    print('Media: ', media_tara)
    return media_tara
'''

#Executando as funções e disponibilizando valores
try:
    print("\nCalibrando Balança 1...")
    tara1 = calibracao(DT1, SCK1)

    print("\nCalibrando Balança 2...")
    tara2 = calibracao(DT2,SCK2)

    while True:
        print('\nAproxime a Tag')
        id, text = reader.read()
        identificacao(id)
        
#interrompe com ctrl+c 
except KeyboardInterrupt:
    GPIO.cleanup()
    pi.set_PWM_dutycycle(pino_pwm, 0) #para o PWM
    pi.stop()
