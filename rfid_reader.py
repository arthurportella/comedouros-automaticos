from mfrc522 import SimpleMFRC522

# Realiza a leitura da tag RFID para identificar o animal e define o percentual de ração conforme o tipo.

reader = SimpleMFRC522()

def obter_tag():
    print("\n\nAproxime a tag")
    id, text = reader.read()
    nome_animal = text.strip().lower()
    print(f"ID da Tag: {id}")
    print(f"Nome do Animal (Tag): {nome_animal}")
    return nome_animal

def definir_percentual(nome_animal):
    return 0.01 if nome_animal == "bovino" else 0.02 if nome_animal == "ovino" else None
