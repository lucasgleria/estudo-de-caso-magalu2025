import mlflow
import mlflow.sklearn
import mlflow.xgboost
import logging
import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_processed_data():
    """
    Carrega e combina os dados processados das etapas anteriores.
    """
    logging.info("Carregando dados processados para experimentos de ML.")
    
    # Carregar dados demográficos
    demographic_path = "../ETAPA2/data/processed/Etapa2.2.3-5_demographic_processed_data.csv"
    demographic_df = pd.read_csv(demographic_path) if os.path.exists(demographic_path) else pd.DataFrame()
    
    # Carregar dados de consumo
    consumption_path = "../ETAPA2/data/processed/Etapa2.2.3-5_consumption_potential.csv"
    consumption_df = pd.read_csv(consumption_path) if os.path.exists(consumption_path) else pd.DataFrame()
    
    # Carregar dados de imóveis
    real_estate_path = "../ETAPA2/data/processed/Etapa2.2.1_real_estate_processed_data.csv"
    real_estate_df = pd.read_csv(real_estate_path) if os.path.exists(real_estate_path) else pd.DataFrame()
    
    # Carregar dados de malha viária
    road_network_path = "../ETAPA2/data/processed/Etapa2.2.2_road_network_processed_data.csv"
    road_network_df = pd.read_csv(road_network_path) if os.path.exists(road_network_path) else pd.DataFrame()
    
    # Combinar dados demográficos e de consumo
    if not demographic_df.empty and not consumption_df.empty:
        # Transformar dados demográficos para formato wide
        demographic_wide = demographic_df.pivot_table(
            index=['city', 'year'],
            columns='metric',
            values='value',
            aggfunc='first'
        ).reset_index()
        
        # Usar apenas o ano mais recente
        demographic_wide = demographic_wide.sort_values('year').groupby('city').last().reset_index()
        
        # Combinar com dados de consumo
        combined_df = pd.merge(
            demographic_wide,
            consumption_df[['city', 'consumption_potential_millions']],
            on='city',
            how='inner'
        )
        
        # Adicionar estatísticas de imóveis
        if not real_estate_df.empty:
            real_estate_stats = real_estate_df.groupby('city').agg({
                'price': 'mean',
                'area': 'mean'
            }).reset_index()
            real_estate_stats.columns = ['city', 'avg_property_price', 'avg_property_area']
            
            combined_df = pd.merge(combined_df, real_estate_stats, on='city', how='left')
        
        # Adicionar estatísticas de malha viária
        if not road_network_df.empty:
            road_network_stats = road_network_df.groupby('origin').agg({
                'distance_km': 'mean',
                'duration_hours': 'mean',
                'avg_speed_kmh': 'mean'
            }).reset_index()
            road_network_stats.columns = ['city', 'avg_distance_km', 'avg_duration_hours', 'avg_speed_kmh']
            
            combined_df = pd.merge(combined_df, road_network_stats, on='city', how='left')
        
        logging.info(f"Dados combinados: {len(combined_df)} cidades")
        return combined_df
    
    return pd.DataFrame()

