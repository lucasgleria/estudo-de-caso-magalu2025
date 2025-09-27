import pandas as pd
import psycopg2
from psycopg2 import extras
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do banco de dados - usando a porta correta
DB_CONFIG = {
    "dbname": "magalu_cd_analysis",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5433"  # Porta correta identificada nos testes
}

def get_db_connection():
    """
    Retorna uma conexão com o banco de dados
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def load_real_estate_data(file_path: str):
    """
    Carrega dados imobiliários processados para a tabela 'imoveis'.
    """
    logging.info(f"Carregando dados imobiliários de {file_path} para o banco de dados.")
    
    if not os.path.exists(file_path):
        logging.error(f"Arquivo {file_path} não encontrado.")
        return False
    
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(file_path)
        logging.info(f"Arquivo lido: {len(df)} registros")
        
        # Remover linhas com valores nulos críticos
        df = df.dropna(subset=['price', 'area', 'city'])
        logging.info(f"Registros após limpeza: {len(df)}")
        
        conn = get_db_connection()
        if not conn:
            return False
        
        cur = conn.cursor()
        
        # Preparar dados para inserção
        records = []
        for index, row in df.iterrows():
            records.append((
                row["source"],
                row["price_raw"],
                row["area_raw"],
                row["address_raw"],
                row["type"],
                row["city"],
                row["price"],
                row["area"],
                row["cep"],
                row["price_per_m2"],
                row["latitude"],
                row["longitude"],
                # Usar ST_MakePoint e ST_SetSRID para criar a geometria
                f"SRID=4326;POINT({row['longitude']} {row['latitude']})" if pd.notna(row['latitude']) and pd.notna(row['longitude']) else None
            ))

        insert_query = """
            INSERT INTO imoveis (source, price_raw, area_raw, address_raw, type, city, price, area, cep, price_per_m2, latitude, longitude, geom)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromEWKT(%s))
        """
        
        extras.execute_batch(cur, insert_query, records)
        conn.commit()
        
        logging.info(f"{len(records)} registros imobiliários inseridos com sucesso.")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"Erro ao carregar dados imobiliários: {e}")
        return False

def load_road_network_data(file_path: str):
    """
    Carrega dados de malha viária processados para a tabela 'rotas'.
    """
    logging.info(f"Carregando dados de rotas de {file_path} para o banco de dados.")
    
    if not os.path.exists(file_path):
        logging.error(f"Arquivo {file_path} não encontrado.")
        return False
    
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(file_path)
        logging.info(f"Arquivo lido: {len(df)} registros")
        
        conn = get_db_connection()
        if not conn:
            return False
        
        cur = conn.cursor()
        
        # Preparar dados para inserção
        records = []
        for index, row in df.iterrows():
            records.append((
                row["origin"],
                row["destination"],
                row["distance_km"],
                row["duration_hours"],
                row["avg_speed_kmh"],
                row["origin_lat"],
                row["origin_lon"],
                row["destination_lat"],
                row["destination_lon"]
            ))

        insert_query = """
            INSERT INTO rotas (origin, destination, distance_km, duration_hours, avg_speed_kmh, origin_lat, origin_lon, destination_lat, destination_lon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        extras.execute_batch(cur, insert_query, records)
        conn.commit()
        
        # Atualizar as colunas geométricas
        # Criar pontos geométricos para origem
        update_origin_query = """
        UPDATE rotas 
        SET origin_geom = ST_SetSRID(ST_MakePoint(origin_lon, origin_lat), 4326)
        WHERE origin_lat IS NOT NULL 
        AND origin_lon IS NOT NULL
        AND origin_geom IS NULL
        """
        cur.execute(update_origin_query)
        
        # Criar pontos geométricos para destino
        update_destination_query = """
        UPDATE rotas 
        SET destination_geom = ST_SetSRID(ST_MakePoint(destination_lon, destination_lat), 4326)
        WHERE destination_lat IS NOT NULL 
        AND destination_lon IS NOT NULL
        AND destination_geom IS NULL
        """
        cur.execute(update_destination_query)
        
        conn.commit()
        
        logging.info(f"{len(records)} registros de rotas inseridos com sucesso.")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"Erro ao carregar dados de rotas: {e}")
        return False

