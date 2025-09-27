# Relatório Técnico Detalhado: Análise de Localização para Novo CD Magalu Nordeste

**Autores:** [Lucas Gomes Leria](https://www.linkedin.com/in/lucasleria/)  
**Data:** 27 de Setembro de 2025  
**Versão:** 1.0  

## Sumário/Índice

1.  Resumo Executivo
2.  Introdução  
    2.1. Contextualização e Problema  
3.  Metodologia e Materiais  
    3.1. Etapa 1: Planejamento e Definição    
        3.1.1. Validação dos KPIs Propostos  
        3.1.2. Plano Detalhado do Projeto  
        3.1.3. Avaliação das Ferramentas e Bibliotecas (Open Source)  
        3.1.4. Documentação Técnica e Executiva  
    3.2. Etapa 2: Coleta, Pré-processamento e Armazenamento de Dados (ETL)  
        3.2.1. Coleta de Dados  
        3.2.2. Pré-processamento (Limpeza e Transformação)  
        3.2.3. Armazenamento dos Dados  
        3.2.4. Fluxo ETL (Arquitetura de Dados)  
    3.3. Etapa 3: Análise, Modelagem e Otimização  
        3.3.1. KPI 1 — Tempo Médio de Entrega (Eficiência Logística)  
        3.3.2. KPI 2 — Custo de Aquisição Imobiliária (CapEx)  
        3.3.3. KPI 3 — Potencial de Consumo da Região (Demanda / Market Potential)  
        3.3.4. KPI 4 — Custo Operacional Total (TCO por Pedido)  
        3.3.5. Integração dos KPIs — Método de Decisão Final (MCDA)  
        3.3.6. Reprodutibilidade, Validação e Governança  
    3.4. Etapa 4: Visualização e Comunicação dos Resultados  
        3.4.1. Construção de Dashboards Interativos  
        3.4.2. Elaboração de Relatório Executivo e Preparação de Apresentação para Stakeholders  
4.  Resultados  
    4.1. Resultados da Etapa 1  
    4.2. Resultados da Etapa 2  
    4.3. Resultados da Etapa 3  
    4.4. Resultados da Etapa 4 (Dashboard Streamlit)  
5.  Discussão  
    5.1. Interpretação dos Resultados  
    5.2. Limitações do Estudo e Pontos de Atenção  
6.  Conclusões  
7.  Recomendações  
8.  Referências Bibliográficas  
9.  Apêndices e Anexos  

## 1. Resumo Executivo

Este relatório técnico detalha o processo de análise para determinar a localização mais estratégica para um novo Centro de Distribuição (CD) do Magalu no Nordeste, comparando Salvador e Recife. O projeto foi estruturado em quatro etapas: Planejamento e Definição, Coleta e Pré-processamento de Dados (ETL), Análise, Modelagem e Otimização, e Visualização e Comunicação dos Resultados. Utilizamos uma abordagem baseada em KPIs (Tempo Médio de Entrega, Custo de Aquisição Imobiliária, Potencial de Consumo da Região e Custo Operacional Total) e um método de Análise de Decisão Multicritério (MCDA - TOPSIS) para consolidar as avaliações. Os dados foram coletados de fontes abertas e processados para alimentar modelos preditivos e análises geoespaciais. A interface de visualização foi desenvolvida em Streamlit, permitindo a interação com os resultados e a simulação de cenários. A análise final, com pesos definidos por stakeholders, aponta Salvador como a localização mais estratégica, embora a decisão seja sensível à priorização do tempo de entrega. Este documento descreve as metodologias, ferramentas e implementações técnicas em cada etapa, bem como os resultados obtidos e as recomendações para futuras melhorias.

## 2. Introdução

### 2.1. Contextualização e Problema

A expansão e otimização da rede logística são cruciais para a competitividade no setor de varejo, especialmente em um mercado tão dinâmico quanto o brasileiro. O Magalu, buscando agilizar suas entregas e fortalecer sua presença no Nordeste, identificou a necessidade de estabelecer um novo Centro de Distribuição (CD) na região. A decisão estratégica recaiu sobre a escolha entre duas capitais: Salvador e Recife, ambas com potenciais e desafios distintos. O objetivo deste projeto foi fornecer uma análise robusta e baseada em dados para fundamentar essa decisão, respondendo a questões chave como a localização mais estratégica, os fatores que sustentam essa escolha e as metodologias empregadas. A complexidade da decisão exige a integração de múltiplos fatores, desde custos e eficiência logística até o potencial de mercado e a capacidade operacional, o que justifica a abordagem multicritério adotada.

## 3. Metodologia e Materiais

O projeto foi estruturado em quatro etapas principais, cada uma com objetivos e implementações técnicas específicas, conforme detalhado no documento `STEP-BY-STEP.MD`.

### 3.1. Etapa 1: Planejamento e Definição

Esta etapa inicial focou em estabelecer as bases do projeto, garantindo que os objetivos e a abordagem estivessem claramente definidos e alinhados.

#### 3.1.1. Validação dos KPIs Propostos

Foram definidos quatro Key Performance Indicators (KPIs) como métricas centrais para a avaliação das cidades, garantindo que fossem relevantes, mensuráveis e alinhados aos objetivos estratégicos do Magalu. Os KPIs validados são:

*   **Tempo Médio de Entrega (Eficiência Logística):** Medido em horas, representa a agilidade na distribuição para as principais capitais e cidades estratégicas da região.
*   **Custo de Aquisição Imobiliária (Investimento Inicial - CAPEX):** Reflete o preço médio por m² de terrenos e galpões industriais, bem como o custo total de aquisição em cada cidade.
*   **Potencial de Consumo da Região (Receita Esperada):** Quantifica a receita projetada com base em indicadores demográficos e de consumo.
*   **Custo Operacional Total (Rentabilidade - OPEX por Pedido):** Estima o custo médio por pedido, incluindo componentes logísticos, mão de obra, energia e custos fixos.

#### 3.1.2. Plano Detalhado do Projeto

O plano detalhou a estrutura do projeto em quatro etapas, atribuiu responsabilidades (Analista A para ETL, análise de custos e modelagem preditiva; Analista B para análise logística, simulação OSRM e mapas interativos), estabeleceu um cronograma estimado (total de ~30 a 40 dias) e definiu os entregáveis: Relatório Técnico Detalhado, Relatório Executivo e Dashboard Interativo.

#### 3.1.3. Avaliação das Ferramentas e Bibliotecas (Open Source)

Uma seleção criteriosa de ferramentas e bibliotecas open source foi realizada para suportar todas as fases do projeto. As principais incluem:

*   **Gestão e Colaboração:** Trello, Notion, Slack, GitHub.
*   **Coleta e ETL:** Python (Requests, BeautifulSoup/Scrapy, Pandas, NumPy), PostgreSQL + PostGIS, GeoPandas.
*   **Análise, Modelagem e Otimização:** GeoPandas, NetworkX, OSRM, Scikit-learn, Statsmodels, XGBoost, OR-Tools, SHAP, NumPy (para Monte Carlo).
*   **Visualização e Comunicação:** Matplotlib, Seaborn, Plotly, Folium, Kepler.gl, Streamlit (prototipagem), Metabase (execução final).
*   **Documentação e Reprodutibilidade:** Jupyter Notebooks, Markdown, LaTeX, MLflow.
*   **Infraestrutura (Escala):** Docker, Kubernetes, Apache Airflow, Prometheus + Grafana.

#### 3.1.4. Documentação Técnica e Executiva

Foi definida a estrutura para dois tipos de documentação: técnica (detalhes de dados, scripts, modelos, versionamento) e executiva (resumo, KPIs, gráficos, conclusão, storytelling), visando atender a diferentes públicos.

### 3.2. Etapa 2: Coleta, Pré-processamento e Armazenamento de Dados (ETL)

Esta etapa focou na construção de uma base de dados confiável e integrada a partir de fontes abertas.

#### 3.2.1. Coleta de Dados

*   **`Etapa2_1_1_collect_real_estate_data.py` (Coleta de Custos Imobiliários):** Utiliza `requests`, `BeautifulSoup` e `Selenium` para realizar web scraping de portais de imóveis (Zap Imóveis, Viva Real, OLX) em Salvador e Recife, coletando dados como preço, área e endereço. Este script é crucial para o KPI de Custo de Aquisição Imobiliária.
*   **`Etapa2_1_2_collect_road_network_data.py` (Coleta de Malha Viária e Tempos de Entrega):** Consulta a `Overpass API` para extrair dados do OpenStreetMap e interage com o `OSRM` (Open Source Routing Machine) para calcular distâncias e tempos de viagem entre as capitais do Nordeste. Inclui um mecanismo de fallback com simulação em caso de falha do OSRM. Este script alimenta o KPI de Tempo Médio de Entrega.
*   **`Etapa2_1_3_collect_demographic_data.py` (Coleta de Demografia e Potencial de Consumo):** Realiza requisições à API do IBGE para obter dados demográficos (população, PIB per capita, rendimento familiar) e inclui uma função de simulação para garantir a execução mesmo com indisponibilidade da API. Os dados coletados são fundamentais para o KPI de Potencial de Consumo da Região.

#### 3.2.2. Pré-processamento (Limpeza e Transformação)

*   **`Etapa2_2_1_preprocess_real_estate_data.py` (Pré-processamento de Dados Imobiliários):** Utiliza `Pandas` para limpar, normalizar e transformar os dados imobiliários brutos. Realiza a conversão de unidades, tratamento de valores ausentes, extração de CEP e georreferenciamento de endereços usando `geopy`, convertendo-os em coordenadas latitude/longitude. Este script prepara os dados para o KPI de Custo de Aquisição Imobiliária.
*   **`Etapa2_2_2_preprocess_road_network_data.py` (Pré-processamento de Dados de Malha Viária):** Processa os dados de rotas, adicionando coordenadas geográficas e criando GeoDataFrames com `Pandas` e `GeoPandas`. Facilita a integração e análise geoespacial dos dados de tempo de entrega.
*   **`Etapa2_2_3_5_preprocess_demographic_data.py` (Pré-processamento de Dados Demográficos):** Limpa, converte e padroniza os dados demográficos coletados, utilizando `Pandas`. Calcula o potencial de consumo e cria chaves unificadas para integração com outros datasets, preparando os dados para o KPI de Potencial de Consumo.

#### 3.2.3. Armazenamento dos Dados

*   **`Etapa2_3_1_2_create_db_schema.py` (Criação do Esquema do Banco de Dados):** Conecta-se a um banco de dados PostgreSQL, cria o banco `magalu_cd_analysis` (se necessário), habilita a extensão PostGIS e define o esquema das tabelas (`imoveis`, `rotas`, `demografia`, `consumo_potencial`, `estatisticas_comparativas`), incluindo colunas geométricas para dados espaciais.
*   **`Eteta2_3_3_load_data_to_db.py` (Carregamento de Dados no Banco):** Utiliza `psycopg2` e `Pandas` para carregar os dados processados de imóveis, malha viária, demográficos e potencial de consumo nas tabelas correspondentes do PostgreSQL, garantindo a persistência e acessibilidade dos dados.

#### 3.2.4. Fluxo ETL (Arquitetura de Dados)

*   **`Etapa2_4_magalu_etl_dag.py` (DAG do Apache Airflow):** Este script define um Directed Acyclic Graph (DAG) para orquestrar o pipeline ETL. Ele integra as tarefas de coleta, pré-processamento e carregamento de dados em uma sequência lógica, garantindo a automação e o monitoramento do fluxo de dados. As funções dentro do DAG chamam os scripts Python individuais para cada etapa.
*   **`ANALISE_DO_DAG.MD`:** Documenta a execução e validação do pipeline ETL, destacando sucessos, observações e pontos de atenção, como a necessidade de ajustes no scraping e o uso de simulação devido a problemas de API.

### 3.3. Etapa 3: Análise, Modelagem e Otimização

Esta etapa aplicou técnicas avançadas para responder aos KPIs e consolidar a decisão.

#### 3.3.1. KPI 1 — Tempo Médio de Entrega (Eficiência Logística)

*   **`Etapa3.1_analyze_delivery_time.py`:** Realiza a análise do tempo de entrega. Calcula estatísticas (média, mediana, percentis), simula incertezas via Monte Carlo, constrói um grafo da malha viária com `NetworkX` para análise de centralidade e gera isócronas com `GeoPandas` e `Shapely` para visualizar áreas de alcance em diferentes tempos de viagem. Depende dos dados processados da malha viária da Etapa 2.

#### 3.3.2. KPI 2 — Custo de Aquisição Imobiliária (CapEx)

*   **`Etapa3.2_analyze_real_estate_cost.py`:** Pré-processa dados imobiliários, treina um modelo hedônico (utilizando `GradientBoostingRegressor` do `Scikit-learn`) para estimar o preço por m² com base em características do imóvel. Calcula o custo total de aquisição (CAPEX) para as cidades, incluindo custos de transação e adaptação. Utiliza dados imobiliários processados da Etapa 2.

#### 3.3.3. KPI 3 — Potencial de Consumo da Região (Demanda / Market Potential)

*   **`Etapa3.3_analyze_consumption_potential.py`:** Carrega e pré-processa dados demográficos, realiza clusterização de regiões com `KMeans` (`Scikit-learn`), treina um modelo preditivo de consumo (`XGBRegressor`) e estima o potencial de receita incremental. Inclui a utilização de `SHAP` para interpretar a importância das features no modelo. Utiliza dados demográficos processados da Etapa 2.

#### 3.3.4. KPI 4 — Custo Operacional Total (TCO por Pedido)

*   **`Etapa3.4_analyze_operational_cost.py`:** Calcula o custo operacional total por pedido, considerando CAPEX amortizado, custo de mão de obra, energia e transporte. Simula a roteirização de frota (com um esqueleto para integração futura com `OR-Tools`) e integra resultados dos KPIs anteriores (tempo de entrega e custo imobiliário) para uma análise abrangente dos custos operacionais.

#### 3.3.5. Integração dos KPIs — Método de Decisão Final (MCDA)

*   **`Etapa3.5_integrate_kpis_mcda.py`:** Este script é central para a tomada de decisão. Ele carrega os resultados dos KPIs individuais, normaliza os valores (min-max), aplica pesos definidos pelos stakeholders e calcula o score TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) para cada cidade. Realiza também uma análise de sensibilidade para avaliar a robustez da decisão frente a variações nos pesos. Os pesos foram atualizados para refletir a prioridade estratégica de 40% para Potencial de Consumo, e 20% para os demais KPIs.
*   **`ANALISE_DOS_KPIS_MCDA.MD`:** Documenta a análise detalhada dos resultados do MCDA, incluindo o ranking, a polarização dos dados, a sensibilidade aos pesos e as recomendações de negócio. Este documento foi atualizado para refletir os pesos definidos pelos stakeholders e os resultados recalculados.

