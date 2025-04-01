 #Ativando motor por relé transistorisado
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pino_rele = 17 #pino fisico 11
GPIO.setup(pino_rele, GPIO.OUT)

#ATIVANDO O RELÉ
GPIO.output(pino_rele, GPIO.HIGH)
print('Entrou')
time.sleep(5)


GPIO.output(pino_rele, GPIO.LOW)
print('Terminou')
GPIO.cleanup()

