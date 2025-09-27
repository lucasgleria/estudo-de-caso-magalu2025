import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def display_cost_breakdown(data):
    """
    Exibe gráfico empilhado de custos (Transporte, Mão de Obra, Energia, Imobiliário).
    """
    st.subheader("Detalhamento dos Custos Operacionais")
    
    # Preparar dados para o gráfico
    cost_data = []
    
    for city, city_data in data.items():
        if isinstance(city_data, dict):
            # Extrair custos por componente
            if "transport_cost" in city_data:
                cost_data.append({
                    "Cidade": city,
                    "Componente": "Transporte",
                    "Valor": city_data["transport_cost"]
                })
            if "labor_cost" in city_data:
                cost_data.append({
                    "Cidade": city,
                    "Componente": "Mão de Obra",
                    "Valor": city_data["labor_cost"]
                })
            if "energy_cost" in city_data:
                cost_data.append({
                    "Cidade": city,
                    "Componente": "Energia",
                    "Valor": city_data["energy_cost"]
                })
            if "facility_cost" in city_data:
                cost_data.append({
                    "Cidade": city,
                    "Componente": "Imobiliário",
                    "Valor": city_data["facility_cost"]
                })
    
    if cost_data:
        cost_df = pd.DataFrame(cost_data)
        
        # Gráfico de barras empilhadas
        fig = px.bar(
            cost_df,
            x="Cidade",
            y="Valor",
            color="Componente",
            title="Detalhamento dos Custos Operacionais por Componente",
            text="Valor"
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='inside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de pizza para mostrar a composição percentual dos custos
        # Calcular totais por cidade
        city_totals = cost_df.groupby("Cidade")["Valor"].sum().reset_index()
        
        # Criar subplots
        fig2 = make_subplots(
            rows=1, cols=len(city_totals),
            subplot_titles=[f"Custos em {city}" for city in city_totals["Cidade"]],
            specs=[[{"type": "pie"} for _ in range(len(city_totals))]]
        )
        
        for i, row in city_totals.iterrows():
            city = row["Cidade"]
            total = row["Valor"]
            
            # Filtrar dados para esta cidade
            city_cost_data = cost_df[cost_df["Cidade"] == city]
            
            # Adicionar gráfico de pizza
            fig2.add_trace(
                go.Pie(
                    labels=city_cost_data["Componente"],
                    values=city_cost_data["Valor"],
                    name=city
                ),
                row=1, col=i+1
            )
        
        fig2.update_layout(title_text="Composição Percentual dos Custos por Cidade")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Dados de detalhamento de custos não disponíveis.")

def display_cost_per_order(data):
    """
    Exibe tabela ou gráfico comparativo de custo por pedido.
    """
    st.subheader("Custo Operacional por Pedido")
    
    # Preparar dados para o gráfico
    cost_per_order = []
    
    for city, city_data in data.items():
        if isinstance(city_data, dict) and "total_operational_cost_per_order" in city_data:
            cost_per_order.append({
                "Cidade": city,
                "Custo por Pedido (R$)": city_data["total_operational_cost_per_order"]
            })
    
    if cost_per_order:
        cost_df = pd.DataFrame(cost_per_order)
        
        # Gráfico de barras
        fig = px.bar(
            cost_df,
            x="Cidade",
            y="Custo por Pedido (R$)",
            title="Custo Operacional por Pedido",
            color="Cidade",
            text="Custo por Pedido (R$)"
        )
        fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Exibir tabela detalhada
        st.dataframe(cost_df)
    else:
        st.warning("Dados de custo por pedido não disponíveis.")

def display_cost_simulation_inputs(data):
    """
    Implementa inputs para simulação interativa e recalcular impacto.
    """
    st.subheader("Simulação de Impacto de Custos")
    
    # Extrair valores base para a simulação
    base_values = {}
    for city, city_data in data.items():
        if isinstance(city_data, dict):
            base_values[city] = {
                "fuel_cost_per_km": city_data.get("fuel_cost_per_km", 0.5),
                "avg_salary_logistics": city_data.get("avg_salary_logistics", 2500),
                "energy_cost_kwh": city_data.get("energy_cost_kwh", 0.8),
                "estimated_monthly_volume": city_data.get("estimated_monthly_volume", 100000)
            }
    
    if base_values:
        # Sliders para ajustar os fatores de custo
        st.write("Ajuste os fatores de custo para ver o impacto nos custos operacionais:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fuel_factor = st.slider("Fator de Custo de Combustível", 0.5, 2.0, 1.0, 0.05)
            salary_factor = st.slider("Fator de Custo de Mão de Obra", 0.5, 2.0, 1.0, 0.05)
        
        with col2:
            energy_factor = st.slider("Fator de Custo de Energia", 0.5, 2.0, 1.0, 0.05)
            volume_factor = st.slider("Fator de Volume de Pedidos", 0.5, 2.0, 1.0, 0.05)
        
        # Calcular custos ajustados
        adjusted_costs = []
        
        for city, values in base_values.items():
            # Cálculos simplificados para demonstração
            adjusted_fuel_cost = values["fuel_cost_per_km"] * fuel_factor
            adjusted_salary = values["avg_salary_logistics"] * salary_factor
            adjusted_energy_cost = values["energy_cost_kwh"] * energy_factor
            adjusted_volume = values["estimated_monthly_volume"] * volume_factor
            
            # Estimativa simplificada do impacto no custo por pedido
            base_cost_per_order = data[city].get("total_operational_cost_per_order", 5.0)
            
            # Fatores de ponderação para cada componente (simplificado)
            fuel_weight = 0.3
            labor_weight = 0.4
            energy_weight = 0.2
            volume_weight = 0.1
            
            # Calcular custo ajustado
            adjusted_cost_per_order = (
                base_cost_per_order * (
                    fuel_weight * fuel_factor +
                    labor_weight * salary_factor +
                    energy_weight * energy_factor +
                    volume_weight * (1/volume_factor)  # Volume maior reduz custo por pedido
                )
            )
            
            adjusted_costs.append({
                "Cidade": city,
                "Custo Base por Pedido (R$)": base_cost_per_order,
                "Custo Ajustado por Pedido (R$)": adjusted_cost_per_order,
                "Variação (%)": (adjusted_cost_per_order - base_cost_per_order) / base_cost_per_order * 100
            })
        
        # Exibir resultados
        if adjusted_costs:
            adjusted_df = pd.DataFrame(adjusted_costs)
            
            # Formatar para exibição
            adjusted_df["Custo Base por Pedido (R$)"] = adjusted_df["Custo Base por Pedido (R$)"].map("R$ {:.2f}".format)
            adjusted_df["Custo Ajustado por Pedido (R$)"] = adjusted_df["Custo Ajustado por Pedido (R$)"].map("R$ {:.2f}".format)
            adjusted_df["Variação (%)"] = adjusted_df["Variação (%)"].map("{:.1f}%".format)
            
            st.dataframe(adjusted_df)
            
            # Gráfico comparativo
            fig = px.bar(
                adjusted_df,
                x="Cidade",
                y=["Custo Base por Pedido (R$)", "Custo Ajustado por Pedido (R$)"],
                title="Impacto da Simulação no Custo por Pedido",
                barmode="group"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Dados insuficientes para realizar simulação.")