#### 3.3.6. Reprodutibilidade, Validação e Governança

*   **`Etapa3.6_reproducibility_validation.py`:** Configura o rastreamento de experimentos com `MLflow`, carrega e combina dados processados (incluindo geração de dados sintéticos para treinamento de modelos em cenários de escassez de dados reais). Executa experimentos de ML (Gradient Boosting e XGBoost) para previsão de potencial de consumo e custo operacional, registrando métricas e modelos para garantir a reprodutibilidade e rastreabilidade.
*   **`Etapa3.6.2_utilize_ml_models.py`:** Demonstra a utilização dos modelos de machine learning treinados. Carrega modelos do MLflow, prepara dados para previsão, realiza previsões e analisa a importância das features. Compara as cidades com base nas previsões e gera insights de negócio, fechando o ciclo de aplicação dos modelos de ML.

### 3.4. Etapa 4: Visualização e Comunicação dos Resultados

Esta etapa visa apresentar os resultados de forma clara e interativa.

#### 3.4.1. Construção de Dashboards Interativos

*   **`app.py` (Dashboard Streamlit):** Este é o principal entregável interativo da Etapa 4. Desenvolvido com `Streamlit`, ele integra todos os resultados das etapas anteriores em um dashboard web. Permite a exploração dos KPIs individuais, visualização de mapas (isócronas, consumo), comparação de cidades e, crucialmente, a interação com a análise MCDA através de sliders para ajustar os pesos dos KPIs e recalcular o score TOPSIS em tempo real. Inclui gráficos de radar para comparação visual e funcionalidade de exportação de resultados. O `app.py` atua como um protótipo funcional para a comunicação dos resultados.

