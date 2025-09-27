# Relatório Executivo: Decisão Estratégica de Localização para Novo CD Magalu Nordeste

**Para:** Diretoria Executiva do Magalu  
**De:** [Lucas Gomes Leria](https://www.linkedin.com/in/lucasleria/)  
**Data:** 27 de Setembro de 2025  
**Assunto:** Recomendação para a Localização do Novo Centro de Distribuição no Nordeste  

## 1. Sumário Executivo

Este relatório apresenta a análise estratégica para a escolha da localização do novo Centro de Distribuição (CD) do Magalu na região Nordeste, comparando as cidades de Salvador e Recife. Nosso objetivo foi identificar a opção mais vantajosa para agilizar as entregas e fortalecer a presença de mercado, utilizando uma metodologia robusta baseada em dados e inteligência artificial. Após uma análise multicritério (MCDA) que considerou Tempo Médio de Entrega, Custo de Aquisição Imobiliária, Potencial de Consumo da Região e Custo Operacional Total, e com pesos definidos pela diretoria, **recomendamos a cidade de Salvador como a localização mais estratégica.**

Salvador se destacou principalmente devido ao seu **elevado Potencial de Consumo da Região**, fator que a diretoria priorizou com 40% de peso na decisão. Embora Recife apresente vantagens em custos (imobiliário e operacional), a capacidade de Salvador de gerar maior receita e sua boa performance logística a tornam a escolha mais alinhada aos objetivos de crescimento do Magalu. A decisão é robusta, com Salvador sendo a vencedora em 71.4% dos cenários de sensibilidade testados. Para explorar os detalhes e simular cenários, desenvolvemos um **Dashboard Interativo no Streamlit**, uma ferramenta intuitiva que permite à equipe de negócios interagir diretamente com os dados e a análise.

## 2. Contexto e Objetivos Estratégicos

A expansão da rede logística do Magalu no Nordeste é uma iniciativa estratégica para:

*   **Reduzir o tempo de entrega:** Melhorar a experiência do cliente e a competitividade.
*   **Otimizar custos operacionais:** Aumentar a eficiência e a rentabilidade.
*   **Capturar maior fatia de mercado:** Aproveitar o potencial de consumo da região.

Diante da necessidade de escolher entre Salvador e Recife, este estudo foi conduzido para fornecer uma base analítica sólida para essa decisão de alto impacto.

## 3. Metodologia de Alto Nível

Nosso projeto seguiu uma abordagem estruturada em quatro etapas principais:

1.  **Planejamento e Definição:** Identificação e validação dos principais indicadores (KPIs) para a decisão.
2.  **Coleta e Preparação de Dados (ETL):** Coleta de dados de fontes abertas (imóveis, malha viária, demografia) e seu tratamento para garantir qualidade e consistência.
3.  **Análise e Modelagem:** Aplicação de técnicas avançadas de análise de dados, incluindo modelos preditivos e geoespaciais, culminando em uma Análise de Decisão Multicritério (MCDA) para comparar as cidades.
4.  **Visualização e Comunicação:** Desenvolvimento de um dashboard interativo para apresentar os resultados de forma clara e permitir a exploração de cenários.

## 4. Principais Descobertas e KPIs Avaliados

A decisão foi fundamentada na avaliação de quatro KPIs críticos, aos quais a diretoria atribuiu os seguintes pesos:

| KPI                                  | Peso Atribuído (%) |
| :----------------------------------- | :----------------: |
| Potencial de Consumo da Região       |        40%         |
| Tempo Médio de Entrega               |        20%         |
| Custo de Aquisição Imobiliária       |        20%         |
| Custo Operacional Total              |        20%         |
| **Total**                            |      **100%**      |

### 4.1. Ranking Final da Análise (TOPSIS)

Com base nos pesos definidos, o resultado da análise MCDA (TOPSIS) é:

1.  **Salvador:** Score TOPSIS de **0.710**
2.  **Recife:** Score TOPSIS de **0.290**

**Recomendação:** **Salvador** é a localização mais estratégica para o novo CD, com uma vantagem clara sobre Recife.

### 4.2. Desempenho por KPI (Resumo)

*   **Potencial de Consumo da Região (40%):** Salvador demonstra um potencial de receita incremental significativamente maior, alinhado à prioridade estratégica de crescimento de mercado.
*   **Tempo Médio de Entrega (20%):** Salvador apresenta um tempo médio de entrega ligeiramente melhor para as principais capitais da região, contribuindo para a eficiência logística.
*   **Custo de Aquisição Imobiliária (20%):** Recife possui um custo de aquisição imobiliária mais vantajoso, o que representa um menor investimento inicial.
*   **Custo Operacional Total (20%):** Recife também mostra um custo operacional por pedido ligeiramente menor, indicando maior eficiência operacional em alguns aspectos.

### 4.3. Análise de Sensibilidade

Realizamos uma análise de sensibilidade com 7 cenários diferentes de pesos para testar a robustez da nossa recomendação. Os resultados mostraram que:

*   **Salvador foi a cidade vencedora em 5 dos 7 cenários (71.4% de robustez).**
*   A decisão é **sensível ao peso do Tempo Médio de Entrega**. Se este KPI for priorizado acima de 40%, Recife pode se tornar a opção preferencial. No entanto, com a priorização atual do Potencial de Consumo, Salvador mantém a liderança.

**Conclusão da Sensibilidade:** A recomendação por Salvador é **robusta** e consistente com a maioria das prioridades estratégicas, especialmente quando o potencial de mercado é um fator chave.

## 5. Análise de Implicações

A escolha de **Salvador** implica em:

*   **Maior Potencial de Receita:** Posicionamento estratégico para capturar o crescimento do mercado e o potencial de consumo da região.
*   **Eficiência Logística Competitiva:** Tempos de entrega favoráveis, embora não seja a líder absoluta em todos os cenários de custo.
*   **Investimento Inicial e Operacional:** Embora os custos imobiliários e operacionais sejam um pouco mais altos que em Recife, a priorização do potencial de consumo justifica essa diferença, indicando um retorno sobre o investimento potencialmente maior.

## 6. Recomendação e Plano de Ação

**Recomendação Final:** Com base na análise multicritério e nos pesos definidos pela diretoria, **recomendamos a implantação do novo Centro de Distribuição do Magalu em Salvador.**

**Próximos Passos Sugeridos:**

1.  **Validação Final dos Pesos:** Confirmar se a prioridade de 40% para o Potencial de Consumo da Região é a diretriz estratégica final. Caso haja ajustes, a análise pode ser rapidamente reexecutada usando o Dashboard Interativo.
2.  **Coleta de Dados Reais:** Priorizar a coleta e validação de dados reais para todos os KPIs, substituindo os dados simulados, para aumentar a precisão da decisão final.
3.  **Análise Qualitativa Complementar:** Realizar uma avaliação de fatores qualitativos (ex: riscos operacionais, incentivos fiscais, infraestrutura local) para complementar a análise quantitativa.
4.  **Apresentação Detalhada:** Utilizar o Dashboard Interativo para uma apresentação aprofundada aos demais stakeholders, permitindo a exploração de cenários e a compreensão dos resultados.

## 7. Riscos e Mitigações

*   **Risco:** Dependência de dados simulados em algumas análises.
    *   **Mitigação:** Priorizar a coleta de dados reais e de alta qualidade para refinar os modelos e a análise.
*   **Risco:** Variação nas prioridades estratégicas (pesos dos KPIs).
    *   **Mitigação:** Utilizar o Dashboard Interativo para simular rapidamente o impacto de diferentes pesos e ajustar a recomendação, se necessário.
*   **Risco:** Fatores qualitativos não considerados na análise MCDA.
    *   **Mitigação:** Realizar uma análise qualitativa complementar e integrar esses insights na decisão final.

## 8. Guia de Utilização do Dashboard Interativo (Streamlit)

Desenvolvemos um Dashboard Interativo para que a equipe de negócios possa explorar os resultados e simular cenários de forma intuitiva. O aplicativo está disponível em [Link para o Dashboard - A ser inserido após deploy].

### 8.1. Como Acessar e Navegar

1.  **Acesso:** Abra o link do Dashboard em seu navegador. A página inicial mostrará a "Visão Geral".
2.  **Menu Lateral:** No lado esquerdo da tela, você encontrará um menu de navegação (`Selecione a Seção`). Use-o para alternar entre as diferentes seções do dashboard:
    *   **Visão Geral:** Resumo dos principais resultados e a recomendação final.
    *   **KPI 1: Tempo de Entrega:** Detalhes sobre a eficiência logística.
    *   **KPI 2: Custo Imobiliário:** Comparativo de custos de terrenos e galpões.
    *   **KPI 3: Potencial de Consumo:** Análise demográfica e de mercado.
    *   **KPI 4: Custo Operacional:** Estimativa do custo médio por pedido.
    *   **Cenários de Decisão (TOPSIS):** A seção mais interativa, onde você pode ajustar os pesos dos KPIs.

### 8.2. Explorando a Seção "Visão Geral"

*   **Score Final (TOPSIS):** Veja o ranking das cidades com base nos pesos atuais. A cidade com o maior score é a recomendada.
*   **Recomendação:** Uma mensagem clara indicará a cidade mais estratégica.
*   **Resumo dos KPIs:** Gráficos de barras simples comparando Salvador e Recife para cada um dos quatro KPIs. Observe as unidades de medida (R$, horas) para entender o que cada barra representa.

### 8.3. Explorando as Seções de KPIs Individuais

Cada seção de KPI oferece uma análise mais aprofundada:

*   **KPI 1: Tempo de Entrega:** Você encontrará estatísticas gerais, mapas de isócronas (mostrando o alcance de entrega em diferentes tempos a partir de cada cidade) e tabelas detalhadas de rotas.
*   **KPI 2: Custo Imobiliário:** Compare o CapEx total e explore detalhes sobre os imóveis analisados.
*   **KPI 3: Potencial de Consumo:** Visualize o potencial de receita, mapas de consumo e clusters de consumidores.
*   **KPI 4: Custo Operacional:** Veja o detalhamento dos custos e o custo por pedido.

**Dica:** Preste atenção aos textos explicativos e títulos dos gráficos para entender os insights específicos de cada KPI.

### 8.4. Utilizando a Seção "Cenários de Decisão (TOPSIS)"

Esta é a seção mais poderosa para a tomada de decisão:

1.  **Definição de Pesos dos KPIs:** Você verá quatro sliders, um para cada KPI. Estes sliders permitem que você ajuste a importância (peso) de cada critério na decisão final. Por exemplo, se a diretoria decidir que o "Potencial de Consumo" é ainda mais crítico, você pode aumentar seu peso.
    *   **Importante:** Ao mover um slider, os outros pesos se ajustarão automaticamente para que a soma total seja sempre 100% (normalizada).
2.  **Ranking Recalculado (TOPSIS):** Após ajustar os pesos, o ranking das cidades será recalculado e exibido imediatamente. Você verá como a recomendação final pode mudar com diferentes prioridades.
3.  **Comparativo Radar entre Cidades:** Um gráfico de radar visualiza o desempenho de Salvador e Recife em cada KPI, ajustado pelos pesos. Quanto mais a linha de uma cidade se estende para fora em um eixo, melhor seu desempenho naquele critério. Isso oferece uma visão rápida e intuitiva das forças e fraquezas de cada opção.
4.  **Exportar Resultados:** Um botão permite baixar os resultados da análise (com os pesos ajustados) em formato CSV, facilitando o compartilhamento e a documentação.

**Objetivo:** Use esta seção para simular diferentes cenários de priorização e entender a robustez da decisão. Por exemplo, "O que aconteceria se o custo imobiliário fosse o mais importante?" ou "E se o tempo de entrega fosse o dobro de importante?".

### 8.5. Considerações Finais sobre o Dashboard

O Dashboard foi projetado para ser uma ferramenta viva, permitindo que a equipe de negócios explore os dados e tome decisões informadas. Ele é um protótipo funcional e pode ser expandido ou integrado a outras plataformas (como o Metabase) para uso em produção. Em caso de dúvidas sobre a interpretação de qualquer seção, consulte a equipe de análise de dados.

