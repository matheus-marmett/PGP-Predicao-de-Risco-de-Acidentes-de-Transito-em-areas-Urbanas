import os
import joblib
import pandas as pd
import streamlit as st

# 1. Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Predição de Hotspots de Acidentes - BH",
    page_icon="🚦",
    layout="wide"
)

# 2. Carregamento do modelo
@st.cache_resource
def load_model():
    model_path = os.path.join(
        os.path.dirname(__file__), '..', 'modelos', 'modelo_hotspot_bh_h3.joblib'
    )
    return joblib.load(model_path)


# Chamada da função para carregar o modelo na variável global 'model'
try:
    model = load_model()
except Exception as e:
    st.error(f"Erro ao carregar o modelo de Machine Learning: {e}")
    st.stop()

# 3. Diagnóstico Automático das Features Esperadas pelo Modelo
features_esperadas = None
if hasattr(model, "feature_names_in_"):
    features_esperadas = list(model.feature_names_in_)
elif hasattr(model, "named_steps"):  # Caso o modelo seja um Pipeline do Scikit-Learn
    first_step = list(model.named_steps.values())[0]
    if hasattr(first_step, "feature_names_in_"):
        features_esperadas = list(first_step.feature_names_in_)

# 4. Título e Descrição
st.title("🚦 Predição Espaço-Temporal de Hotspots em Belo Horizonte")
st.markdown("""
Esta aplicação utiliza aprendizado de máquina e indexação hexagonal Uber H3 
para identificar zonas de alto risco de acidentes de trânsito em Belo Horizonte.
""")

# 5. Formulário de Entradas (Sidebar)
st.sidebar.header("Parâmetros da Região / Período")

# Exibe na sidebar quais são as colunas que o modelo exige
if features_esperadas:
    st.sidebar.info(f"🔍 **Colunas identificadas no modelo ({len(features_esperadas)}):**\n\n`{features_esperadas}`")

total_graves = st.sidebar.number_input("Total de Feridos/Graves", min_value=0, value=1)
total_obitos = st.sidebar.number_input("Total de Óbitos", min_value=0, value=0)
ocorrencias_pico = st.sidebar.number_input("Ocorrências em Horário de Pico", min_value=0, value=2)
ocorrencias_noturnas = st.sidebar.number_input("Ocorrências Noturnas", min_value=0, value=1)
ocorrencias_fds = st.sidebar.number_input("Ocorrências no Fim de Semana", min_value=0, value=0)
total_ocorrencias = st.sidebar.number_input("Total Geral de Ocorrências", min_value=0, value=3)

# 6. Botão de Predição
if st.sidebar.button("Prever Risco"):
    # Dicionário contendo os valores informados no formulário
    dados_usuario = {
        'total_graves': total_graves,
        'total_obitos': total_obitos,
        'ocorrencias_pico': ocorrencias_pico,
        'ocorrencias_noturnas': ocorrencias_noturnas,
        'ocorrencias_fds': ocorrencias_fds,
        'total_ocorrencias': total_ocorrencias,
        'total_acidentes': total_ocorrencias  # Alias para compatibilidade de nome
    }

    # Se identificamos os nomes exatos das colunas do treino, garantimos a ordem e seleção correta
    if features_esperadas:
        try:
            input_data = pd.DataFrame([dados_usuario])[features_esperadas]
        except KeyError as missing_col:
            st.error(f"⚠️ O modelo requer a coluna {missing_col}, que não está mapeada no formulário.")
            st.stop()
    else:
        # Fallback: ordem padrão caso o modelo não armazene os nomes explicitamente
        input_data = pd.DataFrame([{
            'total_graves': total_graves,
            'total_obitos': total_obitos,
            'ocorrencias_pico': ocorrencias_pico,
            'ocorrencias_noturnas': ocorrencias_noturnas,
            'ocorrencias_fds': ocorrencias_fds,
            'total_ocorrencias': total_ocorrencias
        }])

    # Predição e Probabilidade
    prediction = model.predict(input_data)[0]
    
    # Verificação de suporte a probabilidades
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_data)[0][1]
    else:
        proba = None

    # Exibição do Resultado
    st.subheader("Resultado da Análise")
    col1, col2 = st.columns(2)

    with col1:
        if prediction == 1:
            st.error("⚠️ **ÁREA CLASSIFICADA COMO HOTSPOT (ALTO RISCO)**")
        else:
            st.success("✅ **ÁREA FORA DE HOTSPOT (BAIXO RISCO)**")

    with col2:
        if proba is not None:
            st.metric(label="Probabilidade de ser Hotspot", value=f"{proba * 100:.2f}%")