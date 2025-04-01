#Adicionando dados a um arquivo CSV
import pandas as pd

#Novos dados a serem adicionados
novos_dados = {
    "Data": ["2024-09-14", "2024-09-15"],
    "Hora": ["11:30:00", "11:45:00"],
    "Valor1": [200, 250],
    "Valor2": [400, 450]
    }
df_novos = pd.DataFrame(novos_dados)

#Caminho do arquivo CSV existente
arquivo_csv = "dados.csv"

#Lendo os dados antigos
df_existente = pd.read_csv(arquivo_csv)

#Concatenando os novos dados aos existentes
df_final = pd.concat([df_existente, df_novos], ignore_index=True)

#Salvandos no CSV (sobreescrevendo o arquivo original)
df_final.to_csv(arquivo_csv, index=False)

print(f"Novos dados adicionados ao arquivo {arquivo_csv} com sucesso!")
