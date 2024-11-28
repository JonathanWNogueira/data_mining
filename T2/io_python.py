import os
import pandas as pd
from unidecode import unidecode

path = "C:/Users/augus/Documents/Faculdade/6º semestre/Mineração de Dados/Trabalho 2/datasets/IO/"

arquivos = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith('.xlsx')]

print("Arquivos encontrados:", arquivos)

dados_combinados = pd.DataFrame()

for arquivo in arquivos:
    dados = pd.read_excel(arquivo)
    
    print(f"\nLendo arquivo: {arquivo}")
    print(dados.head()) 
    
    dados['Arquivo_Origem'] = os.path.basename(arquivo)
    
    dados = dados.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)
    
    dados_combinados = pd.concat([dados_combinados, dados], ignore_index=True)

print("\n### Dados combinados (visualização inicial): ###")
print(dados_combinados.head())

output_arquivo = "C:/Users/augus/Documents/Faculdade/6º semestre/Mineração de Dados/Trabalho 2/datasets/IO/IO_Formatado.xlsx"
dados_combinados.to_excel(output_arquivo, index=False)
print(f"\nArquivo salvo como: {output_arquivo}")