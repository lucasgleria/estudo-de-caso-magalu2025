import pandas as pd
import logging
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_numeric_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Limpa e converte colunas numéricas, tratando valores não numéricos.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def calculate_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas derivadas, como densidade demográfica (exemplo).
    """
    # Placeholder: em um cenário real, precisaríamos de dados de área para calcular densidade
    # df["density"] = df["population"] / df["area_km2"]
    logging.info("Métricas derivadas calculadas (placeholder).")
    return df

def preprocess_demographic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o pré-processamento dos dados demográficos brutos.
    """
    logging.info("Iniciando pré-processamento de dados demográficos.")

    # Fazer uma cópia para evitar SettingWithCopyWarning
    df = df.copy()

    # Verificar se as colunas necessárias existem
    required_columns = ['city', 'metric', 'year', 'value']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logging.error(f"Colunas necessárias ausentes: {missing_columns}")
        return df

    # Limpar e converter colunas numéricas
    numeric_columns = ['value']
    df = clean_numeric_columns(df, numeric_columns)

    # Tratar valores ausentes
    initial_count = len(df)
    df.dropna(subset=['city', 'metric', 'value'], inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas com valores ausentes.")

    # Remover duplicatas
    initial_count = len(df)
    df.drop_duplicates(subset=['city', 'metric', 'year'], keep='first', inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas duplicadas.")

    # Calcular métricas derivadas
    df = calculate_derived_metrics(df)

    logging.info("Pré-processamento de dados demográficos concluído.")
    return df

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

def generate_comparative_stats(df_consumption: pd.DataFrame) -> dict:
    """
    Gera estatísticas comparativas entre as cidades.
    """
    # Verificar se temos dados para ambas as cidades
    if len(df_consumption) < 2:
        logging.warning("Não há dados suficientes para comparar cidades.")
        return {}
    
    # Comparação direta entre Recife e Salvador
    recife_data = df_consumption[df_consumption['city'] == 'Recife'].iloc[0]
    salvador_data = df_consumption[df_consumption['city'] == 'Salvador'].iloc[0]
    
    # Calcular vantagens percentuais
    pop_diff = ((recife_data['population'] / salvador_data['population']) - 1) * 100
    pib_diff = ((recife_data['pib'] / salvador_data['pib']) - 1) * 100
    pib_capita_diff = ((recife_data['pib_per_capita'] / salvador_data['pib_per_capita']) - 1) * 100
    income_diff = ((recife_data['household_income'] / salvador_data['household_income']) - 1) * 100
    consumption_diff = ((recife_data['consumption_potential_millions'] / salvador_data['consumption_potential_millions']) - 1) * 100
    
    return {
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

if __name__ == "__main__":
    # Caminho para o arquivo de dados brutos
    raw_data_path = "data/raw/Etapa2_1_3_collect_demographic_raw_data.csv"
    
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
    processed_df = preprocess_demographic_data(raw_data)
    
    # Exibir amostra dos dados pré-processados
    print("\nDados demográficos pré-processados (amostra):")
    print(processed_df.head())
    
    # Criar diretório para dados processados se não existir
    os.makedirs('data/processed', exist_ok=True)
    
    # Salvar os dados processados
    processed_path = "data/processed/Etapa2_2_3_5_demographic_processed_data.csv"
    processed_df.to_csv(processed_path, index=False)
    logging.info(f"Dados demográficos pré-processados salvos em '{processed_path}'")
    
    # Salvar também em JSON para preservar tipos de dados
    json_path = "data/processed/Etapa2_2_3_5_demographic_processed_data.json"
    processed_df.to_json(json_path, orient='records', indent=2)
    logging.info(f"Dados demográficos pré-processados salvos em JSON em '{json_path}'")
    
    # Calcular potencial de consumo
    df_consumption = calculate_consumption_potential(processed_df)
    
    print("\nPotencial de consumo calculado:")
    print(df_consumption)
    
    # Salvar potencial de consumo
    consumption_path = "data/processed/Etapa2_2_3_5_consumption_potential.csv"
    df_consumption.to_csv(consumption_path, index=False)
    logging.info(f"Potencial de consumo salvo em '{consumption_path}'")
    
    # Salvar potencial de consumo em JSON
    consumption_json_path = "data/processed/Etapa2_2_3_5_consumption_potential.json"
    df_consumption.to_json(consumption_json_path, orient='records', indent=2)
    logging.info(f"Potencial de consumo salvo em JSON em '{consumption_json_path}'")
    
    # Gerar estatísticas comparativas
    stats = generate_comparative_stats(df_consumption)
    
    if stats:
        # Exibir estatísticas comparativas
        print("\nEstatísticas comparativas:")
        
        print(f"\nComparação Recife vs Salvador (2022):")
        print(f"População: Recife {stats['recife_population']:.0f} vs Salvador {stats['salvador_population']:.0f}")
        print(f"PIB: Recife R$ {stats['recife_pib']/1000000000:.2f} bi vs Salvador R$ {stats['salvador_pib']/1000000000:.2f} bi")
        print(f"PIB per capita: Recife R$ {stats['recife_pib_per_capita']:.2f} vs Salvador R$ {stats['salvador_pib_per_capita']:.2f}")
        print(f"Rendimento médio: Recife R$ {stats['recife_household_income']:.2f} vs Salvador R$ {stats['salvador_household_income']:.2f}")
        print(f"Potencial de consumo: Recife R$ {stats['recife_consumption_potential']:.2f} mi vs Salvador R$ {stats['salvador_consumption_potential']:.2f} mi")
        
        print(f"\nVantagem de Recife sobre Salvador:")
        print(f"População: {stats['population_diff_percent']:.1f}%")
        print(f"PIB: {stats['pib_diff_percent']:.1f}%")
        print(f"PIB per capita: {stats['pib_capita_diff_percent']:.1f}%")
        print(f"Rendimento médio: {stats['income_diff_percent']:.1f}%")
        print(f"Potencial de consumo: {stats['consumption_diff_percent']:.1f}%")
        
        # Salvar estatísticas comparativas
        stats_path = 'data/processed/Etapa2_2_3_5_demographic_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        logging.info(f"Estatísticas comparativas salvas em '{stats_path}'")