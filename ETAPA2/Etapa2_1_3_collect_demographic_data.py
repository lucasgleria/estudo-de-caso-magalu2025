import requests
import pandas as pd
import logging
import json
import os
from typing import Dict, List, Optional, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para obter códigos IBGE dos municípios
def get_municipality_codes() -> Dict[str, str]:
    """
    Obtém os códigos IBGE para Recife e Salvador usando a API de localidades.
    """
    logging.info("Obtendo códigos IBGE dos municípios")
    
    try:
        # API de localidades para obter todos os municípios
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        municipalities = response.json()
        
        # Encontrar códigos para Recife e Salvador
        codes = {}
        for municipality in municipalities:
            name = municipality['nome']
            code = municipality['id']
            
            if name == 'Recife':
                codes['Recife'] = code
                logging.info(f"Código IBGE para Recife: {code}")
            elif name == 'Salvador':
                codes['Salvador'] = code
                logging.info(f"Código IBGE para Salvador: {code}")
                
            # Se já encontramos ambos, podemos parar
            if len(codes) == 2:
                break
        
        return codes
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter códigos dos municípios: {e}")
        return {}

# Códigos IBGE para agregados e variáveis (conforme documentação do IBGE)
IBGE_INDICATORS = {
    'population': {
        'agregado': '6579',
        'variavel': '93',
        'descricao': 'População estimada'
    },
    'pib': {
        'agregado': '5938',
        'variavel': '37',
        'descricao': 'PIB a preços correntes'
    },
    'pib_per_capita': {
        'agregado': '5938',
        'variavel': '39',
        'descricao': 'PIB per capita a preços correntes'
    },
    'household_income': {
        'agregado': '5938',
        'variavel': '76',
        'descricao': 'Rendimento médio mensal dos domicílios'
    }
}

def get_ibge_data(api_url: str, params: dict = None) -> Dict:
    """
    Consulta a API do IBGE para obter dados demográficos e econômicos.
    """
    logging.info(f"Consultando API do IBGE: {api_url}")
    try:
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar API do IBGE: {e}")
        return {}

def parse_ibge_data(json_data: List[Dict], city: str, metric: str) -> pd.DataFrame:
    """
    Processa o JSON retornado pela API do IBGE.
    """
    if not json_data:
        return pd.DataFrame()
    
    parsed_data = []
    
    try:
        # A estrutura da resposta da API do IBGE
        for item in json_data:
            # Extrair o ano e o valor da série temporal
            serie = item.get('series', [{}])[0].get('serie', {})
            for year, value in serie.items():
                parsed_data.append({
                    'city': city,
                    'metric': metric,
                    'year': int(year),
                    'value': float(value)
                })
    except Exception as e:
        logging.error(f"Erro ao processar dados de {metric} para {city}: {e}")
    
    return pd.DataFrame(parsed_data)

def collect_ibge_data(city: str, metric: str, year: int = 2022, municipality_codes: Dict[str, str] = None) -> Optional[pd.DataFrame]:
    """
    Coleta dados específicos do IBGE para uma cidade e métrica.
    """
    if city not in municipality_codes:
        logging.error(f"Cidade {city} não encontrada nos códigos IBGE.")
        return None
    
    if metric not in IBGE_INDICATORS:
        logging.error(f"Métrica {metric} não encontrada nos indicadores IBGE.")
        return None
    
    city_code = municipality_codes[city]
    api_info = IBGE_INDICATORS[metric]
    
    # Construir a URL da API
    api_url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{api_info['agregado']}/periodos/{year}/variaveis/{api_info['variavel']}?localidades=N6[{city_code}]"
    
    # Fazer a requisição
    json_data = get_ibge_data(api_url)
    
    if not json_data:
        logging.warning(f"Nenhum dado retornado para {metric} em {city}")
        return None
    
    # Processar os dados
    return parse_ibge_data(json_data, city, metric)

