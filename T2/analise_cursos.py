import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Pré-processamento
def pre_processing():

    dados_cursos = pd.read_excel("io.xlsx")
    dados_disciplinas = pd.read_excel("diciplinas.xlsx")

    dados_disciplinas.drop('Arquivo_Origem', axis=1, inplace=True)

    # Renomear colunas para facilitar o trabalho, deixando no mesmo formato
    dados_cursos.rename(columns={'COD_CURSO': 'Cod_Curso'}, inplace=True)
    dados_disciplinas.rename(columns={'Cód..Curso': 'Cod_Curso'}, inplace=True)
    
    # "ano" no arquivo de disciplinas era tratado como int64 e no arquivo de cursos como object
    dados_cursos['ANO'] = pd.to_numeric(dados_cursos['ANO'], errors='coerce')
    dados_disciplinas['Ano'] = pd.to_numeric(dados_disciplinas['Ano'], errors='coerce')

    # "cod_curso" no arquivo de disciplinas era tratado como int64 e no arquivo de cursos como object
    dados_cursos['Cod_Curso'] = dados_cursos['Cod_Curso'].str.split('.').str[0]
    dados_cursos['Cod_Curso'] = dados_cursos['Cod_Curso'].astype('Int64')  
    dados_disciplinas['Cod_Curso'] = dados_disciplinas['Cod_Curso'].astype('Int64')

    # Printar os tipos de dados após as modificações
    print(dados_cursos.dtypes)
    print(dados_disciplinas.dtypes)

    return dados_cursos, dados_disciplinas




def situation_dist(dados_disciplinas):
    """
    Função que calcula e plota a distribuição de alunos por situação nas disciplinas.
    """
    # Calcular a distribuição de alunos por situação
    distribuicao_situacao = dados_disciplinas.groupby(['Curso', 'Situação'])['Alunos'].sum().unstack()

    # Plotar gráfico de barras
    distribuicao_situacao.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.title('Distribuição de Alunos por Situação')
    plt.xlabel('Curso')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=90)
    plt.show()


def analise_aprovacao(dados_disciplinas):
    """
    Função que analisa a quantidade de reprovação por curso.
    """
    # Filtrar para as situações de reprovação
    reprovados = dados_disciplinas[dados_disciplinas['Situação'] == 'Reprovado']

    # Agrupar por curso e contar o número de alunos reprovados
    reprovacao_por_curso = reprovados.groupby('Curso')['Alunos'].sum()

    # Plotar gráfico de barras
    reprovacao_por_curso.sort_values(ascending=False).head(10).plot(kind='bar', figsize=(12, 8))
    plt.title('Disciplinas com Maior Número de Reprovação')
    plt.xlabel('Curso')
    plt.ylabel('Número de Alunos Reprovados')
    plt.xticks(rotation=90)
    plt.show()


def professores_dist(dados_disciplinas):
    """
    Função que calcula a distribuição de alunos por professor.
    """
    # Agrupar por professor e somar o número de alunos
    distribuicao_professor = dados_disciplinas.groupby('Professor')['Alunos'].sum()

    # Plotar gráfico de barras
    distribuicao_professor.sort_values(ascending=False).head(10).plot(kind='bar', figsize=(12, 8))
    plt.title('Distribuição de Alunos por Professor')
    plt.xlabel('Professor')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=90)
    plt.show()





def main():
    # Pré-processamento dos dados
    dados_cursos, dados_disciplinas = pre_processing()

    # Realizando outras análises
    situation_dist(dados_disciplinas)
    analise_aprovacao(dados_disciplinas)
    professores_dist(dados_disciplinas)


if __name__ == '__main__':
    main()
