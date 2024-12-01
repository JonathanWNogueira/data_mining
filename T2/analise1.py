import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
file_path = r"C:\Users\augus\Documents\Faculdade\6º semestre\Mineração de Dados\data_mining\T2\io.xlsx"
data = pd.read_excel(file_path)

# Remover as linhas com "TOTAL" no ano
data_filtered = data[data['ANO'] != 'TOTAL']

# Converter a coluna 'ANO' para numérico
data_filtered['ANO'] = pd.to_numeric(data_filtered['ANO'])

# Substituir ingressantes zero por NaN (ou um valor pequeno como 1)
data_filtered['INGRESSANTES'].replace(0, pd.NA, inplace=True)

# Remover linhas onde ingressantes ou formados estão ausentes
data_filtered.dropna(subset=['INGRESSANTES', 'FORMADOS'], inplace=True)

# Calcular a taxa de conclusão (evitar divisões por zero)
data_filtered['TAXA_CONCLUSAO'] = data_filtered['FORMADOS'] / data_filtered['INGRESSANTES']

# Filtrar cursos com pelo menos 5 registros ao longo dos anos
valid_courses = data_filtered['COD_CURSO'].value_counts()
valid_courses = valid_courses[valid_courses >= 5].index  # Definir o limite como 5 registros
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
plt.figure(figsize=(12, 8))
plt.yticks(fontsize=8)
plt.barh(top_cursos['NOME_UNIDADE'] + ' (' + top_cursos['SEXO'] + ')', top_cursos['TAXA_CONCLUSAO'], color='skyblue')
plt.xlabel('Taxa de Conclusão')
plt.title(f"Top {numero_cursos} Cursos com Maior Taxa de Conclusão")
plt.gca().invert_yaxis()
plt.show()

# Análise 1: Proporção de ingressantes por gênero ao longo dos anos
gender_analysis = data_filtered.groupby(['ANO', 'SEXO'])['INGRESSANTES'].sum().reset_index()

# Criar o gráfico de proporção de ingressantes por gênero ao longo dos anos
plt.figure(figsize=(10, 6))
for gender in ['M', 'F']:
    subset = gender_analysis[gender_analysis['SEXO'] == gender]
    plt.plot(subset['ANO'], subset['INGRESSANTES'], label=f'Gênero {gender}')

plt.title('Proporção de Ingressantes por Gênero ao Longo dos Anos')
plt.xlabel('Ano')
plt.ylabel('Número de Ingressantes')
plt.legend()
plt.grid(True)
plt.show()
