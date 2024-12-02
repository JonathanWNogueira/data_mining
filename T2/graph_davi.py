import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Pré-processamento
def pre_processing():
    file_path = r"C:\Users\augus\Documents\Faculdade\6º semestre\Mineração de Dados\data_mining\T2\io.xlsx"
    file_path2 = r"C:\Users\augus\Documents\Faculdade\6º semestre\Mineração de Dados\data_mining\T2\diciplinas.xlsx"

    dados_cursos = pd.read_excel(file_path)
    dados_disciplinas = pd.read_excel(file_path2)

    dados_disciplinas.drop('Arquivo_Origem', axis=1, inplace=True)
    dados_disciplinas['Semestre'] = dados_disciplinas['Semestre'].str.split('.').str[0].astype(int)

    # Renomear colunas para facilitar o trabalho, deixando no mesmo formato
    dados_cursos.rename(columns={'COD_CURSO': 'Cod_Curso'}, inplace=True)
    dados_disciplinas.rename(columns={'Cód..Curso': 'Cod_Curso'}, inplace=True)
    
    # "ano" no arquivo de disciplinas era tratado como int64 e no arquivo de cursos como object
    dados_cursos['ANO'] = pd.to_numeric(dados_cursos['ANO'], errors='coerce')
    dados_disciplinas['Ano'] = pd.to_numeric(dados_disciplinas['Ano'], errors='coerce')

    # "cod_curso" no arquivo de disciplinas era tratado como int64 e no arquivo de cursos como object
    dados_cursos['Cod_Curso'] = dados_cursos['Cod_Curso'].str.split('.').str[0].astype(int)
    dados_disciplinas['Cod_Curso'] = dados_disciplinas['Cod_Curso'].astype(int)

    # Adicionar a coluna 'Semestre' de dados_disciplinas ao dados_cursos
    dados_cursos = pd.merge(dados_cursos, dados_disciplinas[['Cod_Curso', 'Semestre']], on='Cod_Curso', how='left')

    # Printar os tipos de dados após as modificações
    print(dados_cursos.dtypes)
    print(dados_disciplinas.dtypes)

    return dados_cursos, dados_disciplinas





def evolucao_taxa_aprovacao(dados_disciplinas):
    """
    Função que gera um gráfico temporal da evolução da taxa de aprovação a cada semestre.
    """
    # Filtrar os dados para alunos aprovados
    aprovados = dados_disciplinas[dados_disciplinas['Situação'] == 'Aprovado']
    
    # Agrupar para obter o número total de alunos e alunos aprovados por semestre
    total_alunos = dados_disciplinas.groupby(['Ano', 'Semestre'])['Alunos'].sum()
    aprovados_por_semestre = aprovados.groupby(['Ano', 'Semestre'])['Alunos'].sum()

    # Calculando a taxa de aprovação
    taxa_aprovacao = (aprovados_por_semestre / total_alunos * 100).reset_index(name='Taxa')
    
    # Criar uma coluna combinando Ano e Semestre
    taxa_aprovacao['Ano-Semestre'] = taxa_aprovacao['Ano'].astype(str) + ' - ' + taxa_aprovacao['Semestre'].astype(str)

    # Visualizar o DataFrame para verificar os dados
    print(taxa_aprovacao.head())

    # Plotar gráfico de linha
    plt.figure(figsize=(12, 8))
    plt.plot(taxa_aprovacao['Ano-Semestre'], taxa_aprovacao['Taxa'], label="Taxa de Aprovação", marker='o')

    # Adicionar título e rótulos
    plt.title('Evolução da Taxa de Aprovação por Semestre')
    plt.xlabel('Ano e Semestre')
    plt.ylabel('Taxa de Aprovação (%)')
    plt.xticks(rotation=90)
    plt.legend(title='Legenda')

    # Exibir o gráfico
    plt.show()




   



def evolucao_taxa_ingressantes(dados_cursos):
    """
    Função que gera um gráfico temporal da evolução da taxa de ingressantes por semestre.
    A taxa de ingressantes é calculada como a razão entre o número de ingressantes e o total de alunos (ingressantes + formados).
    """
    # Agrupar dados de ingressantes por semestre e ano
    ingressantes_por_semestre = dados_cursos.groupby(['ANO', 'Semestre'])['INGRESSANTES'].sum()
    total_alunos_por_semestre = dados_cursos.groupby(['ANO', 'Semestre'])['INGRESSANTES'].sum() + dados_cursos.groupby(['ANO', 'Semestre'])['FORMADOS'].sum()

    # Calculando a taxa de ingressantes
    taxa_ingressantes = (ingressantes_por_semestre / total_alunos_por_semestre).fillna(0) * 100  # Taxa em percentual

    # Resetar o índice para facilitar o gráfico
    taxa_ingressantes = taxa_ingressantes.reset_index()

    # Plotar gráfico de linha
    plt.figure(figsize=(12, 8))
    plt.plot(taxa_ingressantes['ANO'].astype(str) + ' - ' + taxa_ingressantes['Semestre'].astype(str), taxa_ingressantes[0], label="Taxa de Ingressantes")

    # Adicionar título e rótulos
    plt.title('Evolução da Taxa de Ingressantes por Semestre')
    plt.xlabel('Ano e Semestre')
    plt.ylabel('Taxa de Ingressantes (%)')
    plt.xticks(rotation=90)
    plt.legend(title='Ano-Semestre')
    
    # Exibir o gráfico
    plt.show()




