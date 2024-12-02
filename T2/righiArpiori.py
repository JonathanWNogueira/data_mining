# # # import pandas as pd
# # # from mlxtend.frequent_patterns import apriori, association_rules

# # # # Carregar os dados
# # # df = pd.read_excel("diciplinas.xlsx")

# # # # Verificar as colunas para garantir que as colunas estão corretas
# # # print(df.columns)

# # # # Criar variáveis binarizadas para as colunas de interesse
# # # df_binarizado = pd.get_dummies(df[['Situação', 'Professor', 'Curso', 'Cód..Disciplina']])

# # # # Garantir que os valores são booleanos (True/False ou 1/0)
# # # df_binarizado = df_binarizado.astype(bool)

# # # # Verificar os dados binarizados
# # # print(df_binarizado.head(20))  # Exibe as 20 primeiras linhas

# # # # Aplicar o algoritmo Apriori para descobrir itemsets frequentes
# # # frequent_itemsets = apriori(df_binarizado, min_support=0.3, use_colnames=True)

# # # # Exibir os itemsets frequentes
# # # print("Itemsets Frequentes:")
# # # print(frequent_itemsets)

# # # # Gerar as regras de associação usando "lift" como métrica e um limiar mínimo de 1.0
# # # # Note que não precisamos do "num_itemsets" aqui
# # # rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.5, num_itemsets=3)

# # # # Exibir as regras geradas
# # # print("Regras de Associação:")
# # # print(rules)



# # import pandas as pd
# # from mlxtend.frequent_patterns import apriori, association_rules


# # # Carregar os dados
# # df = pd.read_excel("diciplinas.xlsx")

# # # Filtro de dados onde a Situação é Reprovado
# # df_reprovados = df[df['Situação'] == 'Reprovado']

# # # Agora vamos agrupar por Curso e Professor, e calcular a confiança dessa combinação (percentual de reprovação)
# # combo_prof_curso = df_reprovados.groupby(['Curso', 'Professor']).size().reset_index(name='reprovados')

# # # Agora vamos calcular o total de casos por combinação de Curso e Professor (sem filtro de 'Reprovado')
# # combo_total = df.groupby(['Curso', 'Professor']).size().reset_index(name='total')

# # # Unindo as duas tabelas para calcular a confiança
# # df_combo = pd.merge(combo_prof_curso, combo_total, on=['Curso', 'Professor'])

# # # Calculando a confiança como a razão de reprovação
# # df_combo['confiança'] = df_combo['reprovados'] / df_combo['total']

# # # Ordenando o DataFrame para ver as combinações de maior confiança
# # df_combo_sorted = df_combo.sort_values(by='confiança', ascending=False)

# # # Exibindo as combinações de maior confiança
# # print(df_combo_sorted[['Curso', 'Professor', 'reprovados', 'total', 'confiança']])

# # # # Verificar as colunas para garantir que as colunas estão corretas
# # # print(df.columns)

# # # # Criar variáveis binarizadas para as colunas de interesse
# # # df_binarizado = pd.get_dummies(df[['Situação', 'Professor', 'Curso', 'Cód..Disciplina']])

# # # # Garantir que os valores são booleanos (True/False ou 1/0)
# # # df_binarizado = df_binarizado.astype(bool)


# # # df_encoded = pd.get_dummies(df[['Curso', 'Professor', 'Situação']])

# # # # Aplicando o algoritmo Apriori para encontrar itemsets frequentes
# # # frequent_itemsets = apriori(df_encoded, min_support=0.01, use_colnames=True)


# # # # # Gere os itemsets frequentes com um suporte mais baixo (ex: 0.05)
# # # # frequent_itemsets = apriori(df_binarizado, min_support=0.05, use_colnames=True)

# # # # Gere as regras de associação usando a métrica 'lift' para encontrar relações interessantes
# # # rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.1, num_itemsets=3)

# # # # Filtrando as regras onde o consequente é Situação_Reprovado
# # # rules_reprovado = rules[rules['consequents'].apply(lambda x: 'Situação_Reprovado' in str(x))]

