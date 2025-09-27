import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import shap
import logging
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_demographic_data():
    """
    Carrega e transforma os dados demográficos para o formato wide.
    """
    logging.info("Carregando e transformando dados demográficos.")
    
    # Carregar dados demográficos
    demographic_path = "../ETAPA2/data/processed/Etapa2.2.3-5_demographic_processed_data.csv"
    if not os.path.exists(demographic_path):
        logging.error(f"Arquivo não encontrado: {demographic_path}")
        return None
    
    demographic_df = pd.read_csv(demographic_path)
    logging.info(f"Dados demográficos carregados: {len(demographic_df)} registros")
    logging.info(f"Colunas demográficas: {list(demographic_df.columns)}")
    
    # Transformar de formato long para wide
    # Pivotar a tabela para ter métricas como colunas
    try:
        demographic_wide = demographic_df.pivot_table(
            index=['city', 'year'],
            columns='metric',
            values='value',
            aggfunc='first'
        ).reset_index()
        
        logging.info(f"Dados demográficos após pivot: {len(demographic_wide)} registros")
        logging.info(f"Colunas após pivot: {list(demographic_wide.columns)}")
        
        # Carregar dados de consumo
        consumption_path = "../ETAPA2/data/processed/Etapa2.2.3-5_consumption_potential.csv"
        if os.path.exists(consumption_path):
            consumption_df = pd.read_csv(consumption_path)
            logging.info(f"Dados de consumo carregados: {len(consumption_df)} registros")
            
            # Mesclar com dados demográficos
            merged_df = pd.merge(
                demographic_wide,
                consumption_df[['city', 'consumption_potential_millions']],
                on='city',
                how='inner'
            )
            
            logging.info(f"Dados combinados: {len(merged_df)} cidades")
            return merged_df
        else:
            logging.warning("Arquivo de consumo não encontrado. Usando apenas dados demográficos.")
            return demographic_wide
            
    except Exception as e:
        logging.error(f"Erro ao transformar dados demográficos: {e}")
        return None

def preprocess_demographic_data(df):
    """
    Realiza o pré-processamento dos dados demográficos.
    """
    logging.info("Pré-processando dados demográficos.")
    
    if df is None or df.empty:
        logging.warning("DataFrame vazio ou nulo.")
        return None
    
    # Fazer uma cópia para evitar SettingWithCopyWarning
    df = df.copy()
    
    # Verificar colunas disponíveis
    logging.info(f"Colunas disponíveis: {list(df.columns)}")
    
    # Remover linhas com valores nulos críticos
    critical_columns = ['city']
    if 'population' in df.columns:
        critical_columns.append('population')
    if 'household_income' in df.columns:
        critical_columns.append('household_income')
    if 'consumption_potential_millions' in df.columns:
        critical_columns.append('consumption_potential_millions')
    
    initial_count = len(df)
    df.dropna(subset=critical_columns, inplace=True)
    removed_count = initial_count - len(df)
    logging.info(f"Removidas {removed_count} linhas com valores ausentes.")
    
    # Garantir que temos dados suficientes
    if len(df) < 2:
        logging.warning("Dados insuficientes após pré-processamento.")
        return None
    
    return df

def cluster_regions(df: pd.DataFrame, n_clusters: int = 2) -> pd.DataFrame:
    """
    Realiza a clusterização de regiões com base em dados demográficos.
    """
    logging.info(f"Iniciando clusterização de regiões com {n_clusters} clusters.")
    
    # Features para clusterização
    clustering_features = []
    
    # Adicionar features disponíveis
    if 'population' in df.columns:
        clustering_features.append('population')
    if 'household_income' in df.columns:
        clustering_features.append('household_income')
    if 'consumption_potential_millions' in df.columns:
        clustering_features.append('consumption_potential_millions')
    
    # Se não temos features suficientes, usar apenas o que temos
    if not clustering_features:
        logging.warning("Nenhuma feature disponível para clusterização. Retornando DataFrame original.")
        df["cluster"] = -1  # Marcar como não clusterizado
        return df
    
    logging.info(f"Features para clusterização: {clustering_features}")
    
    X = df[clustering_features].dropna()
    if X.empty:
        logging.warning("Dados insuficientes para clusterização após remoção de NaNs.")
        df["cluster"] = -1
        return df
    
    # Padronizar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Aplicar K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df.loc[X.index, "cluster"] = kmeans.fit_predict(X_scaled)
    
    # Analisar os clusters
    cluster_analysis = df.groupby("cluster")[clustering_features].mean()
    logging.info(f"Análise dos clusters:\n{cluster_analysis}")
    
    logging.info("Clusterização concluída.")
    return df

