#Lendo dados em CSV com pandas
import pandas as pd

#caminho do arquivo CSV
arquivo_csv = "dados.csv"

#lendo os arquivos CSV
df = pd.read_csv(arquivo_csv)

#exibindo dados
print(df)
