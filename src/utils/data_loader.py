import os
import pandas as pd
import logging

# Importações opcionais para conexão com banco de dados
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from dotenv import load_dotenv
    DB_AVAILABLE = True
    load_dotenv()
except ImportError:
    DB_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Módulos de banco de dados não disponíveis. Usando apenas dados mock.")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Estabelece conexão com o banco de dados PostgreSQL usando variáveis de ambiente.
    Retorna None se a conexão falhar ou se os módulos não estiverem disponíveis.
    """
    if not DB_AVAILABLE:
        logger.warning("Módulos de banco de dados não disponíveis.")
        return None
        
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            client_encoding='utf8'
        )
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def load_kpi1_data():
    """
    Carrega dados de rotas e tempos de entrega para o KPI 1.
    Tenta primeiro carregar do banco de dados, fallback para CSV.
    """
    # Tentar carregar do banco de dados
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM kpi1_delivery_data;"
            df = pd.read_sql(query, conn)
            conn.close()
            logger.info("Dados do KPI 1 carregados do banco de dados.")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados do KPI 1 do banco: {e}")
            conn.close()
    
    # Fallback para CSV
    try:
        df = pd.read_csv("../etapa2/data/processed/road_network_processed_data.csv")
        logger.info("Dados do KPI 1 carregados do arquivo CSV.")
        return df
    except FileNotFoundError:
        logger.warning("Arquivo CSV do KPI 1 não encontrado. Usando dados mock.")
        return pd.DataFrame({
            "origin": ["Recife", "Salvador"],
            "destination": ["Salvador", "Recife"],
            "distance_km": [850.5, 850.5],
            "duration_hours": [12.3, 12.3],
            "origin_lat": [-8.05, -12.97],
            "origin_lon": [-34.9, -38.5],
            "destination_lat": [-12.97, -38.5],
            "destination_lon": [-8.05, -34.9]
        })

def load_kpi2_data():
    """
    Carrega dados de custos imobiliários para o KPI 2.
    Tenta primeiro carregar do banco de dados, fallback para CSV.
    """
    # Tentar carregar do banco de dados
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM kpi2_real_estate_data;"
            df = pd.read_sql(query, conn)
            conn.close()
            logger.info("Dados do KPI 2 carregados do banco de dados.")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados do KPI 2 do banco: {e}")
            conn.close()
    
    # Fallback para CSV
    try:
        df = pd.read_csv("../etapa2/data/processed/real_estate_processed_data.csv")
        logger.info("Dados do KPI 2 carregados do arquivo CSV.")
        return df
    except FileNotFoundError:
        logger.warning("Arquivo CSV do KPI 2 não encontrado. Usando dados mock.")
        return pd.DataFrame({
            "source": ["ZapImoveis", "VivaReal", "OLX", "QuintoAndar", "ZapImoveis", "VivaReal", "OLX", "QuintoAndar"],
            "price": ["R$ 1.500.000", "R$ 800.000", "R$ 2.200.000", "R$ 950.000", "R$ 1.800.000", "R$ 1.100.000", "R$ 2.500.000", "R$ 750.000"],
            "area": ["1500 m²", "800 m²", "2000 m²", "1200 m²", "1800 m²", "1000 m²", "2200 m²", "900 m²"],
            "address_raw": [
                "Av. Boa Viagem, 1000 - Recife - PE", 
                "Rua da Bahia, 500 - Salvador - BA",
                "Av. Caxangá, 2000 - Recife - PE",
                "Rua Chile, 300 - Salvador - BA",
                "Rua da Aurora, 1500 - Recife - PE",
                "Av. Tancredo Neves, 800 - Salvador - BA",
                "Av. Recife, 2500 - Recife - PE",
                "Rua Barão de Sergy, 400 - Salvador - BA"
            ],
            "type": ["venda", "aluguel", "venda", "aluguel", "venda", "aluguel", "venda", "aluguel"],
            "city": ["Recife", "Salvador", "Recife", "Salvador", "Recife", "Salvador", "Recife", "Salvador"],
            "price_m2": [1000.0, 1000.0, 1100.0, 791.67, 1000.0, 1100.0, 1136.36, 833.33],
            "area_m2": [1500.0, 800.0, 2000.0, 1200.0, 1800.0, 1000.0, 2200.0, 900.0],
            "latitude": [-8.12, -12.97, -8.05, -12.98, -8.10, -12.96, -8.08, -12.99],
            "longitude": [-34.90, -38.51, -34.88, -38.52, -34.89, -38.50, -34.87, -38.53]
        })

def load_kpi3_data():
    """
    Carrega dados demográficos e de potencial de consumo para o KPI 3.
    Tenta primeiro carregar do banco de dados, fallback para CSV.
    """
    # Tentar carregar do banco de dados
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM kpi3_demographic_data;"
            df = pd.read_sql(query, conn)
            conn.close()
            logger.info("Dados do KPI 3 carregados do banco de dados.")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados do KPI 3 do banco: {e}")
            conn.close()
    
    # Fallback para CSV
    try:
        df = pd.read_csv("../etapa2/data/processed/demographic_processed_data.csv")
        logger.info("Dados do KPI 3 carregados do arquivo CSV.")
        return df
    except FileNotFoundError:
        logger.warning("Arquivo CSV do KPI 3 não encontrado. Usando dados mock.")
        return pd.DataFrame({
            "city": ["Recife", "Salvador", "Recife", "Salvador", "Recife", "Salvador", "Recife", "Salvador"],
            "year": [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022],
            "population": [1661017, 2418005, 1661017, 2418005, 1661017, 2418005, 1661017, 2418005],
            "metric": ["population", "population", "gdp_per_capita", "gdp_per_capita", "avg_income", "avg_income", "consumption_index", "consumption_index"],
            "pib_per_capita": [30000, 28000, 30000, 28000, 2500, 2300, 85, 80],
            "value": [1661017, 2418005, 30000, 28000, 2500, 2300, 85, 80]
        })

def load_kpi4_data():
    """
    Carrega dados operacionais para o KPI 4.
    Tenta primeiro carregar do banco de dados, fallback para dados mock.
    """
    # Tentar carregar do banco de dados
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM kpi4_operational_data;"
            df = pd.read_sql(query, conn)
            conn.close()
            logger.info("Dados do KPI 4 carregados do banco de dados.")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados do KPI 4 do banco: {e}")
            conn.close()
    
    # Fallback para dados mock
    logger.warning("Dados do KPI 4 não encontrados. Usando dados mock.")
    return {
        "Recife": {
            "avg_salary_logistics": 2600,
            "energy_cost_kwh": 0.85,
            "fuel_cost_per_km": 0.52,
            "driver_cost_per_hour": 26,
            "estimated_monthly_volume": 110000,
            "cd_energy_consumption_kwh_month": 55000
        },
        "Salvador": {
            "avg_salary_logistics": 2400,
            "energy_cost_kwh": 0.78,
            "fuel_cost_per_km": 0.50,
            "driver_cost_per_hour": 24,
            "estimated_monthly_volume": 95000,
            "cd_energy_consumption_kwh_month": 48000
        }
    }