def train_consumption_model(df: pd.DataFrame) -> dict:
    """
    Treina um modelo preditivo para estimar o potencial de consumo.
    """
    logging.info("Iniciando treinamento do modelo de potencial de consumo.")
    
    # Definir features e target
    model_features = []
    
    # Adicionar features disponíveis
    if 'cluster' in df.columns:
        model_features.append('cluster')
    if 'population' in df.columns:
        model_features.append('population')
    if 'household_income' in df.columns:
        model_features.append('household_income')
    
    # Definir target
    target_col = None
    if 'consumption_potential_millions' in df.columns:
        target_col = 'consumption_potential_millions'
    elif 'population' in df.columns:
        target_col = 'population'
    
    if not model_features or target_col is None:
        logging.warning(f"Features ({model_features}) ou target ({target_col}) insuficientes para o modelo de consumo.")
        return {"model_trained": False, "message": "Dados insuficientes"}
    
    logging.info(f"Usando features: {model_features}")
    logging.info(f"Usando target: {target_col}")
    
    # Preparar dados para o modelo
    X = df[model_features].dropna()
    y = df.loc[X.index, target_col].dropna()
    
    # Garantir que X e y tenham o mesmo índice após dropna
    common_index = X.index.intersection(y.index)
    X = X.loc[common_index]
    y = y.loc[common_index]
    
    if len(X) < 2:  # Verificar se temos dados suficientes
        logging.warning("Dados insuficientes para treinar o modelo de consumo após limpeza.")
        return {"model_trained": False, "message": "Dados insuficientes após limpeza"}
    
    # Dividir em treino e teste
    # Se temos poucos dados, usar uma divisão menor para teste
    test_size = 0.2 if len(X) >= 5 else 0.1
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Treinar modelo
    model = XGBRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    # Avaliar modelo
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    logging.info(f"Modelo de consumo treinado. RMSE: {rmse:.2f}, R2: {r2:.2f}")
    
    # SHAP explainability
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
        
        # Sumarizar SHAP values (ex: média absoluta)
        feature_importance_shap = pd.Series(np.abs(shap_values).mean(axis=0), index=X_test.columns).to_dict()
    except Exception as e:
        logging.warning(f"Não foi possível calcular SHAP values: {e}")
        feature_importance_shap = {}
    
    return {
        "model_trained": True,
        "rmse": rmse,
        "r2_score": r2,
        "feature_importance_shap": feature_importance_shap,
        "model": model,  # Em um cenário real, o modelo seria serializado
        "features": model_features,
        "target": target_col
    }

def estimate_revenue_potential(df: pd.DataFrame, consumption_model_results: dict, penetration_rate: float = 0.05) -> dict:
    """
    Estima o potencial de receita incremental para cada cidade.
    """
    logging.info(f"Estimando potencial de receita com taxa de penetração de {penetration_rate*100:.2f}%")
    
    if not consumption_model_results["model_trained"]:
        return {"estimated_revenue": None, "message": "Modelo de consumo não treinado."}
    
    model = consumption_model_results["model"]
    model_features = consumption_model_results["features"]
    
    # Prever o consumo para todas as regiões
    # As features devem corresponder às usadas no treinamento
    available_features = [f for f in model_features if f in df.columns]
    
    if not available_features:
        logging.warning("Nenhuma feature correspondente encontrada para previsão de receita.")
        return {"estimated_revenue": None, "message": "Nenhuma feature correspondente para previsão."}
    
    try:
        df["predicted_consumption"] = model.predict(df[available_features])
    except Exception as e:
        logging.error(f"Erro na previsão de consumo: {e}")
        return {"estimated_revenue": None, "message": f"Erro na previsão: {e}"}
    
    # Agrupar por cidade e somar o potencial de consumo
    if 'city' in df.columns:
        city_potential = df.groupby("city")["predicted_consumption"].sum().to_dict()
    else:
        # Se não temos coluna 'city', usar o índice
        city_potential = df["predicted_consumption"].to_dict()
    
    estimated_revenue = {city: potential * penetration_rate for city, potential in city_potential.items()}
    
    return {
        "city_potential": city_potential,
        "estimated_revenue": estimated_revenue,
        "penetration_rate": penetration_rate
    }

