import serial
import time
from reader import Reader

PORTA = "/dev/ttyUSB0"
BAUDRATE = 38400

def ajustar_potencia(leitor, potencia_db):
    """Envia comando para ajustar potência de transmissão"""
    valor_hex = hex(potencia_db + 2)[2:].upper().zfill(2)
    comando = f"\nN1,{valor_hex}\r".encode("utf-8")
    leitor.ser.write(comando)
    time.sleep(0.3)
    leitor.ser.reset_input_buffer()  # ⚠ limpa a resposta
    leitor.ser.reset_output_buffer()

def mostrar_menu():
    print("\n=== Ajuste de Potência do Leitor RFID ===")
    print("[1] 5 dB")
    print("[2] 10 dB")
    print("[3] 15 dB")
    print("[4] 20 dB")
    print("[5] 25 dB")
    print("[6] Máxima (27 dB)")
    escolha = input("Escolha a potência desejada (1-6): ")
    opcoes = {
        "1": 5,
        "2": 10,
        "3": 15,
        "4": 20,
        "5": 25,
        "6": 27
    }
    return opcoes.get(escolha.strip(), 27)  # default: máxima

try:
    print(f"🔌 Conectando à {PORTA} a {BAUDRATE} bps...")
    ser = serial.Serial(PORTA, BAUDRATE, timeout=1)
    print("✅ Porta serial aberta.")
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    leitor = Reader(ser)

    potencia = mostrar_menu()
    ajustar_potencia(leitor, potencia)
    print(f"⚡ Potência ajustada para {potencia} dB.\n")

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
