import pandas as pd
import matplotlib.pyplot as plt

file_path = "io.xlsx"
data = pd.read_excel(file_path)

data_filtered = data[data['ANO'] != 'TOTAL']

data_filtered['ANO'] = pd.to_numeric(data_filtered['ANO'])

data_filtered['INGRESSANTES'].replace(0, pd.NA, inplace=True)

ingressantes_totais = data_filtered.groupby('COD_CURSO')['INGRESSANTES'].sum()

valid_courses = data_filtered['COD_CURSO'].value_counts()
valid_courses = valid_courses[valid_courses >= 20].index  # Definir um número mínimo de registros no dataset
data_filtered = data_filtered[data_filtered['COD_CURSO'].isin(valid_courses)]

gender_analysis = data_filtered.groupby(['ANO', 'SEXO'])['INGRESSANTES'].sum().reset_index()

from sklearn.linear_model import LinearRegression
import numpy as np

model = LinearRegression() #utilização do modelo de regressão linear 

future_years = [2013, 2024]  # Anos para prever - podem ser simplesmente adicionados anos nessa (qualquer ano) e será feita uma preivsão através da regressão linear
predictions = []

for gender in ['M', 'F']:
    subset = gender_analysis[gender_analysis['SEXO'] == gender]
    
    # Treinamento do modelo: x-> ANO e  y-> INGRESSANTES)
    X = subset[['ANO']].values 
    y = subset['INGRESSANTES'].values
    model.fit(X, y)
    
    future_preds = model.predict(np.array(future_years).reshape(-1, 1))
    predictions.append((gender, future_years, future_preds))

    predicted_df = pd.DataFrame({
        'ANO': future_years,
        'SEXO': gender,
        'INGRESSANTES': future_preds
    })
    gender_analysis = pd.concat([gender_analysis, predicted_df], ignore_index=True)

# plto do gráfico
plt.figure(figsize=(10, 6))
for gender in ['M', 'F']:
    subset = gender_analysis[gender_analysis['SEXO'] == gender]
    subset = subset.sort_values(by='ANO') 
    
    plt.plot(subset['ANO'], subset['INGRESSANTES'], label=f'Gênero {gender}', linestyle='-', marker='o')

plt.title('Proporção de Ingressantes por Gênero ao Longo dos Anos (com Previsões)')
plt.xlabel('Ano')
plt.ylabel('Número de Ingressantes')
plt.legend()
plt.grid(True)
plt.show()

# print das previsões no terminal 
for gender, years, preds in predictions:
    print(f"\nPrevisões para Gênero {gender}:")
    for year, pred in zip(years, preds):
        print(f"Ano {year}: {int(pred)} ingressantes (estimado)")

