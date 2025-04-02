import pigpio
import time



pi = pigpio.pi()

if not pi.connected:
    print('Falha ao conectar ao pigpio daemon!')
    exit()

#Com BCM funciona e BOARD não funciona
pin = 18

frequencia = 1000

pi.set_mode(pin, pigpio.OUTPUT)
try:
    while True:
        pi.set_PWM_frequency(pin, frequencia)
        pi.set_PWM_dutycycle(pin, 128)
        print('Chegou aqui')
        time.sleep(3)

except KeyboardInterrupt:
    pi.set_PWM_dutycycle(pin, 0)
    pi.stop()
