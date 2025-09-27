# Planejamento de Projeto: Estudo de Caso MAGALU - Implementação Detalhada

Este documento detalha o planejamento do projeto de estudo de caso para o processo seletivo do MAGALU, com foco na escolha da melhor localização para um novo Centro de Distribuição (CD) no Nordeste (Recife vs Salvador). O projeto é dividido em etapas claras, utilizando o método 'dividir para conquistar', com tarefas pequenas e compreensíveis para a equipe de desenvolvimento, incluindo tecnologias e implementações.

## Objetivo Principal

Determinar qual cidade — Recife ou Salvador — apresenta a melhor localização estratégica para o novo CD, com base em dados abertos, modelos estatísticos e simulações logísticas.

## Estrutura do Projeto

O projeto é dividido em 4 etapas principais, cada uma com suas fases e tarefas detalhadas.

---

## Etapa 1: Planejamento e Definição

**Objetivo:** Estabelecer as bases do projeto, validar KPIs, definir a estrutura, responsabilidades, cronograma e ferramentas.

### 1.1. Validação dos KPIs Propostos

**Descrição:** Garantir que os KPIs escolhidos são relevantes, mensuráveis e alinhados aos objetivos estratégicos da decisão.

**KPIs Validados:**
*   **Tempo Médio de Entrega (Eficiência Logística):** Média de tempo de entrega (em horas) para as principais capitais e cidades estratégicas da região.
*   **Custo de Aquisição Imobiliária (Investimento Inicial):** Preço médio por m² de terrenos e galpões industriais em Recife e Salvador.
*   **Potencial de Consumo da Região (Receita Esperada):** Potencial de receita projetada com base em indicadores demográficos (PIB per capita, população, taxa de consumo das famílias).
*   **Custo Operacional Total (Rentabilidade):** Custo total médio por pedido, incluindo custo logístico, mão de obra, energia, insumos e custos fixos.

### 1.2. Plano Detalhado do Projeto

**Descrição:** Definir a estrutura geral do projeto, responsabilidades da equipe, cronograma estimado e entregáveis.

**Tarefas:**
*   **1.2.1. Definir Estrutura do Projeto:** Confirmar as 4 etapas principais (Planejamento, Coleta/Pré-processamento, Análise/Modelagem, Visualização/Comunicação).
*   **1.2.2. Atribuir Responsabilidades:**
    *   **Analista A (ETL, análise de custos, modelagem preditiva):** Definir quem será o responsável.
    *   **Analista B (análise logística, simulação OSRM, mapas interativos):** Definir quem será o responsável.
    *   **Ambos:** Discussão e validação de resultados, construção de dashboards e relatório executivo.
*   **1.2.3. Estabelecer Cronograma Estimado:**
    *   Etapa 1 (Planejamento): 3 dias
    *   Etapa 2 (ETL): 7–10 dias
    *   Etapa 3 (Análise): 15–20 dias
    *   Etapa 4 (Apresentação): 5 dias
    *   **Total:** ~30 a 40 dias.
*   **1.2.4. Definir Entregáveis:**
    *   Relatório Técnico Detalhado (metodologia, scripts, resultados).
    *   Relatório Executivo (visão de negócio, visualizações, recomendação final).
    *   Dashboard interativo (KPIs, mapas de isócronas, simulações).

### 1.3. Avaliação das Ferramentas e Bibliotecas (Open Source)

**Descrição:** Selecionar e validar as ferramentas e bibliotecas open source que serão utilizadas em cada etapa do projeto.

**Tecnologias e Implementações:**
*   **Gestão e Colaboração:**
    *   **Trello:** Gestão visual do progresso (Kanban).
    *   **Notion:** Centralização da documentação (técnica + executiva).
    *   **Slack:** Comunicação em tempo real.
    *   **GitHub:** Versionamento de código e notebooks.
*   **Coleta e ETL:**
    *   **Linguagem Principal:** Python.
    *   **Bibliotecas:** `Requests`, `BeautifulSoup`/`Scrapy` (web scraping), `Pandas`, `NumPy` (manipulação de dados).
    *   **Banco de Dados:** `PostgreSQL` + `PostGIS` (armazenamento tabular e espacial).
    *   **Geoprocessamento:** `GeoPandas` (integração com PostGIS).
