import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

text = input("Nome: ")
print("Aproxime a Tag")

try:
    reader.write(text)
    print("Salvo") 
finally:
    GPIO.cleanup()
