

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# código focado em encontrar correlações macro dos cursos

# pré-processamento
def pre_processing():

    dados_cursos = pd.read_excel("io.xlsx")
    dados_disciplinas = pd.read_excel("diciplinas.xlsx")

    # Renomear colunas para facilitar o trabalho, deixando no mesmo formato
    dados_cursos.rename(columns={'COD_CURSO': 'Cod_Curso'}, inplace=True)
    dados_disciplinas.rename(columns={'Cód..Curso': 'Cod_Curso'}, inplace=True)
    
    # "ano" no arquivo de disciplinas era tratado como int64 e no arquivo de cursos como object
    dados_cursos['ANO'] = pd.to_numeric(dados_cursos['ANO'], errors='coerce')
    dados_disciplinas['Ano'] = pd.to_numeric(dados_disciplinas['Ano'], errors='coerce')

    # "cod_curso" no arquivo de disciplinas era tratado como int64 e no arquivo de cursos como object
    dados_cursos['Cod_Curso'] = dados_cursos['Cod_Curso'].astype('Int64')  # Suporta valores ausentes
    dados_disciplinas['Cod_Curso'] = dados_disciplinas['Cod_Curso'].astype('Int64')

    # printar os tipos de dados apoós as modficicações
    print(dados_cursos.dtypes)
    print(dados_disciplinas.dtypes)


    return dados_cursos, dados_disciplinas


def merge(dados_cursos, dados_disciplinas):

    dados_combinados = pd.merge(
    dados_cursos,
    dados_disciplinas,
    on='Cod_Curso',
    how='inner'
    )

    return dados_combinados



def main ():

    dados_cursos, dados_disciplinas = pre_processing()

    dados_gerais = merge(dados_cursos, dados_disciplinas)

    print(dados_gerais.head())    



if __name__ == '__main__':
    main()