#### 3.4.2. Elaboração de Relatório Executivo e Preparação de Apresentação para Stakeholders

Embora o `app.py` seja uma ferramenta de visualização, ele serve como base para a elaboração do Relatório Executivo e a preparação de apresentações. Os insights e visualizações gerados pelo dashboard são essenciais para compor esses documentos, que são focados na visão de negócio e na recomendação final.

## 4. Resultados

### 4.1. Resultados da Etapa 1

A Etapa 1 resultou na validação dos KPIs, na definição de um plano de projeto detalhado, na seleção de um robusto conjunto de ferramentas e bibliotecas open source, e na estruturação da documentação técnica e executiva. Todos os artefatos desta etapa estão totalmente alinhados com o planejamento inicial, fornecendo uma base sólida para o projeto.

### 4.2. Resultados da Etapa 2

A Etapa 2 estabeleceu o pipeline ETL para coleta, pré-processamento e armazenamento de dados. Scripts Python foram desenvolvidos para coletar dados imobiliários (web scraping), malha viária (OSRM/Overpass API) e demográficos (IBGE), com mecanismos de simulação para robustez. Os dados foram limpos, transformados (incluindo georreferenciamento) e carregados em um banco de dados PostgreSQL/PostGIS. Um DAG do Apache Airflow (`Etapa2_4_magalu_etl_dag.py`) foi projetado para orquestrar este pipeline. Pontos de atenção identificados incluem a necessidade de melhorar a robustez do web scraping e a dependência de dados simulados devido a falhas de API.

