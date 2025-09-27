import pandas as pd
import numpy as np
import logging
import json
import os
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_kpi_results(kpi_number: int) -> Dict[str, Any]:
    """
    Carrega os resultados de um KPI específico.
    """
    kpi_path = f"data/analysis/Etapa3.{kpi_number}_kpi{kpi_number}_results.json"
    
    if not os.path.exists(kpi_path):
        logging.warning(f"Arquivo {kpi_path} não encontrado. Usando dados mock.")
        return {}
    
    try:
        with open(kpi_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar {kpi_path}: {e}")
        return {}

def define_cost_equation(capex_amortized_per_order: float, labor_cost_per_order: float, 
                         energy_cost_per_order: float, transport_cost_per_order: float, 
                         fixed_admin_cost_per_order: float) -> float:
    """
    Define a equação de custo total por pedido.
    """
    return capex_amortized_per_order + labor_cost_per_order + energy_cost_per_order + \
           transport_cost_per_order + fixed_admin_cost_per_order

def simulate_fleet_routing(city: str, avg_distance_km: float, avg_duration_hours: float, 
                           fuel_cost_per_km: float, driver_cost_per_hour: float, 
                           orders_per_day: int) -> dict:
    """
    Esqueleto para simulação de roteirização de frota.
    """
    logging.info(f"Simulando roteirização de frota para {city}...")
    
    # Parâmetros da simulação
    deliveries_per_vehicle_per_route = 20  # Exemplo
    routes_per_vehicle_per_day = 2  # Exemplo
    
    # Estimativa simplificada de km e tempo por pedido
    km_per_order = avg_distance_km / deliveries_per_vehicle_per_route
    time_per_order_h = avg_duration_hours / deliveries_per_vehicle_per_route
    
    # Custo de transporte por pedido
    transport_cost = (km_per_order * fuel_cost_per_km) + (time_per_order_h * driver_cost_per_hour)
    
    # Número de veículos necessários (muito simplificado)
    num_vehicles_needed = np.ceil(orders_per_day / (deliveries_per_vehicle_per_route * routes_per_vehicle_per_day))
    
    # Custo total de transporte diário
    daily_transport_cost = transport_cost * orders_per_day
    
    return {
        "km_per_order": km_per_order,
        "time_per_order_h": time_per_order_h,
        "transport_cost_per_order": transport_cost,
        "num_vehicles_needed": int(num_vehicles_needed),
        "daily_transport_cost": daily_transport_cost
    }

def analyze_kpi4_operational_cost(kpi1_results: dict, kpi2_results: dict, city_operational_data: dict) -> dict:
    """
    Realiza a análise para o KPI de Custo Operacional Total por pedido.
    """
    logging.info("Iniciando análise para KPI 4: Custo Operacional Total.")
    results = {}

    cities = ["Recife", "Salvador"]

    for city in cities:
        logging.info(f"Calculando custos operacionais para {city}...")
        
        # Dados específicos da cidade (salários, energia, etc.)
        city_data = city_operational_data.get(city, {})
        avg_salary_logistics = city_data.get("avg_salary_logistics", 2500)  # Exemplo
        energy_cost_kwh = city_data.get("energy_cost_kwh", 0.8)  # Exemplo
        fuel_cost_per_km = city_data.get("fuel_cost_per_km", 0.5)  # Exemplo
        driver_cost_per_hour = city_data.get("driver_cost_per_hour", 25)  # Exemplo
        estimated_monthly_volume = city_data.get("estimated_monthly_volume", 100000)  # Exemplo
        num_employees_per_shift = city_data.get("num_employees_per_shift", 50)  # Exemplo
        shifts_per_day = city_data.get("shifts_per_day", 2)  # Exemplo
        days_per_month = city_data.get("days_per_month", 22)  # Exemplo
        cd_energy_consumption_kwh_month = city_data.get("cd_energy_consumption_kwh_month", 50000)  # Exemplo

        # Custo de mão de obra por pedido
        labor_cost_per_order = (avg_salary_logistics * num_employees_per_shift * shifts_per_day) / (estimated_monthly_volume / days_per_month)
        
        # Custo de energia por pedido
        energy_cost_per_order = (cd_energy_consumption_kwh_month * energy_cost_kwh) / estimated_monthly_volume

        # CapEx amortizado por pedido (usando resultados do KPI 2)
        capex_info = kpi2_results.get(f"capex_{city.lower()}", {})
        total_capex = capex_info.get("total_capex", 10_000_000)  # Exemplo se não houver resultado
        cd_lifespan_years = 10  # Exemplo
        annual_volume = estimated_monthly_volume * 12
        capex_amortized_per_order = total_capex / (cd_lifespan_years * annual_volume)

        # Dados de rota do KPI 1 para simulação de transporte
        # Inicializar variáveis com valores padrão
        avg_distance_km = 600  # Valor padrão para distância
        avg_duration_hours = 10  # Valor padrão para duração
        
        # Tenta obter dados específicos da cidade, caso contrário usa média geral
        if "overall_delivery_stats" in kpi1_results:
            # Se tivermos dados por cidade, usar os dados específicos
            overall_stats = kpi1_results.get("overall_delivery_stats", {})
            if "mean_hours" in overall_stats:
                avg_duration_hours = overall_stats["mean_hours"]
            if "mean_distance_km" in overall_stats:
                avg_distance_km = overall_stats["mean_distance_km"]
            else:
                # Fallback: estimativa de distância baseada no tempo (assumindo velocidade média de 60 km/h)
                avg_distance_km = avg_duration_hours * 60
        
        # Se não conseguimos obter dados do KPI1, usar valores padrão
        if avg_distance_km == 0:
            avg_distance_km = 600  # Valor padrão para distância
        if avg_duration_hours == 0:
            avg_duration_hours = 10  # Valor padrão para duração
        
        # Simulação de frota e roteirização para custo de transporte
        fleet_sim_results = simulate_fleet_routing(
            city, avg_distance_km, avg_duration_hours, fuel_cost_per_km, driver_cost_per_hour, 
            estimated_monthly_volume / days_per_month  # Pedidos por dia
        )
        transport_cost_per_order = fleet_sim_results["transport_cost_per_order"]

        # Custo fixo administrativo por pedido (exemplo)
        fixed_admin_cost_per_order = 0.5  # Exemplo: R$ 0.50 por pedido

        # Custo Operacional Total por Pedido
        total_operational_cost_per_order = define_cost_equation(
            capex_amortized_per_order, labor_cost_per_order, energy_cost_per_order,
            transport_cost_per_order, fixed_admin_cost_per_order
        )

        # Calcular custo operacional total mensal
        monthly_operational_cost = total_operational_cost_per_order * estimated_monthly_volume

        results[city] = {
            "capex_amortized_per_order": capex_amortized_per_order,
            "labor_cost_per_order": labor_cost_per_order,
            "energy_cost_per_order": energy_cost_per_order,
            "transport_cost_per_order": transport_cost_per_order,
            "fixed_admin_cost_per_order": fixed_admin_cost_per_order,
            "total_operational_cost_per_order": total_operational_cost_per_order,
            "monthly_operational_cost": monthly_operational_cost,
            "fleet_simulation": fleet_sim_results,
            "operational_cost_breakdown": {
                "capex_percent": (capex_amortized_per_order / total_operational_cost_per_order) * 100,
                "labor_percent": (labor_cost_per_order / total_operational_cost_per_order) * 100,
                "energy_percent": (energy_cost_per_order / total_operational_cost_per_order) * 100,
                "transport_percent": (transport_cost_per_order / total_operational_cost_per_order) * 100,
                "admin_percent": (fixed_admin_cost_per_order / total_operational_cost_per_order) * 100
            }
        }
        logging.info(f"Custo operacional total por pedido para {city}: R$ {total_operational_cost_per_order:.2f}")

    # Adicionar análise comparativa entre as cidades
    if "Recife" in results and "Salvador" in results:
        recife_cost = results["Recife"]["total_operational_cost_per_order"]
        salvador_cost = results["Salvador"]["total_operational_cost_per_order"]
        
        if recife_cost > 0 and salvador_cost > 0:
            cheaper_city = "Recife" if recife_cost < salvador_cost else "Salvador"
            savings_percent = abs(recife_cost - salvador_cost) / max(recife_cost, salvador_cost) * 100
            
            # Calcular economias mensais usando os dados originais
            recife_volume = city_operational_data["Recife"]["estimated_monthly_volume"]
            salvador_volume = city_operational_data["Salvador"]["estimated_monthly_volume"]
            
            recife_monthly_savings = abs(recife_cost - salvador_cost) * recife_volume if cheaper_city == "Salvador" else 0
            salvador_monthly_savings = abs(recife_cost - salvador_cost) * salvador_volume if cheaper_city == "Recife" else 0
            
            results["comparison"] = {
                "cheaper_city": cheaper_city,
                "savings_percent": savings_percent,
                "recife_monthly_savings": recife_monthly_savings,
                "salvador_monthly_savings": salvador_monthly_savings,
                "annual_savings": max(recife_monthly_savings, salvador_monthly_savings) * 12
            }

    logging.info("Análise para KPI 4 concluída.")
    return results

if __name__ == "__main__":
    # Carregar resultados dos KPIs anteriores
    kpi1_results = load_kpi_results(1)
    kpi2_results = load_kpi_results(2)
    
    # Dados operacionais das cidades
    city_operational_data = {
        "Recife": {
            "avg_salary_logistics": 2600,
            "energy_cost_kwh": 0.85,
            "fuel_cost_per_km": 0.52,
            "driver_cost_per_hour": 26,
            "estimated_monthly_volume": 110000,
            "num_employees_per_shift": 50,
            "shifts_per_day": 2,
            "days_per_month": 22,
            "cd_energy_consumption_kwh_month": 55000
        },
        "Salvador": {
            "avg_salary_logistics": 2400,
            "energy_cost_kwh": 0.78,
            "fuel_cost_per_km": 0.50,
            "driver_cost_per_hour": 24,
            "estimated_monthly_volume": 95000,
            "num_employees_per_shift": 45,
            "shifts_per_day": 2,
            "days_per_month": 22,
            "cd_energy_consumption_kwh_month": 48000
        }
    }

    # Realizar análise
    kpi4_results = analyze_kpi4_operational_cost(kpi1_results, kpi2_results, city_operational_data)
    print("\nResultados da Análise KPI 4:")
    print(json.dumps(kpi4_results, indent=4, default=str))
    
    # Salvar resultados para uso posterior
    output_dir = "data/analysis"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Etapa3.4_kpi4_operational_cost_results.json")
    
    with open(output_path, "w") as f:
        json.dump(kpi4_results, f, indent=4, default=str)
    
    logging.info(f"Resultados do KPI 4 salvos em '{output_path}'")