# 📌 **Etapa 1: Planejamento e Definição**

---

## **1.1 – Validação dos KPIs Propostos**

Definir bons **KPIs (Key Performance Indicators)** é fundamental para garantir que a decisão sobre o novo CD (Centro de Distribuição) seja baseada em dados concretos, comparáveis e alinhados à estratégia da empresa.

### KPIs Propostos e Validação:

1. **Tempo Médio de Entrega (Eficiência Logística)**

   * **Justificativa:** O Magalu precisa reduzir o tempo de entrega para os clientes no Nordeste, já que a rapidez está diretamente ligada à satisfação e fidelização do cliente (alinhamento ao SLA).
   * **Métrica:** Média de tempo de entrega (em horas) para as principais capitais e cidades estratégicas da região.

2. **Custo de Aquisição Imobiliária (Investimento Inicial)**

   * **Justificativa:** O custo de terrenos e galpões é significativo na decisão. Embora seja um gasto pontual, impacta diretamente no ROI do projeto.
   * **Métrica:** Preço médio por m² de terrenos e galpões industriais em Recife e Salvador.

3. **Potencial de Consumo da Região (Receita Esperada)**

   * **Justificativa:** Um CD precisa estar próximo de mercados consumidores ativos. Proximidade a áreas de alta densidade populacional e alta renda aumenta o potencial de vendas.
   * **Métrica:** Potencial de receita projetada com base em indicadores demográficos (PIB per capita, população, taxa de consumo das famílias).

4. **Custo Operacional Total (Rentabilidade)**

   * **Justificativa:** O ganho em rapidez só se sustenta se o custo total não inviabilizar a operação.
   * **Métrica:** Custo total médio por pedido, incluindo:

     * Custo logístico (transporte por rota média, combustível, manutenção);
     * Custo de mão de obra (salários médios da região);
     * Energia e insumos locais;
     * Custos fixos associados à operação.

✅ **Validação Concluída:** Os 4 KPIs capturam os **pilares estratégicos da decisão**: rapidez, investimento, mercado e rentabilidade. Além disso, são mensuráveis com dados abertos e comparáveis entre Recife e Salvador.

---

## **1.2 – Plano Detalhado do Projeto**

### Objetivo Principal

Determinar qual cidade — **Recife ou Salvador** — apresenta a melhor localização estratégica para o novo CD, com base em dados abertos, modelos estatísticos e simulações logísticas.

### Estrutura do Projeto

1. **Etapa 1 – Planejamento e Definição** (📍 atual)
2. **Etapa 2 – Coleta e Pré-processamento de Dados (ETL)**
3. **Etapa 3 – Análise e Modelagem**
4. **Etapa 4 – Visualização e Comunicação dos Resultados**

### Responsabilidades (nós dois)

* **Analista A (você ou eu, dependendo da divisão):** ETL, análise de custos e modelagem preditiva.
* **Analista B:** análise logística e simulação com OSRM + mapas interativos.
* **Ambos:** discussão e validação dos resultados, construção de dashboards e relatório executivo.

### Cronograma Estimado

* Etapa 1 (Planejamento): 3 dias
* Etapa 2 (ETL): 7–10 dias
* Etapa 3 (Análise): 15–20 dias
* Etapa 4 (Apresentação): 5 dias

**Total:** \~30 a 40 dias de projeto.

### Entregáveis

* Relatório Técnico Detalhado (com metodologia, scripts e resultados).
* Relatório Executivo (visão de negócio, visualizações e recomendação final).
* Dashboard interativo (KPIs, mapas de isócronas, simulações).

---



### **Etapa 1: Planejamento e Definição**

**Equipe Responsável:** Análise de Negócio e Gestão de Projetos.

* **Ferramentas de Gestão e Colaboração:**

  * **Trello:** gestão visual do progresso (kanban).
  * **Notion:** centralização da documentação (técnica + executiva).
  * **Slack:** comunicação em tempo real.
  * **GitHub:** versionamento de código e notebooks.

---

### **Etapa 2: Coleta, Pré-processamento e Armazenamento de Dados**

**Equipe Responsável:** Engenharia de Dados e Ciência de Dados.

