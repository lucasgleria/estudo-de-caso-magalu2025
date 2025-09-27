import os
import sys
import pandas as pd
import logging
import importlib.util

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Adicionar o diretório atual ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "magalu_cd_analysis",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5433"
}

def import_module_from_file(module_name, file_path):
    """
    Importa um módulo a partir de um arquivo Python
    """
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logging.error(f"Erro ao importar módulo {module_name} de {file_path}: {e}")
        return None

# Funções para coleta de dados
def _collect_real_estate_data_task():
    """
    Coleta dados de imóveis brutos
    """
    logging.info("Iniciando coleta de dados de imóveis")
    
    # Importar a função de coleta
    collect_module = import_module_from_file("collect_real_estate", "Etapa2_1_1_collect_real_estate_data.py")
    if collect_module is None:
        return None
    
    collect_real_estate_data = getattr(collect_module, "collect_real_estate_data", None)
    if collect_real_estate_data is None:
        logging.error("Função collect_real_estate_data não encontrada")
        return None
    
    # URLs de exemplo (precisam ser atualizadas com URLs reais para Recife e Salvador)
    zap_recife_url = "https://www.zapimoveis.com.br/aluguel/galpoes/pe+recife/"
    vivareal_recife_url = "https://www.vivareal.com.br/aluguel/galpoes/pe+recife/"
    olx_recife_url = "https://pe.olx.com.br/grande-recife/imoveis/galpoes-aluguel"
    
    zap_salvador_url = "https://www.zapimoveis.com.br/aluguel/galpoes/ba+salvador/"
    vivareal_salvador_url = "https://www.vivareal.com.br/aluguel/galpoes/ba+salvador/"
    olx_salvador_url = "https://ba.olx.com.br/salvador-e-regiao/imoveis/galpoes-aluguel"
    
    # Coletar dados para Recife
    logging.info("Coletando dados para Recife")
    df_recife = collect_real_estate_data(zap_recife_url, vivareal_recife_url, olx_recife_url, "Recife")
    
    # Coletar dados para Salvador
    logging.info("Coletando dados para Salvador")
    df_salvador = collect_real_estate_data(zap_salvador_url, vivareal_salvador_url, olx_salvador_url, "Salvador")
    
    # Combinar dados
    all_real_estate_data = pd.concat([df_recife, df_salvador], ignore_index=True)
    
    # Criar diretório se não existir
    os.makedirs("data/raw", exist_ok=True)
    
    # Salvar dados brutos
    output_path = "data/raw/Etapa2.1.1_collect_real_estate_raw_data.csv"
    all_real_estate_data.to_csv(output_path, index=False)
    logging.info(f"Dados de imóveis salvos em {output_path}")
    
    return output_path

def _collect_road_network_data_task():
    """
    Coleta dados de malha viária brutos
    """
    logging.info("Iniciando coleta de dados de malha viária")
    
    # Importar a função de coleta
    collect_module = import_module_from_file("collect_road_network", "Etapa2_1_2_collect_road_network_data.py")
    if collect_module is None:
        return None
    
    collect_road_network_data = getattr(collect_module, "collect_road_network_data", None)
    if collect_road_network_data is None:
        logging.error("Função collect_road_network_data não encontrada")
        return None
    
    # Coordenadas das principais capitais do Nordeste brasileiro
    NORTHEAST_CAPITALS = {
        'Recife': (-8.0476, -34.8770),
        'Salvador': (-12.9714, -38.5014),
        'Fortaleza': (-3.7327, -38.5270),
        'Natal': (-5.7945, -35.2110),
        'João Pessoa': (-7.1150, -34.8631),
        'Maceió': (-9.6658, -35.7352),
        'Aracaju': (-10.9091, -37.0748),
        'Teresina': (-5.0892, -42.8016),
        'São Luís': (-2.5307, -44.3068)
    }
    
    # Coletar dados
    df_routes = collect_road_network_data(NORTHEAST_CAPITALS)
    
    # Criar diretório se não existir
    os.makedirs("data/raw", exist_ok=True)
    
    # Salvar dados brutos
    output_path = "data/raw/Etapa2.1.2_collect_road_network_raw_data.csv"
    df_routes.to_csv(output_path, index=False)
    logging.info(f"Dados de malha viária salvos em {output_path}")
    
    return output_path

