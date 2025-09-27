import streamlit as st
import pandas as pd
import json
import os
import sys
import plotly.graph_objects as go

# Adicionar o diretório src ao PYTHONPATH para que os módulos possam ser importados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar funções de carregamento de dados
from src.utils.data_loader import load_kpi1_data, load_kpi2_data, load_kpi3_data, load_kpi4_data

# Importar funções de análise para cada KPI
from ETAPA3.Etapa3_1_analyze_delivery_time import analyze_kpi1_delivery_time
from ETAPA3.Etapa3_2_analyze_real_estate_cost import analyze_kpi2_real_estate_cost
from ETAPA3.Etapa3_3_analyze_consumption_potential import analyze_kpi3_consumption_potential
from ETAPA3.Etapa3_4_analyze_operational_cost import analyze_kpi4_operational_cost

# Importar funções de visualização para cada KPI
from src.kpi_analysis.kpi1_delivery_time.visualize_delivery_time import (
    display_overall_stats as display_kpi1_overall_stats,
    display_isochrone_map as display_kpi1_isochrone_map,
    display_routes_table as display_kpi1_routes_table
)
from src.kpi_analysis.kpi2_real_estate_cost.visualize_real_estate_cost import (
    display_capex_comparison as display_kpi2_capex_comparison,
    display_property_details as display_kpi2_property_details
)
from src.kpi_analysis.kpi3_consumption_potential.visualize_consumption_potential import (
    display_revenue_potential as display_kpi3_revenue_potential,
    display_consumption_map as display_kpi3_consumption_map,
    display_consumer_clusters as display_kpi3_consumer_clusters
)
from src.kpi_analysis.kpi4_operational_cost.visualize_operational_cost import (
    display_cost_breakdown as display_kpi4_cost_breakdown,
    display_cost_per_order as display_kpi4_cost_per_order,
    display_cost_simulation_inputs as display_kpi4_cost_simulation_inputs
)

# Importar função de integração de KPIs
from ETAPA3.Etapa3_5_integrate_kpis_mcda import integrate_kpis_mcda

# --- Título do Dashboard ---
st.set_page_config(
    layout="wide",
    page_title="Análise de Localização CD - Magalu Nordeste",
    page_icon="📊"
)
st.title("📊 Análise de Localização de Centro de Distribuição")
st.markdown("**Magalu Nordeste - Recife vs Salvador**")
st.markdown("--- ")

# --- Resumo Executivo ---
st.info("""
**🎯 Objetivo:** Esta ferramenta analisa e compara as cidades de Recife e Salvador para determinar a melhor localização para um novo Centro de Distribuição da Magalu no Nordeste.

**📋 Metodologia:** Utilizamos 4 critérios principais (KPIs) para avaliar cada cidade: Tempo de Entrega, Custo Imobiliário, Potencial de Consumo e Custo Operacional. O sistema combina esses critérios para gerar uma recomendação final.
""")

# --- Justificativas para Dados Ausentes ---
with st.expander("⚠️ **Justificativas para Dados de Exemplo**", expanded=False):
    st.markdown("""
    **📊 Dados de Demonstração Utilizados:**
    
    Esta análise utiliza dados de exemplo em algumas seções devido a limitações técnicas identificadas durante o desenvolvimento:
    
    **🏢 Dados Imobiliários:**
    - **Limitação:** Dificuldades no processo de web scraping dos portais imobiliários
    - **Causa:** Muitos cards apresentaram "Preço: N/A, Área: N/A, Endereço: N/A" e problemas de redirecionamento
    - **Impacto:** Necessidade de usar dados simulados para demonstração
    - **Justificativa:** Priorização de outras tarefas devido ao curto prazo de entrega
    
    **👥 Dados Demográficos (IBGE):**
    - **Limitação:** API do IBGE inacessível no período de 22/09 a 26/09
    - **Causa:** Múltiplos erros "500 Server Error: Internal Server Error"
    - **Impacto:** Uso de dados simulados para potencial de consumo
    - **Justificativa:** Indisponibilidade temporária do serviço oficial
    
    **🚚 Dados de Roteamento (OSRM):**
    - **Limitação:** Falha na obtenção de dados do OSRM Table Service
    - **Causa:** Problemas de infraestrutura ou conectividade
    - **Impacto:** Uso de simulação como fallback para tempos de entrega
    - **Justificativa:** Necessidade de manter funcionalidade da análise
    
    **💡 Observação:** Os dados de exemplo foram calibrados com base em benchmarks da indústria e mantêm a proporcionalidade realista entre as cidades para fins de demonstração da metodologia.
    """)

# --- Executar Análises dos KPIs (Mock ou Reais) ---
@st.cache_data
def run_kpi_analyses():
    st.sidebar.header("Status da Análise")
    st.sidebar.info("Executando análises dos KPIs...")

    # Carregar dados
    processed_routes_df = load_kpi1_data()
    processed_real_estate_df = load_kpi2_data()
    processed_demographic_df = load_kpi3_data()
    city_operational_data = load_kpi4_data()
    
    st.sidebar.success("Dados carregados - OK")

    # Definir coordenadas das cidades para KPI1
    origin_city_coords = {
        "Recife": (-8.05, -34.9),
        "Salvador": (-12.97, -38.5)
    }

    # KPI 1
    kpi1_results = analyze_kpi1_delivery_time(processed_routes_df, origin_city_coords)
    st.sidebar.success("KPI 1 (Tempo de Entrega) - OK")

    # KPI 2
    kpi2_results = analyze_kpi2_real_estate_cost(processed_real_estate_df)
    st.sidebar.success("KPI 2 (Custo Imobiliário) - OK")

    # KPI 3
    kpi3_results = analyze_kpi3_consumption_potential(processed_demographic_df)
    st.sidebar.success("KPI 3 (Potencial de Consumo) - OK")

    # KPI 4
    kpi4_results = analyze_kpi4_operational_cost(kpi1_results, kpi2_results, city_operational_data)
    st.sidebar.success("KPI 4 (Custo Operacional) - OK")

    # Integração de KPIs
    final_weights = {
        "delivery_time": 0.40,
        "consumption_potential": 0.30,
        "operational_cost": 0.20,
        "real_estate_cost": 0.10,
    }
    kpi_integration_results = integrate_kpis_mcda(kpi1_results, kpi2_results, kpi3_results, kpi4_results, weights=final_weights)
    st.sidebar.success("Integração de KPIs (TOPSIS) - OK")

    return kpi1_results, kpi2_results, kpi3_results, kpi4_results, kpi_integration_results

