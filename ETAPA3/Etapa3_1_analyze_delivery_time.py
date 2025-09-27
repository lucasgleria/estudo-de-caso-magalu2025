import pandas as pd
import geopandas as gpd
import requests
import json
import networkx as nx
from shapely.geometry import Point, LineString
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_osrm_table(coords: list[tuple]) -> dict:
    """
    Obtém uma matriz de duração e distância do OSRM para um conjunto de coordenadas.
    coords: Lista de tuplas (latitude, longitude) para os pontos.
    """
    logging.info(f"Consultando OSRM table para {len(coords)} pontos.")
    osrm_url = "http://localhost:5000/table/v1/driving/"
    coords_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
    full_url = f"{osrm_url}{coords_str}"
    
    try:
        response = requests.get(full_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar OSRM table: {e}")
        return {}

def simulate_travel_time(base_duration: float, num_simulations: int = 100, variability_percent: float = 0.10) -> np.ndarray:
    """
    Simula a variabilidade do tempo de viagem usando Monte Carlo.
    base_duration: Duração base em segundos.
    num_simulations: Número de simulações.
    variability_percent: Percentual de variabilidade (ex: 0.10 para +/- 10%).
    """
    lower_bound = base_duration * (1 - variability_percent)
    upper_bound = base_duration * (1 + variability_percent)
    return np.random.uniform(lower_bound, upper_bound, num_simulations)

def create_road_network_graph(routes_df: pd.DataFrame) -> nx.DiGraph:
    """
    Cria um grafo da malha viária a partir dos dados de rotas.
    """
    G = nx.DiGraph()
    for _, row in routes_df.iterrows():
        G.add_edge(row["origin"], row["destination"], weight=row["duration_hours"], distance=row["distance_km"])
    return G

def generate_isochrones(origin_point: Point, max_travel_time_hours: list[int], routes_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Gera isócronas (áreas alcançáveis em determinado tempo) a partir de um ponto de origem.
    Esta é uma implementação simplificada e pode ser complexa na prática sem um serviço de isócronas dedicado.
    """
    logging.info(f"Gerando isócronas para {origin_point.wkt} para tempos: {max_travel_time_hours}")
    
    isochrones_data = []
    for time_limit in max_travel_time_hours:
        # Estimativa simplificada: assumindo velocidade média para calcular raio
        avg_speed_kmh = routes_df["distance_km"].sum() / routes_df["duration_hours"].sum() if not routes_df.empty else 60
        max_distance_km = avg_speed_kmh * time_limit
        
        # Converter km para graus aproximados para buffer (muito impreciso, apenas para esqueleto)
        buffer_degree = max_distance_km / 111.0
        isochrone_geometry = origin_point.buffer(buffer_degree)
        
        isochrones_data.append({
            "travel_time_hours": time_limit,
            "geometry": isochrone_geometry
        })
        
    return gpd.GeoDataFrame(isochrones_data, crs="EPSG:4326")

def analyze_kpi1_delivery_time(processed_routes_df: pd.DataFrame, origin_city_coords: dict) -> dict:
    """
    Realiza a análise para o KPI de Tempo Médio de Entrega.
    """
    logging.info("Iniciando análise para KPI 1: Tempo Médio de Entrega.")
    results = {}

    # 1. Roteamento determinístico (já feito na coleta, aqui usamos os dados processados)
    # Calcula médias e percentis dos tempos de viagem
    avg_delivery_time = processed_routes_df["duration_hours"].mean()
    median_delivery_time = processed_routes_df["duration_hours"].median()
    p75_delivery_time = processed_routes_df["duration_hours"].quantile(0.75)
    p90_delivery_time = processed_routes_df["duration_hours"].quantile(0.90)
    
    # Calcula médias e percentis das distâncias
    avg_distance = processed_routes_df["distance_km"].mean()
    median_distance = processed_routes_df["distance_km"].median()
    p75_distance = processed_routes_df["distance_km"].quantile(0.75)
    p90_distance = processed_routes_df["distance_km"].quantile(0.90)

    results["overall_delivery_stats"] = {
        "mean_hours": avg_delivery_time,
        "median_hours": median_delivery_time,
        "p75_hours": p75_delivery_time,
        "p90_hours": p90_delivery_time,
        "mean_distance_km": avg_distance,
        "median_distance_km": median_distance,
        "p75_distance_km": p75_distance,
        "p90_distance_km": p90_distance
    }
    logging.info(f"Estatísticas de tempo de entrega: {results['overall_delivery_stats']}")

    # 2. Simulação de incerteza (exemplo para um tempo médio)
    if not processed_routes_df.empty:
        sample_duration = processed_routes_df["duration_hours"].iloc[0] * 3600 # Converter para segundos
        simulated_times = simulate_travel_time(sample_duration) / 3600 # Converter de volta para horas
        results["simulated_delivery_times_mean"] = np.mean(simulated_times)
        results["simulated_delivery_times_std"] = np.std(simulated_times)
        logging.info(f"Simulação de incerteza (média/std): {results['simulated_delivery_times_mean']:.2f}h / {results['simulated_delivery_times_std']:.2f}h")

    # 3. Análise de Grafo (exemplo simplificado)
    G = create_road_network_graph(processed_routes_df)
    if G.nodes:
        centrality = nx.degree_centrality(G)
        results["network_centrality"] = centrality
        logging.info(f"Centralidade da rede (amostra): {list(centrality.items())[:2]}")

    # 4. Geração de Isócronas (exemplo para Recife e Salvador)
    recife_point = Point(origin_city_coords["Recife"][1], origin_city_coords["Recife"][0]) # (lon, lat)
    salvador_point = Point(origin_city_coords["Salvador"][1], origin_city_coords["Salvador"][0]) # (lon, lat)

    isochrones_recife = generate_isochrones(recife_point, [4, 8, 12], processed_routes_df)
    isochrones_salvador = generate_isochrones(salvador_point, [4, 8, 12], processed_routes_df)
    
    results["isochrones_recife"] = isochrones_recife.to_json()
    results["isochrones_salvador"] = isochrones_salvador.to_json()
    logging.info("Isócronas geradas para Recife e Salvador.")

    return results

if __name__ == "__main__":
    # Carregar dados de rotas processados
    processed_routes_path = "../ETAPA2/data/processed/Etapa2.2.2_road_network_processed_data.csv"
    if not os.path.exists(processed_routes_path):
        logging.error(f"Arquivo não encontrado: {processed_routes_path}")
        exit(1)
    
    processed_routes = pd.read_csv(processed_routes_path)
    logging.info(f"Dados de rotas carregados: {len(processed_routes)} registros")

    # Coordenadas das capitais (mesmas da Etapa 2)
    origin_coords = {
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

    kpi1_results = analyze_kpi1_delivery_time(processed_routes, origin_coords)
    print("\nResultados da Análise KPI 1:")
    for key, value in kpi1_results.items():
        if isinstance(value, str) and len(value) > 200: # Para evitar imprimir JSONs muito longos
            print(f"{key}: {value[:200]}...")
        else:
            print(f"{key}: {value}")

    # Salvar resultados para uso posterior (ex: JSON)
    output_dir = "data/analysis"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Etapa3.1_kpi1_delivery_time_results.json")
    with open(output_path, "w") as f:
        json.dump(kpi1_results, f, indent=4)
    logging.info(f"Resultados do KPI 1 salvos em '{output_path}'")