def _collect_demographic_data_task():
    """
    Coleta dados demográficos brutos
    """
    logging.info("Iniciando coleta de dados demográficos")
    
    # Importar a função de coleta
    collect_module = import_module_from_file("collect_demographic", "Etapa2_1_3_collect_demographic_data.py")
    if collect_module is None:
        return None
    
    collect_demographic_data = getattr(collect_module, "collect_demographic_data", None)
    if collect_demographic_data is None:
        logging.error("Função collect_demographic_data não encontrada")
        return None
    
    # Coletar dados
    df_demographic = collect_demographic_data(use_simulation=False)
    
    # Criar diretório se não existir
    os.makedirs("data/raw", exist_ok=True)
    
    # Salvar dados brutos
    output_path = "data/raw/Etapa2.1.3_collect_demographic_raw_data.csv"
    df_demographic.to_csv(output_path, index=False)
    logging.info(f"Dados demográficos salvos em {output_path}")
    
    return output_path

# Funções para pré-processamento de dados
def _preprocess_real_estate_data_task():
    """
    Pré-processa dados de imóveis
    """
    logging.info("Iniciando pré-processamento de dados de imóveis")
    
    # Importar a função de pré-processamento
    preprocess_module = import_module_from_file("preprocess_real_estate", "Etapa2_2_1_preprocess_real_estate_data.py")
    if preprocess_module is None:
        return None
    
    preprocess_real_estate_data = getattr(preprocess_module, "preprocess_real_estate_data", None)
    if preprocess_real_estate_data is None:
        logging.error("Função preprocess_real_estate_data não encontrada")
        return None
    
    # Carregar dados brutos
    raw_data_path = "data/raw/Etapa2.1.1_collect_real_estate_raw_data.csv"
    if not os.path.exists(raw_data_path):
        logging.error(f"Arquivo não encontrado: {raw_data_path}")
        return None
    
    raw_data = pd.read_csv(raw_data_path)
    
    # Pré-processar dados
    processed_df = preprocess_real_estate_data(raw_data)
    
    # Criar diretório se não existir
    os.makedirs("data/processed", exist_ok=True)
    
    # Salvar dados processados
    output_path = "data/processed/Etapa2.2.1_real_estate_processed_data.csv"
    processed_df.to_csv(output_path, index=False)
    logging.info(f"Dados de imóveis processados salvos em {output_path}")
    
    return output_path

# def _preprocess_road_network_data_task():
#     """
#     Pré-processa dados de malha viária
#     """
#     logging.info("Iniciando pré-processamento de dados de malha viária")
    
#     # Importar a função de pré-processamento
#     preprocess_module = import_module_from_file("preprocess_road_network", "Etapa2_2_2_preprocess_road_network_data.py")
#     if preprocess_module is None:
#         return None
    
#     preprocess_road_network_data = getattr(preprocess_module, "preprocess_road_network_data", None)
#     if preprocess_road_network_data is None:
#         logging.error("Função preprocess_road_network_data não encontrada")
#         return None
    
#     # Carregar dados brutos
#     raw_data_path = "data/raw/Etapa2.1.2_collect_road_network_raw_data.csv"
#     if not os.path.exists(raw_data_path):
#         logging.error(f"Arquivo não encontrado: {raw_data_path}")
#         return None
    
#     raw_data = pd.read_csv(raw_data_path)
    
#     # Pré-processar dados
#     processed_df = preprocess_road_network_data(raw_data)
    
#     # Criar diretório se não existir
#     os.makedirs("data/processed", exist_ok=True)
    
#     # Salvar dados processados
#     output_path = "data/processed/Etapa2.2.2_road_network_processed_data.csv"
#     processed_df.to_csv(output_path, index=False)
#     logging.info(f"Dados de malha viária processados salvos em {output_path}")
    
#     return output_path

def _preprocess_road_network_data_task():
    """
    Pré-processa dados de malha viária
    """
    logging.info("Iniciando pré-processamento de dados de malha viária")
    
    # Importar a função de pré-processamento
    preprocess_module = import_module_from_file("preprocess_road_network", "Etapa2_2_2_preprocess_road_network_data.py")
    if preprocess_module is None:
        return None
    
    preprocess_road_network_data = getattr(preprocess_module, "preprocess_road_network_data", None)
    if preprocess_road_network_data is None:
        logging.error("Função preprocess_road_network_data não encontrada")
        return None
    
    # Carregar dados brutos
    raw_data_path = "data/raw/Etapa2.1.2_collect_road_network_raw_data.csv"
    if not os.path.exists(raw_data_path):
        logging.error(f"Arquivo não encontrado: {raw_data_path}")
        return None
    
    raw_data = pd.read_csv(raw_data_path)
    
    # Pré-processar dados - agora retorna uma tupla (df, gdf_origin, gdf_destination)
    processed_result = preprocess_road_network_data(raw_data)
    if processed_result is None:
        logging.error("Falha no pré-processamento dos dados de malha viária")
        return None
    
    # Desempacotar a tupla
    processed_df, gdf_origin, gdf_destination = processed_result
    
    # Criar diretório se não existir
    os.makedirs("data/processed", exist_ok=True)
    
    # Salvar dados processados (DataFrame principal)
    output_path = "data/processed/Etapa2.2.2_road_network_processed_data.csv"
    processed_df.to_csv(output_path, index=False)
    logging.info(f"Dados de malha viária processados salvos em {output_path}")
    
    # Opcional: Salvar os GeoDataFrames se necessário para etapas posteriores
    try:
        gdf_origin_path = "data/processed/Etapa2.2.2_road_network_origin_geodataframe.gpkg"
        gdf_origin.to_file(gdf_origin_path, driver="GPKG")
        logging.info(f"GeoDataFrame de origem salvo em {gdf_origin_path}")
        
        gdf_destination_path = "data/processed/Etapa2.2.2_road_network_destination_geodataframe.gpkg"
        gdf_destination.to_file(gdf_destination_path, driver="GPKG")
        logging.info(f"GeoDataFrame de destino salvo em {gdf_destination_path}")
    except Exception as e:
        logging.warning(f"Não foi possível salvar os GeoDataFrames: {e}")
    
    return output_path