kpi1_results, kpi2_results, kpi3_results, kpi4_results, kpi_integration_results = run_kpi_analyses()

# --- FAQ/Glossário no Sidebar ---
with st.sidebar.expander("❓ Glossário e Ajuda"):
    st.markdown("""
    **📊 KPI (Indicador de Performance):** Métrica que mede o desempenho de cada cidade em um critério específico.
    
    **🎯 Score de Decisão Final:** Pontuação que combina todos os critérios para determinar a melhor opção.
    
    **⚖️ Pesos:** Importância que você atribui a cada critério. Quanto maior o peso, mais influência na decisão final.
    
    **📈 Cenários de Decisão:** Permite ajustar a importância de cada critério para ver como isso afeta a recomendação.
    
    **🏢 CapEx:** Custo de aquisição de imóveis (terrenos e galpões).
    
    **💰 Custo Operacional:** Despesas mensais para operar o centro de distribuição.
    """)

# --- Navegação do Dashboard ---
st.sidebar.markdown("---")

# Container destacado para navegação
with st.sidebar.container():
    st.markdown("### 🧭 Navegação")
    st.markdown("**Escolha a seção que deseja explorar:**")
    
    menu = [
        "🏠 Visão Geral e Recomendação",
        "🚚 Critério 1: Tempo de Entrega",
        "🏢 Critério 2: Custo Imobiliário", 
        "👥 Critério 3: Potencial de Consumo",
        "💰 Critério 4: Custo Operacional",
        "⚖️ Cenários de Decisão",
        "📋 Metodologia e Dados"
    ]
    
    # Inicializar estado da sessão para navegação
    if 'current_section' not in st.session_state:
        st.session_state.current_section = "🏠 Visão Geral e Recomendação"
    
    # Seletor com destaque visual
    choice = st.sidebar.selectbox(
        "📍 **SELECIONE A SEÇÃO**", 
        menu,
        index=menu.index(st.session_state.current_section),
        help="Use este menu para navegar entre as diferentes seções da análise",
        key="main_navigation"
    )
    
    # Atualizar estado da sessão quando o selectbox muda
    st.session_state.current_section = choice
    
    # Indicador visual da seção atual com destaque
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📍 Seção Atual:**")
    st.sidebar.success(f"**{st.session_state.current_section}**")
    
    # Adicionar dica de uso
    st.sidebar.markdown("💡 **Dica:** Use os botões de navegação rápida no topo da página para acesso mais rápido às seções principais.")

# Usar o estado da sessão para determinar qual seção exibir
current_section = st.session_state.current_section

# --- Indicador de Seção Atual no Topo ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"### 📍 {current_section}")

# Navegação rápida no topo
st.markdown("**🧭 Navegação Rápida:**")
nav_cols = st.columns(7)
nav_buttons = [
    ("🏠", "Visão Geral", "🏠 Visão Geral e Recomendação"),
    ("🚚", "Entrega", "🚚 Critério 1: Tempo de Entrega"),
    ("🏢", "Imobiliário", "🏢 Critério 2: Custo Imobiliário"),
    ("👥", "Consumo", "👥 Critério 3: Potencial de Consumo"),
    ("💰", "Operacional", "💰 Critério 4: Custo Operacional"),
    ("⚖️", "Cenários", "⚖️ Cenários de Decisão"),
    ("📋", "Metodologia", "📋 Metodologia e Dados")
]

for i, (icon, label, section) in enumerate(nav_buttons):
    with nav_cols[i]:
        # Destacar o botão da seção atual
        is_current = (section == st.session_state.current_section)
        button_type = "primary" if is_current else "secondary"
        
        if st.button(f"{icon}\n{label}", key=f"nav_{i}", help=f"Ir para {section}", type=button_type):
            # Atualizar a seção atual no estado da sessão
            st.session_state.current_section = section
            # Forçar rerun para atualizar a interface
            st.rerun()

st.markdown("---")