* **Linguagem Principal:** Python.
* **Bibliotecas de ETL:** Requests, BeautifulSoup/Scrapy, Pandas, NumPy.
* **Banco de Dados:** PostgreSQL + PostGIS (armazenamento tabular e espacial).
* **Geoprocessamento:** GeoPandas para integração com PostGIS.

---

### **Etapa 3: Análise, Modelagem e Otimização**

**Equipe Responsável:** Ciência de Dados.

* **Análise Geoespacial:** GeoPandas.
* **Modelagem de Rotas:** NetworkX + OSRM.
* **Modelagem Estatística:** Scikit-learn (regressão, clusterização) + Statsmodels (análises inferenciais).

---

### **Etapa 4: Visualização e Comunicação**

**Equipe Responsável:** Análise de Negócio e Ciência de Dados.

* **Visualização:** Matplotlib, Seaborn, Plotly.
* **Mapas Interativos:** Folium (operacional), Kepler.gl (executivo).
* **Dashboards:** Streamlit (prototipagem) e Metabase (execução final).

---


## **1.3 – Avaliação das Ferramentas e Bibliotecas**

Como o requisito é **Open Source apenas**, vamos nos apoiar em ferramentas confiáveis e reconhecidas pela comunidade.

### Para Coleta e ETL:

**Equipe Responsável:** Engenharia de Dados e Ciência de Dados.

* **Linguagem Principal:** Python.
* **Bibliotecas de ETL:** Requests, BeautifulSoup/Scrapy, Pandas, NumPy.
* **Banco de Dados:** PostgreSQL + PostGIS (armazenamento tabular e espacial).
* **Geoprocessamento:** GeoPandas para integração com PostGIS.

### Para Modelagem Estatística e Machine Learning:

**Equipe Responsável:** Ciência de Dados.

* **Análise Geoespacial:** GeoPandas.
* **Modelagem Estatística:** Scikit-learn (regressão, clusterização) + Statsmodels (análises inferenciais).

### Para Análise Logística:

**Equipe Responsável:** Ciência de Dados.

* **OpenStreetMap + OSRM (Open Source Routing Machine):** cálculo de rotas e tempos de viagem.
* **NetworkX:** modelagem de grafos para simulação logística.

### Para Visualização:

**Equipe Responsável:** Análise de Negócio e Ciência de Dados.

* **Visualização:** Matplotlib, Seaborn, Plotly.
* **Mapas Interativos:** Folium (operacional), Kepler.gl (executivo).

### Para Documentação e Comunicação:

* **Jupyter Notebooks:** documentação técnica e análises.
* **Markdown + LaTeX:** relatórios técnicos.
* **Streamlit:** versão simplificada do dashboard (se for útil).

✅ Todas as ferramentas são **Open Source**, amplamente utilizadas em projetos de ciência de dados e big data.

---

## **1.4 – Documentação Técnica e Executiva**

### Documentação Técnica (nível operacional)

* Descrição detalhada dos **dados brutos coletados** (fonte, formato, volume, licenciamento).
* **Scripts de ETL** com comentários técnicos (Python).
* Modelos estatísticos e parâmetros utilizados.
* Simulações de rotas e cálculos logísticos.
* Versão de controle de código (GitHub privado para versionamento).

### Documentação Executiva (nível estratégico)

* Resumo dos **objetivos e resultados esperados**.
* Explicação simples dos **KPIs e por que foram escolhidos**.
* Gráficos e mapas interativos que ilustram cenários (tempo de entrega, custos, mercado).
* Conclusão clara: Recife x Salvador, destacando **ganhos e riscos**.
* Storytelling para sustentar a decisão (comunicação ao estilo MBA).

✅ Esse duplo formato garante que tanto a **alta gestão** quanto a **equipe técnica** tenham clareza e segurança sobre o processo.

---

# 📊 **Resumo da Etapa 1**

1. **KPIs validados:** refletem rapidez, custo inicial, potencial de mercado e rentabilidade operacional.
2. **Plano de projeto:** dividido em 4 etapas, com cronograma de 30–40 dias e entregáveis claros.
3. **Ferramentas escolhidas:** todas Open Source (Python, GeoPandas, OSRM, Scikit-learn, Plotly/Dash).
4. **Documentação:** preparada em dois níveis (técnico e executivo), garantindo clareza para todos os stakeholders.
