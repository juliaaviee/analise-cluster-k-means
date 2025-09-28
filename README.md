# Relatório de Análise: Segmentação de Clientes e Padrões de Flores

## Visão Geral analise_cobranca

Este relatório detalha a análise realizada sobre uma base de dados de cobrança com o objetivo de segmentar os devedores em perfis distintos (clusters) e identificar os padrões de comportamento (regras) que mais frequentemente resultam em um acordo de pagamento. O objetivo final é cruzar essas duas análises para criar estratégias de cobrança personalizadas e mais eficientes.

## Metodologia

Foram utilizadas duas técnicas de aprendizado não supervisionado para gerar os insights deste relatório:

1.  **Clusterização (K-Means):** O algoritmo K-Means foi aplicado para agrupar os dados em **4 clusters**, número ideal identificado através do Método do Cotovelo. Cada cluster representa um perfil de devedor com características similares.
2.  **Regras de Associação (Apriori):** O algoritmo Apriori foi utilizado para extrair regras no formato "Se {condição A} e {condição B}, então {ocorre um acordo}", permitindo identificar os gatilhos mais fortes para o sucesso na negociação.

---

## 1. Análise dos Clusters Gerados (Perfis de Devedores)

A análise revelou 4 perfis distintos de devedores, com as seguintes características médias:

| Característica | Cluster 0 | Cluster 1 | Cluster 2 | Cluster 3 |
| :--- | :--- | :--- | :--- | :--- |
| **Idade (da dívida)** | 0.81 | 1.83 | **3.99** | 1.95 |
| **Atraso** | 1.25 | **5.86** | 2.05 | 0.88 |
| **Valor** | 1.77 | 0.61 | 2.11 | **4.96** |
| **CONTATO**| 9.54 | 7.27 | 7.91 | 10.37 |
| **EFETIVO**| 1.48 | 1.47 | 1.55 | 1.48 |
| **Taxa de Acordo**| 0.62 | **0.65** | 0.61 | 0.55 |
| **% do Total de Clientes**| 30.2% | 34.3% | 27.5% | 8.0% |

### Descrição dos Perfis:

* **Cluster 0: "Devedores Recentes e Receptivos"**
    * **Perfil:** Composto por dívidas **novas** e com **baixo atraso**. O valor é moderado e, embora exijam uma média de 9-10 contatos, a taxa de sucesso para fechar acordos é boa (62%).
    * **Comportamento:** Representam a "janela de oportunidade". São clientes mais propensos a negociar logo no início do processo de cobrança.

* **Cluster 1: "Devedores Antigos de Baixo Valor"**
    * **Perfil:** Este é o maior grupo (34.3%) e é definido by um **longo tempo de atraso**, mas com o **menor valor** de dívida. Surpreendentemente, possui a **maior taxa de acordos (65%)**.
    * **Comportamento:** O baixo valor da dívida parece ser um facilitador para a quitação, mesmo após muito tempo. Estes clientes podem estar apenas esperando uma boa oportunidade para liquidar pendências de baixo impacto.

* **Cluster 2: "Devedores de Longa Data"**
    * **Perfil:** Agrupa as dívidas **mais antigas** da base. O valor e o atraso são moderados, e a taxa de acordo é a segunda mais baixa (61%).
    * **Comportamento:** São os casos mais "desgastados", onde a negociação é mais difícil devido ao longo tempo de relacionamento na cobrança. Exigem persistência.

* **Cluster 3: "Devedores de Alto Valor"**
    * **Perfil:** Um grupo pequeno (8%), mas financeiramente muito relevante. A característica principal é o **valor de dívida muito elevado**. Possuem a **menor taxa de sucesso (55%)** e exigem o maior número de contatos.
    * **Comportamento:** A complexidade da negociação aumenta com o valor. O sucesso aqui não depende apenas da insistência, mas da qualidade da oferta e da negociação.

---

## 2. Análise das Regras de Associação (Padrões de Sucesso)

As regras extraídas pelo Apriori mostram os padrões que mais levam a um `Acordo = 1`.

| Antecedentes (SE...) | Consequente (...ENTÃO) | Confiança |
| :--- | :--- | :--- |
| `{Idade da dívida = 0, Atraso = 0}` | `{Acordo = 1}` | 80.2% |
| `{Valor = 5, Idade da dívida = 0}` | `{Acordo = 1}` | 78.6% |
| `{Atraso = 0, Valor = 1}` | `{Acordo = 1}` | 78.4% |
| `{Idade da dívida = 4, Atraso = 6, Valor = 0}` | `{Acordo = 1}` | 72.4% |
| `{Idade da dívida = 1, Atraso = 6}` | `{Acordo = 1}` | 68.1% |

---

## 3. Relação entre Clusters e Regras: Gerando Insights

O cruzamento das informações permite entender *por que* cada cluster se comporta de determinada maneira.

* **O sucesso do Cluster 0 ("Recentes") é explicado pela Regra 1.**
    * A alta taxa de acordo (62%) deste grupo é diretamente confirmada pela regra `{Idade=0, Atraso=0} -> {Acordo=1}`, que mostra uma confiança de 80%. Isso prova que a estratégia para este perfil deve ser de **ação imediata**, pois a propensão ao acordo é altíssima no início.

* **O sucesso surpreendente do Cluster 1 ("Antigos de Baixo Valor") é explicado pela Regra 4.**
    * A maior taxa de acordo da base (65%) vem deste perfil de longo atraso. A Regra 4, `{Idade=4, Atraso=6, Valor=0} -> {Acordo=1}` com 72% de confiança, desvenda o mistério: o **baixo valor** da dívida é o grande facilitador. A estratégia para este perfil deve ser focada em campanhas de liquidação de pequenos valores.