def load_demographic_data(file_path: str):
    """
    Carrega dados demográficos processados para a tabela 'demografia'.
    """
    logging.info(f"Carregando dados demográficos de {file_path} para o banco de dados.")
    
    if not os.path.exists(file_path):
        logging.error(f"Arquivo {file_path} não encontrado.")
        return False
    
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(file_path)
        logging.info(f"Arquivo lido: {len(df)} registros")
        
        conn = get_db_connection()
        if not conn:
            return False
        
        cur = conn.cursor()
        
        # Preparar dados para inserção
        records = []
        for index, row in df.iterrows():
            records.append((
                row["city"],
                row["metric"],
                row["year"],
                row["value"]
            ))

        insert_query = """
            INSERT INTO demografia (city, metric, year, value)
            VALUES (%s, %s, %s, %s)
        """
        
        extras.execute_batch(cur, insert_query, records)
        conn.commit()
        
        logging.info(f"{len(records)} registros demográficos inseridos com sucesso.")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"Erro ao carregar dados demográficos: {e}")
        return False

def load_consumption_potential_data(file_path: str):
    """
    Carrega dados de potencial de consumo para a tabela 'consumo_potencial'.
    """
    logging.info(f"Carregando dados de potencial de consumo de {file_path} para o banco de dados.")
    
    if not os.path.exists(file_path):
        logging.error(f"Arquivo {file_path} não encontrado.")
        return False
    
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(file_path)
        logging.info(f"Arquivo lido: {len(df)} registros")
        
        conn = get_db_connection()
        if not conn:
            return False
        
        cur = conn.cursor()
        
        # Preparar dados para inserção
        records = []
        for index, row in df.iterrows():
            records.append((
                row["city"],
                row["year"],
                row["population"],
                row["pib"],
                row["pib_per_capita"],
                row["household_income"],
                row["consumption_potential_millions"]
            ))

        insert_query = """
            INSERT INTO consumo_potencial (city, year, population, pib, pib_per_capita, household_income, consumption_potential_millions)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        extras.execute_batch(cur, insert_query, records)
        conn.commit()
        
        logging.info(f"{len(records)} registros de potencial de consumo inseridos com sucesso.")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"Erro ao carregar dados de potencial de consumo: {e}")
        return False

def verify_import():
    """
    Verifica se os dados foram importados corretamente
    """
    logging.info("Verificando importação dos dados...")
    
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        cur = conn.cursor()
        
        # Verificar contagem de registros em cada tabela
        tables = ['imoveis', 'rotas', 'demografia', 'consumo_potencial']
        
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            logging.info(f"Tabela {table}: {count} registros")
        
        # Verificar alguns exemplos de dados geométricos
        cur.execute("""
            SELECT city, COUNT(*) as total 
            FROM imoveis 
            WHERE geom IS NOT NULL 
            GROUP BY city 
            ORDER BY total DESC
        """)
        imoveis_geom = cur.fetchall()
        logging.info("Imóveis com dados geométricos por cidade:")
        for city, count in imoveis_geom:
            logging.info(f"  - {city}: {count} imóveis")
        
        # Verificar rotas com dados geométricos
        cur.execute("""
            SELECT origin, destination, COUNT(*) as total 
            FROM rotas 
            WHERE origin_geom IS NOT NULL AND destination_geom IS NOT NULL 
            GROUP BY origin, destination 
            LIMIT 5
        """)
        rotas_geom = cur.fetchall()
        logging.info("Exemplos de rotas com dados geométricos:")
        for origin, destination, count in rotas_geom:
            logging.info(f"  - {origin} -> {destination}: {count} rotas")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logging.error(f"Erro ao verificar importação: {e}")
        return False

if __name__ == "__main__":
    logging.info("Iniciando carregamento de dados para o PostgreSQL...")
    
    # Caminhos para os arquivos CSV processados
    real_estate_file = "data/processed/Etapa2_2_1_real_estate_processed_data.csv"
    road_network_file = "data/processed/Etapa2_2_2_road_network_processed_data.csv"
    demographic_file = "data/processed/Etapa2_2_3_5_demographic_processed_data.csv"
    consumption_potential_file = "data/processed/Etapa2_2_3_5_consumption_potential.csv"
    
    # Carregar dados de imóveis
    if not load_real_estate_data(real_estate_file):
        logging.error("Falha ao carregar dados de imóveis")
        sys.exit(1)
    
    # Carregar dados de malha viária
    if not load_road_network_data(road_network_file):
        logging.error("Falha ao carregar dados de malha viária")
        sys.exit(1)
    
    # Carregar dados demográficos
    if not load_demographic_data(demographic_file):
        logging.error("Falha ao carregar dados demográficos")
        sys.exit(1)
    
    # Carregar dados de potencial de consumo
    if not load_consumption_potential_data(consumption_potential_file):
        logging.error("Falha ao carregar dados de potencial de consumo")
        sys.exit(1)
    
    # Verificar importação
    if verify_import():
        logging.info("Carregamento de todos os dados processados para o banco de dados concluído com sucesso!")
    else:
        logging.error("Falha na verificação da importação")
        sys.exit(1)