### 4.3. Resultados da Etapa 3

A Etapa 3 focou na análise e modelagem avançada. Scripts foram desenvolvidos para analisar cada KPI individualmente: `Etapa3.1_analyze_delivery_time.py` (tempo de entrega, isócronas), `Etapa3.2_analyze_real_estate_cost.py` (custo imobiliário, modelo hedônico), `Etapa3.3_analyze_consumption_potential.py` (potencial de consumo, clusterização, modelo preditivo com SHAP) e `Etapa3.4_analyze_operational_cost.py` (custo operacional, simulação de frota). A integração final dos KPIs foi realizada pelo `Etapa3.5_integrate_kpis_mcda.py` usando TOPSIS, com pesos definidos pelos stakeholders (40% Potencial de Consumo, 20% para os demais). A análise de sensibilidade revelou que Salvador é a cidade mais estratégica na maioria dos cenários, com um score TOPSIS de 0.710 contra 0.290 para Recife, embora a decisão seja sensível à priorização do tempo de entrega. A reprodutibilidade foi garantida com `MLflow` (`Etapa3.6_reproducibility_validation.py`, `Etapa3.6.2_utilize_ml_models.py`).

### 4.4. Resultados da Etapa 4 (Dashboard Streamlit)

O `app.py` desenvolvido em Streamlit serve como a interface interativa para explorar todos os resultados do projeto. Ele apresenta uma visão geral comparativa das cidades, seções detalhadas para cada KPI com visualizações específicas (gráficos de barras, mapas, tabelas) e uma seção de "Cenários de Decisão (TOPSIS)" onde os usuários podem ajustar os pesos dos KPIs e observar o impacto na recomendação final em tempo real, visualizado através de um gráfico de radar. Este dashboard é uma ferramenta poderosa para a comunicação e validação dos resultados com stakeholders não-técnicos.

