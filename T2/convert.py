import os
import pandas as pd

from unidecode import unidecode

def converter_xls_para_xlsx(caminho_xls, caminho_xlsx):
    try:
        dados = pd.read_excel(caminho_xls, engine='xlrd')
        dados = dados.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)        
        dados.to_excel(caminho_xlsx, index=False, engine='openpyxl')
        
        print(f"Arquivo convertido com sucesso: {caminho_xlsx}")
    except Exception as e:
        print(f"Erro ao converter o arquivo {caminho_xls}: {e}")

diretorio = "datasets/IO/"

arquivos_xls = [f for f in os.listdir(diretorio) if f.endswith('.xls')]

for arquivo in arquivos_xls:
    caminho_xls = os.path.join(diretorio, arquivo)
    caminho_xlsx = caminho_xls.replace('.xls', '.xlsx')
    
    converter_xls_para_xlsx(caminho_xls, caminho_xlsx)
