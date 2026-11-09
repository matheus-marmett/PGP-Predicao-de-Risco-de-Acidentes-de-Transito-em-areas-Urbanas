"""
Predição Espaço-Temporal de Hotspots de Acidentes de Trânsito em Belo Horizonte.

MVP em Streamlit que consome o modelo treinado no notebook
`notebooks/03_modelagem_preditiva.ipynb` e mostra, para cada hexágono H3
(resolução 8) do município, o risco previsto de ele estar entre os 10%
com mais acidentes de BH no mês seguinte ao último mês com dados.
"""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Predição de Hotspots de Acidentes - BH",
    page_icon="🚦",
    layout="wide",
)

BASE = Path(__file__).resolve().parent.parent
ARQ_MODELO = BASE / "modelos" / "modelo_hotspot_bh_h3.joblib"
ARQ_META = BASE / "modelos" / "metadados_modelo.json"
ARQ_HEX = BASE / "dados" / "hexagonos_bh.csv"
ARQ_HIST = BASE / "dados" / "historico_mensal_bh.csv"

CENTRO_BH = {"latitude": -19.92, "longitude": -43.95}

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

NOMES_ATRIBUTOS = {
    "acid_lag1": "Acidentes no mês anterior",
    "acid_media_3m": "Média de acidentes (3 meses)",
    "acid_media_6m": "Média de acidentes (6 meses)",
    "acid_media_12m": "Média de acidentes (12 meses)",
    "acid_tendencia": "Tendência (média 3m − média 12m)",
    "hotspot_lag1": "Foi hotspot no mês anterior",
    "hotspot_freq_12m": "Frequência como hotspot (12 meses)",
    "obitos_12m": "Óbitos (12 meses)",
    "envolvidos_por_acid_12m": "Envolvidos por acidente (12 meses)",
    "prop_pico_12m": "Proporção em horário de pico (12 meses)",
    "prop_noturnas_12m": "Proporção noturna (12 meses)",
    "prop_fds_12m": "Proporção no fim de semana (12 meses)",
    "vizinhos_media_3m": "Média dos hexágonos vizinhos (3 meses)",
    "mes_sin": "Sazonalidade do mês (seno)",
    "mes_cos": "Sazonalidade do mês (cosseno)",
}


def mes_por_extenso(periodo: str) -> str:
    ano, mes = periodo.split("-")
    return f"{MESES[int(mes) - 1]} de {ano}"


def cor_risco(p: float) -> list[int]:
    """Verde (baixo) → amarelo → vermelho (alto)."""
    verde, amarelo, vermelho = np.array([42, 157, 143]), np.array([233, 196, 106]), np.array([230, 57, 70])
    if p < 0.5:
        rgb = verde + (amarelo - verde) * (p / 0.5)
    else:
        rgb = amarelo + (vermelho - amarelo) * ((p - 0.5) / 0.5)
    return [int(v) for v in rgb] + [170]


# ---------------------------------------------------------------------------
# Carregamento
# ---------------------------------------------------------------------------
@st.cache_resource
def carregar_modelo():
    try:
        return joblib.load(ARQ_MODELO), None
    except Exception as erro:  # versão de biblioteca incompatível, arquivo ausente etc.
        return None, erro


