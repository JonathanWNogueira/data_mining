import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Configurações gerais
sns.set_theme(style="whitegrid")

# Carregar o dataset
file_path = "io.xlsx"  # Substitua pelo caminho correto
data = pd.read_excel(file_path)

# **Pré-processamento**
# Remover linhas com "TOTAL" na coluna 'ANO'
data_filtered = data[data['ANO'] != 'TOTAL'].copy()

# Converter a coluna 'ANO' para numérico
data_filtered['ANO'] = pd.to_numeric(data_filtered['ANO'], errors='coerce')

# Substituir ingressantes zero por NaN
data_filtered.loc[data_filtered['INGRESSANTES'] == 0, 'INGRESSANTES'] = pd.NA

# Remover linhas onde ingressantes ou formados estão ausentes
data_filtered.dropna(subset=['INGRESSANTES', 'FORMADOS'], inplace=True)

# Calcular a taxa de conclusão
data_filtered['TAXA_CONCLUSAO'] = data_filtered['FORMADOS'] / data_filtered['INGRESSANTES']

# Limitar a taxa de conclusão a 1 (para evitar valores incoerentes)
data_filtered['TAXA_CONCLUSAO'] = data_filtered['TAXA_CONCLUSAO'].clip(upper=1)

# Filtrar cursos com pelo menos 5 registros ao longo dos anos
valid_courses = data_filtered['COD_CURSO'].value_counts()
valid_courses = valid_courses[valid_courses >= 5].index  # Cursos com pelo menos 5 registros
data_filtered = data_filtered[data_filtered['COD_CURSO'].isin(valid_courses)]

# **Adicionar a coluna de ÁREA DO CONHECIMENTO**
if 'AREA_CONHECIMENTO' not in data_filtered.columns:
    data_filtered['AREA_CONHECIMENTO'] = data_filtered['NOME_UNIDADE'].apply(
        lambda x: 'Ciências Exatas' if any(term in x for term in ['Engenharia', 'Computação', 'Matemática', 'Física', 'Química', 'Tecnologia']) else
                  'Ciências Humanas' if any(term in x for term in ['Pedagogia', 'Direito', 'Psicologia', 'Sociologia', 'História', 'Filosofia', 'Educação']) else
                  'Ciências Biológicas' if any(term in x for term in ['Biologia', 'Medicina', 'Enfermagem', 'Veterinária', 'Odontologia', 'Farmácia', 'Nutrição']) else
                  'Ciências Sociais Aplicadas' if any(term in x for term in ['Administração', 'Economia', 'Contabilidade', 'Gestão']) else
                  'Artes e Design' if any(term in x for term in ['Artes', 'Design', 'Música', 'Cenografia', 'Teatro']) else
                  'Comunicação e Linguagem' if any(term in x for term in ['Comunicação', 'Jornalismo', 'Publicidade', 'Letras', 'Tradução']) else
                  'Outros'
    )









# Calcular métricas médias por área de conhecimento
metricas_area = data_filtered.groupby('AREA_CONHECIMENTO').agg({
    'TAXA_CONCLUSAO': 'mean',
    'INGRESSANTES': 'sum'
}).reset_index()

# Normalizar os dados para K-Means
scaler = StandardScaler()
metricas_normalizadas = scaler.fit_transform(metricas_area[['TAXA_CONCLUSAO', 'INGRESSANTES']])

# Aplicar K-Means com 3 clusters (ajustável)
kmeans = KMeans(n_clusters=3, random_state=42)
metricas_area['Cluster'] = kmeans.fit_predict(metricas_normalizadas)

# Visualizar os clusters
print("\nClusters das Áreas de Conhecimento:")
print(metricas_area)

# **Gráfico: Clusters das Áreas de Conhecimento**
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=metricas_area,
    x='TAXA_CONCLUSAO',
    y='INGRESSANTES',
    hue='Cluster',
    palette='viridis',
    s=100
)


# Personalizar a legenda com os rótulos de cada cluster
cluster_labels = {
    0: 'Cluster 0: Outros',
    1: 'Cluster 1: Ciências Biológicas',
    2: 'Cluster 2: Ciências Exatas, Humanas e Sociais'
}