*   **Análise, Modelagem e Otimização:**
    *   **Análise Geoespacial:** `GeoPandas`.
    *   **Modelagem de Rotas:** `NetworkX` (modelagem de grafos) + `OSRM` (Open Source Routing Machine).
    *   **Modelagem Estatística:** `Scikit-learn` (regressão, clusterização), `Statsmodels` (análises inferenciais), `XGBoost` (modelos preditivos robustos).
    *   **Otimização:** `OR-Tools` (Google) para VRP/roteirização por frota.
    *   **Interpretabilidade:** `SHAP`.
    *   **Simulações:** `Numpy` para Monte Carlo.
*   **Visualização e Comunicação:**
    *   **Visualização:** `Matplotlib`, `Seaborn`, `Plotly`.
    *   **Mapas Interativos:** `Folium` (operacional), `Kepler.gl` (executivo).
    *   **Dashboards:** `Streamlit` (prototipagem), `Metabase` (execução final).
*   **Documentação e Reprodutibilidade:**
    *   **Jupyter Notebooks:** Documentação técnica e análises.
    *   **Markdown + LaTeX:** Relatórios técnicos.
    *   **MLflow:** Rastreamento de experimentos, parâmetros, métricas e artefatos.
*   **Infraestrutura (se necessário para escala):**
    *   **Docker:** Containerização de jobs e serviços.
    *   **Kubernetes:** Orquestração de containers (para escalar OSRM, Airflow).
    *   **Apache Airflow:** Orquestração de DAGs para ETL e processos.
    *   **Prometheus + Grafana:** Logs e monitoramento (se for para produção).

### 1.4. Documentação Técnica e Executiva

**Descrição:** Definir a estrutura e o conteúdo da documentação para diferentes públicos (técnico e estratégico).

**Tarefas:**
*   **1.4.1. Estruturar Documentação Técnica:**
    *   Descrição detalhada dos dados brutos (fonte, formato, volume, licenciamento).
    *   Scripts de ETL com comentários técnicos (Python).
    *   Modelos estatísticos e parâmetros utilizados.
    *   Simulações de rotas e cálculos logísticos.
    *   Versionamento de código no GitHub.
*   **1.4.2. Estruturar Documentação Executiva:**
    *   Resumo dos objetivos e resultados esperados.
    *   Explicação simples dos KPIs e sua escolha.
    *   Gráficos e mapas interativos que ilustram cenários.
    *   Conclusão clara: Recife x Salvador, destacando ganhos e riscos.
    *   Storytelling para sustentar a decisão.

---

## Etapa 2: Coleta, Pré-processamento e Armazenamento de Dados (ETL)

**Objetivo:** Construir uma base de dados confiável e integrada a partir de fontes abertas, pronta para análise.

### 2.1. Coleta de Dados

**Descrição:** Extrair dados de diversas fontes abertas.

**Tarefas e Implementações:**
*   **2.1.1. Coleta de Custos Imobiliários:**
    *   **Ferramentas:** `Requests`, `BeautifulSoup`/`Scrapy`.
    *   **Fontes:** Portais de imóveis comerciais (Zap Imóveis, Viva Real, OLX Imóveis, sites locais).
    *   **Dados:** Preço do m², área construída, localização (endereço/CEP), tipo (venda/locação).
    *   **Implementação:** Desenvolver scripts de web scraping para cada portal.
*   **2.1.2. Coleta de Malha Viária e Tempos de Entrega:**
    *   **Ferramentas:** `Overpass API` (para OSM), `OSRM` (para cálculo de rotas).
    *   **Fontes:** OpenStreetMap (OSM).
    *   **Dados:** Rotas entre Recife/Salvador e capitais do NE, distância (km), tempo estimado de viagem (h).
    *   **Implementação:** Scripts Python para consulta à Overpass API e chamadas à API do OSRM (assumindo OSRM rodando em container).
*   **2.1.3. Coleta de Demografia e Potencial de Consumo:**
    *   **Ferramentas:** `Requests` (para APIs).
    *   **Fontes:** IBGE (API SIDRA), Censo Demográfico, PNAD Contínua, POF (Pesquisa de Orçamento Familiar).
    *   **Dados:** População, densidade demográfica, PIB per capita, taxa de consumo das famílias.
    *   **Implementação:** Scripts Python para consumir APIs do IBGE e processar dados de arquivos.

### 2.2. Pré-processamento (Limpeza e Transformação)

**Objetivo:** Padronizar, limpar e integrar os dados coletados.

