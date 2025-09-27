import requests
import pandas as pd
import logging
import json
import time
import os
from typing import Dict, List, Tuple, Optional
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def query_overpass_api(bbox: str, query_type: str = 'way[highway]') -> Dict:
    """
    Consulta a Overpass API para extrair dados de malha viária.
    bbox: String no formato "lat_min,lon_min,lat_max,lon_max"
    query_type: Tipo de elemento OSM a ser consultado (ex: 'way[highway]', 'node[place=city]')
    """
    logging.info(f"Consultando Overpass API para bbox: {bbox} e tipo: {query_type}")
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    {query_type}({bbox});
    out body;
    >;
    out skel qt;
    """
    try:
        response = requests.post(overpass_url, data=overpass_query, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar Overpass API: {e}")
        return {}

def get_osrm_route_data(coords: List[Tuple], osrm_url: str = "http://router.project-osrm.org") -> Dict:
    """
    Obtém dados de rota (distância e tempo) do OSRM para um conjunto de coordenadas.
    coords: Lista de tuplas (latitude, longitude) para os pontos da rota.
    osrm_url: URL do servidor OSRM (padrão: instância pública)
    """
    logging.info(f"Consultando OSRM para {len(coords)} pontos.")
    
    # Formata as coordenadas para a URL do OSRM
    coords_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
    full_url = f"{osrm_url}/route/v1/driving/{coords_str}?overview=full&geometries=geojson"
    
    try:
        response = requests.get(full_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar OSRM: {e}")
        return {}

def get_osrm_table_data(origins: List[Tuple], destinations: List[Tuple], osrm_url: str = "http://router.project-osrm.org") -> Dict:
    """
    Obtém matriz de distâncias e tempos entre múltiplos pontos usando OSRM Table Service.
    origins: Lista de tuplas (latitude, longitude) para os pontos de origem.
    destinations: Lista de tuplas (latitude, longitude) para os pontos de destino.
    osrm_url: URL do servidor OSRM (padrão: instância pública)
    """
    logging.info(f"Consultando OSRM Table Service para {len(origins)} origens e {len(destinations)} destinos.")
    
    # Formata as coordenadas para a URL do OSRM
    origins_str = ";".join([f"{lon},{lat}" for lat, lon in origins])
    full_url = f"{osrm_url}/table/v1/driving/{origins_str}"
    
    # Adicionar destinos se forem diferentes das origens
    if origins != destinations:
        destinations_str = ";".join([f"{lon},{lat}" for lat, lon in destinations])
        full_url += f"?destinations={destinations_str}"
    
    try:
        response = requests.get(full_url, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar OSRM Table Service: {e}")
        return {}

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância entre dois pontos na Terra usando a fórmula de Haversine.
    Retorna a distância em quilômetros.
    """
    # Converter graus para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Raio da Terra em quilômetros
    r = 6371
    return c * r

def simulate_osrm_response(cities_coords: Dict[str, Tuple[float, float]]) -> Dict:
    """
    Simula uma resposta do OSRM para desenvolvimento/testes.
    """
    cities_list = list(cities_coords.keys())
    n = len(cities_list)
    
    # Criar matriz de distâncias simuladas (em metros)
    distances = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                # Calcular distância real usando Haversine
                lat1, lon1 = cities_coords[cities_list[i]]
                lat2, lon2 = cities_coords[cities_list[j]]
                distance_km = haversine_distance(lat1, lon1, lat2, lon2)
                row.append(distance_km * 1000)  # converter para metros
        distances.append(row)
    
    # Criar matriz de durações simuladas (em segundos)
    # Assumindo velocidade média de 60 km/h para estradas principais
    # e 40 km/h para distâncias mais curtas (dentro das cidades)
    durations = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                distance_km = distances[i][j] / 1000
                # Velocidade média baseada na distância
                if distance_km > 100:  # longas distâncias
                    avg_speed = 80  # km/h
                elif distance_km > 20:  # distâncias médias
                    avg_speed = 60  # km/h
                else:  # curtas distâncias
                    avg_speed = 40  # km/h
                
                # tempo = distância / velocidade
                duration = (distance_km / avg_speed) * 3600  # converter para segundos
                row.append(duration)
        durations.append(row)
    
    return {
        'distances': distances,
        'durations': durations,
        'sources': [{'location': [lon, lat], 'name': city} for city, (lat, lon) in cities_coords.items()],
        'destinations': [{'location': [lon, lat], 'name': city} for city, (lat, lon) in cities_coords.items()]
    }