def simulate_demographic_data() -> pd.DataFrame:
    """
    Simula dados demográficos e econômicos para desenvolvimento/testes.
    """
    logging.info("Simulando dados demográficos e econômicos")
    
    # Dados simulados para Recife (baseado em dados reais aproximados)
    recife_data = [
        {'city': 'Recife', 'metric': 'population', 'year': 2022, 'value': 1489094},
        {'city': 'Recife', 'metric': 'pib', 'year': 2022, 'value': 72800000000},
        {'city': 'Recife', 'metric': 'pib_per_capita', 'year': 2022, 'value': 48890.5},
        {'city': 'Recife', 'metric': 'household_income', 'year': 2022, 'value': 2850.0}
    ]
    
    # Dados simulados para Salvador (baseado em dados reais aproximados)
    salvador_data = [
        {'city': 'Salvador', 'metric': 'population', 'year': 2022, 'value': 2953986},
        {'city': 'Salvador', 'metric': 'pib', 'year': 2022, 'value': 92100000000},
        {'city': 'Salvador', 'metric': 'pib_per_capita', 'year': 2022, 'value': 31180.0},
        {'city': 'Salvador', 'metric': 'household_income', 'year': 2022, 'value': 2670.0}
    ]
    
    # Combinar os dados
    all_data = recife_data + salvador_data
    
    # Criar DataFrame
    df = pd.DataFrame(all_data)
    
    logging.info(f"Dados simulados criados: {len(df)} registros")
    return df

def collect_demographic_data(use_simulation: bool = True) -> pd.DataFrame:
    """
    Função principal para coletar dados demográficos e de potencial de consumo.
    """
    all_demographic_data = []
    
    if use_simulation:
        logging.info("Usando simulação de dados demográficos")
        return simulate_demographic_data()
    
    logging.info("Coletando dados reais da API do IBGE")
    
    # Obter códigos dos municípios
    municipality_codes = get_municipality_codes()
    if not municipality_codes:
        logging.error("Não foi possível obter códigos dos municípios. Usando simulação.")
        return simulate_demographic_data()
    
    # Métricas a serem coletadas
    metrics = ['population', 'pib', 'pib_per_capita', 'household_income']
    
    # Coletar dados para cada cidade e métrica
    for city in ['Recife', 'Salvador']:
        for metric in metrics:
            df = collect_ibge_data(city, metric, municipality_codes=municipality_codes)
            if df is not None and not df.empty:
                all_demographic_data.append(df)
    
    # Combinar todos os dados
    if all_demographic_data:
        final_df = pd.concat(all_demographic_data, ignore_index=True)
        logging.info(f"{len(final_df)} registros demográficos coletados.")
        return final_df
    else:
        logging.warning("Nenhum dado demográfico coletado. Usando simulação.")
        return simulate_demographic_data()

