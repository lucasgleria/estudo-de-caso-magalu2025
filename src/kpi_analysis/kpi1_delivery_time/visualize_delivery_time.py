import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

def display_overall_stats(data):
    """
    Exibe estatísticas de tempo de entrega em formato de tabela e gráfico.
    """
    st.subheader("Estatísticas Gerais de Tempo de Entrega")
    
    if "overall_delivery_stats" in data:
        stats = data["overall_delivery_stats"]
        
        # Converter para DataFrame para exibição
        stats_df = pd.DataFrame([stats])
        st.dataframe(stats_df)
        
        # Criar gráfico de barras para tempo médio por cidade
        if "city_comparison" in data:
            city_data = data["city_comparison"]
            cities = list(city_data.keys())
            delivery_times = [city_data[city].get("delivery_time", 0) for city in cities]
            
            fig = px.bar(
                x=cities, 
                y=delivery_times,
                title="Tempo Médio de Entrega por Cidade (horas)",
                labels={"x": "Cidade", "y": "Tempo Médio (horas)"}
            )
            st.plotly_chart(fig, use_container_width=True)

def display_isochrone_map(data):
    """
    Exibe mapa interativo com isócronas usando Folium.
    """
    st.subheader("Mapas de Isócronas")
    
    # Verificar se temos dados de isócronas
    if "isochrones_recife" in data and "isochrones_salvador" in data:
        # Mapa centrado no Nordeste brasileiro
        m = folium.Map(location=[-10.5, -36.5], zoom_start=6)
        
        # Adicionar isócronas do Recife
        try:
            recife_iso = folium.GeoJson(
                data["isochrones_recife"],
                name="Isócronas Recife",
                style_function=lambda x: {
                    'fillColor': '#3186cc',
                    'color': '#3186cc',
                    'weight': 2,
                    'fillOpacity': 0.5
                }
            ).add_to(m)
            
            # Adicionar marcador para o Recife
            folium.Marker(
                location=[-8.05, -34.9],
                popup="Recife",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        except Exception as e:
            st.error(f"Erro ao carregar isócronas do Recife: {e}")
        
        # Adicionar isócronas de Salvador
        try:
            salvador_iso = folium.GeoJson(
                data["isochrones_salvador"],
                name="Isócronas Salvador",
                style_function=lambda x: {
                    'fillColor': '#31a354',
                    'color': '#31a354',
                    'weight': 2,
                    'fillOpacity': 0.5
                }
            ).add_to(m)
            
            # Adicionar marcador para Salvador
            folium.Marker(
                location=[-12.97, -38.5],
                popup="Salvador",
                icon=folium.Icon(color='green', icon='info-sign')
            ).add_to(m)
        except Exception as e:
            st.error(f"Erro ao carregar isócronas de Salvador: {e}")
        
        # Adicionar controle de camadas
        folium.LayerControl().add_to(m)
        
        # Exibir mapa
        st_data = st_folium(m, width=700, height=500)
    else:
        st.warning("Dados de isócronas não disponíveis.")

def display_routes_table(data):
    """
    Exibe tabela de tempos médios e custos de transporte por capital atendida.
    """
    st.subheader("Rotas e Tempos de Entrega")
    
    if "delivery_routes" in data:
        routes_df = pd.DataFrame(data["delivery_routes"])
        st.dataframe(routes_df)
        
        # Gráfico de dispersão: distância vs tempo
        fig = px.scatter(
            routes_df,
            x="distance_km",
            y="duration_hours",
            color="origin",
            size="transport_cost",
            hover_name="destination",
            title="Relação entre Distância e Tempo de Entrega",
            labels={
                "distance_km": "Distância (km)",
                "duration_hours": "Tempo (horas)",
                "transport_cost": "Custo de Transporte"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Dados de rotas não disponíveis.")