# # # # Exibindo as regras com antecedentes de curso e professor
# # # print(rules_reprovado[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# # # # Exibe as regras
# # # print(rules)

# # # print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# # # # Você pode querer ordenar as regras pelo 'lift' para ver as associações mais fortes primeiro
# # # rules_sorted = rules.sort_values(by='lift', ascending=False)

# # # # Ajusta a configuração para exibir todas as colunas
# # # pd.set_option('display.max_columns', 16)

# # # # Exibe as primeiras regras mais fortes
# # # print(rules_sorted.head())


# # # Ajusta a configuração para exibir todas as colunas
# # pd.set_option('display.max_rows', 50)
# # pd.set_option('display.max_columns', 50)
# # pd.set_option('display.width', 1000)  # Para garantir que o conteúdo das linhas seja mostrado sem quebras

# # # # Exemplo: Situação por Curso com Número de Alunos
# # # alunos_situacao = df.groupby(['Curso', 'Situação']).size().reset_index(name='Total')
# # # alunos_situacao['Confiança'] = alunos_situacao['Total'] / alunos_situacao.groupby('Curso')['Total'].transform('sum')
# # # print(alunos_situacao)

# # # # Exemplo 2: Cursos com mais de 200 alunos matriculados
# # # cursos_maiores_200 = df.groupby('Curso').size().reset_index(name='Total Alunos')
# # # cursos_maiores_200 = cursos_maiores_200[cursos_maiores_200['Total Alunos'] > 20]
# # # print(cursos_maiores_200)


# # # Exemplo: Análise de Professor e Semestre com Situação
# # professor_semestre = df.groupby(['Professor', 'Semestre', 'Situação']).size().reset_index(name='Total')
# # professor_semestre['Confiança'] = professor_semestre['Total'] / professor_semestre.groupby(['Professor', 'Semestre'])['Total'].transform('sum')
# # # Ordena pelo valor da coluna 'Confiança' de forma decrescente
# # professor_semestre_sorted = professor_semestre.sort_values(by='Confiança', ascending=False)

# # # print(professor_semestre)
# # # print(professor_semestre.head(150))

# # # # Mostrar do índice 100 até o 150
# # # print(professor_semestre.iloc[100:150])




# # # Ordenar pela coluna 'Confiança' de forma decrescente
# # professor_semestre_sorted = professor_semestre.sort_values(by='Confiança', ascending=False)

# # # Exibir as primeiras 10 linhas (top 10 regras)
# # print(professor_semestre_sorted.head(40))

# # from mlxtend.preprocessing import TransactionEncoder

# # # Definir os dados a partir do dataframe que já estamos usando
# # dados_apriori = df[['Curso', 'Professor', 'Situação']]

# # # Transformando os dados em uma lista de transações
# # transacoes = dados_apriori.values.tolist()

# # # Usando o TransactionEncoder para transformar as transações em formato binário
# # te = TransactionEncoder()
# # te_ary = te.fit(transacoes).transform(transacoes)

# # # Criando um dataframe com as variáveis binárias
# # df_apriori = pd.DataFrame(te_ary, columns=te.columns_)

# # # Rodar o algoritmo Apriori com um suporte mínimo
# # frequent_itemsets = apriori(df_apriori, min_support=0.05, use_colnames=True)

# # # Gerar as regras de associação com um lift mínimo de 1 (para evitar regras sem significância)
# # regras = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# # # Exibir as regras encontradas
# # print(regras.head(10))  #



















# import pandas as pd
# from mlxtend.frequent_patterns import fpgrowth, association_rules

# # 1. Carregar os dados
# file_path = "diciplinas.xlsx"
# data = pd.read_excel(file_path)

# # 2. Criar transações
# data['Transacao'] = data['Curso'] + ' - ' + data['Cód..Disciplina'] + ' - ' + data['Situação'] + ' - ' + data['Ano'].astype(str) + '/' + data['Semestre']
# basket = data.groupby(['Arquivo_Origem', 'Transacao']).size().unstack(fill_value=0)
# basket = basket > 0  # Transformar em booleano

# # 3. Limitar itens mais frequentes
# frequent_columns = basket.sum(axis=0)
# basket = basket.loc[:, frequent_columns[frequent_columns > 5].index]  # Apenas itens com mais de 5 ocorrências

