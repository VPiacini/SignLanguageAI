import os
import random
import argparse

def apagar_arquivos_aleatorios(pasta, porcentagem):
    # Verifica se a pasta existe
    if not os.path.isdir(pasta):
        print(f"Erro: A pasta '{pasta}' não existe.")
        return

    # Lista apenas arquivos (ignorando subpastas)
    arquivos = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
    total_arquivos = len(arquivos)

    if total_arquivos == 0:
        print("A pasta não contém arquivos.")
        return

    # Calcula quantos arquivos apagar
    num_apagar = int(total_arquivos * (porcentagem / 100.0))
    arquivos_escolhidos = random.sample(arquivos, num_apagar)

    # Apaga os arquivos escolhidos
    for nome_arquivo in arquivos_escolhidos:
        caminho_arquivo = os.path.join(pasta, nome_arquivo)
        os.remove(caminho_arquivo)

    print(f"{num_apagar} arquivo(s) apagado(s) de um total de {total_arquivos} ({porcentagem}%).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apaga aleatoriamente uma porcentagem de arquivos em uma pasta.")
    parser.add_argument("pasta", help="Caminho da pasta")
    parser.add_argument("porcentagem", type=float, help="Porcentagem de arquivos a apagar (ex: 25.0)")

    args = parser.parse_args()
    apagar_arquivos_aleatorios(args.pasta, args.porcentagem)

