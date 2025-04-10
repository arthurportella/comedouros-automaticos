import serial
import time
from reader import Reader

PORTA = "/dev/ttyUSB0"
BAUDRATE = 38400

nome = "Portella"
hex_str = nome.encode("utf-8").hex()
words = [int(hex_str[i:i+4].ljust(4, '0'), 16) for i in range(0, len(hex_str), 4)]

print(f"🔠 Convertido '{nome}' para:", words)

try:
    ser = serial.Serial(PORTA, BAUDRATE, timeout=1)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    leitor = Reader(ser)

    # Aguarda até que uma tag seja detectada
    print("Aproxime a tag para gravação...")
    tag_detectada = False
    while not tag_detectada:
        # Aqui usamos, por exemplo, a leitura do TID (você pode adaptar para EPC se preferir)
        tag_data = leitor.read_TID_bank(addr=0, words=6)
        if tag_data:
            tag_detectada = True
            print("Tag detectada!")
        else:
            time.sleep(0.2)  # espera 200ms antes de tentar novamente

    # Tenta gravar os dados agora que a tag está presente
    success = leitor.write_user_memory(0, words)
    if success:
        print("✅ Nome gravado com sucesso na tag!")
    else:
        print("❌ Falha ao gravar na tag.")

except Exception as e:
    print("Erro:", e)
