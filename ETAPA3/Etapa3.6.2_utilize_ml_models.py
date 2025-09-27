import mlflow
import mlflow.sklearn
import mlflow.xgboost
import pandas as pd
import numpy as np
import logging
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_trained_model(run_id, model_type="sklearn"):
    """
    Carrega um modelo treinado do MLflow usando o Run ID.
    """
    try:
        model_uri = f"runs:/{run_id}/model"
        
        if model_type == "sklearn":
            model = mlflow.sklearn.load_model(model_uri)
        elif model_type == "xgboost":
            model = mlflow.xgboost.load_model(model_uri)
        else:
            raise ValueError(f"Tipo de modelo não suportado: {model_type}")
        
        logging.info(f"Modelo carregado com sucesso do Run ID: {run_id}")
        return model
    except Exception as e:
        logging.error(f"Erro ao carregar modelo do Run ID {run_id}: {e}")
        return None

def prepare_prediction_data(city_data):
    """
    Prepara os dados para fazer previsões.
    """
    # Criar DataFrame com as features necessárias
    features = [
        'population', 'household_income', 'avg_property_price', 
        'avg_property_area', 'avg_distance_km', 'avg_duration_hours', 'avg_speed_kmh'
    ]
    
    df = pd.DataFrame([city_data])
    
    # Verificar se todas as features estão presentes
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        logging.error(f"Features ausentes: {missing_features}")
        return None
    
    return df[features]

def make_predictions(model, data, model_name):
    """
    Faz previsões usando o modelo carregado.
    """
    try:
        predictions = model.predict(data)
        logging.info(f"Previsões feitas com sucesso usando {model_name}")
        return predictions
    except Exception as e:
        logging.error(f"Erro ao fazer previsões com {model_name}: {e}")
        return None

def analyze_feature_importance(model, features, model_name):
    """
    Analisa e visualiza a importância das features.
    """
    if hasattr(model, 'feature_importances_'):
        # Criar DataFrame com as importâncias
        importance_df = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Plotar gráfico de importância
        plt.figure(figsize=(10, 6))
        sns.barplot(x='importance', y='feature', data=importance_df)
        plt.title(f'Feature Importance - {model_name}')
        plt.tight_layout()
        
        # Salvar o gráfico
        os.makedirs('data/analysis', exist_ok=True)
        plt.savefig(f'data/analysis/feature_importance_{model_name}.png')
        plt.close()
        
        logging.info(f"Gráfico de importância salvo para {model_name}")
        return importance_df
    else:
        logging.warning(f"Modelo {model_name} não possui atributo feature_importances_")
        return None

def compare_cities_with_models(models_info, cities_data):
    """
    Compara diferentes cidades usando os modelos treinados.
    """
    results = {}
    
    for model_name, model_info in models_info.items():
        model = model_info['model']
        target = model_info['target']
        
        results[model_name] = {}
        
        for city_name, city_data in cities_data.items():
            # Preparar dados para a cidade
            data = prepare_prediction_data(city_data)
            
            if data is not None:
                # Fazer previsão
                prediction = make_predictions(model, data, model_name)
                
                if prediction is not None:
                    results[model_name][city_name] = {
                        'prediction': prediction[0],
                        'unit': target
                    }
    
    return results

def generate_business_insights(results):
    """
    Gera insights de negócio com base nos resultados.
    """
    insights = []
    
    # Comparar previsões de consumo
    if 'consumption_gb' in results:
        consumption_results = results['consumption_gb']
        
        if 'Recife' in consumption_results and 'Salvador' in consumption_results:
            recife_consumption = consumption_results['Recife']['prediction']
            salvador_consumption = consumption_results['Salvador']['prediction']
            
            if recife_consumption > salvador_consumption:
                diff_percent = ((recife_consumption - salvador_consumption) / salvador_consumption) * 100
                insights.append(f"Recife tem {diff_percent:.1f}% mais potencial de consumo que Salvador")
            else:
                diff_percent = ((salvador_consumption - recife_consumption) / recife_consumption) * 100
                insights.append(f"Salvador tem {diff_percent:.1f}% mais potencial de consumo que Recife")
    
    # Comparar previsões de custo operacional
    if 'operational_cost_gb' in results:
        cost_results = results['operational_cost_gb']
        
        if 'Recife' in cost_results and 'Salvador' in cost_results:
            recife_cost = cost_results['Recife']['prediction']
            salvador_cost = cost_results['Salvador']['prediction']
            
            if recife_cost < salvador_cost:
                diff_percent = ((salvador_cost - recife_cost) / recife_cost) * 100
                insights.append(f"Recife tem {diff_percent:.1f}% menor custo operacional que Salvador")
            else:
                diff_percent = ((recife_cost - salvador_cost) / salvador_cost) * 100
                insights.append(f"Salvador tem {diff_percent:.1f}% menor custo operacional que Recife")
    
    return insights

