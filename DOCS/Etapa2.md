# 📌 **Etapa 2: Coleta, Pré-processamento e Armazenamento de Dados**

Nesta etapa, construiremos a **base de dados confiável e integrada** que sustentará todas as análises posteriores.
O objetivo é consolidar informações brutas vindas de fontes abertas em um **repositório central (PostgreSQL + PostGIS)**, após passar por etapas de limpeza, transformação e padronização.

---

## **2.1 – Coleta de Dados**

### 📍 **Fontes de Dados Principais**

1. **Custos Imobiliários (aquisição/locação de galpões e terrenos industriais)**

   * **Fonte:** Portais de imóveis comerciais (Zap Imóveis, Viva Real, OLX Imóveis, sites locais de corretoras).
   * **Método:** Web Scraping com **BeautifulSoup/Scrapy**.
   * **Dados coletados:** preço do m², área construída, localização (endereço/CEP), tipo (venda/locação).

   *Snippet ilustrativo:*

   ```python
   import requests
   from bs4 import BeautifulSoup

   url = "https://www.zapimoveis.com.br/aluguel/galpoes/pe+recife/"
   response = requests.get(url)
   soup = BeautifulSoup(response.text, "html.parser")

   # Exemplo: extrair valores de imóveis
   prices = [item.get_text() for item in soup.find_all("div", class_="listing-price")]
   ```

---

2. **Malha Viária e Tempos de Entrega**

   * **Fonte:**

     * **OpenStreetMap (OSM):** extração de dados via **Overpass API**.
     * **OSRM (Open Source Routing Machine):** cálculo de rotas e tempos de viagem.
   * **Dados coletados:** rotas entre Recife/Salvador e as capitais do NE, distância (km), tempo estimado de viagem (h).

   *Snippet ilustrativo (Overpass API):*

   ```python
   import requests

   query = """
   [out:json];
   way["highway"](around:5000, -8.05, -34.9);  # Exemplo: raio de 5km em Recife
   out;
   """
   response = requests.get("http://overpass-api.de/api/interpreter", params={"data": query})
   roads = response.json()
   ```

---

3. **Demografia e Potencial de Consumo**

   * **Fonte:** **IBGE (API SIDRA)**, Censo Demográfico, PNAD Contínua.
   * **Dados coletados:** população, densidade demográfica, PIB per capita, taxa de consumo das famílias.
   * **Outras fontes complementares:** POF (Pesquisa de Orçamento Familiar), dados estaduais de comércio.

   *Snippet ilustrativo (API IBGE):*

   ```python
   import requests

   url = "https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2022/variaveis/93?localidades=N3[26]"  # Exemplo: Pernambuco
   response = requests.get(url)
   data = response.json()
   ```

---

## **2.2 – Pré-processamento (Limpeza e Transformação)**

Após a coleta, os dados precisam ser **padronizados e integrados**.

### Principais Processos:

* **Normalização de formatos** (moeda → R\$, km → m, datas padronizadas).
* **Tratamento de valores ausentes** (média, interpolação, exclusão, conforme contexto).
* **Georreferenciamento de endereços** (endereços de imóveis → coordenadas latitude/longitude com **geopy**).
* **Conversão para formatos compatíveis** com análises espaciais (GeoDataFrames).
* **Criação de chaves unificadas** para integrar dados (ex.: cidade, estado, CEP).

*Snippet ilustrativo (georreferenciamento):*

```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="magalu_project")
location = geolocator.geocode("Av. Recife, 3000 - Recife - PE")
print(location.latitude, location.longitude)
```

---

## **2.3 – Armazenamento dos Dados**

Para garantir escalabilidade e integridade, o armazenamento será feito em **PostgreSQL + PostGIS**.

### Estrutura do Banco:

* **Tabela `imoveis`** → dados imobiliários (id, cidade, preco\_m2, area, coordenadas).
* **Tabela `rotas`** → distâncias e tempos de viagem (origem, destino, distancia\_km, tempo\_horas).
* **Tabela `demografia`** → dados populacionais e de consumo (cidade, populacao, pib\_per\_capita, consumo\_familias).

*Snippet ilustrativo (inserção no PostgreSQL):*

```python
import psycopg2

conn = psycopg2.connect("dbname=magalu user=postgres password=1234 host=localhost")
cur = conn.cursor()

cur.execute("""
    INSERT INTO imoveis (cidade, preco_m2, area, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
""", ("Recife", 3500, 1000, -8.05, -34.9))

conn.commit()
conn.close()
```

---

## **2.4 – Fluxo ETL (Arquitetura de Dados)**

**Esquema do Pipeline ETL:**

1. **Extract (E)**

   * Scraping de dados imobiliários.
   * APIs (IBGE, Overpass API).
   * Dados de rotas via OSRM.

2. **Transform (T)**

   * Limpeza e normalização.
   * Georreferenciamento de endereços.
   * Conversão para GeoDataFrames.
   * Cálculo de métricas derivadas (ex.: custo médio por entrega).

3. **Load (L)**

   * Inserção em **PostgreSQL/PostGIS**.
   * Criação de índices espaciais.
   * Integração com ferramentas analíticas (GeoPandas, Metabase, Streamlit).

📊 **Visão simplificada:**

```
[Fonte bruta] → [Python ETL] → [Pandas/GeoPandas] → [Transformação] → [PostgreSQL + PostGIS] → [Camada analítica]
```

---

# 📑 **Resumo da Etapa 2 (Escopo Documentado)**

* **Fontes:** Portais imobiliários, OpenStreetMap (Overpass API), OSRM, IBGE (SIDRA/PNAD/POF).
* **Processos ETL:** Extração (APIs + scraping), transformação (limpeza, normalização, georreferenciamento), carga em PostgreSQL/PostGIS.
* **Estrutura de Dados:** Tabelas de imóveis, rotas e demografia integradas.
* **Ferramentas Principais:** Python (Requests, Scrapy, Pandas, GeoPandas, Geopy), PostgreSQL + PostGIS.
* **Resultado Esperado:** Base de dados confiável e unificada, pronta para análise estatística, geoespacial e modelagem logística.

