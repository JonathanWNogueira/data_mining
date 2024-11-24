import os
import pandas as pd

def converter_xls_para_xlsx(caminho_xls, caminho_xlsx):
    try:
        # Lê o arquivo .xls
        dados = pd.read_excel(caminho_xls, engine='xlrd')
        
        # Salva como .xlsx
        dados.to_excel(caminho_xlsx, index=False, engine='openpyxl')
        
        print(f"Arquivo convertido com sucesso: {caminho_xlsx}")
    except Exception as e:
        print(f"Erro ao converter o arquivo {caminho_xls}: {e}")

# Diretório onde estão os arquivos .xls
diretorio = "datasets/IO/"

# Lista todos os arquivos .xls no diretório
arquivos_xls = [f for f in os.listdir(diretorio) if f.endswith('.xls')]

# Converte cada arquivo .xls para .xlsx
for arquivo in arquivos_xls:
    caminho_xls = os.path.join(diretorio, arquivo)
    caminho_xlsx = caminho_xls.replace('.xls', '.xlsx')
    
    converter_xls_para_xlsx(caminho_xls, caminho_xlsx)