def calculate_consumption_potential(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o potencial de consumo com base nos dados demográficos e econômicos.
    """
    # Pivotar o DataFrame para ter métricas como colunas
    df_pivot = df.pivot_table(index=['city', 'year'], columns='metric', values='value').reset_index()
    
    # Calcular potencial de consumo (população * rendimento médio / 1000)
    df_pivot['consumption_potential_millions'] = df_pivot.apply(
        lambda row: (row['population'] * row['household_income']) / 1000000, axis=1
    )
    
    return df_pivot

if __name__ == "__main__":
    # Coletar dados demográficos
    # Definir como True para usar simulação, False para tentar API real
    use_simulation = False  # Mudado para False para usar API real
    
    df_demographic = collect_demographic_data(use_simulation=use_simulation)
    
    if not df_demographic.empty:
        print("\nDados demográficos coletados (amostra):")
        print(df_demographic.head())
        
        # Calcular potencial de consumo
        df_consumption = calculate_consumption_potential(df_demographic)
        
        print("\nPotencial de consumo calculado:")
        print(df_consumption)
        
        # Criar diretório para dados brutos se não existir
        os.makedirs('data/raw', exist_ok=True)
        
        # Salvar dados demográficos brutos
        demographic_path = 'data/raw/Etapa2_1_3_collect_demographic_raw_data.csv'
        df_demographic.to_csv(demographic_path, index=False)
        logging.info(f"Dados demográficos brutos salvos em '{demographic_path}'")
        
        # Salvar dados demográficos brutos em JSON
        demographic_json_path = 'data/raw/Etapa2_1_3_collect_demographic_raw_data.json'
        df_demographic.to_json(demographic_json_path, orient='records', indent=2)
        logging.info(f"Dados demográficos brutos salvos em JSON em '{demographic_json_path}'")
        
        # Salvar potencial de consumo
        consumption_path = 'data/raw/Etapa2_1_3_collect_consumption_potential.csv'
        df_consumption.to_csv(consumption_path, index=False)
        logging.info(f"Potencial de consumo salvo em '{consumption_path}'")
        
        # Salvar potencial de consumo em JSON
        consumption_json_path = 'data/raw/Etapa2_1_3_collect_consumption_potential.json'
        df_consumption.to_json(consumption_json_path, orient='records', indent=2)
        logging.info(f"Potencial de consumo salvo em JSON em '{consumption_json_path}'")
        
        # Exibir estatísticas comparativas
        print("\nEstatísticas comparativas:")
        
        # Comparação direta entre Recife e Salvador
        recife_data = df_consumption[df_consumption['city'] == 'Recife'].iloc[0]
        salvador_data = df_consumption[df_consumption['city'] == 'Salvador'].iloc[0]
        
        print(f"\nComparação Recife vs Salvador (2022):")
        print(f"População: Recife {recife_data['population']:.0f} vs Salvador {salvador_data['population']:.0f}")
        print(f"PIB: Recife R$ {recife_data['pib']/1000000000:.2f} bi vs Salvador R$ {salvador_data['pib']/1000000000:.2f} bi")
        print(f"PIB per capita: Recife R$ {recife_data['pib_per_capita']:.2f} vs Salvador R$ {salvador_data['pib_per_capita']:.2f}")
        print(f"Rendimento médio: Recife R$ {recife_data['household_income']:.2f} vs Salvador R$ {salvador_data['household_income']:.2f}")
        print(f"Potencial de consumo: Recife R$ {recife_data['consumption_potential_millions']:.2f} mi vs Salvador R$ {salvador_data['consumption_potential_millions']:.2f} mi")
        
        # Calcular vantagens percentuais
        pop_diff = ((recife_data['population'] / salvador_data['population']) - 1) * 100
        pib_diff = ((recife_data['pib'] / salvador_data['pib']) - 1) * 100
        pib_capita_diff = ((recife_data['pib_per_capita'] / salvador_data['pib_per_capita']) - 1) * 100
        income_diff = ((recife_data['household_income'] / salvador_data['household_income']) - 1) * 100
        consumption_diff = ((recife_data['consumption_potential_millions'] / salvador_data['consumption_potential_millions']) - 1) * 100
        
        print(f"\nVantagem de Recife sobre Salvador:")
        print(f"População: {pop_diff:.1f}%")
        print(f"PIB: {pib_diff:.1f}%")
        print(f"PIB per capita: {pib_capita_diff:.1f}%")
        print(f"Rendimento médio: {income_diff:.1f}%")
        print(f"Potencial de consumo: {consumption_diff:.1f}%")
        
        # Salvar estatísticas comparativas
        stats = {
            'recife_population': float(recife_data['population']),
            'salvador_population': float(salvador_data['population']),
            'recife_pib': float(recife_data['pib']),
            'salvador_pib': float(salvador_data['pib']),
            'recife_pib_per_capita': float(recife_data['pib_per_capita']),
            'salvador_pib_per_capita': float(salvador_data['pib_per_capita']),
            'recife_household_income': float(recife_data['household_income']),
            'salvador_household_income': float(salvador_data['household_income']),
            'recife_consumption_potential': float(recife_data['consumption_potential_millions']),
            'salvador_consumption_potential': float(salvador_data['consumption_potential_millions']),
            'population_diff_percent': pop_diff,
            'pib_diff_percent': pib_diff,
            'pib_capita_diff_percent': pib_capita_diff,
            'income_diff_percent': income_diff,
            'consumption_diff_percent': consumption_diff
        }
        
        stats_path = 'data/raw/Etapa2_1_3_collect_demographic_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(stats, f)
        logging.info(f"Estatísticas comparativas salvas em '{stats_path}'")
    else:
        logging.error("Não foi possível coletar dados demográficos.")