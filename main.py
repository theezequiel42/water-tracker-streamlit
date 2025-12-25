import os
import re
import unicodedata
from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from dotenv import load_dotenv


def _normalize_text(text: str) -> str:
    """Normaliza texto para comparações flexíveis (sem acentos/maiúsculas)."""
    if not isinstance(text, str):
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip().lower()


MESES_PT = {
    "janeiro": 1,
    "fevereiro": 2,
    "marco": 3,
    "março": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}


def _extrair_mes_ano(label: str) -> tuple[int | None, int | None]:
    tokens = _normalize_text(label).replace("/", " ").split()
    mes_num = next((MESES_PT[token] for token in tokens if token in MESES_PT), None)
    ano = next((int(token) for token in tokens if re.fullmatch(r"\d{4}", token)), None)
    return mes_num, ano


def _preparar_meses(df: pd.DataFrame) -> list[dict]:
    meses_info: dict[str, dict] = {}
    for col in df.columns:
        coluna_limpa = col.strip()
        match_consumo = re.match(r"(?i)^consumo\s+(.*?)\s*(?:\(|$)", coluna_limpa)
        match_valor = re.match(r"(?i)^valor\s+(?!em\s+atraso)(.*?)\s*(?:\(|$)", coluna_limpa)

        if match_consumo:
            label = match_consumo.group(1).strip()
            chave = _normalize_text(label)
            meses_info.setdefault(chave, {"label": label})["consumo_col"] = coluna_limpa

        if match_valor:
            label = match_valor.group(1).strip()
            chave = _normalize_text(label)
            meses_info.setdefault(chave, {"label": label})["valor_col"] = coluna_limpa

    meses_validos: list[dict] = []
    for chave, info in meses_info.items():
        if "consumo_col" not in info or "valor_col" not in info:
            continue
        mes_num, ano = _extrair_mes_ano(info["label"])
        meses_validos.append(
            {
                "key": chave,
                "label": info["label"],
                "consumo_col": info["consumo_col"],
                "valor_col": info["valor_col"],
                "mes_num": mes_num,
                "ano": ano,
            }
        )

    meses_validos.sort(
        key=lambda m: (
            m["ano"] if m["ano"] is not None else 0,
            m["mes_num"] if m["mes_num"] is not None else 0,
            m["label"],
        )
    )
    return meses_validos


def _escolher_mes_padrao(meses_validos: list[dict]) -> str:
    hoje = datetime.now()
    alvo_mes = hoje.month - 1 if hoje.month > 1 else 12
    alvo_ano = hoje.year if hoje.month > 1 else hoje.year - 1

    for mes in meses_validos:
        if mes["mes_num"] == alvo_mes and (mes["ano"] == alvo_ano or mes["ano"] is None):
            return mes["key"]
    return meses_validos[-1]["key"] if meses_validos else ""


def converter_valor(valor) -> float:
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        valor_str = valor.replace("R$", "").replace(".", "").replace(",", ".")
        return float(valor_str) if valor_str.strip() else 0.0
    return 0.0


load_dotenv()
sheet_url = os.getenv("SHEET_URL")

if not sheet_url:
    st.error("Erro: URL da planilha não encontrada. Verifique o arquivo .env.")
    st.stop()

try:
    df = pd.read_csv(sheet_url, dtype=str, header=0)
except Exception as exc:
    st.error(f"Erro ao carregar a planilha: {exc}")
    st.stop()

df.columns = df.columns.str.strip()

if "Nome" not in df.columns:
    st.error("Erro: A coluna 'Nome' não foi encontrada. Verifique o cabeçalho na planilha.")
    st.stop()

coluna_atraso = next((c for c in df.columns if _normalize_text(c).startswith("valor em atraso")), None)
if not coluna_atraso:
    st.warning("Coluna de atraso não encontrada na planilha. Valores em atraso não serão exibidos.")

meses_disponiveis = _preparar_meses(df)
if not meses_disponiveis:
    st.error("Não foi possível identificar colunas de consumo e valor por mês na planilha.")
    st.stop()

# Centralizar o logo
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("images/logo.png", width=200)

st.title("Consulta de Consumo e Pagamento")
st.markdown("**Selecione seu nome e o mês para visualizar o consumo, valor a pagar e o valor em atraso.**")

nomes = df["Nome"].dropna().unique()
usuario_selecionado = st.selectbox("Selecione seu nome", nomes)

padrao_key = _escolher_mes_padrao(meses_disponiveis)
indice_padrao = (
    next((i for i, mes in enumerate(meses_disponiveis) if mes["key"] == padrao_key), 0)
    if meses_disponiveis
    else 0
)
mes_selecionado = st.selectbox(
    "Selecione o mês",
    meses_disponiveis,
    index=indice_padrao,
    format_func=lambda mes: mes["label"],
)


def filtrar_dados(nome: str, mes_info: dict) -> pd.DataFrame:
    colunas = ["Nome"]
    for col in (mes_info["consumo_col"], mes_info["valor_col"], coluna_atraso):
        if col and col in df.columns:
            colunas.append(col)
    return df[df["Nome"] == nome][colunas]


dados_usuario = filtrar_dados(usuario_selecionado, mes_selecionado)

if not dados_usuario.empty:
    linha = dados_usuario.iloc[0]
    consumo = linha.get(mes_selecionado["consumo_col"], "")
    valor = linha.get(mes_selecionado["valor_col"], "")
    valor_atraso = linha.get(coluna_atraso, "Indisponível") if coluna_atraso else "Indisponível"

    try:
        consumo_float = float(consumo)
    except (ValueError, TypeError):
        consumo_float = -1

    if consumo_float < 0:
        st.write("**Consumo:** Indisponível")
    elif consumo_float == 0:
        st.write("**Consumo:** Inferior a 1 m³")
    else:
        st.write(f"**Consumo:** {consumo} m³")

    st.write(f"**Valor a pagar:** {valor}")
    if coluna_atraso:
        st.write(f"**Valor em Atraso:** {valor_atraso}")

    valores = []
    for mes in meses_disponiveis:
        dados_mes = filtrar_dados(usuario_selecionado, mes)
        if dados_mes.empty or mes["valor_col"] not in dados_mes:
            valores.append(0.0)
            continue
        valores.append(converter_valor(dados_mes[mes["valor_col"]].iloc[0]))

    df_plot = pd.DataFrame(
        {
            "Mes": [mes["label"] for mes in meses_disponiveis],
            "Valor": valores,
        }
    )

    chart = (
        alt.Chart(df_plot)
        .mark_bar()
        .encode(
            x=alt.X("Mes:N", sort=None, axis=alt.Axis(labelAngle=-45, title="Meses")),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            tooltip=["Mes", alt.Tooltip("Valor:Q", format=".2f")],
        )
        .properties(title="Valor a Pagar por Mês")
    )

    st.altair_chart(chart, width="stretch")
else:
    st.warning("Nenhum dado encontrado para este usuário e mês selecionados.")
