import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

def pre_processing():
    file_path = "io.xlsx"
    file_path2 = "diciplinas.xlsx"

    dados_cursos = pd.read_excel(file_path)
    dados_disciplinas = pd.read_excel(file_path2)

    dados_disciplinas.drop('Arquivo_Origem', axis=1, inplace=True)
    dados_disciplinas['Semestre'] = dados_disciplinas['Semestre'].str.split('.').str[0].astype(int)

    dados_cursos.rename(columns={'COD_CURSO': 'Cod_Curso'}, inplace=True)
    dados_disciplinas.rename(columns={'Cód..Curso': 'Cod_Curso'}, inplace=True)
    
    dados_cursos['ANO'] = pd.to_numeric(dados_cursos['ANO'], errors='coerce')
    dados_disciplinas['Ano'] = pd.to_numeric(dados_disciplinas['Ano'], errors='coerce')

    dados_cursos['Cod_Curso'] = dados_cursos['Cod_Curso'].str.split('.').str[0].astype(int)
    dados_disciplinas['Cod_Curso'] = dados_disciplinas['Cod_Curso'].astype(int)

    dados_cursos = pd.merge(dados_cursos, dados_disciplinas[['Cod_Curso', 'Semestre']], on='Cod_Curso', how='left')

    return dados_cursos, dados_disciplinas


def regressao_linear(data, target_column, anos_semestres):
    """
    Realiza a regressão linear para prever valores futuros com base em ano e semestre.
    """
    
    data['Ano_Sem_Num'] = data['ANO'] + (data['Semestre'] - 1) * 0.5

    X = data['Ano_Sem_Num'].values.reshape(-1, 1)  
    y = data[target_column].values  
    model = LinearRegression()
    model.fit(X, y)

    anos_semestres_num = np.array([ano + (semestre - 1) * 0.5 for ano, semestre in anos_semestres]).reshape(-1, 1)
    predictions = model.predict(anos_semestres_num)

    for (ano, semestre), pred in zip(anos_semestres, predictions):
        data = pd.concat(
            [
                data,
                pd.DataFrame({"ANO": [ano], "Semestre": [semestre], target_column: [pred], "Ano_Sem_Num": [ano + (semestre - 1) * 0.5]}),
            ]
        )

    return data.sort_values(by="Ano_Sem_Num")  


def evolucao_taxa_formados(dados_cursos):
    """
    Gera um gráfico mostrando a evolução da taxa de formados com previsões.
    """
    formados = dados_cursos.groupby(['ANO', 'Semestre'])['FORMADOS'].sum()
    total_alunos = dados_cursos.groupby(['ANO', 'Semestre'])['INGRESSANTES'].sum() + dados_cursos.groupby(['ANO', 'Semestre'])['FORMADOS'].sum()

    taxa_formados = (formados / total_alunos * 100).reset_index(name='Taxa')
    anos_semestres = [(2013, 1), (2013, 2), (2024, 1), (2024, 2)]  # anos a serem previstos na regressão, podem ser adicionadas outros anos 

    taxa_formados = regressao_linear(taxa_formados, 'Taxa', anos_semestres)

    # Plot do gráfico
    plt.figure(figsize=(12, 8))
    plt.plot(taxa_formados['ANO'].astype(str) + "." + taxa_formados['Semestre'].astype(str), taxa_formados['Taxa'], label="Taxa de Formados", marker='o')
    plt.title('Evolução da Taxa de Formados')
    plt.xlabel('Ano e Semestre')
    plt.ylabel('Taxa de Formados (%)')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


def main():
    dados_cursos, dados_disciplinas = pre_processing()
    
    evolucao_taxa_formados(dados_cursos)

if __name__ == '__main__':
    main()

