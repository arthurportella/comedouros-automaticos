import RPi.GPIO as GPIO
import pigpio
import time

# Configura o PWM, ativa o motor e realiza o destravamento da hélice, se necessário.

pino_pwm = 18
pino_rele = 11

pi = pigpio.pi()

def configurar_pwm(duty_cycle):
    """Configura o PWM no pino especificado."""
    pi.set_PWM_dutycycle(pino_pwm, duty_cycle)

def ativar_rele():
    """Ativa o motor por 10 segundos."""
    GPIO.output(pino_rele, GPIO.HIGH)
    print("\nMotor ativado, liberando ração!")
    time.sleep(10)
    GPIO.output(pino_rele, GPIO.LOW)
    print("\nMotor desligado")

def destravar_motor():
    """Tenta destravar a hélice invertendo o sentido."""
    print("Tentando destravar a hélice...")
    configurar_pwm(0)  # Para o motor
    time.sleep(1)
    configurar_pwm(100)  # Gira para frente devagar para tentar soltar
    time.sleep(1)
    configurar_pwm(0)  # Para novamente
    time.sleep(1)
    configurar_pwm(255)  # Gira ao contrário para destravar
    time.sleep(2)
    configurar_pwm(0)  # Para novamente
    print("Destravamento realizado")