def generate_synthetic_data(base_df, n_samples=100):
    """
    Gera dados sintéticos com base nos dados reais para permitir treinamento de modelos.
    """
    logging.info(f"Gerando {n_samples} amostras sintéticas baseadas nos dados reais.")
    
    if base_df.empty:
        logging.error("DataFrame base está vazio. Não é possível gerar dados sintéticos.")
        return pd.DataFrame()
    
    synthetic_data = []
    
    for _, row in base_df.iterrows():
        city = row['city']
        
        # Gerar variações em torno dos valores reais
        for i in range(n_samples // len(base_df)):
            new_row = row.copy()
            
            # Adicionar ruído às variáveis numéricas
            for col in ['population', 'household_income', 'avg_property_price', 
                       'avg_property_area', 'avg_distance_km', 'avg_duration_hours', 'avg_speed_kmh']:
                if col in new_row and pd.notna(new_row[col]):
                    # Ruído gaussiano com 10% de variação
                    noise = np.random.normal(0, new_row[col] * 0.1)
                    new_row[col] = max(0, new_row[col] + noise)
            
            # Recalcular target com base nas features modificadas
            if 'consumption_potential_millions' in new_row:
                # Modelo simples: consumo = população * renda * fator
                population_factor = new_row['population'] / 1_000_000  # Em milhões
                income_factor = new_row['household_income'] / 30_000  # Normalizado
                new_row['consumption_potential_millions'] = population_factor * income_factor * 10
            
            if 'simulated_operational_cost' in new_row:
                # Modelo simples: custo = preço_imóvel * fator + distância * fator
                price_factor = new_row['avg_property_price'] * 0.0001
                distance_factor = new_row['avg_distance_km'] * 0.5
                new_row['simulated_operational_cost'] = price_factor + distance_factor
            
            synthetic_data.append(new_row)
    
    synthetic_df = pd.DataFrame(synthetic_data)
    logging.info(f"Dados sintéticos gerados: {len(synthetic_df)} amostras")
    return synthetic_df

def prepare_features_and_target(df, target_column='consumption_potential_millions'):
    """
    Prepara features e target para o modelo de ML.
    """
    if df.empty:
        return None, None
    
    # Features para o modelo
    feature_columns = []
    
    # Adicionar features numéricas disponíveis
    numeric_features = [
        'population', 'household_income', 'avg_property_price', 
        'avg_property_area', 'avg_distance_km', 'avg_duration_hours', 'avg_speed_kmh'
    ]
    
    for feature in numeric_features:
        if feature in df.columns:
            feature_columns.append(feature)
    
    # Remover linhas com valores nulos nas features ou no target
    df_clean = df[feature_columns + [target_column]].dropna()
    
    if len(df_clean) < 5:  # Aumentado o mínimo para 5
        logging.warning("Dados insuficientes após limpeza.")
        return None, None
    
    X = df_clean[feature_columns]
    y = df_clean[target_column]
    
    logging.info(f"Features preparadas: {feature_columns}")
    logging.info(f"Target: {target_column}")
    logging.info(f"Amostras: {len(X)}")
    
    return X, y

def run_experiment(model_name: str, params: dict, X: pd.DataFrame, y: pd.Series, experiment_name: str):
    """
    Executa um experimento de MLflow para rastrear o treinamento de um modelo.
    """
    with mlflow.start_run(run_name=model_name, experiment_id=mlflow.get_experiment_by_name(experiment_name).experiment_id) as run:
        mlflow.log_params(params)
        mlflow.log_param("model_type", model_name)
        mlflow.log_param("n_features", X.shape[1])
        mlflow.log_param("n_samples", X.shape[0])
        
        # Para poucos dados, usar validação cruzada em vez de split treino/teste
        if len(X) < 20:
            logging.info("Usando validação cruzada devido ao pequeno número de amostras.")
            
            if model_name == "GradientBoostingRegressor":
                model = GradientBoostingRegressor(**params)
                # Usar K-Fold com k=min(5, n_samples)
                k = min(5, len(X))
                if k < 2:
                    k = 2
                kf = KFold(n_splits=k, shuffle=True, random_state=42)
                
                cv_scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
                rmse_scores = np.sqrt(-cv_scores)
                rmse = rmse_scores.mean()
                rmse_std = rmse_scores.std()
                
                # Treinar modelo final com todos os dados
                model.fit(X, y)
                
                mlflow.log_metrics({
                    "rmse": rmse,
                    "rmse_std": rmse_std,
                    "cv_folds": k
                })
                
            elif model_name == "XGBRegressor":
                model = xgb.XGBRegressor(**params)
                # Usar K-Fold com k=min(5, n_samples)
                k = min(5, len(X))
                if k < 2:
                    k = 2
                kf = KFold(n_splits=k, shuffle=True, random_state=42)
                
                cv_scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
                rmse_scores = np.sqrt(-cv_scores)
                rmse = rmse_scores.mean()
                rmse_std = rmse_scores.std()
                
                # Treinar modelo final com todos os dados
                model.fit(X, y)
                
                mlflow.log_metrics({
                    "rmse": rmse,
                    "rmse_std": rmse_std,
                    "cv_folds": k
                })
        else:
            # Para mais dados, usar split treino/teste tradicional
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            if model_name == "GradientBoostingRegressor":
                model = GradientBoostingRegressor(**params)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2 = r2_score(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                
                mlflow.log_metrics({
                    "rmse": rmse,
                    "r2_score": r2,
                    "mae": mae
                })
                
            elif model_name == "XGBRegressor":
                model = xgb.XGBRegressor(**params)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2 = r2_score(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                
                mlflow.log_metrics({
                    "rmse": rmse,
                    "r2_score": r2,
                    "mae": mae
                })
        
        # Logar modelo com input example para melhor rastreamento
        input_example = X.head(1)
        if model_name == "GradientBoostingRegressor":
            mlflow.sklearn.log_model(model, "model", input_example=input_example)
        elif model_name == "XGBRegressor":
            mlflow.xgboost.log_model(model, "model", input_example=input_example)
        
        # Logar feature importances
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(zip(X.columns, model.feature_importances_))
            mlflow.log_dict(feature_importance, "feature_importance")
        
        logging.info(f"MLflow Run ID: {run.info.run_id} - Modelo treinado com sucesso")

def perform_data_validation(df: pd.DataFrame, expected_columns: list, min_rows: int = 5):
    """
    Realiza validações básicas nos dados de entrada.
    """
    logging.info("Iniciando validação de dados...")
    
    # 1. Verificar se o DataFrame está vazio
    if df.empty:
        logging.error("DataFrame vazio.")
        raise ValueError("DataFrame de entrada está vazio.")
    
    # 2. Verificar colunas esperadas
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Colunas ausentes: {missing_columns}")
        raise ValueError(f"Dados de entrada não contêm as colunas esperadas: {missing_columns}")
    
    # 3. Verificar número mínimo de linhas
    if len(df) < min_rows:
        logging.error(f"Número de linhas ({len(df)}) abaixo do mínimo esperado ({min_rows}).")
        raise ValueError(f"Dados de entrada insuficientes: {len(df)} linhas encontradas.")
    
    # 4. Verificar valores nulos em colunas críticas
    critical_columns = [col for col in expected_columns if col in df.columns and df[col].isnull().any()]
    if critical_columns:
        logging.warning(f"Valores nulos encontrados nas colunas críticas: {critical_columns}")
    
    logging.info("Validação de dados concluída com sucesso.")

def setup_mlflow_tracking(tracking_uri: str = "./mlruns"):
    """
    Configura o URI de rastreamento do MLflow.
    """
    mlflow.set_tracking_uri(tracking_uri)
    logging.info(f"MLflow tracking URI configurado para: {tracking_uri}")

def create_experiments():
    """
    Cria experimentos no MLflow para diferentes targets.
    """
    experiments = [
        "consumption_prediction",
        "operational_cost_prediction",
        "delivery_time_prediction"
    ]
    
    for exp_name in experiments:
        try:
            experiment = mlflow.get_experiment_by_name(exp_name)
            if experiment is None:
                mlflow.create_experiment(exp_name)
                logging.info(f"Experimento '{exp_name}' criado.")
            else:
                logging.info(f"Experimento '{exp_name}' já existe.")
        except Exception as e:
            logging.error(f"Erro ao criar experimento '{exp_name}': {e}")

if __name__ == "__main__":
    # Configurar MLflow
    setup_mlflow_tracking()
    
    # Criar experimentos
    create_experiments()
    
    # Carregar dados processados
    processed_data = load_processed_data()
    
    if processed_data.empty:
        logging.error("Não foi possível carregar os dados processados.")
        sys.exit(1)
    
    # Gerar dados sintéticos para permitir treinamento adequado
    synthetic_data = generate_synthetic_data(processed_data, n_samples=100)
    
    if synthetic_data.empty:
        logging.error("Não foi possível gerar dados sintéticos.")
        sys.exit(1)
    
    # Experimento 1: Previsão de Potencial de Consumo
    logging.info("=" * 50)
    logging.info("Experimento 1: Previsão de Potencial de Consumo")
    logging.info("=" * 50)
    
    X_consumption, y_consumption = prepare_features_and_target(synthetic_data, 'consumption_potential_millions')
    
    if X_consumption is not None:
        expected_cols = X_consumption.columns.tolist() + ['consumption_potential_millions']
        try:
            perform_data_validation(synthetic_data, expected_cols, min_rows=5)
            
            # Parâmetros para GradientBoosting
            gb_params = {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 3,
                "random_state": 42
            }
            run_experiment("GradientBoostingRegressor", gb_params, X_consumption, y_consumption, "consumption_prediction")
            
            # Parâmetros para XGBoost
            xgb_params = {
                "n_estimators": 150,
                "learning_rate": 0.05,
                "max_depth": 4,
                "random_state": 42
            }
            run_experiment("XGBRegressor", xgb_params, X_consumption, y_consumption, "consumption_prediction")
            
        except ValueError as e:
            logging.error(f"Erro de validação de dados: {e}")
    
    # Experimento 2: Previsão de Custo Operacional (simulado)
    logging.info("=" * 50)
    logging.info("Experimento 2: Previsão de Custo Operacional (simulado)")
    logging.info("=" * 50)
    
    # Simular custo operacional baseado nas features
    synthetic_data['simulated_operational_cost'] = (
        synthetic_data['avg_property_price'] * 0.0001 +  # 0.01% do preço do imóvel
        synthetic_data['avg_distance_km'] * 0.5 +        # R$ 0.50 por km
        synthetic_data['population'] * 0.000001          # R$ 0.001 por habitante
    )
    
    X_operational, y_operational = prepare_features_and_target(synthetic_data, 'simulated_operational_cost')
    
    if X_operational is not None:
        expected_cols = X_operational.columns.tolist() + ['simulated_operational_cost']
        try:
            perform_data_validation(synthetic_data, expected_cols, min_rows=5)
            
            # Parâmetros para GradientBoosting
            gb_params = {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 3,
                "random_state": 42
            }
            run_experiment("GradientBoostingRegressor", gb_params, X_operational, y_operational, "operational_cost_prediction")
            
            # Parâmetros para XGBoost
            xgb_params = {
                "n_estimators": 150,
                "learning_rate": 0.05,
                "max_depth": 4,
                "random_state": 42
            }
            run_experiment("XGBRegressor", xgb_params, X_operational, y_operational, "operational_cost_prediction")
            
        except ValueError as e:
            logging.error(f"Erro de validação de dados: {e}")
    
    logging.info("Experimentos de ML concluídos. Verifique o diretório 'mlruns' para os logs do MLflow.")
    logging.info("Para visualizar os resultados, execute: mlflow ui")