#Gravando dados em um arquivo CSV com pandas
import pandas as pd

dados = {
    "Data": ["2024-09-12", "2024-09-12"],
    "Hora": ["10:30:00", "10:45:00"],
    "Valor1": [100, 150],
    "Valor2": [200, 250]
}
df = pd.DataFrame(dados)

#Caminho do arquivo CSV
arquivo_csv = "dados.csv"

#Gravando o DataFrame no arquivo CSV
df.to_csv(arquivo_csv, index=False)

print(f"Dados gravados no arquivo {arquivo_csv} com sucesso!")