**Tarefas e Implementações:**
*   **2.2.1. Normalização de Formatos:**
    *   **Ferramentas:** `Pandas`, `NumPy`.
    *   **Implementação:** Funções para converter unidades (moeda, distância, tempo), padronizar datas e tratar valores inconsistentes.
*   **2.2.2. Tratamento de Valores Ausentes:**
    *   **Ferramentas:** `Pandas`.
    *   **Implementação:** Estratégias de imputação (média, mediana, interpolação) ou remoção, conforme a natureza dos dados.
*   **2.2.3. Georreferenciamento de Endereços:**
    *   **Ferramentas:** `geopy`.
    *   **Implementação:** Script para converter endereços de imóveis em coordenadas latitude/longitude.
*   **2.2.4. Conversão para Formatos Espaciais:**
    *   **Ferramentas:** `GeoPandas`.
    *   **Implementação:** Converter DataFrames para GeoDataFrames para facilitar análises geoespaciais.
*   **2.2.5. Criação de Chaves Unificadas:**
    *   **Ferramentas:** `Pandas`.
    *   **Implementação:** Gerar chaves consistentes (ex: cidade, estado, CEP) para integrar diferentes datasets.

### 2.3. Armazenamento dos Dados

**Objetivo:** Persistir os dados limpos e transformados em um banco de dados robusto.

**Tarefas e Implementações:**
*   **2.3.1. Configurar PostgreSQL + PostGIS:**
    *   **Ferramentas:** `PostgreSQL`, `PostGIS`.
    *   **Implementação:** Instalar e configurar o banco de dados, criar extensões PostGIS.
*   **2.3.2. Definir Esquema do Banco de Dados:**
    *   **Tabelas:** `imoveis` (id, cidade, preco_m2, area, coordenadas), `rotas` (origem, destino, distancia_km, tempo_horas), `demografia` (cidade, populacao, pib_per_capita, consumo_familias).
    *   **Implementação:** Scripts SQL para criação das tabelas e índices (incluindo índices espaciais).
*   **2.3.3. Carregar Dados no Banco:**
    *   **Ferramentas:** `psycopg2` (driver Python para PostgreSQL).
    *   **Implementação:** Scripts Python para inserir os dados pré-processados nas tabelas correspondentes.

### 2.4. Fluxo ETL (Arquitetura de Dados)

**Objetivo:** Orquestrar e automatizar o pipeline de dados.

**Tarefas e Implementações:**
*   **2.4.1. Desenhar Pipeline ETL:**
    *   **Extract (E):** Scraping de imóveis, APIs (IBGE, Overpass API), OSRM.
    *   **Transform (T):** Limpeza, normalização, georreferenciamento, conversão para GeoDataFrames, cálculo de métricas derivadas.
    *   **Load (L):** Inserção em PostgreSQL/PostGIS, criação de índices espaciais.
*   **2.4.2. Implementar Orquestração com Apache Airflow:**
    *   **Ferramentas:** `Apache Airflow`.
    *   **Implementação:** Criar DAGs (Directed Acyclic Graphs) para cada etapa do ETL, garantindo agendamento, retry e monitoramento. Containerizar jobs Python com Docker para execução no Airflow.

---

## Etapa 3: Análise, Modelagem e Otimização

**Objetivo:** Aplicar técnicas avançadas de análise de dados, modelagem estatística e otimização para responder aos KPIs.

### 3.1. KPI 1 — Tempo Médio de Entrega (Eficiência Logística)

**Objetivo:** Comparar tempos de entrega e variabilidade a partir de Recife vs Salvador; gerar isócronas e percentis.

**Tarefas e Implementações:**
*   **3.1.1. Roteamento Determinístico:**
    *   **Ferramentas:** `OSRM`.
    *   **Implementação:** Calcular rotas ótimas entre origens (Recife/Salvador) e destinos (capitais/centros de demanda) usando OSRM. Armazenar resultados (distância, tempo) no PostGIS.
*   **3.1.2. Simulação de Incerteza (Monte Carlo):**
    *   **Ferramentas:** `NumPy`.
    *   **Implementação:** Aplicar variações nos perfis de velocidade do OSRM para simular congestionamentos e obter médias e percentis de tempo de viagem.
*   **3.1.3. Análise de Grafo:**
    *   **Ferramentas:** `NetworkX`.
    *   **Implementação:** Modelar a malha viária como um grafo para avaliar centralidade e vulnerabilidade (pontos de falha).
