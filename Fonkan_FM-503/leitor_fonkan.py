import serial
import time
from reader import Reader

PORTA = "/dev/ttyUSB0"
BAUDRATE = 38400

try:
    print(f"🔌 Conectando à {PORTA} a {BAUDRATE} bps...")
    ser = serial.Serial(PORTA, BAUDRATE, timeout=1)
    print("✅ Porta serial aberta.")

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    leitor = Reader(ser)

    # Envia o comando de potência máxima
    leitor.ser.write(b'\nN1,03\r') # Ajuste de potencia para a antena, em hexadecimal mudar o valor apos a virgula entre as barras
    time.sleep(0.3)
    leitor.ser.reset_input_buffer()  # 💡 Limpa a resposta do comando anterior

    print("📡 Leitor iniciado. Aguardando tags...\n")

    while True:
        tags = leitor.multi_tag_EPC_read()
        if tags:
            for tag in tags:
                raw_data = tag[0]
                tag_id = ''.join(f'{word:04X}' for word in raw_data)
                print(f"🆔 Tag ID: {tag_id}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n⛔ Encerrado pelo usuário.")
    ser.close()
except Exception as e:
    print(f"❌ Erro geral: {e}")