# Adicionar a legenda com as descrições personalizadas
handles, labels = plt.gca().get_legend_handles_labels()
labels = [cluster_labels.get(int(label), label) for label in labels]
plt.legend(handles, labels, title='Cluster', loc='upper right')  # Ajustando a posição se necessário

plt.title('Clusters das Áreas de Conhecimento')
plt.xlabel('Taxa de Conclusão Média')
plt.ylabel('Número Total de Ingressantes')
plt.grid(True)
plt.show()


# **Análise: Taxa de Gênero por Área do Conhecimento**
taxa_genero_area = data_filtered.groupby(['AREA_CONHECIMENTO', 'SEXO'])['TAXA_CONCLUSAO'].mean().reset_index()

# Visualizar os resultados
print("\nTaxa média de conclusão por gênero e área do conhecimento:")
print(taxa_genero_area)

# **Gráfico: Taxa de Conclusão por Gênero e Área do Conhecimento**
plt.figure(figsize=(12, 8))
sns.barplot(
    data=taxa_genero_area,
    x='AREA_CONHECIMENTO',
    y='TAXA_CONCLUSAO',
    hue='SEXO',
    palette='pastel'
)
plt.title('Taxa de Conclusão por Gênero e Área do Conhecimento')
plt.ylabel('Taxa de Conclusão')
plt.xlabel('Área do Conhecimento')
plt.legend(title='Gênero', loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# **Análise: Proporção de Gênero por Área do Conhecimento**
proporcao_genero_area = data_filtered.groupby(['AREA_CONHECIMENTO', 'SEXO'])['INGRESSANTES'].sum().reset_index()

# Calcular a proporção de ingressantes
proporcao_genero_area['PROPORCAO'] = proporcao_genero_area.groupby('AREA_CONHECIMENTO')['INGRESSANTES'].transform(
    lambda x: x / x.sum()
)

# Visualizar os resultados
print("\nProporção de ingressantes por gênero e área do conhecimento:")
print(proporcao_genero_area)


# **Gráfico: Proporção de Ingressantes por Gênero e Área do Conhecimento**
plt.figure(figsize=(12, 8))
sns.barplot(
    data=proporcao_genero_area,
    x='AREA_CONHECIMENTO',
    y='PROPORCAO',
    hue='SEXO',
    palette='pastel'
)
plt.title('Proporção de Ingressantes por Gênero e Área do Conhecimento')
plt.ylabel('Proporção de Ingressantes')
plt.xlabel('Área do Conhecimento')
plt.legend(title='Gênero', loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


taxa_area_ano = data_filtered.groupby(['ANO', 'AREA_CONHECIMENTO'])['TAXA_CONCLUSAO'].mean().reset_index()

plt.figure(figsize=(12, 6))
for area in taxa_area_ano['AREA_CONHECIMENTO'].unique():
    subset = taxa_area_ano[taxa_area_ano['AREA_CONHECIMENTO'] == area]
    plt.plot(subset['ANO'], subset['TAXA_CONCLUSAO'], label=area)

plt.title('Taxa de Conclusão por Área do Conhecimento ao Longo dos Anos')
plt.xlabel('Ano')
plt.ylabel('Taxa de Conclusão Média')
plt.legend(title='Área do Conhecimento')
plt.grid(True)
plt.show()



top_taxa_genero = data_filtered.groupby(['NOME_UNIDADE', 'SEXO'])['TAXA_CONCLUSAO'].mean().reset_index()
top_taxa_genero = top_taxa_genero.sort_values('TAXA_CONCLUSAO', ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_taxa_genero['NOME_UNIDADE'] + ' (' + top_taxa_genero['SEXO'] + ')', top_taxa_genero['TAXA_CONCLUSAO'], color='cornflowerblue')
plt.title('Top 10 Cursos com Maior Taxa de Conclusão por Gênero')
plt.xlabel('Taxa de Conclusão Média')
plt.gca().invert_yaxis()
plt.show()




plt.figure(figsize=(8, 6))
plt.scatter(data_filtered['INGRESSANTES'], data_filtered['TAXA_CONCLUSAO'], alpha=0.6, c='teal')
plt.title('Correlação entre Ingressantes e Taxa de Conclusão')
plt.xlabel('Número de Ingressantes')
plt.ylabel('Taxa de Conclusão')
plt.grid(True)
plt.show()
