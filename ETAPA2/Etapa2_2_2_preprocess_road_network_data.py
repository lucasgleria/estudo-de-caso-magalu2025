import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import logging
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_road_network_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o pré-processamento dos dados brutos de malha viária e rotas.
    """
    logging.info("Iniciando pré-processamento de dados de malha viária.")

    # Fazer uma cópia para evitar SettingWithCopyWarning
    df = df.copy()

    # Verificar se as colunas necessárias existem
    required_columns = ['origin', 'destination', 'distance_km', 'duration_hours']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logging.error(f"Colunas necessárias ausentes: {missing_columns}")
        return df

    # Garantir que distância e duração estejam em unidades consistentes (km e horas)
    # O script de coleta já faz isso, mas é bom validar
    logging.info("Validando unidades de distância e tempo...")
    
    # Remover linhas com valores ausentes críticos
    initial_count = len(df)
    df.dropna(subset=['origin', 'destination', 'distance_km', 'duration_hours'], inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas com valores ausentes.")

    # Adicionar coordenadas geográficas para cada cidade
    logging.info("Adicionando coordenadas geográficas...")
    
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
    
    # Adicionar coordenadas de origem
    df['origin_lat'] = df['origin'].map(lambda x: NORTHEAST_CAPITALS.get(x, (None, None))[0])
    df['origin_lon'] = df['origin'].map(lambda x: NORTHEAST_CAPITALS.get(x, (None, None))[1])
    
    # Adicionar coordenadas de destino
    df['destination_lat'] = df['destination'].map(lambda x: NORTHEAST_CAPITALS.get(x, (None, None))[0])
    df['destination_lon'] = df['destination'].map(lambda x: NORTHEAST_CAPITALS.get(x, (None, None))[1])
    
    # Remover linhas sem coordenadas
    initial_count = len(df)
    df.dropna(subset=['origin_lat', 'origin_lon', 'destination_lat', 'destination_lon'], inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas sem coordenadas geográficas.")

    # Calcular velocidade média (km/h)
    df['avg_speed_kmh'] = df.apply(
        lambda row: row['distance_km'] / row['duration_hours'] 
        if row['duration_hours'] > 0 else None, 
        axis=1
    )

    # Criar GeoDataFrame para os pontos de origem
    gdf_origin = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.origin_lon, df.origin_lat), 
        crs="EPSG:4326"
    )
    
    # Criar GeoDataFrame para os pontos de destino
    gdf_destination = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.destination_lon, df.destination_lat), 
        crs="EPSG:4326"
    )
    
    logging.info("Pré-processamento de dados de malha viária concluído.")
    return df, gdf_origin, gdf_destination

if __name__ == "__main__":
    # Caminho para o arquivo de dados brutos
    raw_data_path = "data/raw/Etapa2_1_2_collect_road_network_raw_data.csv"
    
    # Verificar se o arquivo existe
    if not os.path.exists(raw_data_path):
        logging.error(f"Arquivo não encontrado: {raw_data_path}")
        exit(1)
    
    # Carregar os dados brutos
    try:
        raw_data = pd.read_csv(raw_data_path)
        logging.info(f"Dados carregados: {len(raw_data)} registros de {raw_data_path}")
    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        exit(1)
    
    # Pré-processar os dados
    processed_df, gdf_origin, gdf_destination = preprocess_road_network_data(raw_data)
    
    # Exibir amostra dos dados pré-processados
    print("\nDados de malha viária pré-processados (amostra):")
    print(processed_df.head())
    
    # Criar diretório para dados processados se não existir
    os.makedirs('data/processed', exist_ok=True)
    
    # Salvar os dados processados
    processed_path = "data/processed/Etapa2_2_2_road_network_processed_data.csv"
    processed_df.to_csv(processed_path, index=False)
    logging.info(f"Dados de malha viária pré-processados salvos em '{processed_path}'")
    
    # Salvar também em JSON para preservar tipos de dados
    json_path = "data/processed/Etapa2_2_2_road_network_processed_data.json"
    processed_df.to_json(json_path, orient='records', indent=2)
    logging.info(f"Dados de malha viária pré-processados salvos em JSON em '{json_path}'")
    
    # Salvar GeoDataFrames
    gdf_origin_path = "data/processed/Etapa2_2_2_road_network_origin_geodataframe.gpkg"
    gdf_origin.to_file(gdf_origin_path, driver="GPKG")
    logging.info(f"GeoDataFrame de origem salvo em '{gdf_origin_path}'")
    
    gdf_destination_path = "data/processed/Etapa2_2_2_road_network_destination_geodataframe.gpkg"
    gdf_destination.to_file(gdf_destination_path, driver="GPKG")
    logging.info(f"GeoDataFrame de destino salvo em '{gdf_destination_path}'")
    
    # Exibir estatísticas por cidade de origem
    print("\nEstatísticas por cidade de origem:")
    origin_stats = processed_df.groupby('origin').agg({
        'distance_km': ['mean', 'min', 'max', 'count'],
        'duration_hours': ['mean', 'min', 'max'],
        'avg_speed_kmh': ['mean', 'min', 'max']
    })
    print(origin_stats)
    
    # Exibir estatísticas por cidade de destino
    print("\nEstatísticas por cidade de destino:")
    destination_stats = processed_df.groupby('destination').agg({
        'distance_km': ['mean', 'min', 'max', 'count'],
        'duration_hours': ['mean', 'min', 'max'],
        'avg_speed_kmh': ['mean', 'min', 'max']
    })
    print(destination_stats)
    
    # Calcular e exibir estatísticas específicas para Recife e Salvador
    recife_routes = processed_df[(processed_df['origin'] == 'Recife') | (processed_df['destination'] == 'Recife')]
    salvador_routes = processed_df[(processed_df['origin'] == 'Salvador') | (processed_df['destination'] == 'Salvador')]
    
    print("\nEstatísticas para Recife:")
    print(f"Número de rotas: {len(recife_routes)}")
    print(f"Distância média: {recife_routes['distance_km'].mean():.2f} km")
    print(f"Tempo médio: {recife_routes['duration_hours'].mean():.2f} horas")
    print(f"Velocidade média: {recife_routes['avg_speed_kmh'].mean():.2f} km/h")
    
    print("\nEstatísticas para Salvador:")
    print(f"Número de rotas: {len(salvador_routes)}")
    print(f"Distância média: {salvador_routes['distance_km'].mean():.2f} km")
    print(f"Tempo médio: {salvador_routes['duration_hours'].mean():.2f} horas")
    print(f"Velocidade média: {salvador_routes['avg_speed_kmh'].mean():.2f} km/h")
    
    # Salvar estatísticas específicas
    stats = {
        'recife': {
            'avg_distance': recife_routes['distance_km'].mean(),
            'avg_duration': recife_routes['duration_hours'].mean(),
            'avg_speed': recife_routes['avg_speed_kmh'].mean(),
            'route_count': len(recife_routes)
        },
        'salvador': {
            'avg_distance': salvador_routes['distance_km'].mean(),
            'avg_duration': salvador_routes['duration_hours'].mean(),
            'avg_speed': salvador_routes['avg_speed_kmh'].mean(),
            'route_count': len(salvador_routes)
        }
    }
    
    stats_path = 'data/processed/Etapa2_2_2_road_network_stats.json'
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    logging.info(f"Estatísticas específicas salvas em '{stats_path}'")