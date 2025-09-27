import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import logging
import json
import os
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_price(price_str):
    """
    Converte string de preço (ex: "R$ 1.500.000") para float.
    """
    if pd.isna(price_str):
        return np.nan
    
    if isinstance(price_str, (int, float)):
        return float(price_str)
    
    # Remover símbolos de moeda e espaços
    price_clean = re.sub(r'[R$\s.]', '', str(price_str))
    price_clean = price_clean.replace(',', '.')
    
    try:
        return float(price_clean)
    except (ValueError, TypeError):
        return np.nan

def clean_area(area_str):
    """
    Converte string de área (ex: "1500 m²") para float.
    """
    if pd.isna(area_str):
        return np.nan
    
    if isinstance(area_str, (int, float)):
        return float(area_str)
    
    # Remover "m²" e espaços
    area_clean = re.sub(r'[m²\s]', '', str(area_str))
    area_clean = area_clean.replace(',', '.')
    
    try:
        return float(area_clean)
    except (ValueError, TypeError):
        return np.nan

def preprocess_real_estate_data(df):
    """
    Realiza o pré-processamento dos dados imobiliários.
    """
    logging.info("Pré-processando dados imobiliários.")
    
    # Fazer uma cópia para evitar SettingWithCopyWarning
    df = df.copy()
    
    # Limpar colunas de preço e área
    df['price_clean'] = df['price'].apply(clean_price)
    df['area_clean'] = df['area'].apply(clean_area)
    
    # Calcular preço por m²
    df['price_m2'] = df.apply(
        lambda row: row['price_clean'] / row['area_clean'] 
        if row['price_clean'] > 0 and row['area_clean'] > 0 else np.nan, 
        axis=1
    )
    
    # Remover linhas com valores críticos ausentes
    initial_count = len(df)
    df.dropna(subset=['price_clean', 'area_clean', 'price_m2', 'city'], inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas com valores ausentes.")
    
    return df

def train_hedonic_model(df: pd.DataFrame) -> dict:
    """
    Treina um modelo hedônico para estimar o preço por m² de imóveis.
    """
    logging.info("Iniciando treinamento do modelo hedônico para custo imobiliário.")
    
    # Verificar se temos dados suficientes
    if len(df) < 10:
        logging.warning("Dados insuficientes para treinar o modelo hedônico.")
        return {"model_trained": False, "message": "Dados insuficientes"}
    
    # Features de exemplo (precisam ser refinadas com base nos dados reais)
    features = ['area_clean']
    
    # Adicionar features dummy para a cidade, se houver mais de uma
    if "city" in df.columns and df["city"].nunique() > 1:
        df = pd.get_dummies(df, columns=["city"], prefix="city", drop_first=True)
        features.extend([col for col in df.columns if col.startswith("city_")])
    
    # Adicionar log da área para capturar efeitos não lineares
    df["area_log"] = np.log1p(df["area_clean"])
    features.append("area_log")
    
    # Filtrar apenas as features que existem no DataFrame
    available_features = [f for f in features if f in df.columns]
    
    if not available_features:
        logging.warning("Nenhuma feature disponível para treinar o modelo.")
        return {"model_trained": False, "message": "Nenhuma feature disponível"}
    
    X = df[available_features]
    y = df["price_m2"]
    
    # Remover linhas com NaN nas features ou no target
    combined = pd.concat([X, y], axis=1).dropna()
    X = combined[available_features]
    y = combined["price_m2"]
    
    if X.empty or y.empty:
        logging.warning("Dados insuficientes para treinar o modelo hedônico após limpeza.")
        return {"model_trained": False, "message": "Dados insuficientes após limpeza"}
    
    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Usando GradientBoostingRegressor como exemplo de modelo robusto
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    logging.info(f"Modelo hedônico treinado. RMSE: {rmse:.2f}, R2: {r2:.2f}")
    
    return {
        "model_trained": True,
        "rmse": rmse,
        "r2_score": r2,
        "feature_importances": dict(zip(available_features, model.feature_importances_)),
        "model": model, # Em um cenário real, o modelo seria serializado (ex: pickle, joblib)
        "features": available_features
    }

def estimate_total_acquisition_cost(city_data: pd.DataFrame, model_results: dict, transaction_costs_percent: float = 0.05, adaptation_costs_percent: float = 0.10) -> dict:
    """
    Estima o custo total de aquisição para uma cidade, incluindo encargos.
    """
    city_name = city_data["city"].iloc[0] if not city_data.empty else "cidade desconhecida"
    logging.info(f"Estimando custo total de aquisição para {city_name}.")
    
    if not model_results["model_trained"] or city_data.empty:
        return {"estimated_cost": None, "message": "Modelo não treinado ou dados da cidade ausentes."}
    
    model = model_results["model"]
    features = model_results["features"]
    
    # Prever o preço por m² médio para a cidade usando o modelo
    # Criar um DataFrame de input para a previsão
    # Exemplo simplificado: usar a média das features da cidade para prever
    
    # Criar um DataFrame de exemplo para a previsão
    # Usar a mediana da área da cidade como representativa
    median_area = city_data["area_clean"].median()
    
    # Criar DataFrame com as features necessárias
    example_features = pd.DataFrame({
        "area_clean": [median_area],
        "area_log": [np.log1p(median_area)]
    })
    
    # Adicionar colunas dummy para a cidade, se aplicável
    if "city" in city_data.columns:
        # Inicializar todas as colunas de cidade com 0
        for feature in features:
            if feature.startswith("city_"):
                example_features[feature] = 0
        
        # Definir 1 para a cidade atual
        target_city_col = f"city_{city_name}"
        if target_city_col in example_features.columns:
            example_features[target_city_col] = 1
    
    # Filtrar apenas as colunas que o modelo espera
    model_features = [f for f in features if f in example_features.columns]
    
    if not model_features:
        logging.warning("Nenhuma feature correspondente encontrada para previsão.")
        return {"estimated_cost": None, "message": "Nenhuma feature correspondente para previsão."}
    
    # Garantir que as colunas estejam na ordem correta
    X_predict = example_features[model_features]
    
    try:
        predicted_price_m2 = model.predict(X_predict)[0]
    except Exception as e:
        logging.error(f"Erro na previsão: {e}")
        return {"estimated_cost": None, "message": f"Erro na previsão: {e}"}
    
    # Assumir uma área padrão para o CD para estimativa
    # Em um cenário real, esta área viria de requisitos de negócio
    cd_area_m2 = 10000  # Exemplo: 10.000 m²
    
    base_acquisition_cost = predicted_price_m2 * cd_area_m2
    total_transaction_costs = base_acquisition_cost * transaction_costs_percent
    total_adaptation_costs = base_acquisition_cost * adaptation_costs_percent
    
    total_capex = base_acquisition_cost + total_transaction_costs + total_adaptation_costs
    
    return {
        "city": city_name,
        "predicted_price_m2": predicted_price_m2,
        "cd_area_m2": cd_area_m2,
        "base_acquisition_cost": base_acquisition_cost,
        "transaction_costs": total_transaction_costs,
        "adaptation_costs": total_adaptation_costs,
        "total_capex": total_capex
    }

def analyze_kpi2_real_estate_cost(processed_real_estate_df: pd.DataFrame) -> dict:
    """
    Realiza a análise para o KPI de Custo de Aquisição Imobiliária.
    """
    logging.info("Iniciando análise para KPI 2: Custo de Aquisição Imobiliária.")
    results = {}
    
    # Pré-processar os dados
    df = preprocess_real_estate_data(processed_real_estate_df)
    
    # Verificar se temos dados suficientes após o pré-processamento
    if len(df) < 10:
        logging.warning("Dados insuficientes para análise após pré-processamento.")
        return {
            "error": "Dados insuficientes para análise após pré-processamento",
            "data_points": len(df)
        }
    
    # 1. Treinar modelo hedônico
    model_results = train_hedonic_model(df)
    results["hedonic_model_performance"] = {
        "rmse": model_results.get("rmse"),
        "r2_score": model_results.get("r2_score"),
        "feature_importances": model_results.get("feature_importances"),
        "model_trained": model_results.get("model_trained", False)
    }
    
    # 2. Estimar custo total de aquisição para Recife e Salvador
    recife_data = df[df["city"] == "Recife"]
    salvador_data = df[df["city"] == "Salvador"]
    
    if model_results["model_trained"]:
        if not recife_data.empty:
            results["capex_recife"] = estimate_total_acquisition_cost(recife_data, model_results)
        else:
            results["capex_recife"] = {"estimated_cost": None, "message": "Dados de Recife não disponíveis."}
            
        if not salvador_data.empty:
            results["capex_salvador"] = estimate_total_acquisition_cost(salvador_data, model_results)
        else:
            results["capex_salvador"] = {"estimated_cost": None, "message": "Dados de Salvador não disponíveis."}
    else:
        results["capex_recife"] = {"estimated_cost": None, "message": "Modelo não treinado."}
        results["capex_salvador"] = {"estimated_cost": None, "message": "Modelo não treinado."}
    
    # 3. Estatísticas descritivas por cidade
    if not recife_data.empty:
        results["stats_recife"] = {
            "avg_price_m2": recife_data["price_m2"].mean(),
            "median_price_m2": recife_data["price_m2"].median(),
            "avg_area_m2": recife_data["area_clean"].mean(),
            "property_count": len(recife_data)
        }
    
    if not salvador_data.empty:
        results["stats_salvador"] = {
            "avg_price_m2": salvador_data["price_m2"].mean(),
            "median_price_m2": salvador_data["price_m2"].median(),
            "avg_area_m2": salvador_data["area_clean"].mean(),
            "property_count": len(salvador_data)
        }
    
    logging.info("Análise para KPI 2 concluída.")
    return results

if __name__ == "__main__":
    # Carregar dados imobiliários processados
    processed_real_estate_path = "../ETAPA2/data/processed/Etapa2.2.1_real_estate_processed_data.csv"
    
    if not os.path.exists(processed_real_estate_path):
        logging.error(f"Arquivo não encontrado: {processed_real_estate_path}")
        exit(1)
    
    processed_real_estate = pd.read_csv(processed_real_estate_path)
    logging.info(f"Dados imobiliários carregados: {len(processed_real_estate)} registros")
    
    # Verificar colunas disponíveis
    logging.info(f"Colunas disponíveis: {list(processed_real_estate.columns)}")
    
    kpi2_results = analyze_kpi2_real_estate_cost(processed_real_estate)
    print("\nResultados da Análise KPI 2:")
    print(json.dumps(kpi2_results, indent=4, default=str))
    
    # Salvar resultados para uso posterior (ex: JSON)
    output_dir = "data/analysis"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Etapa3.2_kpi2_real_estate_cost_results.json")
    
    with open(output_path, "w") as f:
        json.dump(kpi2_results, f, indent=4, default=str)
    
    logging.info(f"Resultados do KPI 2 salvos em '{output_path}'")