## 5. Discussão

### 5.1. Interpretação dos Resultados

A análise multicritério, com os pesos definidos pelos stakeholders, indica claramente **Salvador como a localização mais estratégica** para o novo CD do Magalu no Nordeste. Esta recomendação é impulsionada principalmente pelo maior peso atribuído ao Potencial de Consumo da Região, onde Salvador demonstra uma vantagem significativa. Embora Recife apresente vantagens em Custo de Aquisição Imobiliária e Custo Operacional Total (com base nos dados simulados), a priorização do potencial de mercado pelos stakeholders inclina a balança para Salvador.

A análise de sensibilidade reforça esta conclusão, mostrando que Salvador é a vencedora em 5 dos 7 cenários testados, resultando em um score de robustez de 71.4%. No entanto, a análise também revelou que a decisão é sensível ao peso do Tempo Médio de Entrega: se este KPI receber uma prioridade muito alta (acima de 40%), Recife pode se tornar a opção preferencial. Isso sublinha a importância da definição de pesos alinhada à estratégia de negócio.

### 5.2. Limitações do Estudo e Pontos de Atenção

*   **Qualidade dos Dados de Entrada:** Uma limitação significativa é a dependência de dados simulados ou mock para alguns KPIs (especialmente demográficos e de malha viária) devido a desafios na coleta de dados reais (problemas com APIs, web scraping). Isso pode introduzir incertezas nos resultados. A polarização observada na normalização dos dados também é um sintoma dessa limitação.
*   **Complexidade da Simulação de Frota:** A simulação de roteirização de frota no KPI de Custo Operacional (`Etapa3.4_analyze_operational_cost.py`) é um esqueleto e não integra plenamente ferramentas de otimização como `OR-Tools`, o que poderia refinar as estimativas de custo.
*   **Implementação do Airflow:** Embora um DAG tenha sido projetado, a verificação da sua implantação e funcionamento em um ambiente real do Apache Airflow, bem como a containerização dos jobs, não foi explicitamente demonstrada.
*   **Metabase:** O `app.py` é um protótipo em Streamlit. A transição para uma ferramenta de BI de produção como Metabase para a execução final dos dashboards ainda é uma etapa a ser realizada.
*   **Fatores Qualitativos:** O estudo focou em aspectos quantitativos. Fatores qualitativos como riscos operacionais, qualidade da infraestrutura local, disponibilidade de mão de obra qualificada e incentivos fiscais não foram explicitamente incorporados na análise MCDA, mas são cruciais para a decisão final.