*   **3.1.4. Geração de Isócronas:**
    *   **Ferramentas:** `GeoPandas`, `Shapely`.
    *   **Implementação:** Criar buffers de rotas/isócronas para 4h, 8h, 12h de viagem a partir de cada CD.
*   **3.1.5. Validação e Métricas:**
    *   `mean_travel_time`, `median`, `p75`, `p90` por destino.
    *   % da população alcançável em diferentes janelas de tempo.
    *   Variação padrão nas simulações.

### 3.2. KPI 2 — Custo de Aquisição Imobiliária (CapEx)

**Objetivo:** Comparar custos médios de imóveis em Recife e Salvador e estimar investimento inicial.

**Tarefas e Implementações:**
*   **3.2.1. Limpeza e Padronização de Preços:**
    *   **Ferramentas:** `Pandas`.
    *   **Implementação:** Remover outliers, padronizar moeda, ajustar preços pela inflação (usando IPCA).
*   **3.2.2. Modelagem de Preços Hedônicos:**
    *   **Ferramentas:** `Scikit-learn` (regressão linear múltipla) ou `XGBoost`.
    *   **Implementação:** Treinar modelo `preco_m2 ~ area + prox_porto + acesso_rodoviario + bairro + estado`.
*   **3.2.3. Estimativa de Custo Total:**
    *   **Implementação:** Aplicar encargos de transação e custos de adequação (estimados) para obter o custo total de aquisição.
*   **3.2.4. Validação e Métricas:**
    *   R² / RMSE do modelo hedônico.
    *   Estimativa pontual e intervalo de confiança (CI 95%) para `preco_m2`.

### 3.3. KPI 3 — Potencial de Consumo da Região (Demanda / Market Potential)

**Objetivo:** Quantificar o potencial de receita incremental e/ou market share para cada localização.

**Tarefas e Implementações:**
*   **3.3.1. Clusterização de Áreas:**
    *   **Ferramentas:** `Scikit-learn` (KMeans / DBSCAN).
    *   **Implementação:** Segmentar microrregiões em buckets de potencial (alto/médio/baixo) com base em dados demográficos.
*   **3.3.2. Modelagem Preditiva de Consumo:**
    *   **Ferramentas:** `Statsmodels` (OLS), `Scikit-learn` (RandomForest) ou `XGBoost`.
    *   **Implementação:** Treinar modelo para prever `gasto_estimado_per_capita` ou `vendas_per_capita` com base em features demográficas.
*   **3.3.3. Interpretabilidade do Modelo:**
    *   **Ferramentas:** `SHAP`.
    *   **Implementação:** Identificar os principais drivers do potencial de consumo (renda, densidade, proximidade).
*   **3.3.4. Cenários de Penetração:**
    *   **Implementação:** Calcular receitas projetadas sob diferentes taxas de penetração de mercado e elasticidade preço-tempo.
*   **3.3.5. Validação e Métricas:**
    *   R² / RMSE no conjunto de validação.
    *   Coeficientes / importância de features.
    *   Acrescentamento de receita esperado por cenário.

### 3.4. KPI 4 — Custo Operacional Total (TCO por Pedido)

**Objetivo:** Estimar o custo médio por pedido para cada localização, considerando CapEx amortizado, OpEx e transporte.

**Tarefas e Implementações:**
*   **3.4.1. Definir Equação de Custo:**
    *   **Implementação:** Formalizar a equação de custo por pedido, incluindo CapEx amortizado, mão de obra, energia, transporte e custos fixos.
*   **3.4.2. Simulação de Frota/Roteiro:**
    *   **Ferramentas:** `OR-Tools`.
    *   **Implementação:** Simular roteiros eficientes (VRP) para calcular `km_por_pedido` médio e `tempo_por_pedido_h` sob restrições reais (capacidade, janelas de entrega).
*   **3.4.3. Análise de Cenários:**
    *   **Implementação:** Variar parâmetros como custo de combustível, salários, volume de pedidos para analisar a sensibilidade do custo total.
*   **3.4.4. Validação e Métricas:**
    *   `C_{pedido}` médio e percentis.
    *   Elasticidade do custo frente a variáveis.

### 3.5. Integração dos KPIs — Método de Decisão Final (MCDA)

**Objetivo:** Consolidar os resultados heterogêneos dos KPIs em uma recomendação quantitativa.

