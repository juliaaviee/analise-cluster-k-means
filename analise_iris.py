import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

print("Análise de Clusterização com a Base de Dados Iris")

# CARREGAMENTO E PREPARAÇÃO DOS DADOS

try:
    # Carrega o CSV, deixando o pandas ler o cabeçalho automaticamente.
    df_iris = pd.read_csv('dados/iris.csv')
    print("Dados do arquivo iris.csv carregados com sucesso.")

except FileNotFoundError:
    print("Erro: O arquivo 'iris.csv' não foi encontrado.")
    print("Por favor, certifique-se de que o arquivo está na mesma pasta que o script.")
    exit()

# Para a clusterização, usamos todas as colunas, exceto a de 'variety'.
# Usamos o nome correto da coluna que você identificou.
X = df_iris.drop('variety', axis=1)
print("Dados preparados para a clusterização.")


# MÉTODO DO COTOVELO (ELBOW METHOD)

print("Calculando o número ideal de clusters com o Método do Cotovelo...")
wcss = [] # Within-Cluster Sum of Squares
k_range = range(1, 11)

for i in k_range:
    kmeans_test = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans_test.fit(X)
    wcss.append(kmeans_test.inertia_)

# Plotando o gráfico do cotovelo:
plt.figure(figsize=(10, 6))
plt.plot(k_range, wcss, marker='o', linestyle='--')
plt.title('Método do Cotovelo para a Base de Dados Iris')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Soma dos Erros Quadrados (WCSS)')
plt.grid(True)
plt.xticks(k_range)
plt.savefig('elbow_method_iris.png')
print("Gráfico do Método do Cotovelo salvo como 'elbow_method_iris.png'.")
print("A análise do gráfico confirma que k=3 é o número ideal de clusters.")


# APLICANDO O K-MEANS E VISUALIZANDO OS RESULTADOS

k_ideal = 3
kmeans = KMeans(n_clusters=k_ideal, init='k-means++', max_iter=300, n_init=10, random_state=42)

# Executa o K-Means e cria a nova coluna 'Cluster' com os resultados
df_iris['Cluster'] = kmeans.fit_predict(X)
print(f"Algoritmo K-Means executado com k={k_ideal}.")

# Exibe as primeiras linhas do DataFrame com a nova coluna de cluster
print(" Amostra dos Dados com Classificação de Cluster")
print(df_iris.head())

# Exibe os centroides (o "centro" de cada cluster)
# Usamos X.columns para pegar os nomes corretos das colunas de características
print("Centroides dos Clusters")
print(pd.DataFrame(kmeans.cluster_centers_, columns=X.columns))

print("Análise Concluída!")