def _preprocess_demographic_data_task():
    """
    Pré-processa dados demográficos
    """
    logging.info("Iniciando pré-processamento de dados demográficos")
    
    # Importar a função de pré-processamento
    preprocess_module = import_module_from_file("preprocess_demographic", "Etapa2_2_3_5_preprocess_demographic_data.py")
    if preprocess_module is None:
        return None
    
    preprocess_demographic_data = getattr(preprocess_module, "preprocess_demographic_data", None)
    if preprocess_demographic_data is None:
        logging.error("Função preprocess_demographic_data não encontrada")
        return None
    
    # Carregar dados brutos
    raw_data_path = "data/raw/Etapa2.1.3_collect_demographic_raw_data.csv"
    if not os.path.exists(raw_data_path):
        logging.error(f"Arquivo não encontrado: {raw_data_path}")
        return None
    
    raw_data = pd.read_csv(raw_data_path)
    
    # Pré-processar dados
    processed_df = preprocess_demographic_data(raw_data)
    
    # Criar diretório se não existir
    os.makedirs("data/processed", exist_ok=True)
    
    # Salvar dados processados
    output_path = "data/processed/Etapa2.2.3-5_demographic_processed_data.csv"
    processed_df.to_csv(output_path, index=False)
    logging.info(f"Dados demográficos processados salvos em {output_path}")
    
    # Salvar também os dados de potencial de consumo
    consumption_output_path = "data/processed/Etapa2.2.3-5_consumption_potential.csv"
    consumption_df = processed_df.pivot_table(index=['city', 'year'], columns='metric', values='value').reset_index()
    consumption_df['consumption_potential_millions'] = consumption_df.apply(
        lambda row: (row['population'] * row['household_income']) / 1000000, axis=1
    )
    consumption_df.to_csv(consumption_output_path, index=False)
    logging.info(f"Dados de potencial de consumo salvos em {consumption_output_path}")
    
    return output_path, consumption_output_path

# Funções para criação do esquema do banco de dados
def _create_db_schema_task():
    """
    Cria o esquema do banco de dados
    """
    logging.info("Iniciando criação do esquema do banco de dados")
    
    # Importar as funções de criação do esquema
    schema_module = import_module_from_file("create_db_schema", "Etapa2_3_1_2_create_db_schema.py")
    if schema_module is None:
        return False
    
    create_database_and_extensions = getattr(schema_module, "create_database_and_extensions", None)
    create_tables = getattr(schema_module, "create_tables", None)
    create_indexes = getattr(schema_module, "create_indexes", None)
    
    if None in [create_database_and_extensions, create_tables, create_indexes]:
        logging.error("Funções de criação do esquema não encontradas")
        return False
    
    # Criar banco de dados e extensões
    create_database_and_extensions()
    
    # Criar tabelas
    create_tables()
    
    # Criar índices
    create_indexes()
    
    logging.info("Esquema do banco de dados criado com sucesso")
    return True

# Funções para carregamento de dados no banco de dados
def _load_real_estate_data_task():
    """
    Carrega dados de imóveis no banco de dados
    """
    logging.info("Iniciando carregamento de dados de imóveis no banco de dados")
    
    # Importar a função de carregamento
    load_module = import_module_from_file("load_data_to_db", "Etapa2_3_3_load_data_to_db.py")
    if load_module is None:
        return False
    
    load_real_estate_data = getattr(load_module, "load_real_estate_data", None)
    if load_real_estate_data is None:
        logging.error("Função load_real_estate_data não encontrada")
        return False
    
    # Carregar dados
    file_path = "data/processed/Etapa2.2.1_real_estate_processed_data.csv"
    if not os.path.exists(file_path):
        logging.error(f"Arquivo não encontrado: {file_path}")
        return False
    
    load_real_estate_data(file_path)
    
    logging.info("Dados de imóveis carregados com sucesso")
    return True

