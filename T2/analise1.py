import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
file_path = r"C:\Users\augus\Documents\Faculdade\6º semestre\Mineração de Dados\data_mining\T2\io.xlsx"
data = pd.read_excel(file_path)

data_filtered = data[data['ANO'] != 'TOTAL']

# Converter a coluna 'ANO' para numérico
data_filtered['ANO'] = pd.to_numeric(data_filtered['ANO'])

data_filtered['INGRESSANTES'].replace(0, pd.NA, inplace=True)

# Remover linhas onde ingressantes ou formados estão ausentes
data_filtered.dropna(subset=['INGRESSANTES', 'FORMADOS'], inplace=True)

# Calcular a soma total de ingressantes por curso
ingressantes_totais = data_filtered.groupby('COD_CURSO')['INGRESSANTES'].sum()

# Filtrar apenas os cursos com pelo menos 100 ingressantes
cursos_validos = ingressantes_totais[ingressantes_totais >= 100].index
data_filtered = data_filtered[data_filtered['COD_CURSO'].isin(cursos_validos)]

# Calcular a taxa de conclusão (formados/ingressantes)
data_filtered['TAXA_CONCLUSAO'] = data_filtered['FORMADOS'] / data_filtered['INGRESSANTES']

# Analisar a média da taxa de conclusão por curso e gênero
taxa_conclusao = data_filtered.groupby(['COD_CURSO', 'NOME_UNIDADE', 'SEXO'])['TAXA_CONCLUSAO'].mean().reset_index()

# Filtrar os cursos com maior taxa de conclusão
top_cursos = taxa_conclusao.sort_values('TAXA_CONCLUSAO', ascending=False).head(10)

# Filtrar cursos com pelo menos 5 registros ao longo dos anos
valid_courses = data_filtered['COD_CURSO'].value_counts()
valid_courses = valid_courses[valid_courses >= 10].index  # Definir o limite como 5 registros
data_filtered = data_filtered[data_filtered['COD_CURSO'].isin(valid_courses)]

# Analisar a média da taxa de conclusão por curso e gênero
taxa_conclusao = data_filtered.groupby(['COD_CURSO', 'NOME_UNIDADE', 'SEXO'])['TAXA_CONCLUSAO'].mean().reset_index()

numero_cursos = 30

# Filtrar os cursos com maior taxa de conclusão
top_cursos = taxa_conclusao.sort_values('TAXA_CONCLUSAO', ascending=False).head(numero_cursos)

# Exibir os cursos com maior taxa de conclusão
print(f"Top {numero_cursos} Cursos com Maior Taxa de Conclusão:")
print(top_cursos)

# Gráfico dos top 10 cursos
plt.figure(figsize=(14, 12))
plt.yticks(fontsize=8)
plt.barh(top_cursos['NOME_UNIDADE'] + ' (' + top_cursos['SEXO'] + ')', top_cursos['TAXA_CONCLUSAO'], color='skyblue')
plt.xlabel('Taxa de Conclusão')
plt.title(f"Top {numero_cursos} Cursos com Maior Taxa de Conclusão")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Análise 1: Proporção de ingressantes por gênero ao longo dos anos
gender_analysis = data_filtered.groupby(['ANO', 'SEXO'])['INGRESSANTES'].sum().reset_index()

from sklearn.linear_model import LinearRegression
import numpy as np

# Criar o modelo de regressão linear
model = LinearRegression()

# Previsão para cada gênero ('M' e 'F')
future_years = [2013, 2024]  # Anos para prever
predictions = []

for gender in ['M', 'F']:
    # Filtrar os dados para o gênero atual
    subset = gender_analysis[gender_analysis['SEXO'] == gender]
    
    # Treinamento do modelo (X: ANO, y: INGRESSANTES)
    X = subset[['ANO']].values  # Transformar em matriz 2D
    y = subset['INGRESSANTES'].values
    model.fit(X, y)
    
    # Prever para os anos futuros
    future_preds = model.predict(np.array(future_years).reshape(-1, 1))
    predictions.append((gender, future_years, future_preds))

    # Adicionar previsões ao dataframe existente
    predicted_df = pd.DataFrame({
        'ANO': future_years,
        'SEXO': gender,
        'INGRESSANTES': future_preds
    })
    gender_analysis = pd.concat([gender_analysis, predicted_df], ignore_index=True)

# Replotar o gráfico com linhas e pontos
plt.figure(figsize=(10, 6))
for gender in ['M', 'F']:
    subset = gender_analysis[gender_analysis['SEXO'] == gender]
    subset = subset.sort_values(by='ANO')  # Ordenar os dados por ano
    
    # Plotar linha conectando os pontos
    plt.plot(subset['ANO'], subset['INGRESSANTES'], label=f'Gênero {gender}', linestyle='-', marker='o')

# Configurações do gráfico
plt.title('Proporção de Ingressantes por Gênero ao Longo dos Anos (com Previsões)')
plt.xlabel('Ano')
plt.ylabel('Número de Ingressantes')
plt.legend()
plt.grid(True)
plt.show()

# Exibir previsões
for gender, years, preds in predictions:
    print(f"\nPrevisões para Gênero {gender}:")
    for year, pred in zip(years, preds):
        print(f"Ano {year}: {int(pred)} ingressantes (estimado)")

# Verificar registros com taxa de conclusão acima de 1.0
acima_de_um = data_filtered[data_filtered['TAXA_CONCLUSAO'] > 1.0]

print("Registros com Taxa de Conclusão acima de 1.0:")
print(acima_de_um)

# Exibir estatísticas gerais para os registros
print("\nResumo dos Dados Anômalos:")
print(acima_de_um[['COD_CURSO', 'ANO', 'INGRESSANTES', 'FORMADOS']].describe())

# Corrigir registros (se necessário)
# Opcional: Limitar a taxa de conclusão a 1.0 para fins de análise
data_filtered['TAXA_CONCLUSAO'] = data_filtered['TAXA_CONCLUSAO'].clip(upper=1.0)

# Recalcular as médias e exibir novamente o top 10
taxa_conclusao_corrigida = data_filtered.groupby(['COD_CURSO', 'NOME_UNIDADE', 'SEXO'])['TAXA_CONCLUSAO'].mean().reset_index()
top_cursos_corrigidos = taxa_conclusao_corrigida.sort_values('TAXA_CONCLUSAO', ascending=False).head(10)

print("\nTop 10 Cursos com Taxas Corrigidas:")
print(top_cursos_corrigidos)