@st.cache_data
def carregar_metadados() -> dict:
    with open(ARQ_META, encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def carregar_hexagonos() -> pd.DataFrame:
    return pd.read_csv(ARQ_HEX)


@st.cache_data
def carregar_historico() -> pd.DataFrame:
    hist = pd.read_csv(ARQ_HIST)
    limiar = hist.groupby("periodo")["acidentes"].quantile(0.90).rename("limiar_p90")
    return hist.merge(limiar, left_on="periodo", right_index=True)


try:
    meta = carregar_metadados()
    hexagonos = carregar_hexagonos()
    historico = carregar_historico()
except FileNotFoundError as erro:
    st.error(f"Arquivo de dados não encontrado: {erro.filename}")
    st.stop()

FEATURES = meta["features"]
LIMIAR = meta.get("limiar_decisao", 0.5)
modelo, erro_modelo = carregar_modelo()

if modelo is not None:
    hexagonos["probabilidade"] = modelo.predict_proba(hexagonos[FEATURES])[:, 1]
    hexagonos["previsao_hotspot"] = (hexagonos["probabilidade"] >= LIMIAR).astype(int)
    hexagonos["ranking_risco"] = hexagonos["probabilidade"].rank(ascending=False, method="min").astype(int)

hexagonos["rotulo"] = hexagonos.apply(
    lambda r: f"#{r['ranking_risco']} · {r['bairro'].title()} · {r['h3']}", axis=1
)
hexagonos = hexagonos.sort_values("ranking_risco").reset_index(drop=True)

# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
mes_alvo = mes_por_extenso(meta["mes_previsto"])
inicio, fim = meta["periodo_dados"]

st.title("🚦 Predição de Hotspots de Acidentes em Belo Horizonte")
st.markdown(
    f"Risco previsto para **{mes_alvo}** de cada hexágono H3 (~0,74 km²) estar entre os "
    f"**10% com mais acidentes** da cidade. Modelo: **{meta['modelo']}**, treinado com dados do "
    f"RENAEST de {mes_por_extenso(inicio)} a {mes_por_extenso(fim)}."
)

if erro_modelo is not None:
    st.warning(
        "O modelo não pôde ser carregado neste ambiente; exibindo as probabilidades "
        f"pré-calculadas no notebook. Detalhe técnico: `{erro_modelo}`"
    )

n_hot = int(hexagonos["previsao_hotspot"].sum())
topo = hexagonos.iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Hexágonos analisados", f"{len(hexagonos):,}".replace(",", "."))
c2.metric("Hotspots previstos", n_hot, help=f"Hexágonos com risco ≥ {LIMIAR:.0%}")
c3.metric("Maior risco", topo["bairro"].title(), help=f"Hexágono {topo['h3']}")
c4.metric("Acidentes na base", f"{meta['n_acidentes']:,}".replace(",", "."))

# ---------------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------------
st.sidebar.header("🔎 Filtros do mapa")
risco_min = st.sidebar.slider("Risco mínimo", 0.0, 1.0, 0.0, 0.05, format="%.2f")
somente_hotspots = st.sidebar.checkbox("Mostrar só hotspots previstos")
bairros = st.sidebar.multiselect(
    "Bairros", sorted(hexagonos["bairro"].unique()),
    help="Bairro mais frequente nos registros de acidentes de cada hexágono.",
)

filtrado = hexagonos[hexagonos["probabilidade"] >= risco_min]
if somente_hotspots:
    filtrado = filtrado[filtrado["previsao_hotspot"] == 1]
if bairros:
    filtrado = filtrado[filtrado["bairro"].isin(bairros)]

st.sidebar.header("📍 Hexágono em destaque")
opcoes = filtrado["rotulo"].tolist() or hexagonos["rotulo"].tolist()
rotulo_sel = st.sidebar.selectbox("Escolha um hexágono (ordenado por risco)", opcoes)
selecionado = hexagonos[hexagonos["rotulo"] == rotulo_sel].iloc[0]

st.sidebar.caption(f"{len(filtrado)} de {len(hexagonos)} hexágonos atendem aos filtros.")

# ---------------------------------------------------------------------------
# Abas
# ---------------------------------------------------------------------------
aba_mapa, aba_ranking, aba_hex, aba_modelo = st.tabs(
    ["🗺️ Mapa de risco", "📊 Ranking", "📈 Hexágono em destaque", "ℹ️ Sobre o modelo"]
)

with aba_mapa:
    dados_mapa = filtrado.assign(
        cor=filtrado["probabilidade"].apply(cor_risco),
        risco_txt=(filtrado["probabilidade"] * 100).round(1).astype(str) + "%",
        media_txt=filtrado["acid_media_3m"].round(1).astype(str),
    )[["h3", "bairro", "cor", "risco_txt", "media_txt", "ranking_risco"]]

    camadas = [
        pdk.Layer(
            "H3HexagonLayer",
            data=dados_mapa,
            get_hexagon="h3",
            get_fill_color="cor",
            get_line_color=[255, 255, 255, 120],
            line_width_min_pixels=1,
            stroked=True,
            filled=True,
            extruded=False,
            pickable=True,
        ),
        pdk.Layer(
            "H3HexagonLayer",
            data=pd.DataFrame([{"h3": selecionado["h3"]}]),
            get_hexagon="h3",
            filled=False,
            stroked=True,
            get_line_color=[20, 20, 20, 255],
            line_width_min_pixels=3,
        ),
    ]
    st.pydeck_chart(
        pdk.Deck(
            layers=camadas,
            initial_view_state=pdk.ViewState(**CENTRO_BH, zoom=10.8, pitch=0),
            tooltip={
                "html": "<b>{bairro}</b><br/>Risco: {risco_txt}<br/>Ranking: #{ranking_risco}"
                        "<br/>Média 3 meses: {media_txt} acidentes",
            },
        ),
    )
    st.caption(
        "Cores: verde = risco baixo, amarelo = intermediário, vermelho = alto. "
        "O contorno preto marca o hexágono em destaque na barra lateral."
    )

with aba_ranking:
    st.subheader(f"Hexágonos com maior risco previsto para {mes_alvo}")
    n_linhas = len(filtrado)
    if n_linhas > 10:
        n_linhas = st.slider("Quantidade de hexágonos", 10, n_linhas, min(20, n_linhas))
    tabela = filtrado.head(n_linhas)[
        ["ranking_risco", "bairro", "h3", "probabilidade", "acid_lag1", "acid_media_3m", "hotspot_freq_12m"]
    ].assign(hotspot_freq_12m=lambda d: d["hotspot_freq_12m"] * 100)
    st.dataframe(
        tabela,
        hide_index=True,
        column_config={
            "ranking_risco": st.column_config.NumberColumn("Ranking"),
            "bairro": "Bairro",
            "h3": "Hexágono H3",
            "probabilidade": st.column_config.ProgressColumn("Risco", min_value=0.0, max_value=1.0, format="%.2f"),
            "acid_lag1": st.column_config.NumberColumn("Acidentes no último mês", format="%d"),
            "acid_media_3m": st.column_config.NumberColumn("Média 3 meses", format="%.1f"),
            "hotspot_freq_12m": st.column_config.NumberColumn("Hotspot nos últimos 12 meses", format="%.0f%%"),
        },
    )
    st.download_button(
        "Baixar ranking completo (CSV)",
        filtrado[["ranking_risco", "bairro", "h3", "lat", "lng", "probabilidade", "previsao_hotspot"]]
        .to_csv(index=False).encode("utf-8"),
        file_name=f"ranking_hotspots_bh_{meta['mes_previsto']}.csv",
        mime="text/csv",
    )

with aba_hex:
    st.subheader(f"{selecionado['bairro'].title()} — hexágono {selecionado['h3']}")
    risco = float(selecionado["probabilidade"])
    if selecionado["previsao_hotspot"] == 1:
        st.error(f"⚠️ **Hotspot previsto** para {mes_alvo} — risco {risco:.1%} (#{selecionado['ranking_risco']} de {len(hexagonos)})")
    else:
        st.success(f"✅ **Fora da zona de maior criticidade** em {mes_alvo} — risco {risco:.1%} (#{selecionado['ranking_risco']} de {len(hexagonos)})")

    serie = historico[historico["h3"] == selecionado["h3"]]
    m1, m2, m3 = st.columns(3)
    m1.metric("Acidentes no período", f"{int(serie['acidentes'].sum()):,}".replace(",", "."))
    m2.metric("Óbitos no período", int(serie["obitos"].sum()))
    m3.metric("Meses como hotspot", f"{int(serie['is_hotspot'].sum())} de {len(serie)}")

    st.markdown("**Acidentes por mês no hexágono × limiar de hotspot da cidade (P90)**")
    st.line_chart(
        serie.set_index("periodo")[["acidentes", "limiar_p90"]]
        .rename(columns={"acidentes": "Acidentes no hexágono", "limiar_p90": "Limiar P90 de BH"})
    )

    st.markdown("**Fatores considerados na previsão**")
    valores = selecionado[FEATURES].astype(float)
    contribuicoes = None
    if modelo is not None and hasattr(modelo, "steps"):
        estimador = modelo.steps[-1][1]
        if hasattr(estimador, "coef_"):
            x = modelo[:-1].transform(pd.DataFrame([valores], columns=FEATURES))[0]
            contribuicoes = pd.Series(estimador.coef_[0] * x, index=FEATURES)

    tabela_fatores = pd.DataFrame({
        "Atributo": [NOMES_ATRIBUTOS.get(f, f) for f in FEATURES],
        "Valor": valores.round(3).values,
    })
    if contribuicoes is not None:
        tabela_fatores["Peso na decisão"] = contribuicoes.round(3).values
        tabela_fatores = tabela_fatores.reindex(
            tabela_fatores["Peso na decisão"].abs().sort_values(ascending=False).index
        )
        st.caption(
            "Peso na decisão = coeficiente do modelo × valor padronizado do atributo. "
            "Valores positivos aumentam o risco; negativos reduzem."
        )
    st.dataframe(tabela_fatores, hide_index=True)

with aba_modelo:
    st.subheader("Como a previsão é feita")
    st.markdown(
        f"""
- **Unidade de análise:** hexágono H3 de resolução {meta['resolucao_h3']} × mês ({meta['n_hexagonos']} hexágonos cobrindo o município).
- **Hotspot:** hexágono cujo número de acidentes no mês está no **percentil {int(meta['percentil_hotspot'] * 100)}** entre os hexágonos de BH naquele mês.
- **Atributos:** somente informações de meses **anteriores** ao mês previsto — histórico de acidentes, frequência como hotspot, óbitos, perfil horário, vizinhança e sazonalidade.
- **Validação:** treino nos meses até {mes_por_extenso(str(pd.Period(meta['inicio_teste'], 'M') - 1))} e teste nos meses a partir de {mes_por_extenso(meta['inicio_teste'])}, simulando o uso real.
- **Hotspot previsto:** risco ≥ {LIMIAR:.0%}.
        """
    )

    st.subheader("Desempenho no conjunto de teste")
    metricas = pd.DataFrame(meta["metricas_teste"]).set_index("Modelo").sort_values("PR-AUC", ascending=False)
    st.dataframe(
        metricas,
        column_config={c: st.column_config.NumberColumn(c, format="%.4f") for c in metricas.columns},
    )
    st.caption(
        "As heurísticas são referências simples sem aprendizado de máquina. "
        "PR-AUC foi o critério de escolha do modelo por ser adequado a classes desbalanceadas."
    )

    st.subheader("Limitações")
    st.markdown(
        """
- O treino usa subamostragem da classe majoritária, o que eleva os valores de risco: eles servem para **ordenar** os hexágonos, não como probabilidade calibrada.
- A cobertura do RENAEST em BH cresce ao longo do período; meses mais recentes têm mais registros.
- A base não distingue feridos de ilesos; a severidade considerada é a ocorrência de óbitos.
        """
    )
    st.caption("Projeto acadêmico — Planejamento e Gestão de Projetos, Ciência da Computação, UFFS.")
