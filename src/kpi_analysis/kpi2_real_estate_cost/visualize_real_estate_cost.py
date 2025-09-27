import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def display_capex_comparison(data):
    """
    Exibe gráfico de barras comparativo de CapEx por cidade.
    """
    st.subheader("Comparativo de CapEx por Cidade")
    
    # Extrair dados de CapEx
    capex_data = []
    
    if "capex_recife" in data and data["capex_recife"]:
        recife_capex = data["capex_recife"].get("total_capex", 0)
        capex_data.append({"Cidade": "Recife", "CapEx (R$)": recife_capex})
    
    if "capex_salvador" in data and data["capex_salvador"]:
        salvador_capex = data["capex_salvador"].get("total_capex", 0)
        capex_data.append({"Cidade": "Salvador", "CapEx (R$)": salvador_capex})
    
    if capex_data:
        capex_df = pd.DataFrame(capex_data)
        
        # Gráfico de barras
        fig = px.bar(
            capex_df,
            x="Cidade",
            y="CapEx (R$)",
            title="Comparativo de CapEx entre Recife e Salvador",
            color="Cidade",
            text="CapEx (R$)"
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de pizza com detalhamento do CapEx
        if "capex_recife" in data and data["capex_recife"] and "capex_salvador" in data and data["capex_salvador"]:
            # Extrair detalhes do CapEx
            recife_details = data["capex_recife"]
            salvador_details = data["capex_salvador"]
            
            # Preparar dados para o gráfico
            capex_breakdown = []
            
            # Adicionar custos do Recife
            if "land_cost" in recife_details:
                capex_breakdown.append({"Cidade": "Recife", "Componente": "Custo do Terreno", "Valor": recife_details["land_cost"]})
            if "construction_cost" in recife_details:
                capex_breakdown.append({"Cidade": "Recife", "Componente": "Custo de Construção", "Valor": recife_details["construction_cost"]})
            if "equipment_cost" in recife_details:
                capex_breakdown.append({"Cidade": "Recife", "Componente": "Custo de Equipamentos", "Valor": recife_details["equipment_cost"]})
            if "other_costs" in recife_details:
                capex_breakdown.append({"Cidade": "Recife", "Componente": "Outros Custos", "Valor": recife_details["other_costs"]})
            
            # Adicionar custos de Salvador
            if "land_cost" in salvador_details:
                capex_breakdown.append({"Cidade": "Salvador", "Componente": "Custo do Terreno", "Valor": salvador_details["land_cost"]})
            if "construction_cost" in salvador_details:
                capex_breakdown.append({"Cidade": "Salvador", "Componente": "Custo de Construção", "Valor": salvador_details["construction_cost"]})
            if "equipment_cost" in salvador_details:
                capex_breakdown.append({"Cidade": "Salvador", "Componente": "Custo de Equipamentos", "Valor": salvador_details["equipment_cost"]})
            if "other_costs" in salvador_details:
                capex_breakdown.append({"Cidade": "Salvador", "Componente": "Outros Custos", "Valor": salvador_details["other_costs"]})
            
            if capex_breakdown:
                breakdown_df = pd.DataFrame(capex_breakdown)
                
                # Gráfico de barras empilhadas
                fig2 = px.bar(
                    breakdown_df,
                    x="Cidade",
                    y="Valor",
                    color="Componente",
                    title="Detalhamento do CapEx por Componente",
                    text="Valor"
                )
                fig2.update_traces(texttemplate='%{text:,.0f}', textposition='inside')
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Dados de CapEx não disponíveis.")

def display_property_details(data):
    """
    Exibe tabela detalhada de imóveis e seus custos.
    """
    st.subheader("Detalhes dos Imóveis Analisados")
    
    if "property_details" in data:
        details_df = pd.DataFrame(data["property_details"])
        st.dataframe(details_df)
        
        # Mapa de dispersão: preço vs área
        fig = px.scatter(
            details_df,
            x="area_m2",
            y="price_m2",
            color="city",
            size="price_m2",
            hover_name="address_raw",
            title="Relação entre Preço por m² e Área do Imóvel",
            labels={
                "area_m2": "Área (m²)",
                "price_m2": "Preço por m² (R$)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Detalhes de imóveis não disponíveis.")