* **A dificuldade com o Cluster 3 ("Alto Valor") é refletida na ausência de regras simples e fortes.**
    * A menor taxa de acordo (55%) deste cluster se manifesta no fato de que não há regras de alta confiança que dependam de poucas variáveis. A Regra 2, `{Valor=5, Idade=0} -> {Acordo=1}`, mostra que o sucesso só é alto quando a dívida de alto valor é muito recente. Para dívidas de alto valor mais antigas, a negociação é complexa e exige estratégias mais robustas.

### Conclusão

A combinação da clusterização com as regras de associação permitiu não apenas segmentar os clientes, mas também entender a "lógica" por trás do comportamento de cada segmento. Isso possibilita a criação de estratégias de cobrança personalizadas, alocando os recursos de forma mais inteligente: agilidade para os novos, campanhas de baixo valor para os antigos, e negociadores especializados para as dívidas de alto valor.

---
# Análise Avançada da Base Iris: K-Means com Descrição por Regras de Associação

## Visão Geral 2 analise_iris

Este projeto aprofunda a análise da clássica base de dados Iris. Em vez de apenas agrupar os dados, o objetivo é utilizar um método de duas etapas para, primeiro, segmentar as flores com o algoritmo **K-Means** e, em seguida, usar o algoritmo **Apriori** para gerar regras de associação que forneçam uma descrição clara e legível das características que definem cada cluster.

Esta abordagem demonstra como as regras de associação podem ser usadas para interpretar e validar os agrupamentos encontrados por algoritmos de clusterização.

## Metodologia

1.  **Clusterização (K-Means):** Primeiramente, o K-Means foi executado com k=3 (o número ideal validado) para agrupar as flores em três segmentos distintos.
2.  **Discretização:** As características contínuas da base (como `sepal.length`) foram convertidas em categorias discretas ("baixa", "média", "alta") para viabilizar a análise de associação.
3.  **Regras de Associação (Apriori):** O algoritmo Apriori foi aplicado sobre os dados discretizados para encontrar as regras mais fortes que ligam as características das flores ao cluster em que foram classificadas.

---

## 1. Resultados da Clusterização (K-Means)

O K-Means identificou 3 clusters com os seguintes "centros" (características médias), que correspondem claramente às três espécies de Iris:

| Característica | Cluster 0 (Versicolor-like) | Cluster 1 (Setosa-like) | Cluster 2 (Virginica-like) |
| :--- | :--- | :--- | :--- |
| **sepal.length** | 5.90 | 5.00 | **6.85** |
| **sepal.width** | 2.74 | **3.42** | 3.07 |
| **petal.length** | 4.39 | **1.46** | **5.74** |
| **petal.width** | 1.43 | **0.24** | **2.07** |

### Descrição dos Perfis:

* **Cluster 0: "Flores de Pétala Média"** (Semelhante à *Iris Versicolor*)
* **Cluster 1: "Flores de Pétala Pequena e Sépala Larga"** (Semelhante à *Iris Setosa*)
* **Cluster 2: "Flores de Pétala Grande"** (Semelhante à *Iris Virginica*)

---

## 2. Resultados das Regras de Associação (Apriori)

O Apriori gerou regras de altíssima confiança que descrevem perfeitamente o que define cada cluster. As regras mais fortes são:

| Regra (SE... ENTÃO...) | Confiança |
| :--- | :--- |
| **SE** `petal.width` é **baixa** E `petal.length` é **baixa** **ENTÃO** a flor é do **Cluster 1** | 100% |
| **SE** `petal.width` é **alta** E `petal.length` é **alta** **ENTÃO** a flor é do **Cluster 2** | 97.4% |
| **SE** `petal.width` é **média** E `petal.length` é **média** **ENTÃO** a flor é do **Cluster 0**| 93.3% |

---

## 3. Síntese: Apriori Explicando os Clusters do K-Means

A sinergia entre os dois algoritmos nesta análise é o principal insight. O Apriori fornece uma tradução perfeita e legível dos agrupamentos matemáticos criados pelo K-Means.

* **O Cluster 1 é perfeitamente definido pela Regra 1.**
    O K-Means encontrou um grupo com pétalas visivelmente pequenas. A primeira regra de associação confirma isso com **100% de confiança**: toda flor com largura e comprimento de pétala na categoria "baixa" pertence, sem exceção, ao Cluster 1.

* **O Cluster 2 é inequivocamente descrito pela Regra 2.**
    O agrupamento de flores com pétalas grandes é explicado pela regra que diz: se uma flor tem pétala com largura e comprimento "altos", há 97.4% de chance de ela pertencer ao Cluster 2.

* **O Cluster 0 é validado pela Regra 3.**
    Da mesma forma, o cluster de características intermediárias é bem definido pela regra que associa pétalas de tamanho "médio" ao Cluster 0, com mais de 93% de confiança.

### Conclusão Final

Este exercício demonstra um caso de uso ideal da combinação dos dois algoritmos. O K-Means é excelente para encontrar a estrutura e os grupos ocultos nos dados, mas seus resultados nem sempre são fáceis de traduzir em regras de negócio. O Apriori, quando aplicado sobre os resultados do K-Means, serve como uma **"camada de interpretação"**, transformando os agrupamentos numéricos em regras lógicas, claras e de alta confiança que validam e descrevem as características de cada segmento encontrado.
