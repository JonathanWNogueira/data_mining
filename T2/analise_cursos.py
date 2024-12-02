import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


#  Pré-processamento
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


# def analise_aprovacao(dados_disciplinas):
#     """
#     Função que analisa a quantidade de reprovação por curso.
#     """
#     # Filtrar para as situações de reprovação
#     reprovados = dados_disciplinas[dados_disciplinas['Situação'] == 'Reprovado']

#     # Agrupar por curso e contar o número de alunos reprovados
#     reprovacao_por_curso = reprovados.groupby('Curso')['Alunos'].sum()

#     # Plotar gráfico de barras
#     reprovacao_por_curso.sort_values(ascending=False).head(10).plot(kind='bar', figsize=(12, 8))
#     plt.title('Disciplinas com Maior Número de Reprovação')
#     plt.xlabel('Curso')
#     plt.ylabel('Número de Alunos Reprovados')
#     plt.xticks(rotation=90)
#     plt.show()


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












def situation_kmeans(dados_disciplinas, nomes_cursos):
    """
    Função que calcula a distribuição de alunos por situação,
    aplica o K-Means e plota os clusters com visualização aprimorada.
    """
    # Calcular a distribuição de alunos por situação
    distribuicao_situacao = dados_disciplinas.groupby(['Cod_Curso', 'Situação'])['Alunos'].sum().unstack(fill_value=0)
    
    # Normalizar os dados
    scaler = StandardScaler()
    situacoes_normalizadas = scaler.fit_transform(distribuicao_situacao)
    
    situacoes_normalizadas_df = pd.DataFrame(
        situacoes_normalizadas, 
        columns=distribuicao_situacao.columns, 
        index=distribuicao_situacao.index
    )

    # Calcular a taxa baseada na situação "Aprovado"
    situacoes_normalizadas_df["Taxa_Aprovacao"] = situacoes_normalizadas_df["Aprovado"] / situacoes_normalizadas_df.sum(axis=1)

    # Normalizar novamente a variável de interesse
    scaler_taxa = StandardScaler()
    taxa_normalizada = scaler_taxa.fit_transform(situacoes_normalizadas_df[["Taxa_Aprovacao"]])

    # Aplicar k-means para agrupar os cursos
    kmeans = KMeans(n_clusters=6, random_state=19)
    situacoes_normalizadas_df["Cluster"] = kmeans.fit_predict(taxa_normalizada)

    # Ordenar os resultados por taxa de aprovação
    situacoes_normalizadas_df = situacoes_normalizadas_df.sort_values(by="Taxa_Aprovacao", ascending=False)

    # Resetando o índice para garantir um mapeamento adequado
    situacoes_normalizadas_df.reset_index(inplace=True)

    # Mapeando o nome dos cursos (coluna 'nome_unidade') com base no 'Cod_Curso'
    situacoes_normalizadas_df['NOME_UNIDADE'] = situacoes_normalizadas_df['Cod_Curso'].map(nomes_cursos)
    situacoes_normalizadas_df['NOME_UNIDADE'] = situacoes_normalizadas_df['NOME_UNIDADE'].fillna(situacoes_normalizadas_df['Cod_Curso'])

    # Preparar os dados para o gráfico
    x_labels = situacoes_normalizadas_df['NOME_UNIDADE']  # Usar o nome do curso
    x_positions = range(len(situacoes_normalizadas_df))  # Posições numéricas para o eixo X

    # Ajuste para melhorar a legibilidade do gráfico
    plt.figure(figsize=(14, 7))  # Ajuste o tamanho da figura
    scatter = plt.scatter(
        x_positions, 
        situacoes_normalizadas_df["Taxa_Aprovacao"], 
        c=situacoes_normalizadas_df["Cluster"], 
        cmap="viridis",
        s=60,  # Tamanho dos pontos
        edgecolor='k',
        alpha=0.8
    )

    plt.title("Clusters Baseados na Taxa de Aprovação", fontsize=13)
    plt.ylabel("Taxa de Aprovação ", fontsize=12)
    

    # Calcula os índices para exibir apenas metade dos ticks (a cada 2 cursos)
    indices_mostrados = np.arange(0, len(situacoes_normalizadas_df), step=2)

    # Ajustar a exibição dos rótulos do eixo X
    plt.xticks(
        ticks=indices_mostrados,  # Exibe apenas os índices calculados
        labels=situacoes_normalizadas_df['NOME_UNIDADE'].iloc[indices_mostrados],  # Usar os nomes correspondentes aos índices
        rotation=45,
        fontsize=10
    )


    plt.colorbar(scatter, label="Clusters")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Exibir o gráfico
    plt.tight_layout()
    plt.show()

    return distribuicao_situacao








