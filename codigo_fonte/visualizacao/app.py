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

# 3. Título e Descrição
st.title("🚦 Predição Espaço-Temporal de Hotspots em Belo Horizonte")
st.markdown("""
Esta aplicação utiliza aprendizado de máquina (LightGBM) e indexação hexagonal Uber H3 
para identificar zonas de alto risco de acidentes de trânsito em Belo Horizonte.
""")

# 4. Formulário de Entradas (Sidebar)
st.sidebar.header("Parâmetros da Região / Período")

total_graves = st.sidebar.number_input("Total de Feridos/Graves", min_value=0, value=1)
total_obitos = st.sidebar.number_input("Total de Óbitos", min_value=0, value=0)
ocorrencias_pico = st.sidebar.number_input("Ocorrências em Horário de Pico", min_value=0, value=2)
ocorrencias_noturnas = st.sidebar.number_input("Ocorrências Noturnas", min_value=0, value=1)
ocorrencias_fds = st.sidebar.number_input("Ocorrências no Fim de Semana", min_value=0, value=0)

# 5. Botão de Predição
if st.sidebar.button("Prever Risco"):
    # Organizar dados de entrada no formato esperado pelo modelo
    input_data = pd.DataFrame([{
        'total_graves': total_graves,
        'total_obitos': total_obitos,
        'ocorrencias_pico': ocorrencias_pico,
        'ocorrencias_noturnas': ocorrencias_noturnas,
        'ocorrencias_fds': ocorrencias_fds
        # ATENÇÃO: Garanta que todas as colunas do seu treinamento (ex: variáveis seno/cosseno)
        # estejam incluídas aqui na exata ordem em que o modelo foi treinado.
    }])

    # Predição e Probabilidade
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0][1]

    # Exibição do Resultado
    st.subheader("Resultado da Análise")
    col1, col2 = st.columns(2)

    with col1:
        if prediction == 1:
            st.error("⚠️ **ÁREA CLASSIFICADA COMO HOTSPOT (ALTO RISCO)**")
        else:
            st.success("✅ **ÁREA FORA DE HOTSPOT (BAIXO RISCO)**")

    with col2:
        st.metric(label="Probabilidade de ser Hotspot", value=f"{proba * 100:.2f}%")