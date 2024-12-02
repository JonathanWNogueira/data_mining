

import csv
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)  # Para garantir que o conteúdo das linhas seja mostrado sem quebras

file_path = "diciplinas.xlsx"
data = pd.read_excel(file_path)

data['Curso_Professor'] = data['Curso'] + ' - ' + data['Professor']
data['Transacao'] = data['Curso_Professor'] + ' - ' + data['Situação']

transactions = data[['Curso_Professor', 'Situação']].values.tolist()


transactions = [[str(item) for item in transaction if pd.notna(item)] for transaction in transactions]

te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_basket = pd.DataFrame(te_ary, columns=te.columns_)

support_threshold = 2  # Número mínimo de transações
item_counts = df_basket.sum(axis=0)
frequent_items = item_counts[item_counts >= support_threshold].index
df_basket = df_basket[frequent_items]

print(df_basket.info())
print(df_basket.sum(axis=0))  # Número de vezes que cada item aparece
print(df_basket.head())       # Amostra da matriz binária

min_support = 0.0002  # Ajuste conforme necessário
frequent_itemsets = apriori(df_basket, min_support=min_support, use_colnames=True)

print(frequent_itemsets)

total_transactions = len(df_basket)
absolute_support = min_support * total_transactions
print(f"Suporte absoluto mínimo: {absolute_support} transações.")

print(df_basket.shape)
print("Itens por transação (média):", df_basket.sum(axis=1).mean())


if not frequent_itemsets.empty:

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)
 
    regras_relevantes = rules[rules['lift'] > 0.5]  # Ajuste o limiar de lift
    rules.to_csv('regras_associacao.csv', index=False)

    regras_relevantes.to_csv('regras_relevantes.csv', index=False)

    print(regras_relevantes[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
else:
    print("Nenhum conjunto frequente encontrado com o suporte especificado.")