def analyze_kpi3_consumption_potential(processed_demographic_df: pd.DataFrame) -> dict:
    """
    Realiza a análise para o KPI de Potencial de Consumo da Região.
    """
    logging.info("Iniciando análise para KPI 3: Potencial de Consumo da Região.")
    results = {}
    
    # 1. Clusterização de áreas
    # Com apenas 2 cidades, vamos usar 2 clusters
    n_clusters = min(2, len(processed_demographic_df))
    df_clustered = cluster_regions(processed_demographic_df.copy(), n_clusters=n_clusters)
    
    if 'cluster' in df_clustered.columns:
        results["cluster_distribution"] = df_clustered["cluster"].value_counts().to_dict()
        
        # Estatísticas por cluster
        cluster_stats = {}
        for cluster_id in df_clustered['cluster'].unique():
            if cluster_id != -1:  # Ignorar não clusterizados
                cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]
                cluster_stats[f"cluster_{cluster_id}"] = {
                    "count": len(cluster_data),
                    "cities": cluster_data['city'].tolist() if 'city' in cluster_data.columns else []
                }
                
                # Adicionar estatísticas numéricas se disponíveis
                numeric_cols = cluster_data.select_dtypes(include=[np.number]).columns
                for col in ['population', 'household_income', 'consumption_potential_millions']:
                    if col in numeric_cols:
                        cluster_stats[f"cluster_{cluster_id}"][f"avg_{col}"] = cluster_data[col].mean()
        
        results["cluster_stats"] = cluster_stats
    
    # 2. Treinar modelo preditivo de consumo
    consumption_model_results = train_consumption_model(df_clustered.copy())
    results["consumption_model_performance"] = {
        "rmse": consumption_model_results.get("rmse"),
        "r2_score": consumption_model_results.get("r2_score"),
        "feature_importance_shap": consumption_model_results.get("feature_importance_shap"),
        "model_trained": consumption_model_results.get("model_trained", False)
    }
    
    # 3. Estimar potencial de receita para diferentes cenários de penetração
    if consumption_model_results["model_trained"]:
        results["revenue_scenario_conservative"] = estimate_revenue_potential(
            df_clustered.copy(), consumption_model_results, penetration_rate=0.03
        )
        results["revenue_scenario_probable"] = estimate_revenue_potential(
            df_clustered.copy(), consumption_model_results, penetration_rate=0.05
        )
        results["revenue_scenario_aggressive"] = estimate_revenue_potential(
            df_clustered.copy(), consumption_model_results, penetration_rate=0.08
        )
    else:
        results["revenue_scenarios"] = {"message": "Modelo não treinado, não foi possível estimar receita."}
    
    # 4. Análise comparativa entre Recife e Salvador
    if 'city' in df_clustered.columns:
        recife_data = df_clustered[df_clustered['city'] == 'Recife']
        salvador_data = df_clustered[df_clustered['city'] == 'Salvador']
        
        if not recife_data.empty and not salvador_data.empty:
            results["city_comparison"] = {
                "recife": {
                    "population": float(recife_data['population'].iloc[0]) if 'population' in recife_data.columns else None,
                    "household_income": float(recife_data['household_income'].iloc[0]) if 'household_income' in recife_data.columns else None,
                    "consumption_potential": float(recife_data['consumption_potential_millions'].iloc[0]) if 'consumption_potential_millions' in recife_data.columns else None,
                    "cluster": int(recife_data['cluster'].iloc[0]) if 'cluster' in recife_data.columns else None
                },
                "salvador": {
                    "population": float(salvador_data['population'].iloc[0]) if 'population' in salvador_data.columns else None,
                    "household_income": float(salvador_data['household_income'].iloc[0]) if 'household_income' in salvador_data.columns else None,
                    "consumption_potential": float(salvador_data['consumption_potential_millions'].iloc[0]) if 'consumption_potential_millions' in salvador_data.columns else None,
                    "cluster": int(salvador_data['cluster'].iloc[0]) if 'cluster' in salvador_data.columns else None
                }
            }
    
    # 5. Estatísticas descritivas gerais
    numeric_cols = df_clustered.select_dtypes(include=[np.number]).columns
    if not df_clustered.empty and len(numeric_cols) > 0:
        results["descriptive_stats"] = df_clustered[numeric_cols].describe().to_dict()
    
    logging.info("Análise para KPI 3 concluída.")
    return results

if __name__ == "__main__":
    # Carregar e pré-processar dados demográficos
    demographic_data = load_demographic_data()
    processed_demographic = preprocess_demographic_data(demographic_data)
    
    if processed_demographic is None or processed_demographic.empty:
        logging.error("Não foi possível carregar ou processar os dados demográficos.")
        exit(1)
    
    # Realizar análise
    kpi3_results = analyze_kpi3_consumption_potential(processed_demographic)
    print("\nResultados da Análise KPI 3:")
    print(json.dumps(kpi3_results, indent=4, default=str))
    
    # Salvar resultados para uso posterior (ex: JSON)
    output_dir = "data/analysis"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Etapa3.3_kpi3_consumption_potential_results.json")
    
    with open(output_path, "w") as f:
        json.dump(kpi3_results, f, indent=4, default=str)
    
    logging.info(f"Resultados do KPI 3 salvos em '{output_path}'")