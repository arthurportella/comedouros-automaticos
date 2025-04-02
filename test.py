import time
from balanca import calibracao, calculo_peso, read_count, BALANCAS

def testar_balanca_1():
    print("Calibrando Balança 1...")
    try:
        # Calibração da balança 1
        tara1 = calibracao(BALANCAS[1]['DT'], BALANCAS[1]['SCK'])
        print(f"Tara inicial: {tara1}")

        while True:
            # Leitura do peso
            peso = calculo_peso(tara1, read_count(BALANCAS[1]['DT'], BALANCAS[1]['SCK']), BALANCAS[1]['fator'])
            print(f"Peso atual: {peso:.2f} g")
            time.sleep(1)  # Intervalo entre as leituras

    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário.")

if __name__ == "__main__":
    testar_balanca_1()