# # 4. Aplicar FP-Growth
# min_support_value = 0.001  # Ajuste aqui
# frequent_itemsets = fpgrowth(basket, min_support=min_support_value, use_colnames=True)

# # Estatísticas básicas do dataset
# print("Dimensão da matriz basket:")
# print(f"Transações: {basket.shape[0]}, Itens: {basket.shape[1]}")

# # Frequência dos itens
# item_frequencies = basket.sum(axis=0)
# print("\n10 itens mais frequentes:")
# print(item_frequencies.sort_values(ascending=False).head(10))

# # Número de itens com baixa frequência
# rare_items = item_frequencies[item_frequencies < 5]
# print(f"\nItens com frequência < 5: {len(rare_items)}")


# if frequent_itemsets.empty:
#     print(f"Nenhum itemset frequente encontrado com suporte mínimo de {min_support_value}.")
# else:
#     # Gerar as regras
#     rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
#     print(f"Itemsets Frequentes (total: {len(frequent_itemsets)}):")
#     print(frequent_itemsets)
#     print("\nRegras de Associação:")
#     print(rules)


import csv
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)  # Para garantir que o conteúdo das linhas seja mostrado sem quebras

# Carregar os dados
file_path = "diciplinas.xlsx"
data = pd.read_excel(file_path)

# Criar uma transação baseada nas colunas relevantes
# data['Transacao'] = data['Curso'] + ' - ' + data['Situação']
data['Curso_Professor'] = data['Curso'] + ' - ' + data['Professor']
data['Transacao'] = data['Curso_Professor'] + ' - ' + data['Situação']

# transactions = data.groupby('Arquivo_Origem')['Transacao'].apply(list).values.tolist()
transactions = data[['Curso_Professor', 'Situação']].values.tolist()


# Garantir que todos os itens nas transações sejam strings
transactions = [[str(item) for item in transaction if pd.notna(item)] for transaction in transactions]

# Transformar as transações em matriz binária
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_basket = pd.DataFrame(te_ary, columns=te.columns_)

# Filtrar colunas com suporte baixo
support_threshold = 2  # Número mínimo de transações
item_counts = df_basket.sum(axis=0)
frequent_items = item_counts[item_counts >= support_threshold].index
df_basket = df_basket[frequent_items]

# Exibir uma amostra
print(df_basket.info())
print(df_basket.sum(axis=0))  # Número de vezes que cada item aparece
print(df_basket.head())       # Amostra da matriz binária

# Executar Apriori com suporte mínimo ajustável
min_support = 0.0002  # Ajuste conforme necessário
frequent_itemsets = apriori(df_basket, min_support=min_support, use_colnames=True)

# Exibir os itemsets encontrados
print(frequent_itemsets)

total_transactions = len(df_basket)
absolute_support = min_support * total_transactions
print(f"Suporte absoluto mínimo: {absolute_support} transações.")

print(df_basket.shape)
print("Itens por transação (média):", df_basket.sum(axis=1).mean())


# Gerar as regras com métricas como 'confidence' ou 'lift'
if not frequent_itemsets.empty:
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3, num_itemsets=1)
    
    # Salvar com a biblioteca csv para garantir que a formatação seja correta
    with open('regras_associacao.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['antecedents', 'consequents', 'antecedent support', 'consequent support', 'support', 'confidence'])
        for row in rules.itertuples(index=False):
            writer.writerow([str(row.antecedents), str(row.consequents), row._1, row._2, row._3, row._4])
    # Salvar como CSV
    # rules.to_csv('regras_associacao.csv', index=False)
    regras_relevantes = rules[rules['lift'] > 0.5]  # Ajuste o limiar de lift
    # Salvar as regras de associação em um arquivo CSV
    rules.to_csv('regras_associacao.csv', index=False)
    # Converter 'frozenset' em string antes de salvar

    regras_relevantes.to_csv('regras_relevantes.csv', index=False)

    print(regras_relevantes[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
else:
    print("Nenhum conjunto frequente encontrado com o suporte especificado.")
