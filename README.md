# Predição de Risco de Acidentes de Trânsito em Áreas Urbanas

**Disciplina:** Planejamento e Gestão de Projetos (PGP) - Ciência da Computação

**Integrantes:** Matheus de Anhaya Marmett & Guilherme Scortegagna Ribeiro

Projeto proposto pelo docente Fabricio Herpich, responsável por ministrar a disciplina de Planejamento e Gestão de Projetos no curso de graduação em Ciência da Computação pela Universidade Federal da Fronteira Sul (UFFS), Campus Chapecó/SC.

Objetivos do projeto:

* Desenvolver um projeto aplicando Machine Learning para a Segurança Pública Brasileira.
* Conduzir o ciclo de vida de um projeto de ML, de ponta a ponta.
* Entregar uma solução tecnológica completa e publicada.
* Comunicar cientificamente os resultados por meio de um artigo.

---

## 📄 Artigo Científico

O artigo científico completo sobre a predição espaço-temporal de hotspots de acidentes de trânsito em Belo Horizonte utilizando indexação H3, modelos de Machine Learning e a metodologia DSRM está disponível em:

* **Artigo Científico (Word):** [`documentacao/artigo/artigo_hotspots_bh.docx`](documentacao/artigo/artigo_hotspots_bh.docx)
* **Versão editável (Google Docs):** [Acessar documento](https://docs.google.com/document/d/1cSGHn5iTDPIglaVhDRAHO9t2_PpPaSP_CavH2OUc2HY/edit?usp=sharing)

---

## 📦 Releases

Cada sprint entregue tem uma release no GitHub, que aponta para o estado do repositório ao final da sprint. As releases v0.0 a v0.3 foram criadas retroativamente, a partir do último commit de cada sprint.

| Versão | Sprint | Conteúdo principal |
| --- | --- | --- |
| [`v0.0`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.0) | Sprint 0 – Estruturação e iniciação | Project Model Canvas, backlog inicial e estrutura do repositório |
| [`v0.1`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.1) | Sprint 1 – Validação dos dados e exploração | Backlog priorizado e exploração dos dados |
| [`v0.2`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.2) | Sprint 2 – Engenharia de dados e modelo baseline | Primeiro modelo exportado (substituído na v0.4) |
| [`v0.3`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.3) | Sprint 3 – Desenvolvimento e publicação do MVP | Primeira versão do app em Streamlit (reescrito na v0.4) |
| [`v0.4`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.4) | Sprint 4 – Validação, explicabilidade e release intermediária | Modelo sem vazamento de dados, app atualizado e artigo revisado (versão atual) |

Lista completa: [Releases do repositório](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases)

---

## 🚀 Entregáveis do Projeto

### Entregáveis da Sprint 0

* **Project Model Canvas (PMC):** [`documentacao/canvas.md`](documentacao/canvas.md)
* **Product Backlog:** [`documentacao/backlog.md`](documentacao/backlog.md)
* **Quadro Kanban:** [Acessar GitHub Projects](https://github.com/users/matheus-marmett/projects/1)
* **Release:** [`v0.0`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.0)

### Entregáveis da Sprint 1

* **Product Backlog priorizado (Histórias de Usuário):** [`documentacao/backlog.md`](documentacao/backlog.md)
* **Notebook de Exploração:** [`notebooks/01_exploracao_dados.ipynb`](notebooks/01_exploracao_dados.ipynb) · [Google Colab](https://colab.research.google.com/drive/1rqLzvzHPVH2hqNjvK_Y4RLOM6Did7ZQR?usp=sharing)
* **Release:** [`v0.1`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.1)

### Entregáveis da Sprint 2

* **Notebook de Pipeline e Modelagem (H3 + ML):** [`notebooks/02_feature_engineering_e_treinamento.ipynb`](notebooks/02_feature_engineering_e_treinamento.ipynb) · [Google Colab](https://colab.research.google.com/drive/14jam3dvSFaVjhnrpr-RLYCx8IZuLfFgT?usp=sharing)
* **Atualizações no Quadro Kanban:** [Acessar GitHub Projects](https://github.com/users/matheus-marmett/projects/1)
* **Atualizações do Artigo Científico:** [Google Docs](https://docs.google.com/document/d/1cSGHn5iTDPIglaVhDRAHO9t2_PpPaSP_CavH2OUc2HY/edit?usp=sharing)
* **Modelo Treinado Exportado (`.joblib`):** [`codigo_fonte/modelos/`](codigo_fonte/modelos/)
* **Release:** [`v0.2`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.2)

### Entregáveis da Sprint 3

* **Aplicação Web (Streamlit Cloud - MVP público):** [Acessar Solução Web](https://pgp-predicao-acidentes-transito.streamlit.app/)
* **Código Fonte da Aplicação:** [`codigo_fonte/visualizacao/app.py`](codigo_fonte/visualizacao/app.py)
* **Especificação de Dependências:** [`requirements.txt`](requirements.txt)
* **Quadro Kanban Final:** [Acessar GitHub Projects](https://github.com/users/matheus-marmett/projects/1)
* **Release:** [`v0.3`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.3)

### Entregáveis da Sprint 4

* **Notebook de Modelagem Preditiva (H3 + ML + LIME):** [`notebooks/03_modelagem_preditiva.ipynb`](notebooks/03_modelagem_preditiva.ipynb) · [Google Colab](https://colab.research.google.com/drive/1Gw0L65qX25j-XYbZM3rCbA10mPib-Nxy?usp=sharing) Pipeline refeito sem vazamento de dados: recorte pelo limite oficial de Belo Horizonte, alvo P90 recalculado a cada mês, 15 atributos calculados só com meses anteriores, divisão temporal (treino até 2024, teste em 2025), comparação com heurísticas de referência, importância por permutação e LIME.
* **Modelo atualizado e metadados:** [`codigo_fonte/modelos/`](codigo_fonte/modelos/). Regressão Logística, melhor PR-AUC no teste (0,9106).
* **MVP atualizado (Streamlit Cloud):** [Acessar Solução Web](https://pgp-predicao-acidentes-transito.streamlit.app/). Mapa de risco dos 462 hexágonos de BH, filtros por risco e bairro, ranking exportável, histórico mensal e fatores da previsão de cada hexágono.
* **Release (intermediária):** [`v0.4`](https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas/releases/tag/v0.4)
* **Artigo Científico atualizado (Resultados, Discussão e Limitações):** [Google Docs](https://docs.google.com/document/d/1cSGHn5iTDPIglaVhDRAHO9t2_PpPaSP_CavH2OUc2HY/edit?usp=sharing) · [`documentacao/artigo/artigo_hotspots_bh.docx`](documentacao/artigo/artigo_hotspots_bh.docx)
* **Quadro Kanban:** [Acessar GitHub Projects](https://github.com/users/matheus-marmett/projects/1)

---

## 🧠 Pipeline de Dados e Modelo

O pipeline atual está em [`notebooks/03_modelagem_preditiva.ipynb`](notebooks/03_modelagem_preditiva.ipynb) e roda no Google Colab:

1. **Limpeza:** registros do RENAEST dentro do limite oficial de Belo Horizonte ([`dados/limite_bh.geojson`](dados/limite_bh.geojson), malha IBGE), sem duplicatas e restritos aos meses com cobertura regular.
2. **Indexação espacial:** cada acidente é associado a um hexágono Uber H3 de resolução 8 (~0,74 km²).
3. **Alvo:** um hexágono é *hotspot* no mês quando seu número de acidentes está no percentil 90 entre os hexágonos de BH naquele mês.
4. **Atributos:** apenas informações de meses anteriores (histórico de acidentes, frequência como hotspot, óbitos, perfil horário, vizinhança e sazonalidade).
5. **Validação temporal:** treino nos meses até 2024 e teste em 2025, com comparação contra heurísticas simples e explicabilidade com LIME.

O notebook gera os arquivos consumidos pelo app:

| Arquivo | Conteúdo |
| --- | --- |
| `codigo_fonte/modelos/modelo_hotspot_bh_h3.joblib` | Modelo treinado (pipeline scikit-learn) |
| `codigo_fonte/modelos/metadados_modelo.json` | Atributos, período, configurações e métricas de teste |
| `codigo_fonte/dados/hexagonos_bh.csv` | Atributos de cada hexágono para a previsão do mês seguinte |
| `codigo_fonte/dados/historico_mensal_bh.csv` | Acidentes, óbitos e rótulo de hotspot por hexágono e mês |

Para atualizar o modelo com dados novos, rode o notebook 03 e substitua esses quatro arquivos.

---

## 🛠️ Como Executar a Aplicação Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/matheus-marmett/PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas.git
   cd PGP-Predicao-de-Risco-de-Acidentes-de-Transito-em-areas-Urbanas
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o servidor Streamlit:
   ```bash
   streamlit run codigo_fonte/visualizacao/app.py
   ```