def analise_aprovacao(dados_disciplinas):
    # Filtrar dados de reprovados e aprovados
    reprovados = dados_disciplinas[dados_disciplinas['Situação'] == 'Reprovado']
    aprovados = dados_disciplinas[dados_disciplinas['Situação'] == 'Aprovado']

    # Agrupar por curso e contar o número de alunos reprovados e aprovados
    reprovacao_por_curso = reprovados.groupby('Curso')['Alunos'].sum()
    aprovacao_por_curso = aprovados.groupby('Curso')['Alunos'].sum()

    # Calcular o total de alunos por curso
    total_por_curso = dados_disciplinas.groupby('Curso')['Alunos'].sum()

    # Calcular taxas de aprovação e reprovação
    taxas = pd.DataFrame({
        'Taxa_Aprovacao': aprovacao_por_curso / total_por_curso,
        'Taxa_Reprovacao': reprovacao_por_curso / total_por_curso
    }).fillna(0)  # Substituir NaN por 0

    # Normalizar as taxas
    scaler = StandardScaler()
    taxas_normalizadas = scaler.fit_transform(taxas)

    # Aplicar k-means para agrupar os cursos
    kmeans = KMeans(n_clusters=3, random_state=42)
    taxas['Cluster'] = kmeans.fit_predict(taxas_normalizadas)

    # Exibir as taxas e clusters
    print(taxas)

    # Gráfico: Clusters baseados nas taxas de aprovação e reprovação
    plt.scatter(
        taxas['Taxa_Aprovacao'], 
        taxas['Taxa_Reprovacao'], 
        c=taxas['Cluster'], 
        cmap='viridis'
    )
    plt.title('Clusters Baseados em Taxas de Aprovação e Reprovação')
    plt.xlabel('Taxa de Aprovação')
    plt.ylabel('Taxa de Reprovação')
    plt.show()


def professores_dist_taxa_reprovacao(dados_disciplinas):
    # Filtrar dados de reprovados
    reprovados = dados_disciplinas[dados_disciplinas['Situação'] == 'Reprovado']

    # Agrupar por professor e somar o número de alunos reprovados
    reprovacao_por_professor = reprovados.groupby('Professor')['Alunos'].sum()

    # Calcular o total de alunos por professor
    total_por_professor = dados_disciplinas.groupby('Professor')['Alunos'].sum()

    # Calcular a taxa de reprovação por professor
    taxas_reprovacao_professor = (reprovacao_por_professor / total_por_professor).fillna(0)  # Substituir NaN por 0

    # Normalizar as taxas
    scaler = StandardScaler()
    taxas_normalizadas = scaler.fit_transform(taxas_reprovacao_professor.values.reshape(-1, 1))

    # Aplicar k-means para agrupar os professores
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(taxas_normalizadas)

    # Criar um DataFrame para exibir resultados
    resultados = pd.DataFrame({
        'Taxa_Reprovacao': taxas_reprovacao_professor,
        'Cluster': clusters
    })

    # Exibir os resultados
    print(resultados)

    # Ordenar os resultados por taxa de reprovação
    resultados = resultados.sort_values(by='Taxa_Reprovacao', ascending=False)


    # Gráfico: Distribuição de alunos por professor
    distribuicao_professor = dados_disciplinas.groupby('Professor')['Alunos'].sum()
    distribuicao_professor.sort_values(ascending=False).head(10).plot(kind='barh', figsize=(12, 8))
    plt.title('Distribuição de Alunos por Professor')
    plt.xlabel('Número de Alunos')
    plt.ylabel('Professor')
    plt.xticks(rotation=90)
    plt.show()

    # Gráfico: Clusters baseados na taxa de reprovação por professor
    plt.scatter(
        resultados.index, 
        resultados['Taxa_Reprovacao'], 
        c=resultados['Cluster'], 
        cmap='viridis'
    )

    # Calcula os índices para exibir apenas metade dos ticks
    indices_mostrados = np.arange(0, len(resultados.index), step=2)

    plt.xticks(indices_mostrados, resultados.index[indices_mostrados], rotation=90, fontsize=5)

    plt.title('Clusters Baseados na Taxa de Reprovação por Professor')
    plt.xlabel('Professor')
    plt.ylabel('Taxa de Reprovação')
    plt.xticks(rotation=90)
    plt.show()






def get_nome_cursos(dados_cursos):

    nome_cursos = dados_cursos.set_index('Cod_Curso')['NOME_UNIDADE'].to_dict()
    
    # Converter as chaves do dicionário para int (se necessário)
    nome_cursos = {int(k): v for k, v in nome_cursos.items()}

    # Ordenar o dicionário pelas chaves (Cod_Curso)
    nome_cursos = {k: nome_cursos[k] for k in sorted(nome_cursos)}
    
    return nome_cursos



def main():
    # Pré-processamento dos dados
    dados_cursos, dados_disciplinas = pre_processing()
    nomes_cursos = get_nome_cursos(dados_cursos)


    # Aplicar o K-Means na distribuição de situações

    professores_dist_taxa_reprovacao(dados_disciplinas)
    
    situation_dist(dados_disciplinas)

    situation_kmeans(dados_disciplinas, nomes_cursos)

    analise_aprovacao(dados_disciplinas)



if __name__ == '__main__':
    main()


