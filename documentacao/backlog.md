# Product Backlog - Predição de Risco de Acidentes de Trânsito em áreas urbanas

Este documento apresenta o backlog priorizado do projeto, dividido ao longo das 6 Sprints do ciclo de vida.

### **Histórias de Usuario:**

### História de Usuário 1 — Identificação de áreas de risco

**Como** gestor municipal de trânsito,
**quero** visualizar em um mapa as áreas urbanas classificadas de acordo com o risco previsto de acidentes,
**para** identificar antecipadamente regiões com maior probabilidade de ocorrência e direcionar minha atenção aos locais mais críticos.

### História de Usuário 2 — Análise histórica e temporal

**Como** analista de trânsito,
**quero** consultar o risco previsto de acidentes utilizando filtros por região e período, comparando essas informações com os registros históricos disponíveis,
**para** complementar a análise baseada em ocorrências passadas e identificar padrões espaciais e temporais de risco.

### História de Usuário 3 — Priorização e distribuição de recursos

**Como** gestor municipal de trânsito,
**quero** visualizar e ordenar as regiões de acordo com seus níveis previstos de risco,
**para** priorizar os locais que necessitam de maior atenção e direcionar de forma mais eficiente os recursos públicos disponíveis.

### História de Usuário 4 — Apoio à tomada de decisão

**Como** engenheiro ou responsável pelo planejamento de tráfego,
**quero** consultar os níveis previstos de risco e as informações associadas às diferentes áreas urbanas,
**para** apoiar decisões relacionadas a possíveis ações de fiscalização, sinalização e melhorias na infraestrutura viária.


---

## Sprint 0: Estruturação e Iniciação (Concluído)
* **PB01 [Gestão]:** Elaborar e validar o Project Model Canvas (PMC).
* **PB02 [DevOps]:** Criar repositório no GitHub com estrutura de pastas padronizada (`dados`, `codigo_fonte`, `documentacao`, `notebooks`).
* **PB03 [Gestão]:** Configurar o quadro Kanban no GitHub Projects e mapear o Product Backlog inicial.

---

## Sprint 1: Validação dos Dados e Exploração

* **PB04 [Dados]:** Identificar e avaliar bases públicas de acidentes de trânsito quanto à cobertura geográfica, granularidade espacial e temporal, qualidade, volume e disponibilidade de atributos relevantes.
* **PB05 [Escopo]:** Definir o recorte geográfico inicial do projeto com base na disponibilidade e qualidade dos dados encontrados.
* **PB06 [Dados]:** Selecionar e coletar as fontes de dados de acidentes, dados meteorológicos e informações da malha viária necessárias ao projeto.
* **PB07 [Dados]:** Implementar rotinas de limpeza, padronização, remoção de duplicatas e tratamento de valores ausentes.
* **PB08 [Análise]:** Avaliar a qualidade dos dados coletados, identificando inconsistências, valores atípicos, cobertura temporal e limitações das bases.
* **PB09 [Geoprocessamento]:** Definir e implementar uma estratégia de discretização espacial adequada à granularidade dos dados, avaliando o uso da biblioteca Uber H3.
* **PB10 [Análise]:** Criar caderno Jupyter de Análise Exploratória de Dados (EDA), contendo análises estatísticas, temporais e espaciais das ocorrências.
* **PB11 [Pesquisa]:** Realizar levantamento inicial de trabalhos relacionados sobre predição espaço-temporal de acidentes, mapas de risco e aplicações de Machine Learning em segurança viária.
* **PB12 [Gestão]:** Refinar e priorizar o Product Backlog com base nos resultados da exploração e nas limitações identificadas nas fontes de dados.

---

## Sprint 2: Engenharia de Dados e Modelo Baseline

* **PB13 [ML]:** Definir formalmente a variável-alvo do modelo e os critérios utilizados para representar ou classificar o nível de risco de acidentes.
* **PB14 [Engenharia]:** Definir a unidade espaço-temporal de análise, combinando região geográfica e intervalo de tempo utilizados pelo modelo.
* **PB15 [Engenharia]:** Criar variáveis espaço-temporais, incluindo faixa horária, dia da semana, período do dia, histórico de ocorrências e demais atributos derivados relevantes.
* **PB16 [Engenharia]:** Integrar atributos externos disponíveis, como condições meteorológicas, densidade ou características da malha viária e informações geográficas.
* **PB17 [ML]:** Preparar os conjuntos de treinamento, validação e teste utilizando estratégia que preserve a separação temporal e espacial dos dados.
* **PB18 [ML]:** Implementar um modelo baseline simples, como regressão logística ou heurística baseada na frequência histórica de ocorrências.
* **PB19 [ML]:** Treinar modelos de Machine Learning mais robustos, avaliando algoritmos como Random Forest e XGBoost.
* **PB20 [ML]:** Avaliar os modelos utilizando métricas adequadas a dados desbalanceados, incluindo Precision, Recall, F1-Score, Precision-Recall AUC e Matriz de Confusão.
* **PB21 [ML]:** Comparar os modelos treinados com o baseline e selecionar a abordagem com melhor equilíbrio entre capacidade preditiva, generalização e custo computacional.
* **PB22 [Artigo]:** Redigir as seções iniciais de Introdução, Trabalhos Relacionados e descrição preliminar da Metodologia no template oficial da SBC.
* **PB23 [DevOps]:** Versionar códigos, configurações, métricas e artefatos necessários para reprodução dos experimentos.