def collect_road_network_data(cities_coords: Dict[str, Tuple[float, float]], osrm_url: str = "http://router.project-osrm.org") -> pd.DataFrame:
    """
    Função principal para coletar dados de malha viária e tempos de entrega.
    cities_coords: Dicionário com as coordenadas das cidades.
    osrm_url: URL do servidor OSRM.
    """
    all_routes_data = []
    
    # Coleta dados de malha viária para cada cidade
    for city, coords in cities_coords.items():
        lat, lon = coords
        # Criar um bbox de aproximadamente 0.2 graus ao redor da cidade
        bbox = f"{lat-0.1},{lon-0.1},{lat+0.1},{lon+0.1}"
        
        # Consultar por estradas
        highways_data = query_overpass_api(bbox, 'way[highway]')
        
        # Salvar dados brutos para análise posterior
        os.makedirs('data/raw', exist_ok=True)
        with open(f'data/raw/highways_{city.lower()}.json', 'w', encoding='utf-8') as f:
            json.dump(highways_data, f)
        
        logging.info(f"Dados de malha viária coletados para {city}: {len(highways_data.get('elements', []))} elementos")
    
    # Preparar lista de coordenadas para o OSRM
    cities_list = list(cities_coords.keys())
    coords_list = [cities_coords[city] for city in cities_list]
    
    # Obter matriz de distâncias e tempos entre todas as cidades
    table_data = get_osrm_table_data(coords_list, coords_list, osrm_url)
    
    # Verificar se obteve dados do OSRM
    if table_data and 'distances' in table_data and 'durations' in table_data:
        distances = table_data['distances']  # em metros
        durations = table_data['durations']  # em segundos
        
        # Converter para DataFrame
        for i, origin in enumerate(cities_list):
            for j, destination in enumerate(cities_list):
                if i != j:  # Ignorar rotas de uma cidade para ela mesma
                    distance_km = distances[i][j] / 1000  # converter para km
                    duration_hours = durations[i][j] / 3600  # converter para horas
                    
                    all_routes_data.append({
                        'origin': origin,
                        'destination': destination,
                        'distance_km': distance_km,
                        'duration_hours': duration_hours
                    })
    else:
        logging.warning("Não foi possível obter dados do OSRM. Usando simulação como fallback.")
        # Simular resposta do OSRM
        table_data = simulate_osrm_response(cities_coords)
        
        if 'distances' in table_data and 'durations' in table_data:
            distances = table_data['distances']  # em metros
            durations = table_data['durations']  # em segundos
            
            for i, origin in enumerate(cities_list):
                for j, destination in enumerate(cities_list):
                    if i != j:  # Ignorar rotas de uma cidade para ela mesma
                        distance_km = distances[i][j] / 1000  # converter para km
                        duration_hours = durations[i][j] / 3600  # converter para horas
                        
                        all_routes_data.append({
                            'origin': origin,
                            'destination': destination,
                            'distance_km': distance_km,
                            'duration_hours': duration_hours
                        })
    
    return pd.DataFrame(all_routes_data)

