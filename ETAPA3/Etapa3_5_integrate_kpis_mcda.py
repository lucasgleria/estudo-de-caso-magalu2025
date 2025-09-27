import pandas as pd
import numpy as np
import json
import logging
import os
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_kpi_results(kpi_number: int) -> dict:
    """
    Carrega os resultados de um KPI específico.
    """
    kpi_path = f"data/analysis/Etapa3.{kpi_number}_kpi{kpi_number}_results.json"
    
    if not os.path.exists(kpi_path):
        logging.warning(f"Arquivo {kpi_path} não encontrado. Usando dados mock.")
        return get_mock_data(kpi_number)
    
    try:
        with open(kpi_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar {kpi_path}: {e}")
        return get_mock_data(kpi_number)

def get_mock_data(kpi_number: int) -> dict:
    """
    Retorna dados mock mais realistas para cada KPI.
    """
    if kpi_number == 1:
        return {
            "overall_delivery_stats": {"mean_hours": 9.8},
            "city_comparison": {
                "recife": {"delivery_time": 9.5},
                "salvador": {"delivery_time": 10.2}
            }
        }
    elif kpi_number == 2:
        return {
            "capex_recife": {"total_capex": 11_500_000},
            "capex_salvador": {"total_capex": 10_800_000}
        }
    elif kpi_number == 3:
        return {
            "revenue_scenario_probable": {
                "estimated_revenue": {
                    "Recife": 9_500_000,
                    "Salvador": 8_700_000
                }
            }
        }
    elif kpi_number == 4:
        return {
            "Recife": {"total_operational_cost_per_order": 4.8},
            "Salvador": {"total_operational_cost_per_order": 4.6}
        }
    return {}

def check_data_polarization(df_normalized: pd.DataFrame) -> Tuple[bool, str]:
    """
    Verifica se os dados estão polarizados (apenas 0s e 1s).
    Retorna (polarizado, mensagem)
    """
    polarized = False
    message = ""
    
    for col in df_normalized.columns:
        unique_values = set(df_normalized[col].unique())
        if unique_values == {0.0, 1.0}:
            polarized = True
            message += f"Coluna '{col}' está polarizada (valores apenas 0 e 1). "
    
    if polarized:
        message += "Isso pode tornar a análise de sensibilidade menos informativa."
    
    return polarized, message

def normalize_kpis(df: pd.DataFrame, criteria_type: dict) -> pd.DataFrame:
    """
    Normaliza os valores dos KPIs usando min-max normalization.
    criteria_type: Dicionário indicando se o critério é de benefício (">") ou custo ("<").
    """
    df_normalized = df.copy()
    for col, c_type in criteria_type.items():
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val == min_val:
            df_normalized[col] = 0.5  # Se todos os valores são iguais, normaliza para 0.5
        elif c_type == ">":  # Benefício: quanto maior, melhor
            df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
        else:  # Custo: quanto menor, melhor
            df_normalized[col] = (max_val - df[col]) / (max_val - min_val)
    return df_normalized

def calculate_topsis_score(df_normalized: pd.DataFrame, weights: dict, criteria_type: dict) -> pd.DataFrame:
    """
    Calcula o score TOPSIS para cada alternativa.
    """
    df_weighted = df_normalized.copy()
    for col, weight in weights.items():
        df_weighted[col] = df_weighted[col] * weight

    # Identificar soluções ideais e anti-ideais
    ideal_solution = pd.Series(index=df_weighted.columns, dtype=float)
    anti_ideal_solution = pd.Series(index=df_weighted.columns, dtype=float)

    for col, c_type in criteria_type.items():
        if c_type == ">":  # Benefício: ideal é o máximo, anti-ideal é o mínimo
            ideal_solution[col] = df_weighted[col].max()
            anti_ideal_solution[col] = df_weighted[col].min()
        else:  # Custo: ideal é o mínimo, anti-ideal é o máximo
            ideal_solution[col] = df_weighted[col].min()
            anti_ideal_solution[col] = df_weighted[col].max()

    # Calcular distância euclidiana para a solução ideal e anti-ideal
    distance_to_ideal = np.sqrt(((df_weighted - ideal_solution)**2).sum(axis=1))
    distance_to_anti_ideal = np.sqrt(((df_weighted - anti_ideal_solution)**2).sum(axis=1))

    # Calcular score TOPSIS
    topsis_score = distance_to_anti_ideal / (distance_to_ideal + distance_to_anti_ideal)
    return topsis_score

def extract_kpi_values(kpi1_results: dict, kpi2_results: dict, kpi3_results: dict, kpi4_results: dict) -> dict:
    """
    Extrai os valores dos KPIs para Recife e Salvador.
    """
    logging.info("Extraindo valores dos KPIs para as cidades.")
    
    # Extrair KPI1: Tempo médio de entrega
    delivery_time_recife = kpi1_results.get("overall_delivery_stats", {}).get("mean_hours", 9.8)
    delivery_time_salvador = delivery_time_recife  # Se não tiver dados específicos, usar o mesmo valor
    
    # Se tivermos dados por cidade, usar os específicos
    if "city_comparison" in kpi1_results:
        recife_stats = kpi1_results["city_comparison"].get("recife", {})
        salvador_stats = kpi1_results["city_comparison"].get("salvador", {})
        
        # Tentar obter tempos específicos
        if "delivery_time" in recife_stats:
            delivery_time_recife = recife_stats["delivery_time"]
        if "delivery_time" in salvador_stats:
            delivery_time_salvador = salvador_stats["delivery_time"]
    
    # Extrair KPI2: Custo de aquisição imobiliária
    real_estate_cost_recife = kpi2_results.get("capex_recife", {}).get("total_capex", 11_500_000) / 1_000_000
    real_estate_cost_salvador = kpi2_results.get("capex_salvador", {}).get("total_capex", 10_800_000) / 1_000_000
    
    # Extrair KPI3: Potencial de consumo
    consumption_potential_recife = kpi3_results.get("revenue_scenario_probable", {}).get("estimated_revenue", {}).get("Recife", 9_500_000) / 1_000_000
    consumption_potential_salvador = kpi3_results.get("revenue_scenario_probable", {}).get("estimated_revenue", {}).get("Salvador", 8_700_000) / 1_000_000
    
    # Extrair KPI4: Custo operacional
    operational_cost_recife = kpi4_results.get("Recife", {}).get("total_operational_cost_per_order", 4.8)
    operational_cost_salvador = kpi4_results.get("Salvador", {}).get("total_operational_cost_per_order", 4.6)
    
    return {
        "Recife": {
            "delivery_time": delivery_time_recife,
            "real_estate_cost": real_estate_cost_recife,
            "consumption_potential": consumption_potential_recife,
            "operational_cost": operational_cost_recife
        },
        "Salvador": {
            "delivery_time": delivery_time_salvador,
            "real_estate_cost": real_estate_cost_salvador,
            "consumption_potential": consumption_potential_salvador,
            "operational_cost": operational_cost_salvador
        }
    }

def integrate_kpis_mcda(kpi1_results: dict, kpi2_results: dict, kpi3_results: dict, kpi4_results: dict, weights: dict = None) -> dict:
    """
    Integra os resultados dos KPIs usando o método MCDA (TOPSIS).
    """
    logging.info("Iniciando integração dos KPIs com MCDA (TOPSIS).")

    # Extrair os valores dos KPIs para Recife e Salvador
    data = extract_kpi_values(kpi1_results, kpi2_results, kpi3_results, kpi4_results)
    
    df_kpis = pd.DataFrame.from_dict(data, orient="index")
    logging.info("Valores dos KPIs extraídos:\n%s", df_kpis)

    # Definir tipo de critério (benefício ">" ou custo "<")
    criteria_type = {
        "delivery_time": "<",  # Menor tempo é melhor
        "real_estate_cost": "<",  # Menor custo é melhor
        "consumption_potential": ">",  # Maior potencial é melhor
        "operational_cost": "<",  # Menor custo é melhor
    }

    # Pesos padrão se não forem fornecidos (exemplo, devem vir de stakeholders)
    if weights is None:
        weights = {
            "delivery_time": 0.20,
            "consumption_potential": 0.40,
            "operational_cost": 0.20,
            "real_estate_cost": 0.20,
        }
    
    # Garantir que os pesos somem 1
    total_weight = sum(weights.values())
    if not np.isclose(total_weight, 1.0):
        logging.warning(f"Os pesos fornecidos somam {total_weight:.2f}, não 1.0. Normalizando pesos.")
        weights = {k: v / total_weight for k, v in weights.items()}

    # Normalizar KPIs
    df_normalized = normalize_kpis(df_kpis, criteria_type)
    logging.info("KPIs normalizados:\n%s", df_normalized)
    
    # Verificar polarização dos dados
    is_polarized, polarization_msg = check_data_polarization(df_normalized)
    if is_polarized:
        logging.warning(f"Detectada polarização nos dados: {polarization_msg}")

    # Calcular score TOPSIS
    topsis_score = calculate_topsis_score(df_normalized, weights, criteria_type)
    df_kpis["topsis_score"] = topsis_score
    df_kpis = df_kpis.sort_values(by="topsis_score", ascending=False)

    # Adicionar ranking
    df_kpis["ranking"] = range(1, len(df_kpis) + 1)
    
    # Calcular diferença percentual entre as cidades
    comparison = {}
    if len(df_kpis) >= 2:
        score_diff = df_kpis.iloc[0]["topsis_score"] - df_kpis.iloc[1]["topsis_score"]
        
        # Tratar divisão por zero
        if df_kpis.iloc[1]["topsis_score"] == 0:
            score_diff_percent = float('inf')
            logging.warning("Score da segunda cidade é 0. Diferença percentual é infinita.")
        else:
            score_diff_percent = (score_diff / df_kpis.iloc[1]["topsis_score"]) * 100
        
        comparison = {
            "winner": df_kpis.iloc[0].name,
            "loser": df_kpis.iloc[1].name,
            "score_difference": score_diff,
            "score_difference_percent": score_diff_percent
        }
    else:
        comparison = {
            "message": "Não há cidades suficientes para comparação"
        }

    results = {
        "final_ranking": df_kpis.to_dict(orient="index"),
        "weights_used": weights,
        "criteria_type": criteria_type,
        "comparison": comparison,
        "normalized_values": df_normalized.to_dict(orient="index"),
        "data_polarization_warning": polarization_msg if is_polarized else None
    }
    logging.info("Integração dos KPIs concluída. Ranking final:\n%s", df_kpis)
    return results

def run_sensitivity_analysis(kpi1_results: dict, kpi2_results: dict, kpi3_results: dict, kpi4_results: dict, 
                            sensitivity_weights: List[Dict[str, float]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Executa análise de sensibilidade testando diferentes combinações de pesos.
    
    Args:
        kpi1_results: Resultados do KPI1
        kpi2_results: Resultados do KPI2
        kpi3_results: Resultados do KPI3
        kpi4_results: Resultados do KPI4
        sensitivity_weights: Lista de dicionários com diferentes combinações de pesos
        
    Returns:
        Tupla com (resultados_detalhados, resumo)
    """
    logging.info("Iniciando análise de sensibilidade com %d cenários de pesos", len(sensitivity_weights))
    sensitivity_results = []
    
    for i, weights in enumerate(sensitivity_weights):
        logging.info(f"Executando cenário {i+1}/{len(sensitivity_weights)} com pesos: {weights}")
        result = integrate_kpis_mcda(
            kpi1_results, kpi2_results, kpi3_results, kpi4_results, 
            weights=weights
        )
        
        # Extrair informações relevantes para análise
        scenario_result = {
            "scenario_id": i + 1,
            "weights": weights,
            "winner": result['comparison'].get('winner', 'N/A'),
            "loser": result['comparison'].get('loser', 'N/A'),
            "score_difference": result['comparison'].get('score_difference', 0),
            "score_difference_percent": result['comparison'].get('score_difference_percent', 0),
            "ranking": result['final_ranking']
        }
        sensitivity_results.append(scenario_result)
    
    # Identificar qual cidade venceu mais vezes
    winners_count = {}
    for result in sensitivity_results:
        winner = result['winner']
        winners_count[winner] = winners_count.get(winner, 0) + 1
    
    # Calcular métricas de robustez
    total_scenarios = len(sensitivity_weights)
    most_frequent_winner = max(winners_count, key=winners_count.get) if winners_count else None
    robustness_score = max(winners_count.values()) / total_scenarios if winners_count else 0
    weight_variation_impact = "low" if len(set(winners_count.keys())) == 1 else "high"
    
    # Adicionar resumo da análise
    summary = {
        "total_scenarios": total_scenarios,
        "winners_frequency": winners_count,
        "most_frequent_winner": most_frequent_winner,
        "robustness_score": robustness_score,
        "weight_variation_impact": weight_variation_impact,
        "interpretation": get_robustness_interpretation(robustness_score, weight_variation_impact)
    }
    
    logging.info("Análise de sensibilidade concluída. Resumo: %s", summary)
    return sensitivity_results, summary

def get_robustness_interpretation(robustness_score: float, weight_variation_impact: str) -> str:
    """
    Retorna uma interpretação textual da robustez da decisão.
    """
    if robustness_score >= 0.9:
        return "Decisão altamente robusta. A cidade vencedora é consistentemente melhor independentemente dos pesos."
    elif robustness_score >= 0.7:
        return "Decisão robusta. A cidade vencedora é preferível na maioria dos cenários."
    elif robustness_score >= 0.5:
        return "Decisão moderadamente robusta. A cidade vencedora tem vantagem, mas resultados podem variar."
    else:
        return "Decisão não robusta. Os resultados são sensíveis à variação dos pesos."

if __name__ == "__main__":
    # Carregar resultados dos KPIs anteriores
    kpi1_results = load_kpi_results(1)
    kpi2_results = load_kpi_results(2)
    kpi3_results = load_kpi_results(3)
    kpi4_results = load_kpi_results(4)
    
    # Verificar se temos dados suficientes
    if not all([kpi1_results, kpi2_results, kpi3_results, kpi4_results]):
        logging.warning("Alguns KPIs não foram carregados. Usando dados mock para os faltantes.")
    
    # Pesos customizados (opcional)
    custom_weights = {
        "delivery_time": 0.35,
        "consumption_potential": 0.25,
        "operational_cost": 0.25,
        "real_estate_cost": 0.15,
    }

    # Realizar integração dos KPIs com pesos customizados
    final_results = integrate_kpis_mcda(kpi1_results, kpi2_results, kpi3_results, kpi4_results, weights=custom_weights)
    print("\nResultados Finais da Integração dos KPIs (MCDA):")
    print(json.dumps(final_results, indent=4, default=str))
    
    # Salvar resultados para uso posterior
    output_dir = "data/analysis"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Etapa3.5_kpi_integration_results.json")
    
    with open(output_path, "w") as f:
        json.dump(final_results, f, indent=4, default=str)
    
    logging.info(f"Resultados da integração dos KPIs salvos em '{output_path}'")
    
    # Definir cenários para análise de sensibilidade
    sensitivity_weights = [
        # Cenário 1: Ênfase em tempo de entrega
        {"delivery_time": 0.50, "consumption_potential": 0.20, "operational_cost": 0.20, "real_estate_cost": 0.10},
        
        # Cenário 2: Ênfase em potencial de consumo
        {"delivery_time": 0.20, "consumption_potential": 0.50, "operational_cost": 0.20, "real_estate_cost": 0.10},
        
        # Cenário 3: Ênfase em custos operacionais
        {"delivery_time": 0.20, "consumption_potential": 0.20, "operational_cost": 0.50, "real_estate_cost": 0.10},
        
        # Cenário 4: Ênfase em custos imobiliários
        {"delivery_time": 0.20, "consumption_potential": 0.20, "operational_cost": 0.10, "real_estate_cost": 0.50},
        
        # Cenário 5: Pesos balanceados
        {"delivery_time": 0.25, "consumption_potential": 0.25, "operational_cost": 0.25, "real_estate_cost": 0.25},
        
        # Cenário 6: Pesos originais do script
        {"delivery_time": 0.40, "consumption_potential": 0.30, "operational_cost": 0.20, "real_estate_cost": 0.10},
        
        # Cenário 7: Pesos customizados do usuário
        custom_weights
    ]
    
    # Executar análise de sensibilidade
    sensitivity_results, summary = run_sensitivity_analysis(
        kpi1_results, kpi2_results, kpi3_results, kpi4_results, 
        sensitivity_weights
    )
    
    # Exibir resumo da análise de sensibilidade
    print("\n" + "="*50)
    print("RESUMO DA ANÁLISE DE SENSIBILIDADE")
    print("="*50)
    print(f"Total de cenários testados: {summary['total_scenarios']}")
    print(f"Cidade vencedora mais frequente: {summary['most_frequent_winner']}")
    print(f"Score de robustez: {summary['robustness_score']:.1%}")
    print(f"Impacto da variação de pesos: {summary['weight_variation_impact'].upper()}")
    print("\nFrequência de vitórias por cidade:")
    for city, count in summary['winners_frequency'].items():
        print(f"  {city}: {count} vitórias ({count/summary['total_scenarios']*100:.1f}%)")
    print(f"\nInterpretação: {summary['interpretation']}")
    
    # Salvar resultados da análise de sensibilidade
    sensitivity_output_path = os.path.join(output_dir, "Etapa3.5_sensitivity_analysis_results.json")
    with open(sensitivity_output_path, "w") as f:
        json.dump({
            "summary": summary,
            "scenarios": sensitivity_results
        }, f, indent=4, default=str)
    
    logging.info(f"Resultados da análise de sensibilidade salvos em '{sensitivity_output_path}'")