**Tarefas e Implementações:**
*   **3.5.1. Normalização dos KPIs:**
    *   **Implementação:** Aplicar normalização (min-max ou z-score) para tornar os KPIs comparáveis.
*   **3.5.2. Definição de Pesos:**
    *   **Implementação:** Realizar workshop com stakeholders para atribuir pesos a cada KPI (ex: Tempo de Entrega: 40%, Potencial de Consumo: 30%, Custos Operacionais: 20%, Imobiliário: 10%). Documentar justificativas.
*   **3.5.3. Aplicação do Método TOPSIS:**
    *   **Implementação:** Calcular o score final para Recife e Salvador usando o método TOPSIS (Technique for Order Preference by Similarity to Ideal Solution).
*   **3.5.4. Análise de Sensibilidade:**
    *   **Implementação:** Avaliar como o score final muda com variações nos pesos dos KPIs.

### 3.6. Reprodutibilidade, Validação e Governança

**Objetivo:** Garantir a robustez, rastreabilidade e qualidade das análises e modelos.

**Tarefas e Implementações:**
*   **3.6.1. Versionamento de Experimentos:**
    *   **Ferramentas:** `MLflow`.
    *   **Implementação:** Rastrear modelos, parâmetros, métricas e artefatos de cada experimento.
*   **3.6.2. Versionamento de Código:**
    *   **Ferramentas:** `GitHub`.
    *   **Implementação:** Manter todo o código (scripts Python, notebooks, DAGs Airflow) versionado.
*   **3.6.3. Testes e Validação:**
    *   **Ferramentas:** `pytest` (para unit tests).
    *   **Implementação:** Desenvolver unit tests para transformações de dados. Realizar backtests e validação cruzada para modelos preditivos.
*   **3.6.4. Documentação:**
    *   **Ferramentas:** `Jupyter Notebooks`, `Markdown`.
    *   **Implementação:** Criar notebooks com narrativa clara para documentar análises. Gerar relatórios técnicos.
*   **3.6.5. Governança de Dados:**
    *   **Implementação:** Registrar origem e licença de cada dado. Garantir anonimização de dados sensíveis. Definir planos de atualização e refresh dos dados.

---

## Etapa 4: Visualização e Comunicação dos Resultados

**Objetivo:** Transformar as análises em dashboards interativos e uma comunicação executiva estratégica.

### 4.1. BI e Visualização Interativa (Etapa 4A)

**Objetivo:** Criar dashboards que permitam a exploração interativa dos resultados pelos gestores.

**Tarefas e Implementações:**
*   **4.1.1. Dashboard 1 – Visão Geral (Executivo):**
    *   **Ferramentas:** `Metabase` ou `Streamlit`.
    *   **Conteúdo:** Comparativo Recife vs Salvador para todos os KPIs (Tempo de Entrega, Custo Imobiliário, Potencial de Consumo, Custo Operacional Total), Score Final (MCDA – TOPSIS).
    *   **Implementação:** Conectar Metabase ao PostgreSQL/PostGIS. Desenvolver dashboard Streamlit com gráficos `Matplotlib`/`Seaborn`/`Plotly`.
*   **4.1.2. Dashboard 2 – Logística e Entregas:**
    *   **Ferramentas:** `Metabase` ou `Streamlit` com `Folium`.
    *   **Conteúdo:** Mapa interativo com isócronas (4h, 8h, 12h), rotas otimizadas, tabela de tempos médios e custos de transporte por capital. Filtro por cidade.
    *   **Implementação:** Integrar mapas Folium no Streamlit. Criar queries no Metabase para dados de rotas.
*   **4.1.3. Dashboard 3 – Mercado e Consumo:**
    *   **Ferramentas:** `Metabase` ou `Streamlit` com `Plotly`.
    *   **Conteúdo:** Mapa de calor com potencial de consumo por microrregião, clusterização de perfis de consumidores, comparativo de receita potencial.
    *   **Implementação:** Visualizações de mapas choropleth e gráficos de barras/pizza para clusters.
*   **4.1.4. Dashboard 4 – Custos Operacionais:**
    *   **Ferramentas:** `Metabase` ou `Streamlit`.
    *   **Conteúdo:** Gráfico empilhado de componentes de custo (Transporte, Mão de Obra, Energia, Imobiliário). Simulação interativa de impacto de variáveis (combustível, salários).
    *   **Implementação:** Gráficos de barras empilhadas e sliders para simulação no Streamlit.