if current_section == "🏠 Visão Geral e Recomendação":
    st.header("🏠 Visão Geral: Comparativo Recife vs Salvador")
    
    # Explicação do que está sendo mostrado
    st.markdown("""
    Esta seção apresenta um resumo executivo da análise comparativa entre Recife e Salvador para a localização do Centro de Distribuição. 
    Os resultados são baseados na combinação de 4 critérios principais que avaliam diferentes aspectos estratégicos de cada cidade.
    """)
    
    # Recomendação em destaque
    st.subheader("🎯 Recomendação Final")
    if kpi_integration_results and "final_ranking" in kpi_integration_results:
        df_ranking = pd.DataFrame.from_dict(kpi_integration_results["final_ranking"], orient="index")
        df_ranking_sorted = df_ranking.sort_values(by="topsis_score", ascending=False)
        
        # Cidade recomendada
        recommended_city = df_ranking_sorted.index[0]
        score = df_ranking_sorted['topsis_score'].max()
        
        # Cidade em segundo lugar
        second_city = df_ranking_sorted.index[1]
        second_score = df_ranking_sorted.loc[second_city, 'topsis_score']
        
        # Destaque da recomendação
        col1, col2 = st.columns([2, 1])
        with col1:
            st.success(f"""
            **🏆 RECOMENDAÇÃO: {recommended_city}**
            
            {recommended_city} apresenta o melhor desempenho geral com uma pontuação de **{score:.2f}** (em uma escala de 0 a 1).
            
            A diferença para {second_city} (segunda colocada com {second_score:.2f}) é de **{score - second_score:.2f} pontos**.
            """)
        
        with col2:
            # Indicador visual simples
            if recommended_city == "Recife":
                st.markdown("📍 **Recife**")
                st.markdown("🥈 **Salvador**")
            else:
                st.markdown("🥈 **Recife**")
                st.markdown("📍 **Salvador**")
        
        # Tabela de resultados
        st.subheader("📊 Pontuação Detalhada por Critério")
        st.markdown("""
        A tabela abaixo mostra como cada cidade se saiu em cada critério. 
        **Valores mais altos indicam melhor desempenho** em cada métrica.
        """)
        
        # Renomear colunas para linguagem mais amigável
        display_df = df_ranking_sorted.copy()
        
        # Verificar quantas colunas existem e renomear adequadamente
        if len(display_df.columns) == 5:
            display_df.columns = [
                "Tempo de Entrega", 
                "Potencial de Consumo", 
                "Custo Operacional", 
                "Custo Imobiliário", 
                "Score Final"
            ]
        elif len(display_df.columns) == 6:
            display_df.columns = [
                "Tempo de Entrega", 
                "Potencial de Consumo", 
                "Custo Operacional", 
                "Custo Imobiliário", 
                "Score Final",
                "Coluna Extra"
            ]
        else:
            # Se houver um número diferente de colunas, usar nomes genéricos
            display_df.columns = [f"Critério {i+1}" for i in range(len(display_df.columns)-1)] + ["Score Final"]
        st.dataframe(display_df, use_container_width=True)
        
    else:
        st.warning("⚠️ Resultados da análise não estão disponíveis no momento.")
    
    # Gráficos resumidos para cada KPI
    st.subheader("📈 Comparativo Visual por Critério")
    st.markdown("""
    Os gráficos abaixo mostram o desempenho de cada cidade nos 4 critérios principais. 
    **Para tempo de entrega e custos, valores menores são melhores. Para potencial de consumo, valores maiores são melhores.**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # KPI 1 - Tempo de entrega
        st.markdown("**🚚 Tempo Médio de Entrega**")
        st.caption("Menor tempo = Melhor para clientes")
        
        # Dados de fallback para demonstração
        fallback_delivery_data = {
            "Recife": 2.5,
            "Salvador": 3.2
        }
        
        if kpi1_results and "city_comparison" in kpi1_results:
            city_data = kpi1_results["city_comparison"]
            cities = list(city_data.keys())
            delivery_times = [city_data[city].get("delivery_time", 0) for city in cities]
            
            # Se os dados estão vazios ou zerados, usar fallback
            if not delivery_times or all(t == 0 for t in delivery_times):
                delivery_times = [fallback_delivery_data.get(city, 3.0) for city in cities]
                st.info("📊 *Exibindo dados de exemplo para demonstração*")
        else:
            cities = ["Recife", "Salvador"]
            delivery_times = [fallback_delivery_data[city] for city in cities]
            st.info("📊 *Exibindo dados de exemplo para demonstração*")
        
        fig1 = pd.DataFrame({
            "Cidade": cities,
            "Tempo (horas)": delivery_times
        }).set_index("Cidade")
        
        st.bar_chart(fig1)
    
    with col2:
        # KPI 2 - CapEx
        st.markdown("**🏢 Custo de Aquisição Imobiliária**")
        st.caption("Menor custo = Menor investimento inicial")
        
        # Dados de fallback para demonstração
        fallback_capex_data = {
            "Recife": 45.2,  # R$ 45.2 milhões
            "Salvador": 38.7  # R$ 38.7 milhões
        }
        
        capex_data = []
        using_fallback = False
        
        if kpi2_results:
            if "capex_recife" in kpi2_results and kpi2_results["capex_recife"]:
                recife_capex = kpi2_results["capex_recife"].get("total_capex", 0)
                if recife_capex > 0:
                    capex_data.append({"Cidade": "Recife", "Custo (R$ milhões)": recife_capex / 1_000_000})
                else:
                    capex_data.append({"Cidade": "Recife", "Custo (R$ milhões)": fallback_capex_data["Recife"]})
                    using_fallback = True
            else:
                capex_data.append({"Cidade": "Recife", "Custo (R$ milhões)": fallback_capex_data["Recife"]})
                using_fallback = True
            
            if "capex_salvador" in kpi2_results and kpi2_results["capex_salvador"]:
                salvador_capex = kpi2_results["capex_salvador"].get("total_capex", 0)
                if salvador_capex > 0:
                    capex_data.append({"Cidade": "Salvador", "Custo (R$ milhões)": salvador_capex / 1_000_000})
                else:
                    capex_data.append({"Cidade": "Salvador", "Custo (R$ milhões)": fallback_capex_data["Salvador"]})
                    using_fallback = True
            else:
                capex_data.append({"Cidade": "Salvador", "Custo (R$ milhões)": fallback_capex_data["Salvador"]})
                using_fallback = True
        else:
            # Usar dados de fallback se não há resultados
            capex_data = [
                {"Cidade": "Recife", "Custo (R$ milhões)": fallback_capex_data["Recife"]},
                {"Cidade": "Salvador", "Custo (R$ milhões)": fallback_capex_data["Salvador"]}
            ]
            using_fallback = True
        
        if using_fallback:
            st.info("📊 *Exibindo dados de exemplo para demonstração*")
        
        fig2 = pd.DataFrame(capex_data).set_index("Cidade")
        st.bar_chart(fig2)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # KPI 3 - Potencial de consumo
        st.markdown("**👥 Potencial de Receita Anual**")
        st.caption("Maior receita = Maior oportunidade de mercado")
        
        # Dados de fallback para demonstração
        fallback_revenue_data = {
            "Recife": 125.8,  # R$ 125.8 milhões
            "Salvador": 98.3   # R$ 98.3 milhões
        }
        
        if kpi3_results and "revenue_scenario_probable" in kpi3_results:
            revenue_data = kpi3_results["revenue_scenario_probable"]["estimated_revenue"]
            if revenue_data and any(v > 0 for v in revenue_data.values()):
                fig3 = pd.DataFrame([
                    {"Cidade": city, "Receita (R$ milhões)": revenue / 1_000_000}
                    for city, revenue in revenue_data.items()
                ]).set_index("Cidade")
            else:
                fig3 = pd.DataFrame([
                    {"Cidade": city, "Receita (R$ milhões)": fallback_revenue_data[city]}
                    for city in fallback_revenue_data.keys()
                ]).set_index("Cidade")
                st.info("📊 *Exibindo dados de exemplo para demonstração*")
        else:
            fig3 = pd.DataFrame([
                {"Cidade": city, "Receita (R$ milhões)": fallback_revenue_data[city]}
                for city in fallback_revenue_data.keys()
            ]).set_index("Cidade")
            st.info("📊 *Exibindo dados de exemplo para demonstração*")
        
        st.bar_chart(fig3)
    
    with col4:
        # KPI 4 - Custo operacional
        st.markdown("**💰 Custo Operacional por Pedido**")
        st.caption("Menor custo = Maior eficiência operacional")
        
        # Dados de fallback para demonstração
        fallback_operational_data = {
            "Recife": 12.50,  # R$ 12.50 por pedido
            "Salvador": 14.80  # R$ 14.80 por pedido
        }
        
        cost_data = []
        using_fallback = False
        
        if kpi4_results:
            for city, city_data in kpi4_results.items():
                if isinstance(city_data, dict) and "total_operational_cost_per_order" in city_data:
                    cost = city_data["total_operational_cost_per_order"]
                    if cost > 0:
                        cost_data.append({
                            "Cidade": city,
                            "Custo (R$)": cost
                        })
                    else:
                        cost_data.append({
                            "Cidade": city,
                            "Custo (R$)": fallback_operational_data.get(city, 15.0)
                        })
                        using_fallback = True
                else:
                    cost_data.append({
                        "Cidade": city,
                        "Custo (R$)": fallback_operational_data.get(city, 15.0)
                    })
                    using_fallback = True
            
            # Se não encontrou dados válidos, usar fallback
            if not cost_data:
                cost_data = [
                    {"Cidade": "Recife", "Custo (R$)": fallback_operational_data["Recife"]},
                    {"Cidade": "Salvador", "Custo (R$)": fallback_operational_data["Salvador"]}
                ]
                using_fallback = True
        else:
            # Usar dados de fallback se não há resultados
            cost_data = [
                {"Cidade": "Recife", "Custo (R$)": fallback_operational_data["Recife"]},
                {"Cidade": "Salvador", "Custo (R$)": fallback_operational_data["Salvador"]}
            ]
            using_fallback = True
        
        if using_fallback:
            st.info("📊 *Exibindo dados de exemplo para demonstração*")
        
        fig4 = pd.DataFrame(cost_data).set_index("Cidade")
        st.bar_chart(fig4)

elif current_section == "🚚 Critério 1: Tempo de Entrega":
    st.header("🚚 Critério 1: Tempo de Entrega")
    
    # Contexto do KPI
    st.markdown("""
    **🎯 O que medimos:** Tempo médio para entregar produtos aos clientes a partir de cada cidade.
    
    **💡 Por que é importante:** Tempos de entrega menores significam maior satisfação do cliente e vantagem competitiva.
    
    **📊 Como interpretar:** Valores menores indicam melhor desempenho logístico.
    """)
    
    # Insights principais
    if kpi1_results and "city_comparison" in kpi1_results:
        city_data = kpi1_results["city_comparison"]
        cities = list(city_data.keys())
        delivery_times = [city_data[city].get("delivery_time", 0) for city in cities]
        
        best_city = cities[delivery_times.index(min(delivery_times))]
        worst_city = cities[delivery_times.index(max(delivery_times))]
        time_diff = max(delivery_times) - min(delivery_times)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏆 Melhor Cidade", best_city, f"{min(delivery_times):.1f}h")
        with col2:
            st.metric("📊 Diferença", f"{time_diff:.1f}h", "entre cidades")
        with col3:
            st.metric("⚡ Vantagem", f"{((max(delivery_times) - min(delivery_times))/max(delivery_times)*100):.1f}%", "mais rápido")
    
    # Exibir estatísticas gerais
    display_kpi1_overall_stats(kpi1_results)
    
    # Exibir mapa de isócronas
    display_kpi1_isochrone_map(kpi1_results)
    
    # Exibir tabela de rotas
    display_kpi1_routes_table(kpi1_results)

elif current_section == "🏢 Critério 2: Custo Imobiliário":
    st.header("🏢 Critério 2: Custo Imobiliário")
    
    # Contexto do KPI
    st.markdown("""
    **🎯 O que medimos:** Custo total para adquirir terrenos e construir galpões em cada cidade.
    
    **💡 Por que é importante:** Custos menores significam menor investimento inicial e melhor retorno financeiro.
    
    **📊 Como interpretar:** Valores menores indicam menor investimento necessário.
    """)
    
    # Insights principais
    if kpi2_results:
        capex_data = []
        if "capex_recife" in kpi2_results and kpi2_results["capex_recife"]:
            recife_capex = kpi2_results["capex_recife"].get("total_capex", 0)
            capex_data.append({"Cidade": "Recife", "Custo": recife_capex})
        if "capex_salvador" in kpi2_results and kpi2_results["capex_salvador"]:
            salvador_capex = kpi2_results["capex_salvador"].get("total_capex", 0)
            capex_data.append({"Cidade": "Salvador", "Custo": salvador_capex})
        
        if capex_data:
            costs = [item["Custo"] for item in capex_data]
            cities = [item["Cidade"] for item in capex_data]
            best_city = cities[costs.index(min(costs))]
            worst_city = cities[costs.index(max(costs))]
            cost_diff = max(costs) - min(costs)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Menor Custo", best_city, f"R$ {min(costs)/1_000_000:.1f}M")
            with col2:
                st.metric("📊 Diferença", f"R$ {cost_diff/1_000_000:.1f}M", "entre cidades")
            with col3:
                st.metric("💡 Economia", f"{((max(costs) - min(costs))/max(costs)*100):.1f}%", "menor investimento")
    
    # Exibir comparativo de CapEx
    display_kpi2_capex_comparison(kpi2_results)
    
    # Exibir detalhes dos imóveis
    display_kpi2_property_details(kpi2_results)

elif current_section == "👥 Critério 3: Potencial de Consumo":
    st.header("👥 Critério 3: Potencial de Consumo")
    
    # Contexto do KPI
    st.markdown("""
    **🎯 O que medimos:** Potencial de receita anual estimado baseado na população e poder de compra da região.
    
    **💡 Por que é importante:** Maior potencial de consumo significa mais oportunidades de vendas e crescimento.
    
    **📊 Como interpretar:** Valores maiores indicam maior oportunidade de mercado.
    """)
    
    # Insights principais
    if kpi3_results and "revenue_scenario_probable" in kpi3_results:
        revenue_data = kpi3_results["revenue_scenario_probable"]["estimated_revenue"]
        cities = list(revenue_data.keys())
        revenues = list(revenue_data.values())
        
        best_city = cities[revenues.index(max(revenues))]
        worst_city = cities[revenues.index(min(revenues))]
        revenue_diff = max(revenues) - min(revenues)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📈 Maior Potencial", best_city, f"R$ {max(revenues)/1_000_000:.1f}M")
        with col2:
            st.metric("📊 Diferença", f"R$ {revenue_diff/1_000_000:.1f}M", "entre cidades")
        with col3:
            st.metric("💼 Oportunidade", f"{((max(revenues) - min(revenues))/max(revenues)*100):.1f}%", "maior receita")
    
    # Exibir receita potencial
    display_kpi3_revenue_potential(kpi3_results)
    
    # Exibir mapa de consumo
    display_kpi3_consumption_map(kpi3_results)
    
    # Exibir clusters de consumidores
    display_kpi3_consumer_clusters(kpi3_results)

elif current_section == "💰 Critério 4: Custo Operacional":
    st.header("💰 Critério 4: Custo Operacional")
    
    # Contexto do KPI
    st.markdown("""
    **🎯 O que medimos:** Custo médio por pedido para operar o centro de distribuição em cada cidade.
    
    **💡 Por que é importante:** Custos operacionais menores significam maior eficiência e melhor margem de lucro.
    
    **📊 Como interpretar:** Valores menores indicam maior eficiência operacional.
    """)
    
    # Insights principais
    if kpi4_results:
        cost_data = []
        for city, city_data in kpi4_results.items():
            if isinstance(city_data, dict) and "total_operational_cost_per_order" in city_data:
                cost_data.append({
                    "Cidade": city,
                    "Custo": city_data["total_operational_cost_per_order"]
                })
        
        if cost_data:
            costs = [item["Custo"] for item in cost_data]
            cities = [item["Cidade"] for item in cost_data]
            best_city = cities[costs.index(min(costs))]
            worst_city = cities[costs.index(max(costs))]
            cost_diff = max(costs) - min(costs)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⚡ Menor Custo", best_city, f"R$ {min(costs):.2f}")
            with col2:
                st.metric("📊 Diferença", f"R$ {cost_diff:.2f}", "por pedido")
            with col3:
                st.metric("💡 Eficiência", f"{((max(costs) - min(costs))/max(costs)*100):.1f}%", "mais eficiente")
    
    # Exibir detalhamento de custos
    display_kpi4_cost_breakdown(kpi4_results)
    
    # Exibir custo por pedido
    display_kpi4_cost_per_order(kpi4_results)
    
    # Exibir simulação de custos
    display_kpi4_cost_simulation_inputs(kpi4_results)

elif current_section == "⚖️ Cenários de Decisão":
    st.header("⚖️ Cenários de Decisão")
    
    # Explicação do conceito
    st.markdown("""
    **🎯 O que você pode fazer aqui:** Ajustar a importância de cada critério para ver como isso afeta a recomendação final.
    
    **💡 Como funciona:** Os "pesos" representam o quanto cada critério importa para sua decisão. 
    - **Peso maior** = Critério mais importante
    - **Peso menor** = Critério menos importante
    
    **📊 Exemplo:** Se você priorizar "Tempo de Entrega" com peso alto, a cidade com melhor logística será favorecida.
    """)

    st.subheader("🎛️ Ajuste a Importância de Cada Critério")
    st.markdown("**Arraste os controles abaixo para definir o que é mais importante para sua decisão:**")
    
    # Sliders para ajustar os pesos com descrições mais claras
    col1, col2 = st.columns(2)
    
    with col1:
        weight_delivery_time = st.slider(
            "🚚 Velocidade de Entrega", 
            0.0, 1.0, 0.40, 0.05,
            help="Quão importante é entregar rapidamente aos clientes?"
        )
        weight_consumption_potential = st.slider(
            "👥 Potencial de Mercado", 
            0.0, 1.0, 0.30, 0.05,
            help="Quão importante é ter um grande mercado consumidor?"
        )
    
    with col2:
        weight_operational_cost = st.slider(
            "💰 Eficiência Operacional", 
            0.0, 1.0, 0.20, 0.05,
            help="Quão importante é ter custos operacionais baixos?"
        )
        weight_real_estate_cost = st.slider(
            "🏢 Investimento Inicial", 
            0.0, 1.0, 0.10, 0.05,
            help="Quão importante é ter baixo custo de aquisição imobiliária?"
        )

    total_weights = weight_delivery_time + weight_consumption_potential + weight_operational_cost + weight_real_estate_cost
    if total_weights == 0:
        st.warning("A soma dos pesos não pode ser zero. Por favor, ajuste.")
    else:
        # Normalizar pesos para que a soma seja 1
        normalized_weights = {
            "delivery_time": weight_delivery_time / total_weights,
            "consumption_potential": weight_consumption_potential / total_weights,
            "operational_cost": weight_operational_cost / total_weights,
            "real_estate_cost": weight_real_estate_cost / total_weights,
        }
        
        # Mostrar pesos atuais
        st.subheader("📊 Pesos Atuais dos Critérios")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🚚 Entrega", f"{normalized_weights['delivery_time']*100:.0f}%")
        with col2:
            st.metric("👥 Mercado", f"{normalized_weights['consumption_potential']*100:.0f}%")
        with col3:
            st.metric("💰 Operacional", f"{normalized_weights['operational_cost']*100:.0f}%")
        with col4:
            st.metric("🏢 Imobiliário", f"{normalized_weights['real_estate_cost']*100:.0f}%")

        # Recalcular TOPSIS com os novos pesos
        recalculated_integration_results = integrate_kpis_mcda(
            kpi1_results, kpi2_results, kpi3_results, kpi4_results, weights=normalized_weights
        )
        
        st.subheader("🎯 Nova Recomendação")
        df_recalculated_ranking = pd.DataFrame.from_dict(recalculated_integration_results["final_ranking"], orient="index")
        df_recalculated_ranking_sorted = df_recalculated_ranking.sort_values(by="topsis_score", ascending=False)
        
        # Cidade recomendada
        recommended_city = df_recalculated_ranking_sorted.index[0]
        score = df_recalculated_ranking_sorted['topsis_score'].max()
        second_city = df_recalculated_ranking_sorted.index[1]
        second_score = df_recalculated_ranking_sorted.loc[second_city, 'topsis_score']
        
        # Destaque da nova recomendação
        st.success(f"""
        **🏆 NOVA RECOMENDAÇÃO: {recommended_city}**
        
        Com os pesos ajustados, {recommended_city} apresenta o melhor desempenho geral com uma pontuação de **{score:.2f}**.
        
        A diferença para {second_city} (segunda colocada com {second_score:.2f}) é de **{score - second_score:.2f} pontos**.
        """)
        
        # Análise de sensibilidade simplificada
        st.subheader("📈 Análise de Impacto")
        if kpi_integration_results and "final_ranking" in kpi_integration_results:
            original_ranking = pd.DataFrame.from_dict(kpi_integration_results["final_ranking"], orient="index")
            original_ranking_sorted = original_ranking.sort_values(by="topsis_score", ascending=False)
            
            if recommended_city != original_ranking_sorted.index[0]:
                st.info(f"""
                **🔄 Mudança na Recomendação:** 
                
                Com os novos pesos, a recomendação mudou de **{original_ranking_sorted.index[0]}** para **{recommended_city}**.
                
                Isso mostra que a priorização dos critérios tem impacto significativo na decisão final.
                """)
            else:
                st.success(f"""
                **✅ Consistência:** 
                
                A recomendação permanece **{recommended_city}** mesmo com os pesos ajustados, 
                indicando que esta cidade tem um desempenho robusto em múltiplos cenários.
                """)
        else:
            st.info("Análise de impacto não disponível - dados originais não encontrados.")
        
        # Tabela de resultados
        st.subheader("📊 Pontuação Detalhada")
        display_df = df_recalculated_ranking_sorted.copy()
        
        # Verificar quantas colunas existem e renomear adequadamente
        if len(display_df.columns) == 5:
            display_df.columns = [
                "Tempo de Entrega", 
                "Potencial de Consumo", 
                "Custo Operacional", 
                "Custo Imobiliário", 
                "Score Final"
            ]
        elif len(display_df.columns) == 6:
            display_df.columns = [
                "Tempo de Entrega", 
                "Potencial de Consumo", 
                "Custo Operacional", 
                "Custo Imobiliário", 
                "Score Final",
                "Coluna Extra"
            ]
        else:
            # Se houver um número diferente de colunas, usar nomes genéricos
            display_df.columns = [f"Critério {i+1}" for i in range(len(display_df.columns)-1)] + ["Score Final"]
        st.dataframe(display_df, use_container_width=True)
        
        # Adicionar radar chart comparativo
        st.subheader("📊 Comparativo Visual de Desempenho")
        st.markdown("""
        **Como interpretar o gráfico radar:**
        - **Quanto mais a linha se estende para fora** em um eixo, melhor o desempenho da cidade naquele critério
        - **Área maior** = Desempenho geral melhor
        - **Forma mais equilibrada** = Desempenho mais consistente em todos os critérios
        """)
        
        # Preparar dados para o radar chart
        categories = ["Tempo de Entrega", "Potencial de Consumo", "Custo Operacional", "Custo Imobiliário"]
        
        # Normalizar valores para o radar (0-1)
        radar_data = []
        
        for city in df_recalculated_ranking.index:
            city_data = df_recalculated_ranking.loc[city]
            
            # Valores normalizados (inverter para custos onde menor é melhor)
            delivery_time_norm = 1 - city_data["delivery_time"] / df_recalculated_ranking["delivery_time"].max()
            consumption_potential_norm = city_data["consumption_potential"] / df_recalculated_ranking["consumption_potential"].max()
            operational_cost_norm = 1 - city_data["operational_cost"] / df_recalculated_ranking["operational_cost"].max()
            real_estate_cost_norm = 1 - city_data["real_estate_cost"] / df_recalculated_ranking["real_estate_cost"].max()
            
            radar_data.append({
                "Cidade": city,
                "Tempo de Entrega": delivery_time_norm,
                "Potencial de Consumo": consumption_potential_norm,
                "Custo Operacional": operational_cost_norm,
                "Custo Imobiliário": real_estate_cost_norm,
                "Score Final": city_data["topsis_score"]
            })
        
        radar_df = pd.DataFrame(radar_data)
        
        # Criar radar chart
        fig = go.Figure()
        
        for i, row in radar_df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[
                    row["Tempo de Entrega"],
                    row["Potencial de Consumo"],
                    row["Custo Operacional"],
                    row["Custo Imobiliário"],
                    row["Tempo de Entrega"]  # Fechar o gráfico
                ],
                theta=categories + [categories[0]],  # Fechar o gráfico
                fill='toself',
                name=row["Cidade"],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            title="Comparativo de Desempenho por Critério",
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Adicionar botão para exportar resultados
        if st.button("📥 Exportar Resultados"):
            # Criar DataFrame com os resultados
            export_df = df_recalculated_ranking.copy()
            export_df["Pesos Utilizados"] = str(normalized_weights)
            
            # Converter para CSV
            csv = export_df.to_csv(index=True)
            
            # Botão de download
            st.download_button(
                label="📊 Baixar Resultados como CSV",
                data=csv,
                file_name="analise_localizacao_cd.csv",
                mime="text/csv"
            )

elif current_section == "📋 Metodologia e Dados":
    st.header("📋 Metodologia e Dados Utilizados")
    
    # Seção de Metodologia Simplificada
    st.subheader("🔬 Metodologia da Análise")
    st.markdown("""
    **📊 Processo de Análise:**
    
    1. **Coleta de Dados:** Reunimos informações sobre cada cidade em 4 áreas principais
    2. **Processamento:** Organizamos e padronizamos os dados para comparação
    3. **Análise por Critério:** Avaliamos cada cidade em cada critério separadamente
    4. **Integração:** Combinamos todos os critérios usando uma metodologia científica
    5. **Recomendação:** Geramos uma pontuação final e recomendação baseada em evidências
    
    **⚖️ Metodologia de Decisão (TOPSIS):**
    - Utilizamos uma técnica chamada TOPSIS (Técnica de Ordenação por Similaridade à Solução Ideal)
    - Esta metodologia é amplamente utilizada em tomadas de decisão empresariais
    - Ela considera tanto os pontos fortes quanto fracos de cada opção
    - Permite ajustar a importância de cada critério conforme suas prioridades
    """)
    
    # Seção de Dados Utilizados
    st.subheader("📊 Fontes de Dados")
    st.markdown("""
    **🏢 Dados Imobiliários:**
    - **Fonte Planejada:** Zap Imóveis e Viva Real para preços de terrenos e galpões
    - **Status Atual:** Dados simulados devido a limitações de scraping
    - **Justificativa:** Dificuldades técnicas no web scraping (cards com N/A, redirecionamentos)
    - **Impacto:** Análise baseada em benchmarks da indústria
    
    **🚚 Dados Logísticos:**
    - **Fonte Planejada:** APIs de roteamento (OSRM) para calcular tempos de entrega
    - **Status Atual:** Simulação devido a falhas no OSRM Table Service
    - **Justificativa:** Problemas de infraestrutura ou conectividade
    - **Impacto:** Análise baseada em distâncias e cenários realistas
    
    **👥 Dados Demográficos:**
    - **Fonte Planejada:** IBGE (Instituto Brasileiro de Geografia e Estatística)
    - **Status Atual:** Dados simulados devido a indisponibilidade da API
    - **Justificativa:** API do IBGE inacessível de 22/09 a 26/09 (erros 500)
    - **Impacto:** Análise baseada em benchmarks demográficos regionais
    
    **💰 Dados Operacionais:**
    - **Fonte:** Estimativas baseadas em benchmarks da indústria
    - **Status:** Dados calculados com base em parâmetros realistas
    - **Justificativa:** Metodologia validada com dados de mercado
    - **Impacto:** Análise confiável para comparação entre cidades
    
    **⚠️ Transparência:** Todos os dados simulados são claramente identificados e justificados por limitações técnicas temporárias.
    """)
    
    # Seção de Limitações
    st.subheader("⚠️ Limitações e Considerações")
    st.markdown("""
    **📋 Limitações Técnicas Identificadas:**
    
    **🏢 Dados Imobiliários:**
    - **Problema:** Web scraping limitado devido a proteções anti-bot
    - **Impacto:** Dados simulados baseados em benchmarks de mercado
    - **Solução Futura:** Implementar técnicas de scraping mais robustas
    
    **👥 Dados Demográficos:**
    - **Problema:** API do IBGE indisponível (22-26/09/2025)
    - **Impacto:** Dados simulados baseados em censos anteriores
    - **Solução Futura:** Implementar retry com backoff exponencial
    
    **🚚 Dados de Roteamento:**
    - **Problema:** OSRM Table Service com falhas de conectividade
    - **Impacto:** Simulação baseada em distâncias geográficas
    - **Solução Futura:** Containerização do OSRM ou APIs alternativas
    
    **📊 Limitações Gerais:**
    - Os dados podem não refletir mudanças recentes no mercado
    - Estimativas de custos operacionais são baseadas em benchmarks gerais
    - Fatores qualitativos (como clima político, incentivos fiscais) não foram quantificados
    
    **💡 Recomendações para Implementação Real:**
    - Realizar visitas técnicas às cidades candidatas
    - Consultar especialistas locais em logística e imóveis
    - Considerar fatores específicos da Magalu (parcerias, infraestrutura existente)
    - Avaliar incentivos fiscais e regulamentações locais
    - Implementar coleta de dados em tempo real para produção
    """)
    
    # Botão para gerar relatório executivo
    st.subheader("📄 Relatório Executivo")
    st.markdown("""
    **📊 Geração de Relatório:**
    Clique no botão abaixo para gerar um relatório executivo com os principais insights e recomendações desta análise.
    """)
    
    if st.button("📋 Gerar Relatório Executivo"):
        # Simular geração de relatório
        st.success("✅ Relatório executivo gerado com sucesso!")
        st.info("""
        **📄 Conteúdo do Relatório:**
        - Resumo executivo da recomendação
        - Análise detalhada por critério
        - Comparativo visual das cidades
        - Cenários de sensibilidade
        - Próximos passos recomendados
        
        *Nota: Em uma implementação completa, este botão geraria um PDF ou documento Word com todos os insights.*
        """)
        
        # Simular download do relatório
        if kpi_integration_results and "final_ranking" in kpi_integration_results:
            ranking_df = pd.DataFrame.from_dict(kpi_integration_results["final_ranking"], orient="index")
            ranking_sorted = ranking_df.sort_values(by="topsis_score", ascending=False)
            
            report_content = f"""
        RELATÓRIO EXECUTIVO - ANÁLISE DE LOCALIZAÇÃO CD MAGALU NORDESTE
        
        RECOMENDAÇÃO FINAL: {ranking_sorted.index[0]}
        
        RESUMO:
        Esta análise comparou Recife e Salvador para localização do Centro de Distribuição da Magalu no Nordeste.
        A recomendação é baseada em 4 critérios principais: Tempo de Entrega, Custo Imobiliário, 
        Potencial de Consumo e Custo Operacional.
        
        PRINCIPAIS INSIGHTS:
        - {ranking_sorted.index[0]} apresenta melhor desempenho geral
        - Score final: {ranking_sorted['topsis_score'].max():.2f}
        - Diferença para segunda colocada: {ranking_sorted['topsis_score'].max() - ranking_sorted['topsis_score'].min():.2f} pontos
        
        LIMITAÇÕES TÉCNICAS:
        - Dados imobiliários: Simulados devido a limitações de web scraping
        - Dados demográficos: Simulados devido a indisponibilidade da API do IBGE (22-26/09/2025)
        - Dados de roteamento: Simulados devido a falhas no OSRM Table Service
        - Todos os dados simulados foram calibrados com benchmarks da indústria
        
        PRÓXIMOS PASSOS:
        1. Validação técnica das localizações específicas
        2. Análise de incentivos fiscais locais
        3. Estudo de viabilidade financeira detalhado
        4. Consulta a stakeholders locais
        5. Implementação de coleta de dados em tempo real para produção
        """
        else:
            report_content = """
        RELATÓRIO EXECUTIVO - ANÁLISE DE LOCALIZAÇÃO CD MAGALU NORDESTE
        
        RESUMO:
        Esta análise comparou Recife e Salvador para localização do Centro de Distribuição da Magalu no Nordeste.
        A recomendação é baseada em 4 critérios principais: Tempo de Entrega, Custo Imobiliário, 
        Potencial de Consumo e Custo Operacional.
        
        PRÓXIMOS PASSOS:
        1. Validação técnica das localizações específicas
        2. Análise de incentivos fiscais locais
        3. Estudo de viabilidade financeira detalhado
        4. Consulta a stakeholders locais
        """
        
        st.download_button(
            label="📥 Baixar Relatório Executivo",
            data=report_content,
            file_name="relatorio_executivo_cd_magalu.txt",
            mime="text/plain"
        )

# --- Metabase (Instruções) ---
st.sidebar.markdown("--- ")
st.sidebar.header("🔗 Integração com Metabase")
st.sidebar.info("""
**📊 Para implementação completa:**
- Conectar ao banco de dados PostgreSQL
- Criar dashboards interativos
- Configurar alertas automáticos
- Permitir drill-down nos dados
""")