---

## Sprint 3: Desenvolvimento e Publicação do MVP

* **PB24 [Backend]:** Estruturar o pipeline de inferência responsável por transformar localização, data e demais entradas disponíveis nas variáveis esperadas pelo modelo.
* **PB25 [Backend]:** Implementar função ou serviço de inferência capaz de retornar o nível ou índice de risco estimado para determinada região e período.
* **PB26 [Frontend]:** Desenvolver interface web interativa utilizando Streamlit para consulta dos níveis de risco.
* **PB27 [Geoprocessamento]:** Integrar visualização geográfica utilizando Folium, PyDeck ou tecnologia equivalente para representação dos níveis de risco no mapa.
* **PB28 [Frontend]:** Implementar filtros de consulta, como localização, data, período e demais parâmetros relevantes definidos durante a modelagem.
* **PB29 [Deploy]:** Publicar a primeira versão funcional do MVP na plataforma Streamlit Community Cloud ou infraestrutura equivalente.
* **PB30 [Validação]:** Validar o fluxo completo do MVP, desde a entrada do usuário até a geração da previsão e sua representação no mapa.
* **PB31 [Artigo]:** Atualizar a seção de Metodologia com a descrição do tratamento dos dados, engenharia de atributos, estratégia experimental, modelos avaliados e arquitetura do MVP.

---

## Sprint 4: Validação, Explicabilidade e Release Intermediária

* **PB32 [UX/UI]:** Realizar testes de uso do painel com usuários e registrar dificuldades de navegação, interpretação dos resultados e oportunidades de melhoria.
* **PB33 [Feedback]:** Consolidar os feedbacks recebidos e priorizar os ajustes com maior impacto sobre a experiência e compreensão do produto.
* **PB34 [Explicabilidade]:** Implementar mecanismo de explicabilidade do modelo utilizando SHAP ou abordagem equivalente para identificar os principais fatores associados às previsões.
* **PB35 [Frontend]:** Integrar ao painel uma visualização compreensível dos fatores que contribuíram para o nível de risco apresentado.
* **PB36 [ML]:** Refinar o modelo com base nos resultados obtidos, avaliando ajustes de hiperparâmetros, atributos e estratégia de classificação quando justificável.
* **PB37 [Otimização]:** Otimizar o pipeline de inferência e o carregamento dos dados e mapas interativos para melhorar o desempenho da aplicação.
* **PB38 [Validação]:** Executar nova avaliação do modelo final utilizando exclusivamente o conjunto de teste reservado.
* **PB39 [Release]:** Publicar uma release intermediária da aplicação contendo as melhorias de usabilidade, desempenho e explicabilidade implementadas.
* **PB40 [Artigo]:** Redigir a seção de Resultados e iniciar a Discussão, incluindo comparação entre modelos, métricas obtidas, mapas de risco e análises de explicabilidade.

---

## Sprint 5: Consolidação, Release Final e Apresentação

* **PB41 [Produto]:** Revisar as funcionalidades da aplicação e corrigir erros identificados durante os testes finais.
* **PB42 [Validação]:** Executar testes finais do fluxo completo da aplicação e documentar as principais limitações conhecidas do produto e do modelo.
* **PB43 [Documentação]:** Atualizar o `README` do repositório com descrição do projeto, arquitetura, fontes de dados, instruções de execução, tecnologias utilizadas e acesso à aplicação.
* **PB44 [Artigo]:** Finalizar a seção de Discussão, relacionando os resultados obtidos aos trabalhos relacionados e às limitações encontradas.
* **PB45 [Artigo]:** Redigir as Considerações Finais, contribuições, limitações e possibilidades de trabalhos futuros.
* **PB46 [Artigo]:** Revisar integralmente o artigo e adequá-lo às normas e ao template oficial da SBC.
* **PB47 [Release Final]:** Publicar e versionar a release final e estável da aplicação tecnológica.
* **PB48 [Apresentação]:** Elaborar os slides da apresentação final do projeto.
* **PB49 [Apresentação]:** Preparar roteiro de demonstração prática do produto, destacando problema, dados, funcionamento do modelo, mapa de risco, explicabilidade e resultados.
* **PB50 [Apresentação]:** Realizar ensaio da apresentação e da demonstração do produto, ajustando conteúdo e tempo de exposição.