*   **4.1.5. Dashboard 5 – Cenários de Decisão (Simulação Interativa):**
    *   **Ferramentas:** `Streamlit`.
    *   **Conteúdo:** Input de pesos dos KPIs (sliders), recalcular score TOPSIS em tempo real, visualização em radar chart. Exportação de relatórios.
    *   **Implementação:** Interface Streamlit para interação com o modelo TOPSIS.

### 4.2. Comunicação Executiva (Etapa 4B)

**Objetivo:** Transformar os insights em storytelling estratégico para a diretoria, com recomendações claras.

**Tarefas e Implementações:**
*   **4.2.1. Roteiro de Apresentação (Estilo PowerPoint):**
    *   **Conteúdo:** Slides para Abertura, Contexto do Projeto, Metodologia, KPIs Avaliados, Resultados (comparativo Recife vs Salvador), Simulação Multi-Critério (TOPSIS), Recomendação Final, Próximos Passos.
    *   **Implementação:** Criar estrutura de slides com os principais pontos e visualizações dos dashboards.
*   **4.2.2. Relatório Executivo (Whitepaper):**
    *   **Conteúdo:** Contexto, Metodologia, KPIs Avaliados, Resultados Detalhados, Integração Multi-Critério, Recomendação, Próximos Passos.
    *   **Implementação:** Redigir um documento formal e detalhado, com gráficos e tabelas relevantes, explicando a análise e a recomendação de forma clara e concisa.

---

## Avaliação Geral do Planejamento

O planejamento apresentado é **robusto, abrangente e bem estruturado**, cobrindo todas as fases essenciais de um projeto de análise de dados e decisão estratégica. A escolha por ferramentas **Open Source** é um ponto forte, garantindo flexibilidade e escalabilidade sem custos de licenciamento. A metodologia de 


dividir para conquistar" é aplicada de forma eficaz, quebrando o projeto em tarefas gerenciáveis e bem definidas. A inclusão de detalhes sobre tecnologias, implementações e até snippets de código demonstra um entendimento profundo das necessidades técnicas.

**Pontos Fortes:**

*   **Clareza e Detalhamento:** Cada etapa e sub-etapa é bem explicada, com objetivos, tarefas, ferramentas e implementações específicas.
*   **Foco em Open Source:** A adesão a ferramentas open source é consistente e bem justificada.
*   **Metodologia Abrangente:** Aborda desde a coleta de dados até a comunicação executiva, passando por ETL, modelagem avançada (geoespacial, estatística, otimização) e integração de KPIs.
*   **Governança e Reprodutibilidade:** A inclusão de MLflow, GitHub, Airflow e testes unitários garante a robustez e a capacidade de auditoria do projeto.
*   **Comunicação Dupla:** A estratégia de documentação técnica e executiva, juntamente com dashboards interativos e apresentações, assegura que todos os stakeholders sejam bem informados.

**Sugestões de Melhoria/Considerações:**

*   **Disponibilidade de Dados:** Embora o plano mencione fontes abertas, a obtenção de dados de tráfego em tempo real ou dados muito específicos de consumo de e-commerce pode ser um desafio. A mitigação com simulações de Monte Carlo é boa, mas é importante ter clareza sobre a granularidade e a confiabilidade dos dados de entrada.
*   **Escalabilidade do OSRM:** A menção de Docker e Kubernetes para escalar o OSRM é pertinente, mas a complexidade de gerenciar essa infraestrutura deve ser considerada no cronograma, especialmente se a equipe for pequena.
*   **Validação com Dados Reais:** Se possível, a validação dos modelos de tempo de entrega e custos operacionais com dados históricos reais do Magalu (mesmo que anonimizados) seria um diferencial significativo para aumentar a confiança nas projeções.
*   **Engajamento dos Stakeholders:** A definição de pesos para o TOPSIS via workshop é crucial. É importante garantir que os stakeholders entendam as implicações de cada peso na decisão final.

**Conclusão:**

Este planejamento é um excelente roteiro para o projeto, demonstrando uma abordagem madura e técnica para a resolução de um problema de negócio complexo. A estrutura detalhada e a escolha de ferramentas adequadas garantem que o projeto possa ser executado de forma eficiente e com resultados confiáveis. A equipe de desenvolvimento terá um guia claro para seguir, minimizando ambiguidades e acelerando a implementação.



