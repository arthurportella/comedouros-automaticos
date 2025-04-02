# motor.py
import RPi.GPIO as GPIO
import pigpio
import time

pino_pwm = 18
pino_rele = 11


def configurar_pwm(duty_cycle):
    pi = pigpio.pi()
    pi.set_PWM_dutycycle(pino_pwm, duty_cycle)


def ativar_rele():
    GPIO.output(pino_rele, GPIO.HIGH)
    print("\nMotor ativado, liberando ração!")
    time.sleep(10)
    GPIO.output(pino_rele, GPIO.LOW)
    print("\nMotor desligado")
