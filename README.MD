# 📊 Análise de Localização para Novo CD Magalu Nordeste

**Projeto de Análise de Dados para Decisão Estratégica de Localização de Centro de Distribuição no Nordeste do Brasil.**

[![Licença](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0-green.svg)]()
[![Status](https://img.shields.io/badge/status-concluído-green.svg)]()
[![deploy](https://img.shields.io/badge/deploy-Streamlit-blue.svg)](https://estudo-de-caso-magalu2025.streamlit.app/) 

---

Acesse [aqui](https://estudo-de-caso-magalu2025.streamlit.app/) visualização online da análise.   
Acesse [aqui](ETAPA4\Relatorio_Tecnico.pdf) o Relatório Executivo  
Acesse [aqui](ETAPA4\Relatório_Executivo.pdf) o Relatório Técnico   
Acesse [aqui]() a Apresentação em Slides  


## 📌 Sumário

1. [Sobre o Projeto](#-sobre-o-projeto)
2. [Objetivos](#-objetivos)
3. [Tecnologias](#-tecnologias)
4. [Funcionalidades](#-funcionalidades)
5. [Pré-requisitos](#%EF%B8%8F-pré-requisitos)
6. [Instalação](#%EF%B8%8F-instalação)
7. [Como Utilizar](#-como-utilizar)
8. [Estrutura do Projeto](#-estrutura-do-projeto)
9. [Licença](#-licença)
10. [Contato](#-contato)
11. [Recursos Adicionais](#-recursos-adicionais)

## 💻 Sobre o Projeto

Este projeto é um estudo de caso detalhado para o Magazine Luiza (Magalu), focado na decisão estratégica de onde localizar um novo Centro de Distribuição (CD) na região Nordeste do Brasil. O objetivo principal é determinar qual cidade — Recife ou Salvador — apresenta a localização mais vantajosa para agilizar as entregas e fortalecer a presença de mercado do Magalu, utilizando uma abordagem baseada em dados e inteligência artificial.

O projeto foi desenvolvido em quatro etapas principais: Planejamento e Definição, Coleta e Pré-processamento de Dados (ETL), Análise, Modelagem e Otimização, e Visualização e Comunicação dos Resultados. Utiliza-se uma metodologia de Análise de Decisão Multicritério (MCDA - TOPSIS) para consolidar a avaliação de KPIs como Tempo Médio de Entrega, Custo de Aquisição Imobiliária, Potencial de Consumo da Região e Custo Operacional Total. Os resultados são apresentados através de um dashboard interativo desenvolvido em Streamlit, que permite a exploração de cenários e a simulação de diferentes prioridades. Também foram elaborados dois relatórios, um técnico e outro Executivo.

-   **Motivação**: Fornecer uma base analítica robusta para decisões de alto impacto no varejo, otimizando a logística e a expansão de mercado.
-   **Público-alvo**: Diretores, gerentes de logística, analistas de negócios e cientistas de dados.

## 🎯 Objetivos

### 📈 Estratégicos
-   Determinar a localização mais estratégica (Recife ou Salvador) para o novo CD do Magalu no Nordeste.
-   Identificar os principais fatores que sustentam essa decisão, com base em dados e análises.
-   Fornecer uma ferramenta interativa para a equipe de negócios explorar cenários e entender a sensibilidade da decisão.

### 🛠️ Técnicos
-   Implementar um pipeline ETL robusto para coleta, pré-processamento e armazenamento de dados de fontes abertas.
-   Aplicar modelos estatísticos e de Machine Learning para análise de KPIs (tempo de entrega, custos, potencial de consumo).
-   Utilizar o método TOPSIS para Análise de Decisão Multicritério, integrando os resultados dos KPIs.
-   Desenvolver um dashboard interativo com Streamlit para visualização e simulação de cenários.
-   Garantir a reprodutibilidade das análises e a rastreabilidade dos experimentos.

## 🚀 Tecnologias

**Linguagens e Frameworks**
-   Python (principal)
-   Streamlit (para o dashboard interativo)

**Bibliotecas e Ferramentas**
-   `Pandas`, `NumPy`, `GeoPandas` (Manipulação e Análise de Dados)
-   `Requests`, `BeautifulSoup`, `Selenium` (Web Scraping e Coleta de Dados)
-   `OSRM` (Open Source Routing Machine) (Cálculo de Rotas e Tempos de Entrega)
-   `Scikit-learn`, `XGBoost`, `Statsmodels` (Modelagem Preditiva e Estatística)
-   `NetworkX`, `Shapely` (Análise Geoespacial e de Grafos)
-   `Plotly` (Visualização Interativa)
-   `psycopg2`, `PostgreSQL`, `PostGIS` (Banco de Dados e Armazenamento Espacial)
-   `Apache Airflow` (Orquestração de ETL - DAGs)
-   `MLflow` (Rastreamento de Experimentos e Reprodutibilidade)

**Outras Ferramentas**
-   `Docker` (Containerização) -- Não foi utilizado no desenvolvimento
-   `GitHub` (Versionamento de Código)
-   `Notion`, `Trello`, `Slack` (Gestão e Colaboração) -- Não foi utilizado no desenvolvimento

## ✨ Funcionalidades

-   ✅ **Coleta de Dados Automatizada:** Scripts para extrair dados de custos imobiliários, malha viária e demografia de fontes abertas.
-   ✅ **Pipeline ETL:** Processamento, limpeza e integração de dados em um banco de dados PostgreSQL/PostGIS.
-   ✅ **Análise de KPIs:** Avaliação detalhada de Tempo Médio de Entrega, Custo de Aquisição Imobiliária, Potencial de Consumo e Custo Operacional Total.
-   ✅ **Modelagem Preditiva:** Utilização de modelos de ML para estimar custos e potencial de consumo.
-   ✅ **Análise de Decisão Multicritério (MCDA):** Aplicação do método TOPSIS para ranquear as cidades com base em múltiplos critérios e pesos definidos.
-   ✅ **Análise de Sensibilidade:** Avaliação da robustez da decisão frente a variações nos pesos dos KPIs.
-   ✅ **Dashboard Interativo (Streamlit):** Interface gráfica para visualização dos resultados, comparação de cidades e simulação de cenários em tempo real.
-   ✅ **Documentação Abrangente:** Relatórios técnico e executivo detalhados, além de documentação de código.

## ⚙️ Pré-requisitos

-   Python 3.8+
-   Docker e Docker Compose (recomendado para OSRM e PostgreSQL)
-   Acesso à internet para coleta de dados e APIs
-   Ambiente de desenvolvimento Python com `pip`

## 🛠️ Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/lucasgleria/estudo-de-caso-magalu2025.git # Substitua pelo seu repositório
    cd estudo-de-caso-magalu2025
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/macOS
    # venv\Scripts\activate # Windows
    ```

3.  **Instale as dependências Python:**
    ```bash
    pip install -r requirements.txt 
    ```

4.  **Configuração do Banco de Dados (PostgreSQL/PostGIS) e OSRM (via Docker):**
    *   Este projeto assume que você terá um ambiente PostgreSQL com PostGIS e uma instância do OSRM rodando. Você pode configurá-los via Docker Compose. Exemplo de `docker-compose.yml` (simplificado):
    ```yaml
    version: '3.8'
    services:
      db:
        image: postgis/postgis:13-3.1
        environment:
          POSTGRES_DB: magalu_cd_analysis
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
        ports:
          - 

    5432:5432
          osrm:
            image: osrm/osrm-backend
            ports:
              - "5000:5000"
            volumes:
              - ./data/osrm:/data
            command: "osrm-routed --algorithm mld /data/map.osm.pbf"
    ```

    *   **Importante:** Você precisará baixar um arquivo `.osm.pbf` da região Nordeste (ou Brasil) e colocá-lo em `./data/osrm/map.osm.pbf` para o OSRM funcionar corretamente. Ferramentas como `Geofabrik` podem ser usadas para isso.

5.  **Configure as variáveis de ambiente:**
    *   Crie um arquivo `.env` na raiz do projeto com as credenciais do banco de dados e outras configurações necessárias. Exemplo:
    ```dotenv
    DB_HOST=localhost
    DB_NAME=magalu_cd_analysis
    DB_USER=user
    DB_PASSWORD=password
    DB_PORT=5432
    ```

6.  **Execute o pipeline ETL (via scripts Python ou Airflow):**
    *   Para popular o banco de dados com os dados processados, você pode executar os scripts da Etapa 2 e 3 sequencialmente, ou, se tiver o Apache Airflow configurado, utilizar o DAG `Etapa2_4_magalu_etl_dag.py`.
    *   **Exemplo de execução manual:**
        ```bash
        python ETAPA2/Etapa2_1_1_collect_real_estate_data.py
        python ETAPA2/Etapa2_1_2_collect_road_network_data.py
        python ETAPA2/Etapa2_1_3_collect_demographic_data.py
        python ETAPA2/Etapa2_2_1_preprocess_real_estate_data.py
        # ... e assim por diante para todos os scripts de ETL e análise
        ```

## ❗ Como Utilizar

Após a instalação e a execução do pipeline ETL para popular o banco de dados, você pode interagir com o Dashboard do Streamlit para explorar os resultados.

1.  **Inicie o aplicativo Streamlit:**
    ```bash
    streamlit run app.py
    ```

2.  **Acesse o Dashboard:** Abra seu navegador e navegue para o endereço exibido no terminal (geralmente `http://localhost:8501`).

### Guia Rápido do Dashboard Streamlit

O Dashboard foi projetado para ser intuitivo e permitir que a equipe de negócios explore os resultados da análise de localização do CD.

*   **Menu Lateral:** Use o menu à esquerda para navegar entre as seções:
    *   **Visão Geral:** Apresenta um resumo dos principais resultados, o ranking final das cidades (Recife vs Salvador) e gráficos comparativos dos KPIs.
    *   **KPI 1: Tempo de Entrega:** Detalhes sobre a eficiência logística, incluindo mapas de isócronas e tabelas de rotas.
    *   **KPI 2: Custo Imobiliário:** Comparativo de custos de aquisição e detalhes de imóveis.
    *   **KPI 3: Potencial de Consumo:** Análise demográfica e de mercado, com mapas de consumo e clusters.
    *   **KPI 4: Custo Operacional:** Estimativa do custo médio por pedido e detalhamento de custos.
    *   **Cenários de Decisão (TOPSIS):** **Seção mais interativa.** Aqui você pode ajustar os pesos de cada KPI usando sliders. Ao fazer isso, o ranking das cidades é recalculado em tempo real, e um gráfico de radar mostra visualmente o impacto das suas escolhas. Há também um botão para exportar os resultados recalculados.

**Dica:** A seção "Cenários de Decisão" é ideal para simular diferentes prioridades estratégicas e entender como elas afetam a recomendação final.

## 📂 Estrutura do Projeto

```plaintext
. (Visualize por um computador)
├── DOCS/
|   ├── Etapa1.md                                     # Planejamento da Etapa 1
|   ├── Etapa2.md                                     # Planejamento da Etapa 2
|   ├── Etapa3.md                                     # Planejamento da Etapa 3
|   ├── Etapa4.md                                     # Planejamento da Etapa 4
|   ├── relatorio_etapas_faltantes.md                 # Relatorio de problemas
|   ├── simulacao_reuniao_stackeholders.md            # Reuniao para definição dos KPIs
|   ├── STEP-BY-STEP.MD                               # Planejamento completo de ponta a ponta
├── ETAPA1/ 
│   ├── ALINHAMENTO.md                                # Avaliação da ETAPA 1
│   ├── Etapa_1_1_KPIs_Validados.md
│   ├── Etapa_1_2_Plano_Detalhado_do_Projeto.md
│   ├── Etapa_1_3_Avaliação_das_Ferramentas_e_Bibliotecas_Open_Source.md
│   ├── Etapa_1_4_Documentação_Executiva.md
│   ├── Etapa_1_4_Documentação_Técnica.md
├── ETAPA2/ 
│   ├── data/                                         # Pasta de dados
│   |   ├── processed/                                # Dados pós processamento
│   |   ├── raw/                                      # Dados pós coleta (brutos)
│   ├── debug/                                        # debug para scraping
│   ├── ALINHAMENTO.md                                # Avaliação da ETAPA 2
|   ├── ANALISE_DO_DAG.MD                             # Avaliação do arquivo magalu_etl_dag.py
│   ├── Etapa2_1_1_collect_real_estate_data.py        # Extrai dados dos estados
│   ├── Etapa2_1_2_collect_road_network_data.py       # Extrai dados das rodovias
│   ├── Etapa2_1_3_collect_demographic_data.py        # Extrai de dados demograficos
│   ├── Etapa2_2_1_preprocess_real_estate_data.py     # Transforma dados dos estados
│   ├── Etapa2_2_2_preprocess_road_network_data.py    # Transforma dados das rodovias
│   ├── Etapa2_2_3_5_preprocess_demographic_data.py   # Transforma dados demograficos
│   ├── Etapa2_3_1_2_create_db_schema.py              # Criar o banco de dados
│   ├── Etapa2_3_3_load_data_to_db.py                 # Carrega dados processados no bd
│   └── Etapa2_4_magalu_etl_dag.py                    # Arquivo de automação
├── ETAPA3/ 
│   ├── data/                                         # Pasta de dados
│   |   ├── analysis/                                 # Pasta de dados analisados
│   ├── mlruns/                                       # Pasta com os modelos de Machine Learning
│   ├── ALINHAMENTO.md                                # Avaliação da ETAPA 3
|   ├── ANALISE_DOS_KPIS_MCDA.MD                      # Avaliação do arquivo integrate_kpis_mcda.py
│   ├── Etapa3.1_analyze_delivery_time.py             # Analiza dados para tempo de entrega
│   ├── Etapa3.2_analyze_real_estate_cost.py          # Analiza dados de custo imobiliário
│   ├── Etapa3.3_analyze_consumption_potential.py     # Analiza dados para consumidores pontenciais
│   ├── Etapa3.4_analyze_operational_cost.py          # Analiza dados de custo operacional
│   ├── Etapa3.5_integrate_kpis_mcda.py               # Análise completa dos dados de acordo com KPIs
│   └── Etapa3.6_reproducibility_validation.py        # Criação dos modelos de Machine Learning
│   ├── Etapa3.6.2_utilize_ml_models.py               # Arquivo de utilização dos modelos (posterior)
├── ETAPA4/ 
│   ├── ALINHAMENTO.md                                # Avaliação da ETAPA 4
|   ├── relatorio_executivo_final.md                  # Relatório final executivo
|   ├── relatorio_tecnico_final.md                    # Relatório final técnico
├── src/                                              # Source para Streamlit (app.py)
│   ├── kpi_analysis/ 
│   │   ├── kpi1_delivery_time/                       # KPI 1
│   │   │   └── visualize_delivery_time.py            # Display para Pagina de Entrega
│   │   ├── kpi2_real_estate_cost/                    # KPI 2
│   │   │   └── visualize_real_estate_cost.py         # Display para Pagina de Imobiliario
│   │   ├── kpi3_consumption_potential/               # KPI 3
│   │   │   └── visualize_consumption_potential.py    # Display para Pagina de Consumo
│   │   └── kpi4_operational_cost/                    # KPI 4
│   │       └── visualize_operational_cost.py         # Display para Pagina de Operacional
│   └── utils/ 
│       └── data_loader.py                            # Loader dos dados
├── .gitignore                                        
├── app.py                                            # Point entry streamlit
├── README.md 
├── requirements.txt                                  # Arquivo de requirements (talvez haja 2 importações faltantes)
└── .env                                              # Crie esse arquivo
```

## 📜 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

## 📞 Contato & Evidências

-   **Autor**: Lucas Leria
-   **LinkedIn**: https://www.linkedin.com/in/lucasleria/
-   **GitHub**: https://github.com/lucasgleria

## 🔍 Recursos Adicionais

-   [Streamlit Documentation](https://docs.streamlit.io/) - Documentação oficial
-   [Pandas Documentation](https://pandas.pydata.org/docs/) - Documentação oficial
-   [Scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html) - Documentação oficial
-   [Plotly Documentation](https://plotly.com/python/) - Documentação oficial
-   [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Documentação oficial
-   [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html) - Documentação oficial
-   [MLflow Documentation](https://mlflow.org/docs/latest/index.html) - Documentação oficial


