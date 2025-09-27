import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

def display_revenue_potential(data):
    """
    Exibe gráfico comparativo de receita potencial estimada.
    """
    st.subheader("Receita Potencial Estimada")
    
    if "revenue_scenarios" in data:
        # Extrair dados de receita para cada cenário
        scenarios = data["revenue_scenarios"]
        cities = []
        revenues = []
        scenario_types = []
        
        for scenario, values in scenarios.items():
            for city, revenue in values.get("estimated_revenue", {}).items():
                cities.append(city)
                revenues.append(revenue)
                scenario_types.append(scenario)
        
        # Criar DataFrame
        revenue_df = pd.DataFrame({
            "Cidade": cities,
            "Receita Estimada (R$)": revenues,
            "Cenário": scenario_types
        })
        
        # Gráfico de barras comparativo
        fig = px.bar(
            revenue_df,
            x="Cidade",
            y="Receita Estimada (R$)",
            color="Cenário",
            barmode="group",
            title="Receita Potencial Estimada por Cenário",
            text="Receita Estimada (R$)"
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de pizza para o cenário provável
        if "revenue_scenario_probable" in data:
            probable_data = data["revenue_scenario_probable"]["estimated_revenue"]
            probable_df = pd.DataFrame([
                {"Cidade": city, "Receita": revenue}
                for city, revenue in probable_data.items()
            ])
            
            fig2 = px.pie(
                probable_df,
                values="Receita",
                names="Cidade",
                title="Distribuição da Receita Potencial (Cenário Provável)",
                hover_data=["Receita"]
            )
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Dados de receita potencial não disponíveis.")

def display_consumption_map(data):
    """
    Exibe mapa de calor interativo com potencial de consumo por microrregião.
    """
    st.subheader("Mapa de Potencial de Consumo por Região")
    
    if "geojson_data" in data and "consumption_data" in data:
        try:
            # Mapa centrado no Nordeste brasileiro
            m = folium.Map(location=[-10.5, -36.5], zoom_start=6)
            
            # Adicionar camada de calor
            consumption_data = data["consumption_data"]
            
            # Criar pontos para o mapa de calor
            heat_data = []
            for region, values in consumption_data.items():
                if "latitude" in values and "longitude" in values and "consumption_index" in values:
                    heat_data.append([values["latitude"], values["longitude"], values["consumption_index"]])
            
            if heat_data:
                HeatMap(heat_data).add_to(m)
                
                # Adicionar marcadores para as cidades principais
                folium.Marker(
                    location=[-8.05, -34.9],
                    popup="Recife",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
                
                folium.Marker(
                    location=[-12.97, -38.5],
                    popup="Salvador",
                    icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(m)
                
                # Exibir mapa
                st_data = st_folium(m, width=700, height=500)
            else:
                st.warning("Dados insuficientes para gerar o mapa de calor.")
        except Exception as e:
            st.error(f"Erro ao gerar mapa de consumo: {e}")
    else:
        st.warning("Dados geoespaciais de consumo não disponíveis.")

def display_consumer_clusters(data):
    """
    Exibe visualização de clusters de perfis de consumidores.
    """
    st.subheader("Clusters de Perfis de Consumidores")
    
    if "consumer_clusters" in data:
        clusters = data["consumer_clusters"]
        
        # Preparar dados para visualização
        cluster_data = []
        for cluster_id, cluster_info in clusters.items():
            if "size" in cluster_info and "characteristics" in cluster_info:
                cluster_data.append({
                    "Cluster ID": cluster_id,
                    "Tamanho": cluster_info["size"],
                    "Características": ", ".join(cluster_info["characteristics"])
                })
        
        if cluster_data:
            cluster_df = pd.DataFrame(cluster_data)
            st.dataframe(cluster_df)
            
            # Gráfico de pizza para distribuição de clusters
            fig = px.pie(
                cluster_df,
                values="Tamanho",
                names="Cluster ID",
                title="Distribuição de Consumidores por Cluster",
                hover_data=["Características"]
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dados de clusters não disponíveis ou incompletos.")
    else:
        st.warning("Dados de clusters de consumidores não disponíveis.")