def evolucao_formados(dados_cursos):
    """
    Gera um gráfico único mostrando o total de formados consolidado por semestre.
    """
    formados_por_semestre = dados_cursos.groupby(['ANO', 'Semestre'])['FORMADOS'].sum().reset_index()
    formados_por_semestre['Ano-Semestre'] = formados_por_semestre['ANO'].astype(str) + ' - ' + formados_por_semestre['Semestre'].astype(str)

    plt.figure(figsize=(12, 8))
    plt.plot(formados_por_semestre['Ano-Semestre'], formados_por_semestre['FORMADOS'], label="Formados", marker='o')
    plt.title('Evolução do Número de Formados')
    plt.xlabel('Ano e Semestre')
    plt.ylabel('Número de Formados')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()




def evolucao_taxa_ingressantes(dados_cursos):
    """
    Gera um gráfico único mostrando a taxa de ingressantes consolidada por semestre.
    """
    ingressantes = dados_cursos.groupby(['ANO', 'Semestre'])['INGRESSANTES'].sum()
    total_alunos = dados_cursos.groupby(['ANO', 'Semestre'])['INGRESSANTES'].sum() + dados_cursos.groupby(['ANO', 'Semestre'])['FORMADOS'].sum()

    taxa_ingressantes = (ingressantes / total_alunos * 100).reset_index(name='Taxa')
    taxa_ingressantes['Ano-Semestre'] = taxa_ingressantes['ANO'].astype(str) + ' - ' + taxa_ingressantes['Semestre'].astype(str)

    plt.figure(figsize=(12, 8))
    plt.plot(taxa_ingressantes['Ano-Semestre'], taxa_ingressantes['Taxa'], label="Taxa de Ingressantes", marker='o')
    plt.title('Evolução da Taxa de Ingressantes')
    plt.xlabel('Ano e Semestre')
    plt.ylabel('Taxa de Ingressantes (%)')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()

def evolucao_taxa_formados(dados_cursos):
    """
    Gera um gráfico único mostrando a taxa de formados consolidada por semestre.
    """
    formados = dados_cursos.groupby(['ANO', 'Semestre'])['FORMADOS'].sum()
    total_alunos = dados_cursos.groupby(['ANO', 'Semestre'])['INGRESSANTES'].sum() + dados_cursos.groupby(['ANO', 'Semestre'])['FORMADOS'].sum()

    taxa_formados = (formados / total_alunos * 100).reset_index(name='Taxa')
    taxa_formados['Ano-Semestre'] = taxa_formados['ANO'].astype(str) + ' - ' + taxa_formados['Semestre'].astype(str)

    plt.figure(figsize=(12, 8))
    plt.plot(taxa_formados['Ano-Semestre'], taxa_formados['Taxa'], label="Taxa de Formados", marker='o')
    plt.title('Evolução da Taxa de Formados')
    plt.xlabel('Ano e Semestre')
    plt.ylabel('Taxa de Formados (%)')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


def evolucao_ingressantes(dados_cursos):
    """
    Gera um gráfico único mostrando o total de ingressantes consolidado por semestre.
    """
    ingressantes_por_semestre = dados_cursos.groupby(['ANO', 'Semestre'])['INGRESSANTES'].sum().reset_index()
    ingressantes_por_semestre['Ano-Semestre'] = ingressantes_por_semestre['ANO'].astype(str) + ' - ' + ingressantes_por_semestre['Semestre'].astype(str)

    plt.figure(figsize=(12, 8))
    plt.plot(ingressantes_por_semestre['Ano-Semestre'], ingressantes_por_semestre['INGRESSANTES'], label="Ingressantes", marker='o')
    plt.title('Evolução do Número de Ingressantes')
    plt.xlabel('Ano e Semestre')
    plt.ylabel('Número de Ingressantes')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()



def main():
    # Pré-processamento dos dados
    dados_cursos, dados_disciplinas = pre_processing()

    evolucao_taxa_aprovacao(dados_disciplinas)
    evolucao_formados(dados_cursos)
    evolucao_ingressantes(dados_cursos)
    evolucao_taxa_formados(dados_cursos)
    evolucao_taxa_ingressantes(dados_cursos)


if __name__ == '__main__':
    main()