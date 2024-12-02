import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

sns.set_theme(style="whitegrid")

file_path = "io.xlsx"
data = pd.read_excel(file_path)

data_filtered = data[data['ANO'] != 'TOTAL'].copy()
data_filtered['ANO'] = pd.to_numeric(data_filtered['ANO'], errors='coerce')
data_filtered.loc[data_filtered['INGRESSANTES'] == 0, 'INGRESSANTES'] = pd.NA
data_filtered.dropna(subset=['INGRESSANTES', 'FORMADOS'], inplace=True)
data_filtered['TAXA_CONCLUSAO'] = data_filtered['FORMADOS'] / data_filtered['INGRESSANTES']
data_filtered['TAXA_CONCLUSAO'] = data_filtered['TAXA_CONCLUSAO'].clip(upper=1)

valid_courses = data_filtered['COD_CURSO'].value_counts()
valid_courses = valid_courses[valid_courses >= 5].index
data_filtered = data_filtered[data_filtered['COD_CURSO'].isin(valid_courses)]

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

taxa_area_ano = data_filtered.groupby(['ANO', 'AREA_CONHECIMENTO'])['TAXA_CONCLUSAO'].mean().reset_index()
anos_existentes = taxa_area_ano['ANO'].unique()

anos_para_prever = [2013, 2024] #podem ser adicionados outros anos também
regressao_resultados = []

for area in taxa_area_ano['AREA_CONHECIMENTO'].unique():
    subset = taxa_area_ano[taxa_area_ano['AREA_CONHECIMENTO'] == area]
    X = subset[['ANO']].values
    y = subset['TAXA_CONCLUSAO'].values
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    previsoes = modelo.predict(np.array(anos_para_prever).reshape(-1, 1))
    for ano, previsao in zip(anos_para_prever, previsoes):
        regressao_resultados.append({'ANO': ano, 'AREA_CONHECIMENTO': area, 'TAXA_CONCLUSAO': previsao})

previsoes_df = pd.DataFrame(regressao_resultados)
taxa_area_ano = pd.concat([taxa_area_ano, previsoes_df]).sort_values(by='ANO')

plt.figure(figsize=(12, 6))
for area in taxa_area_ano['AREA_CONHECIMENTO'].unique():
    subset = taxa_area_ano[taxa_area_ano['AREA_CONHECIMENTO'] == area]
    plt.plot(subset['ANO'], subset['TAXA_CONCLUSAO'], marker='o', label=area)

plt.title('Taxa de Conclusão por Área do Conhecimento ao Longo dos Anos (Com Previsão)')
plt.xlabel('Ano')
plt.ylabel('Taxa de Conclusão Média')
plt.legend(title='Área do Conhecimento')
plt.grid(True)
plt.tight_layout()
plt.show()