if __name__ == "__main__":
    # Verificar se devemos usar simulação ou OSRM real
    use_simulation = False  # Mudar para False quando quiser usar o OSRM real
    
    # URL do servidor OSRM (pode ser alterado para uma instância pública ou local)
    osrm_url = "http://router.project-osrm.org"
    
    # Coletar dados de malha viária e rotas
    if use_simulation:
        logging.info("Usando simulação de dados de rota (OSRM não disponível)")
        # Simular resposta do OSRM
        table_data = simulate_osrm_response(NORTHEAST_CAPITALS)
        
        # Converter para DataFrame
        all_routes_data = []
        cities_list = list(NORTHEAST_CAPITALS.keys())
        
        if 'distances' in table_data and 'durations' in table_data:
            distances = table_data['distances']  # em metros
            durations = table_data['durations']  # em segundos
            
            for i, origin in enumerate(cities_list):
                for j, destination in enumerate(cities_list):
                    if i != j:  # Ignorar rotas de uma cidade para ela mesma
                        distance_km = distances[i][j] / 1000  # converter para km
                        duration_hours = durations[i][j] / 3600  # converter para horas
                        
                        all_routes_data.append({
                            'origin': origin,
                            'destination': destination,
                            'distance_km': distance_km,
                            'duration_hours': duration_hours
                        })
        
        df_routes = pd.DataFrame(all_routes_data)
    else:
        logging.info(f"Usando OSRM real em {osrm_url}")
        try:
            df_routes = collect_road_network_data(NORTHEAST_CAPITALS, osrm_url)
            
            # Se o DataFrame estiver vazio, usar simulação como fallback
            if df_routes.empty:
                logging.warning("OSRM real retornou dados vazios. Usando simulação como fallback.")
                # Simular resposta do OSRM
                table_data = simulate_osrm_response(NORTHEAST_CAPITALS)
                
                # Converter para DataFrame
                all_routes_data = []
                cities_list = list(NORTHEAST_CAPITALS.keys())
                
                if 'distances' in table_data and 'durations' in table_data:
                    distances = table_data['distances']  # em metros
                    durations = table_data['durations']  # em segundos
                    
                    for i, origin in enumerate(cities_list):
                        for j, destination in enumerate(cities_list):
                            if i != j:  # Ignorar rotas de uma cidade para ela mesma
                                distance_km = distances[i][j] / 1000  # converter para km
                                duration_hours = durations[i][j] / 3600  # converter para horas
                                
                                all_routes_data.append({
                                    'origin': origin,
                                    'destination': destination,
                                    'distance_km': distance_km,
                                    'duration_hours': duration_hours
                                })
                
                df_routes = pd.DataFrame(all_routes_data)
        except Exception as e:
            logging.error(f"Erro ao usar OSRM real: {e}")
            logging.info("Usando simulação como fallback.")
            
            # Simular resposta do OSRM
            table_data = simulate_osrm_response(NORTHEAST_CAPITALS)
            
            # Converter para DataFrame
            all_routes_data = []
            cities_list = list(NORTHEAST_CAPITALS.keys())
            
            if 'distances' in table_data and 'durations' in table_data:
                distances = table_data['distances']  # em metros
                durations = table_data['durations']  # em segundos
                
                for i, origin in enumerate(cities_list):
                    for j, destination in enumerate(cities_list):
                        if i != j:  # Ignorar rotas de uma cidade para ela mesma
                            distance_km = distances[i][j] / 1000  # converter para km
                            duration_hours = durations[i][j] / 3600  # converter para horas
                            
                            all_routes_data.append({
                                'origin': origin,
                                'destination': destination,
                                'distance_km': distance_km,
                                'duration_hours': duration_hours
                            })
            
            df_routes = pd.DataFrame(all_routes_data)
    
    # Verificar se o DataFrame está vazio antes de continuar
    if df_routes.empty:
        logging.error("Não foi possível obter dados de rota. O DataFrame está vazio.")
        exit(1)
    
    print("\nDados de rotas coletados (amostra):")
    print(df_routes.head())
    
    # Criar diretório para dados brutos se não existir
    os.makedirs('data/raw', exist_ok=True)
    
    # Salvar para processamento posterior
    output_path = 'data/raw/Etapa2_1_2_collect_road_network_raw_data.csv'
    df_routes.to_csv(output_path, index=False)
    logging.info(f"Dados de malha viária e rotas brutos salvos em '{output_path}'")
    
    # Salvar também em JSON
    json_path = 'data/raw/Etapa2_1_2_collect_road_network_raw_data.json'
    df_routes.to_json(json_path, orient='records', indent=2)
    logging.info(f"Dados de malha viária e rotas brutos salvos em JSON em '{json_path}'")
    
    # Exibir estatísticas básicas
    print("\nEstatísticas básicas:")
    print(f"Total de rotas: {len(df_routes)}")
    print(f"Distância média: {df_routes['distance_km'].mean():.2f} km")
    print(f"Tempo médio: {df_routes['duration_hours'].mean():.2f} horas")
    
    # Exibir matriz de distâncias
    print("\nMatriz de distâncias (km):")
    distance_matrix = df_routes.pivot(index='origin', columns='destination', values='distance_km')
    print(distance_matrix)
    
    # Exibir matriz de tempos
    print("\nMatriz de tempos (horas):")
    duration_matrix = df_routes.pivot(index='origin', columns='destination', values='duration_hours')
    print(duration_matrix)
    
    # Calcular e exibir estatísticas específicas para Recife e Salvador
    recife_routes = df_routes[(df_routes['origin'] == 'Recife') | (df_routes['destination'] == 'Recife')]
    salvador_routes = df_routes[(df_routes['origin'] == 'Salvador') | (df_routes['destination'] == 'Salvador')]
    
    print("\nEstatísticas para Recife:")
    print(f"Número de rotas: {len(recife_routes)}")
    print(f"Distância média: {recife_routes['distance_km'].mean():.2f} km")
    print(f"Tempo médio: {recife_routes['duration_hours'].mean():.2f} horas")
    
    print("\nEstatísticas para Salvador:")
    print(f"Número de rotas: {len(salvador_routes)}")
    print(f"Distância média: {salvador_routes['distance_km'].mean():.2f} km")
    print(f"Tempo médio: {salvador_routes['duration_hours'].mean():.2f} horas")
    
    # Salvar estatísticas específicas
    stats = {
        'recife_avg_distance': recife_routes['distance_km'].mean(),
        'recife_avg_duration': recife_routes['duration_hours'].mean(),
        'salvador_avg_distance': salvador_routes['distance_km'].mean(),
        'salvador_avg_duration': salvador_routes['duration_hours'].mean()
    }
    
    stats_path = 'data/raw/Etapa2_1_2_collect_road_network_stats.json'
    with open(stats_path, 'w') as f:
        json.dump(stats, f)
    logging.info(f"Estatísticas específicas salvas em '{stats_path}'")