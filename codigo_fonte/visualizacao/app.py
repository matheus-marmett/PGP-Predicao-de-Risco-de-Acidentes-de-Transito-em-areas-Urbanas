import os
import joblib
import pandas as pd
import pydeck as pdk
import streamlit as st

# 1. Configuração da página
st.set_page_config(
    page_title="Predição de Hotspots de Acidentes - BH",
    page_icon="🚦",
    layout="wide"
)

# 2. Carregamento do Modelo e dos Dados Geográficos
@st.cache_resource
def load_model():
    model_path = os.path.join(
        os.path.dirname(__file__), '..', 'modelos', 'modelo_hotspot_bh_h3.joblib'
    )
    return joblib.load(model_path)

@st.cache_data
def load_h3_data():
    data_path = os.path.join(
        os.path.dirname(__file__), '..', 'dados', 'hexagones_bh.csv'
    )
    # Exemplo: se o arquivo não existir localmente para teste, gera um mockup
    if not os.path.exists(data_path):
        return pd.DataFrame([
            {
                'h3_index': '88a2a10d29fffff', 'bairro': 'Centro',
                'lat': -19.9191, 'lng': -43.9386,
                'total_graves': 4, 'total_obitos': 0, 'ocorrencias_pico': 8,
                'ocorrencias_noturnas': 3, 'ocorrencias_fds': 2, 'total_ocorrencias': 15
            },
            {
                'h3_index': '88a2a10d21fffff', 'bairro': 'Savassi',
                'lat': -19.9332, 'lng': -43.9351,
                'total_graves': 1, 'total_obitos': 0, 'ocorrencias_pico': 3,
                'ocorrencias_noturnas': 5, 'ocorrencias_fds': 4, 'total_ocorrencias': 11
            }
        ])
    return pd.read_csv(data_path)

try:
    model = load_model()
    df_h3 = load_h3_data()
except Exception as e:
    st.error(f"Erro ao carregar arquivos: {e}")
    st.stop()

# 3. Título e Descrição
st.title("🚦 Predição Espaço-Temporal de Hotspots em Belo Horizonte")
st.markdown("Selecione um local ou hexágono H3 para analisar a probabilidade de risco de acidentes.")

# 4. Filtros de Localização na Sidebar
st.sidebar.header("📍 Seleção da Localização")

# Opção de busca por Bairro ou Hexágono H3
modo_selecao = st.sidebar.radio("Buscar por:", ["Bairro / Região", "Código H3"])

if modo_selecao == "Bairro / Região" and 'bairro' in df_h3.columns:
    bairro_selecionado = st.sidebar.selectbox("Escolha o Bairro:", df_h3['bairro'].unique())
    hex_info = df_h3[df_h3['bairro'] == bairro_selecionado].iloc[0]
else:
    h3_selecionado = st.sidebar.selectbox("Escolha o Hexágono H3:", df_h3['h3_index'].unique())
    hex_info = df_h3[df_h3['h3_index'] == h3_selecionado].iloc[0]

# Preenchimento automático dos atributos baseados na localização escolhida
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Estatísticas da Região Selecionada")
st.sidebar.text(f"Feridos/Graves: {hex_info['total_graves']}")
st.sidebar.text(f"Óbitos: {hex_info['total_obitos']}")
st.sidebar.text(f"Pico: {hex_info['ocorrencias_pico']}")
st.sidebar.text(f"Noturnas: {hex_info['ocorrencias_noturnas']}")
st.sidebar.text(f"Fim de Semana: {hex_info['ocorrencias_fds']}")
st.sidebar.text(f"Total Ocorrências: {hex_info['total_ocorrencias']}")

# 5. Predição
features_esperadas = list(model.feature_names_in_) if hasattr(model, "feature_names_in_") else [
    'total_graves', 'total_obitos', 'ocorrencias_pico', 
    'ocorrencias_noturnas', 'ocorrencias_fds', 'total_ocorrencias'
]

input_data = pd.DataFrame([hex_info.to_dict()])[features_esperadas]

prediction = model.predict(input_data)[0]
proba = model.predict_proba(input_data)[0][1] if hasattr(model, "predict_proba") else 0.0

# 6. Exibição dos Resultados e do Mapa
col_metricas, col_mapa = st.columns([1, 2])

with col_metricas:
    st.subheader("Resultado da Análise")
    if prediction == 1:
        st.error(f"⚠️ **HOTSPOT (ALTO RISCO)**\n\nA região do **{hex_info.get('bairro', hex_info['h3_index'])}** foi classificada como zona de atenção crítica.")
    else:
        st.success(f"✅ **BAIXO RISCO**\n\nA região do **{hex_info.get('bairro', hex_info['h3_index'])}** está fora da zona de maior criticidade.")
    
    st.metric(label="Probabilidade de Risco", value=f"{proba * 100:.2f}%")

with col_mapa:
    st.subheader("Visualização Geográfica")
    
    # Definir cor do marcador (Vermelho para Hotspot, Verde para Baixo Risco)
    cor_rgba = [230, 57, 70, 200] if prediction == 1 else [42, 157, 143, 200]
    
    # Adicionar cor ao DataFrame do ponto selecionado
    df_ponto = pd.DataFrame([{
        'lat': hex_info['lat'],
        'lng': hex_info['lng'],
        'bairro': hex_info.get('bairro', hex_info['h3_index']),
        'cor': cor_rgba
    }])

    # Camada no PyDeck
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_ponto,
        get_position=["lng", "lat"],
        get_color="cor",
        get_radius=300,
        pickable=True
    )

    # Estado da Câmera (centralizado no ponto selecionado)
    view_state = pdk.ViewState(
        latitude=hex_info['lat'],
        longitude=hex_info['lng'],
        zoom=14,
        pitch=40
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Região: {bairro}"}
    ))