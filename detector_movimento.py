import cv2
import numpy as np
import subprocess
import time
import os

def capturar_imagem(nome_arquivo):
    subprocess.run([
        "libcamera-still",
        "-o", nome_arquivo,
        "--width", "640",
        "--height", "480",
        "--timeout", "1",
        "--nopreview"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def calcular_diferenca(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        return 0

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    movimento = np.sum(thresh) / 255
    return movimento

def detectar_movimento(threshold=10000):
    print("Iniciando detecção de movimento...")

    anterior = "frame1.jpg"
    atual = "frame2.jpg"

    try:
        capturar_imagem(anterior)
        time.sleep(1)

        while True:
            capturar_imagem(atual)

            movimento = calcular_diferenca(anterior, atual)
            print(f"Pixels em movimento: {movimento:.0f}")

            if movimento > threshold:
                print("⚠️ Movimento detectado! (Possível cabeça levantando)")
                return True

            os.rename(atual, anterior)
            time.sleep(2)

    finally:
        # Remove os arquivos, mesmo em caso de erro
        for arquivo in [anterior, atual]:
            if os.path.exists(arquivo):
                os.remove(arquivo)

    return False

if __name__ == "__main__":
    movimento_detectado = detectar_movimento()
    if movimento_detectado:
        print(">> Movimento detectado com sucesso.")
    else:
        print(">> Nenhum movimento detectado.")
