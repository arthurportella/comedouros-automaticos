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
    print("📡 Leitor iniciado. Aguardando tags...\n")

    while True:
        tags = leitor.multi_tag_EPC_read()
        if tags:
            for tag in tags:
                raw_data = tag[0]  # lista de inteiros (dados brutos da tag)
                tag_id = ''.join(f'{word:04X}' for word in raw_data)  # Formata como HEX contínuo
                print(f"🆔 Tag ID: {tag_id}")


except KeyboardInterrupt:
    print("\n⛔ Encerrado pelo usuário.")
    ser.close()
except Exception as e:
    print(f"❌ Erro: {e}")
