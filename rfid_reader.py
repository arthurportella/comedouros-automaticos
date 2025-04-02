'''
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Aproxime a Tag")
    id,text = reader.read()
    print(id)
    print(text)
finally:
    GPIO.cleanup()
'''

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

try:
    print("Aguardando...CTRL+C para o programa")
    while True:
        print("\n\nAproxime a tag")
        id, text = reader.read()
        print(f"ID da Tag: {id}")
        print(f"Conteúdo da Tag: {text}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Encerrado!")

finally:
    GPIO.cleanup()
        
        
