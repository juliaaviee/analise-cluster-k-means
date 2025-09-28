import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules

print ("Análise de Cobrança")

# Carregar os dados

try:
    df = pd.read_csv('dados/A4.csv')
    print("Dados carregados com sucesso.")
    print(f"O conjunto de dados tem {df.shape[0]} linhas e {df.shape[1]} colunas.")
except FileNotFoundError:
    print("Erro: O arquivo 'A4.csv' não foi encontrado.")
    print("Por favor, certifique-se de que o arquivo está na mesma pasta que o script.")
    exit()

# Analise de clusterização (K-Means)
print("Iniciando Análise de Clusterização (K-Means)")

#Método do Cotovelo (Elbow Method) para encontrar o k ideal -> O objetivo é encontrar o ponto onde a curva "achata" (o cotovelo).

print("Calculando o número ideal de clusters com o Método do Cotovelo...")
wcss = []
k_range = range(1, 11)

for i in k_range:
    kmeans_test = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans_test.fit(df)
    wcss.append(kmeans_test.inertia_)

# Plotando o gráfico do cotovelo
plt.figure(figsize=(10, 6))
plt.plot(k_range, wcss, marker='o', linestyle='--')
plt.title('Método do Cotovelo (Elbow Method)')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Soma dos Erros Quadrados (WCSS)')
plt.grid(True)
plt.xticks(k_range)
plt.savefig('grafico_cotovelo.png')
print("Gráfico do Método do Cotovelo salvo como 'grafico_cotovelo.png'.")
print("Análise do gráfico sugere k=4 como um bom valor para o cotovelo.")

#Aplicando o K-Means com o k escolhido
k_ideal = 4
kmeans = KMeans(n_clusters=k_ideal, init='k-means++', max_iter=300, n_init=10, random_state=42)
df['Cluster'] = kmeans.fit_predict(df)
print(f"Algoritmo K-Means executado com k={k_ideal}.")

#Análise dos Clusters Gerados
print("Características Médias de Cada Cluster")
# Usamos groupby() para agrupar os dados por cluster e .mean() para ver a média das características.
cluster_analysis = df.groupby('Cluster').mean()
print(cluster_analysis)

#ETAPA 4: MINERAÇÃO DE REGRAS DE ASSOCIAÇÃO (APRIORI)
print("Iniciando Mineração de Regras de Associação (Apriori)")

#Preparação dos Dados
# O Apriori precisa de dados em formato binário (One-Hot Encoding).
# Primeiro, removemos a coluna 'Cluster' que acabamos de criar.
df_apriori = df.drop('Cluster', axis=1)

# Convertendo todas as colunas para string para que o get_dummies as trate como categorias distintas.
df_str = df_apriori.astype(str)

# Transformando o dataframe em formato binário.
df_encoded = pd.get_dummies(df_str)
print("Dados preparados para o Apriori (One-Hot Encoding).")

#Aplicação do Algoritmo Apriori
# min_support define a frequência mínima para um conjunto de itens ser considerado "frequente".
# Um valor de 0.05 significa que o padrão deve ocorrer em pelo menos 5% dos dados.
frequent_itemsets = apriori(df_encoded, min_support=0.05, use_colnames=True)
print("Algoritmo Apriori executado para encontrar conjuntos frequentes.")

#Geração e Filtragem das Regras
# Geramos as regras a partir dos conjuntos frequentes.
# A métrica 'lift' com threshold de 1 nos ajuda a encontrar regras onde a associação é positiva.
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Filtramos para manter apenas as regras que levam a um acordo ('Acordo_1').
acordo_rules = rules[rules['consequents'].astype(str).str.contains('Acordo_1')]

# Ordenamos pelas métricas de maior relevância.
acordo_rules_sorted = acordo_rules.sort_values(by=['confidence', 'lift'], ascending=False)

print("\n--- Principais Regras de Associação que levam a um Acordo ---")
# Exibimos apenas as colunas mais importantes para facilitar a leitura.
print(acordo_rules_sorted[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

print("Análise Concluída")