def _load_road_network_data_task():
    """
    Carrega dados de malha viária no banco de dados
    """
    logging.info("Iniciando carregamento de dados de malha viária no banco de dados")
    
    # Importar a função de carregamento
    load_module = import_module_from_file("load_data_to_db", "Etapa2_3_3_load_data_to_db.py")
    if load_module is None:
        return False
    
    load_road_network_data = getattr(load_module, "load_road_network_data", None)
    if load_road_network_data is None:
        logging.error("Função load_road_network_data não encontrada")
        return False
    
    # Carregar dados
    file_path = "data/processed/Etapa2.2.2_road_network_processed_data.csv"
    if not os.path.exists(file_path):
        logging.error(f"Arquivo não encontrado: {file_path}")
        return False
    
    load_road_network_data(file_path)
    
    logging.info("Dados de malha viária carregados com sucesso")
    return True

def _load_demographic_data_task():
    """
    Carrega dados demográficos no banco de dados
    """
    logging.info("Iniciando carregamento de dados demográficos no banco de dados")
    
    # Importar a função de carregamento
    load_module = import_module_from_file("load_data_to_db", "Etapa2_3_3_load_data_to_db.py")
    if load_module is None:
        return False
    
    load_demographic_data = getattr(load_module, "load_demographic_data", None)
    load_consumption_potential_data = getattr(load_module, "load_consumption_potential_data", None)
    
    if None in [load_demographic_data, load_consumption_potential_data]:
        logging.error("Funções de carregamento de dados demográficos não encontradas")
        return False
    
    # Carregar dados demográficos
    demographic_file_path = "data/processed/Etapa2.2.3-5_demographic_processed_data.csv"
    if not os.path.exists(demographic_file_path):
        logging.error(f"Arquivo não encontrado: {demographic_file_path}")
        return False
    
    load_demographic_data(demographic_file_path)
    
    # Carregar dados de potencial de consumo
    consumption_file_path = "data/processed/Etapa2.2.3-5_consumption_potential.csv"
    if not os.path.exists(consumption_file_path):
        logging.error(f"Arquivo não encontrado: {consumption_file_path}")
        return False
    
    load_consumption_potential_data(consumption_file_path)
    
    logging.info("Dados demográficos e de potencial de consumo carregados com sucesso")
    return True

def execute_etl_pipeline():
    """
    Executa o pipeline ETL completo
    """
    logging.info("Iniciando execução do pipeline ETL")
    
    # 1. Criação do esquema do banco de dados
    logging.info("Etapa 1: Criando esquema do banco de dados")
    if not _create_db_schema_task():
        logging.error("Falha na criação do esquema do banco de dados")
        return False
    
    # 2. Coleta de Dados
    logging.info("Etapa 2: Coletando dados")
    real_estate_raw_path = _collect_real_estate_data_task()
    if real_estate_raw_path is None:
        logging.error("Falha na coleta de dados de imóveis")
        return False
    
    road_network_raw_path = _collect_road_network_data_task()
    if road_network_raw_path is None:
        logging.error("Falha na coleta de dados de malha viária")
        return False
    
    demographic_raw_path = _collect_demographic_data_task()
    if demographic_raw_path is None:
        logging.error("Falha na coleta de dados demográficos")
        return False
    
    # 3. Pré-processamento de Dados
    logging.info("Etapa 3: Pré-processando dados")
    real_estate_processed_path = _preprocess_real_estate_data_task()
    if real_estate_processed_path is None:
        logging.error("Falha no pré-processamento de dados de imóveis")
        return False
    
    road_network_processed_path = _preprocess_road_network_data_task()
    if road_network_processed_path is None:
        logging.error("Falha no pré-processamento de dados de malha viária")
        return False
    
    demographic_processed_result = _preprocess_demographic_data_task()
    if demographic_processed_result is None:
        logging.error("Falha no pré-processamento de dados demográficos")
        return False
    
    demographic_processed_path, consumption_path = demographic_processed_result
    
    # 4. Carregamento de Dados no Banco
    logging.info("Etapa 4: Carregando dados no banco de dados")
    if not _load_real_estate_data_task():
        logging.error("Falha no carregamento de dados de imóveis")
        return False
    
    if not _load_road_network_data_task():
        logging.error("Falha no carregamento de dados de malha viária")
        return False
    
    if not _load_demographic_data_task():
        logging.error("Falha no carregamento de dados demográficos")
        return False
    
    logging.info("Pipeline ETL concluído com sucesso!")
    return True

if __name__ == "__main__":
    success = execute_etl_pipeline()
    if success:
        print("Pipeline executado com sucesso!")
    else:
        print("Ocorreram erros durante a execução do pipeline. Verifique os logs para mais detalhes.")