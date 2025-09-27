import psycopg2
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do banco de dados - ATUALIZADO PARA A PORTA 5433
DB_CONFIG = {
    "dbname": "magalu_cd_analysis",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5433"  # ATUALIZADO: Usando a porta que funcionou
}

def test_connection():
    """
    Testa a conexão com o PostgreSQL
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        cur = conn.cursor()
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        logging.info(f"Conexão com PostgreSQL estabelecida. Versão: {version}")
        cur.close()
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        logging.error(f"Erro ao conectar ao PostgreSQL: {e}")
        logging.error(f"Verifique se o PostgreSQL está rodando na porta {DB_CONFIG['port']}")
        logging.error("Verifique se a senha do usuário 'postgres' está correta")
        return False
    except Exception as e:
        logging.error(f"Erro inesperado ao testar conexão: {e}")
        return False

def create_database_and_extensions():
    """
    Cria o banco de dados e habilita a extensão PostGIS.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_CONFIG['dbname']}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {DB_CONFIG['dbname']}")
            logging.info(f"Banco de dados '{DB_CONFIG['dbname']}' criado com sucesso.")
        else:
            logging.info(f"Banco de dados '{DB_CONFIG['dbname']}' já existe.")

        cur.close()
    except Exception as e:
        logging.error(f"Erro ao criar o banco de dados: {e}")
        return False
    finally:
        if conn:
            conn.close()

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM pg_extension WHERE extname = 'postgis'")
        if not cur.fetchone():
            cur.execute("CREATE EXTENSION postgis;")
            conn.commit()
            logging.info("Extensão PostGIS habilitada com sucesso.")
        else:
            logging.info("Extensão PostGIS já está habilitada.")
        
        cur.execute("SELECT PostGIS_Version()")
        version = cur.fetchone()[0]
        logging.info(f"Versão do PostGIS: {version}")
        
        cur.close()
    except Exception as e:
        logging.error(f"Erro ao habilitar PostGIS: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    return True

def create_tables():
    """
    Cria as tabelas necessárias no banco de dados.
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Tabela imoveis
        cur.execute("""
            CREATE TABLE IF NOT EXISTS imoveis (
                id SERIAL PRIMARY KEY,
                source VARCHAR(50),
                price_raw TEXT,
                area_raw TEXT,
                address_raw TEXT,
                type VARCHAR(20),
                city VARCHAR(50),
                price NUMERIC,
                area NUMERIC,
                cep VARCHAR(10),
                price_per_m2 NUMERIC,
                latitude NUMERIC,
                longitude NUMERIC,
                geom GEOMETRY(Point, 4326)
            );
        """)
        logging.info("Tabela 'imoveis' criada ou já existente.")

        # Tabela rotas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rotas (
                id SERIAL PRIMARY KEY,
                origin VARCHAR(50),
                destination VARCHAR(50),
                distance_km NUMERIC,
                duration_hours NUMERIC,
                avg_speed_kmh NUMERIC,
                origin_lat NUMERIC,
                origin_lon NUMERIC,
                destination_lat NUMERIC,
                destination_lon NUMERIC,
                origin_geom GEOMETRY(Point, 4326),
                destination_geom GEOMETRY(Point, 4326)
            );
        """)
        logging.info("Tabela 'rotas' criada ou já existente.")

        # Tabela demografia
        cur.execute("""
            CREATE TABLE IF NOT EXISTS demografia (
                id SERIAL PRIMARY KEY,
                city VARCHAR(50),
                metric VARCHAR(50),
                year INTEGER,
                value NUMERIC
            );
        """)
        logging.info("Tabela 'demografia' criada ou já existente.")

        # Tabela consumo_potencial
        cur.execute("""
            CREATE TABLE IF NOT EXISTS consumo_potencial (
                id SERIAL PRIMARY KEY,
                city VARCHAR(50),
                year INTEGER,
                population NUMERIC,
                pib NUMERIC,
                pib_per_capita NUMERIC,
                household_income NUMERIC,
                consumption_potential_millions NUMERIC
            );
        """)
        logging.info("Tabela 'consumo_potencial' criada ou já existente.")

        # Tabela estatisticas_comparativas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS estatisticas_comparativas (
                id SERIAL PRIMARY KEY,
                city VARCHAR(50),
                population NUMERIC,
                pib NUMERIC,
                pib_per_capita NUMERIC,
                household_income NUMERIC,
                consumption_potential_millions NUMERIC,
                comparison_date DATE DEFAULT CURRENT_DATE
            );
        """)
        logging.info("Tabela 'estatisticas_comparativas' criada ou já existente.")

        conn.commit()
        cur.close()
        return True
    except Exception as e:
        logging.error(f"Erro ao criar tabelas: {e}")
        return False
    finally:
        if conn:
            conn.close()

def create_indexes():
    """
    Cria índices para melhorar a performance das consultas.
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Índices para tabela imoveis
        cur.execute("CREATE INDEX IF NOT EXISTS idx_imoveis_city ON imoveis(city);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_imoveis_source ON imoveis(source);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_imoveis_geom ON imoveis USING GIST(geom);")
        
        # Índices para tabela rotas
        cur.execute("CREATE INDEX IF NOT EXISTS idx_rotas_origin ON rotas(origin);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_rotas_destination ON rotas(destination);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_rotas_origin_geom ON rotas USING GIST(origin_geom);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_rotas_destination_geom ON rotas USING GIST(destination_geom);")
        
        # Índices para tabela demografia
        cur.execute("CREATE INDEX IF NOT EXISTS idx_demografia_city ON demografia(city);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_demografia_metric ON demografia(metric);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_demografia_year ON demografia(year);")
        
        # Índices para tabela consumo_potencial
        cur.execute("CREATE INDEX IF NOT EXISTS idx_consumo_city ON consumo_potencial(city);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_consumo_year ON consumo_potencial(year);")

        conn.commit()
        logging.info("Índices criados com sucesso.")
        cur.close()
        return True
    except Exception as e:
        logging.error(f"Erro ao criar índices: {e}")
        return False
    finally:
        if conn:
            conn.close()

def verify_setup():
    """
    Verifica se tudo foi configurado corretamente
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        tables = cur.fetchall()
        logging.info("Tabelas criadas:")
        for table in tables:
            logging.info(f"  - {table[0]}")
        
        cur.execute("SELECT PostGIS_Version()")
        version = cur.fetchone()[0]
        logging.info(f"PostGIS versão: {version}")
        
        cur.close()
        return True
    except Exception as e:
        logging.error(f"Erro ao verificar configuração: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    logging.info("Iniciando configuração do banco de dados...")
    
    if not test_connection():
        logging.error("Não foi possível conectar ao PostgreSQL. Verifique a instalação.")
        sys.exit(1)
    
    if not create_database_and_extensions():
        logging.error("Não foi possível criar o banco de dados ou habilitar extensões.")
        sys.exit(1)
    
    if not create_tables():
        logging.error("Não foi possível criar as tabelas.")
        sys.exit(1)
    
    if not create_indexes():
        logging.error("Não foi possível criar os índices.")
        sys.exit(1)
    
    if verify_setup():
        logging.info("Configuração do esquema do banco de dados concluída com sucesso!")
    else:
        logging.error("Falha na verificação da configuração.")
        sys.exit(1)