def main():
    """
    Função principal para demonstrar o uso dos modelos.
    """
    logging.info("Iniciando utilização dos modelos de machine learning")
    
    # Run IDs dos modelos treinados (substitua pelos seus Run IDs reais)
    # Você pode obter esses IDs no MLflow UI
    run_ids = {
        'consumption_gb': '656e005cf88041da91f19d0b6d8342cd',      # GradientBoosting para consumo
        'consumption_xgb': '7659b41ccb704735a5ec8dee1c2a2230',    # XGBoost para consumo
        'operational_cost_gb': 'fae9eef1d6b14bfe897d69313619390c', # GradientBoosting para custo
        'operational_cost_xgb': '216c7947335b4e80bc4caa768ff89b97'  # XGBoost para custo
    }
    
    # Carregar os modelos
    models = {}
    for model_name, run_id in run_ids.items():
        model_type = "sklearn" if "gb" in model_name else "xgboost"
        target = "consumption_potential_millions" if "consumption" in model_name else "simulated_operational_cost"
        
        model = load_trained_model(run_id, model_type)
        if model is not None:
            models[model_name] = {
                'model': model,
                'target': target
            }
    
    # Dados das cidades para previsão
    cities_data = {
        'Recife': {
            'population': 1661017,
            'household_income': 30000,
            'avg_property_price': 1500000,
            'avg_property_area': 1000,
            'avg_distance_km': 600,
            'avg_duration_hours': 10,
            'avg_speed_kmh': 60
        },
        'Salvador': {
            'population': 2418005,
            'household_income': 28000,
            'avg_property_price': 1200000,
            'avg_property_area': 900,
            'avg_distance_km': 550,
            'avg_duration_hours': 9,
            'avg_speed_kmh': 61
        }
    }
    
    # Analisar importância das features para cada modelo
    features = [
        'population', 'household_income', 'avg_property_price', 
        'avg_property_area', 'avg_distance_km', 'avg_duration_hours', 'avg_speed_kmh'
    ]
    
    for model_name, model_info in models.items():
        importance_df = analyze_feature_importance(model_info['model'], features, model_name)
        if importance_df is not None:
            print(f"\nFeature Importance - {model_name}:")
            print(importance_df.to_string(index=False))
    
    # Comparar cidades usando os modelos
    results = compare_cities_with_models(models, cities_data)
    
    # Exibir resultados
    print("\n" + "="*50)
    print("RESULTADOS DAS PREVISÕES")
    print("="*50)
    
    for model_name, model_results in results.items():
        print(f"\n{model_name}:")
        for city, prediction_data in model_results.items():
            print(f"  {city}: {prediction_data['prediction']:.2f} {prediction_data['unit']}")
    
    # Gerar insights de negócio
    insights = generate_business_insights(results)
    
    print("\n" + "="*50)
    print("INSIGHTS DE NEGÓCIO")
    print("="*50)
    
    for insight in insights:
        print(f"- {insight}")
    
    # Salvar resultados
    os.makedirs('data/analysis', exist_ok=True)
    
    with open('data/analysis/model_predictions_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    with open('data/analysis/business_insights.json', 'w') as f:
        json.dump({'insights': insights}, f, indent=4)
    
    logging.info("Análise concluída. Resultados salvos em data/analysis/")

if __name__ == "__main__":
    main()