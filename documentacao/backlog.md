# Product Backlog - Predição de Risco de Acidentes de Trânsito em áreas urbanas

Este documento apresenta o backlog priorizado do projeto, dividido ao longo das 6 Sprints do ciclo de vida.

---

## Sprint 0: Estruturação e Iniciação (Concluído)
* **PB01 [Gestão]:** Elaborar e validar o Project Model Canvas (PMC).
* **PB02 [DevOps]:** Criar repositório no GitHub com estrutura de pastas padronizada (`dados`, `codigo_fonte`, `documentacao`, `notebooks`).
* **PB03 [Gestão]:** Configurar o quadro Kanban no GitHub Projects e mapear o Product Backlog inicial.

---

## Sprint 1: Validação de Dados e Exploração
* **PB04 [Dados]:** Coletar dados brutos de acidentes urbanos (PRF/Portais Municipais), dados meteorológicos (INMET) e malha viária (OpenStreetMap via OSMnx).
* **PB05 [Dados]:** Implementar rotinas de limpeza, remoção de duplicatas e tratamento de dados nulos.
* **PB06 [Geoprocessamento]:** Aplicar a discretização geográfica em hexágonos usando a biblioteca Uber H3.
* **PB07 [Análise]:** Criar caderno Jupyter de Análise Exploratória de Dados (EDA) com gráficos estatísticos e espaciais.
* **PB08 [Gestão]:** Refinar e detalhar o Product Backlog com base nos aprendizados da exploração.

---

## Sprint 2: Modelo Baseline e Prova de Conceito
* **PB09 [Engenharia]:** Criar variáveis espaço-temporais (faixa horária, dia da semana, densidade viária, histórico de ocorrências por hexágono).
* **PB10 [ML]:** Aplicar estratégia de validação cruzada espacial/temporal para evitar vazamento de dados.
* **PB11 [ML]:** Treinar modelos *baseline* de Aprendizado de Máquina (Classificação de Risco com XGBoost / Random Forest).
* **PB12 [ML]:** Calcular métricas de avaliação adequadas a dados desbalanceados (Precision-Recall AUC, F1-Score, Matriz de Confusão).
* **PB13 [DevOps]:** Versionar scripts e artefatos do modelo treinado no repositório.

---

## Sprint 3: Desenvolvendo e Publicando o MVP
* **PB14 [Backend]:** Mapear script de inferência para receber coordenadas/datas e retornar o nível de risco.
* **PB15 [Frontend]:** Desenvolver interface web interativa utilizando **Streamlit** e mapas com Folium/PyDeck.
* **PB16 [Deploy]:** Publicar a primeira versão funcional (MVP) da aplicação na plataforma **Streamlit Community Cloud**.
* **PB17 [UX/UI]:** Garantir facilidade de uso do painel para navegação e visualização dos mapas de calor.

---

## Sprint 4: Release Intermediária e Ajustes
* **PB18 [Feedback]:** Coletar impressões de uso da aplicação e mapear pontos de melhoria no painel.
* **PB19 [Explicabilidade]:** Integrar **SHAP (SHapley Additive exPlanations)** para apresentar os principais fatores de risco no painel.
* **PB20 [Otimização]:** Refinar o modelo de ML e otimizar o tempo de carregamento dos mapas interativos.
* **PB21 [Release]:** Lançar a nova versão da aplicação com correções e novas funcionalidades ativas.

---

## Sprint 5: Consolidação, Artigo Científico e Apresentação
* **PB22 [Artigo]:** Redigir Introdução, Trabalhos Relacionados e Metodologia no template oficial da SBC (LaTeX/Overleaf).
* **PB23 [Artigo]:** Inserir seção de Resultados, Discussão (SHAP/Mapas de risco) e Considerações Finais.
* **PB24 [Release Final]:** Publicar a versão final e estável da aplicação tecnológica.
* **PB25 [Apresentação]:** Elaborar slides e preparar a demonstração prática do produto final para a banca/disciplina de PGP.
