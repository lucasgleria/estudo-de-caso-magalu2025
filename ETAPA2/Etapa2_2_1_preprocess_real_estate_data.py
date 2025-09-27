import pandas as pd
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_price(price_str):
    """
    Limpa e converte string de preço para float.
    """
    if isinstance(price_str, str):
        # Remove símbolos de moeda, pontos e espaços
        cleaned = re.sub(r'[R$\.\s]', '', price_str)
        # Substitui vírgula por ponto
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return None
    return price_str if pd.notna(price_str) else None

def clean_area(area_str):
    """
    Limpa e converte string de área (m²) para float.
    """
    if isinstance(area_str, str):
        # Remove 'm²' e espaços
        cleaned = re.sub(r'[m²\s]', '', area_str)
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return None
    return area_str if pd.notna(area_str) else None

def extract_cep(address):
    """Extrai CEP de um endereço usando regex."""
    if pd.isna(address) or address == 'N/A':
        return None
    # Padrão para CEP brasileiro: XXXXX-XXX
    cep_match = re.search(r'(\d{5}-\d{3})', address)
    return cep_match.group(1) if cep_match else None

def geocode_addresses(df):
    """
    Geocodifica endereços e adiciona colunas de latitude e longitude.
    """
    geolocator = Nominatim(user_agent="magalu_project_geocoder")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    # Criar um cache para evitar geocodificações repetidas
    location_cache = {}
    
    # Lista para armazenar os resultados
    latitudes = []
    longitudes = []
    
    # Contador para acompanhar o progresso
    total = len(df)
    processed = 0
    successful = 0
    
    for idx, row in df.iterrows():
        address = row["address_raw"]
        city = row["city"]
        
        # Pular se o endereço for nulo ou "N/A"
        if pd.isna(address) or address == "N/A":
            latitudes.append(None)
            longitudes.append(None)
            processed += 1
            continue
        
        # Verificar se já temos no cache
        if address in location_cache:
            lat, lon = location_cache[address]
            latitudes.append(lat)
            longitudes.append(lon)
            if lat is not None and lon is not None:
                successful += 1
            processed += 1
            continue
        
        # Tentar geocodificar
        try:
            # Adicionar a cidade para melhorar a precisão
            full_address = f"{address}, {city}" if city not in address else address
            location = geocode(full_address)
            
            if location:
                latitudes.append(location.latitude)
                longitudes.append(location.longitude)
                location_cache[address] = (location.latitude, location.longitude)
                successful += 1
            else:
                latitudes.append(None)
                longitudes.append(None)
                location_cache[address] = (None, None)
                logging.warning(f"Não foi possível geocodificar: {full_address}")
        except Exception as e:
            logging.warning(f"Erro ao geocodificar {address}: {e}")
            latitudes.append(None)
            longitudes.append(None)
            location_cache[address] = (None, None)
        
        processed += 1
        if processed % 10 == 0 or processed == total:
            logging.info(f"Geocodificação: {processed}/{total} endereços processados, {successful} bem-sucedidos")
    
    # Adicionar as colunas ao DataFrame
    df["latitude"] = latitudes
    df["longitude"] = longitudes
    
    logging.info(f"Geocodificação concluída. {successful} de {total} endereços geocodificados com sucesso.")
    return df

def preprocess_real_estate_data(df):
    """
    Realiza o pré-processamento dos dados imobiliários brutos.
    """
    logging.info("Iniciando pré-processamento de dados imobiliários.")
    
    # Fazer uma cópia para evitar SettingWithCopyWarning
    df = df.copy()
    
    # Limpeza e conversão de preço e área
    df["price"] = df["price_raw"].apply(clean_price)
    df["area"] = df["area_raw"].apply(clean_area)
    
    # Extrair CEP
    df["cep"] = df["address_raw"].apply(extract_cep)
    
    # Calcular preço por m²
    df["price_per_m2"] = df.apply(
        lambda row: row["price"] / row["area"] 
        if pd.notna(row["price"]) and pd.notna(row["area"]) and row["area"] > 0 
        else None, 
        axis=1
    )
    
    # Tratamento de valores ausentes
    # Remover linhas com preço ou área nulos
    initial_count = len(df)
    df.dropna(subset=["price", "area"], inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas com preço ou área nulos.")
    
    # Remover duplicatas baseadas em endereço e preço
    initial_count = len(df)
    df.drop_duplicates(subset=["address_raw", "price_raw"], keep="first", inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas duplicadas.")
    
    # Verificar se temos endereços válidos antes de geocodificar
    valid_addresses = df[df["address_raw"] != "N/A"]["address_raw"].count()
    if valid_addresses == 0:
        logging.warning("Nenhum endereço válido encontrado para geocodificação. Adicionando colunas de latitude e longitude com valores nulos.")
        df["latitude"] = None
        df["longitude"] = None
    else:
        # Georreferenciamento
        df = geocode_addresses(df)
        
        # Não remover linhas que não puderam ser geocodificadas, apenas registrar
        missing_geo = df["latitude"].isna().sum()
        if missing_geo > 0:
            logging.warning(f"{missing_geo} registros não puderam ser geocodificados, mas serão mantidos.")
    
    logging.info("Pré-processamento de dados imobiliários concluído.")
    return df

if __name__ == "__main__":
    # Caminho para o arquivo de dados brutos
    raw_data_path = "data/raw/Etapa2_1_1_collect_real_estate_raw_data.csv"
    
    # Verificar se o arquivo existe
    if not os.path.exists(raw_data_path):
        logging.error(f"Arquivo não encontrado: {raw_data_path}")
        exit(1)
    
    # Carregar os dados brutos
    try:
        raw_data = pd.read_csv(raw_data_path)
        logging.info(f"Dados carregados: {len(raw_data)} registros de {raw_data_path}")
        
        # Verificar endereços
        na_addresses = (raw_data["address_raw"] == "N/A").sum()
        logging.info(f"Endereços 'N/A': {na_addresses} de {len(raw_data)} registros")
    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        exit(1)
    
    # Pré-processar os dados
    processed_df = preprocess_real_estate_data(raw_data)
    
    # Exibir amostra dos dados pré-processados
    print("\nDados imobiliários pré-processados (amostra):")
    print(processed_df.head())
    
    # Criar diretório para dados processados se não existir
    os.makedirs('data/processed', exist_ok=True)
    
    # Salvar os dados processados
    processed_path = "data/processed/Etapa2_2_1_real_estate_processed_data.csv"
    processed_df.to_csv(processed_path, index=False)
    logging.info(f"Dados imobiliários pré-processados salvos em '{processed_path}'")
    
    # Salvar também em JSON para preservar tipos de dados
    json_path = "data/processed/Etapa2_2_1_real_estate_processed_data.json"
    processed_df.to_json(json_path, orient='records', indent=2)
    logging.info(f"Dados imobiliários pré-processados salvos em JSON em '{json_path}'")
    
    # Exibir estatísticas por cidade
    print("\nEstatísticas por cidade:")
    city_stats = processed_df.groupby('city').agg({
        'price': ['mean', 'min', 'max', 'count'],
        'area': ['mean', 'min', 'max'],
        'price_per_m2': ['mean', 'min', 'max']
    })
    print(city_stats)
    
    # Exibir estatísticas por fonte
    print("\nEstatísticas por fonte:")
    source_stats = processed_df.groupby(['source', 'city']).size().unstack(fill_value=0)
    print(source_stats)