## 6. Conclusões

O projeto forneceu uma análise abrangente e metodologicamente robusta para a escolha da localização do novo CD do Magalu no Nordeste. Através da integração de dados, modelagem avançada e análise multicritério, foi possível quantificar o desempenho de Salvador e Recife em relação a KPIs estratégicos. A recomendação final, baseada nos pesos definidos pelos stakeholders, aponta para Salvador como a opção mais vantajosa. O dashboard interativo em Streamlit é uma ferramenta eficaz para explorar e comunicar esses resultados.

## 7. Recomendações

Com base nas análises e limitações identificadas, as seguintes recomendações são propostas:

1.  **Priorizar a Melhoria da Coleta de Dados:** Investir no aprimoramento dos scripts de web scraping, tratamento de erros de API e georreferenciamento para substituir dados simulados por dados reais e de alta qualidade. Isso aumentará a confiança e a precisão de todas as análises.
2.  **Implementar Otimização de Roteirização:** Integrar plenamente a biblioteca `OR-Tools` no script `Etapa3.4_analyze_operational_cost.py` para simular roteiros de frota de forma mais precisa e otimizada, refinando as estimativas de custo operacional.
3.  **Validar a Implantação do Airflow:** Assegurar que o DAG do Apache Airflow esteja implantado e funcionando corretamente em um ambiente de produção, com monitoramento adequado e jobs containerizados.
4.  **Transição para Metabase (Produção):** Replicar ou migrar os dashboards do Streamlit para o Metabase, conforme planejado, para a execução final e acesso contínuo pelos usuários de negócio.
5.  **Análise Qualitativa Complementar:** Realizar uma análise aprofundada dos fatores qualitativos não incluídos nos KPIs para fornecer uma visão mais holística e mitigar riscos não quantificados.
6.  **Revisar Normalização MCDA:** Explorar métodos de normalização alternativos para o TOPSIS que possam oferecer maior nuance em cenários com poucas alternativas, reduzindo a polarização extrema.

## 8. Referências Bibliográficas

*   `STEP-BY-STEP.MD` - Documento de Planejamento do Projeto.
*   Relatórios de Alinhamento das Etapas 1, 2, 3 e 4.
*   Documentação das bibliotecas Python utilizadas (Pandas, NumPy, Scikit-learn, XGBoost, Streamlit, Plotly, etc.).
*   Documentação do OSRM, Overpass API, IBGE API.

## 9. Apêndices e Anexos

*   `Etapa2_1_1_collect_real_estate_data.py`
*   `Etapa2_1_2_collect_road_network_data.py`
*   `Etapa2_1_3_collect_demographic_data.py`
*   `Etapa2_2_1_preprocess_real_estate_data.py`
*   `Etapa2_2_2_preprocess_road_network_data.py`
*   `Etapa2_2_3_5_preprocess_demographic_data.py`
*   `Etapa2_3_1_2_create_db_schema.py`
*   `Etapa2_3_3_load_data_to_db.py`
*   `Etapa2_4_magalu_etl_dag.py`
*   `Etapa3.1_analyze_delivery_time.py`
*   `Etapa3.2_analyze_real_estate_cost.py`
*   `Etapa3.3_analyze_consumption_potential.py`
*   `Etapa3.4_analyze_operational_cost.py`
*   `Etapa3.5_integrate_kpis_mcda.py`
*   `Etapa3.6_reproducibility_validation.py`
*   `Etapa3.6.2_utilize_ml_models.py`
*   `app.py`
*   `ANALISE_DO_DAG.MD`
*   `ANALISE_DOS_KPIS_MCDA.MD`
*   `contexto_reuniao_stakeholders.md`
*   `melhorias_streamlit_nao_tecnicos.md`
*   `modificacoes_necessarias_kpi_pesos.md`
*   `relatorio_alinhamento_etapa1.md`
*   `relatorio_alinhamento_etapa2.md`
*   `relatorio_alinhamento_etapa3.md`
*   `relatorio_alinhamento_etapa4.md`


