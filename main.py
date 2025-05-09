import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter a URL segura da planilha do Google Sheets
sheet_url = os.getenv("SHEET_URL")

# Garantir que a URL foi carregada corretamente
if not sheet_url:
    st.error("Erro: URL da planilha não encontrada. Verifique o arquivo .env")
    st.stop()

# Carregar os dados diretamente do Google Sheets com o cabeçalho correto
df = pd.read_csv(sheet_url, dtype=str, header=0)  # header=0 garante que a primeira linha é o cabeçalho

# Remover espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Verificar se a coluna "Nome" realmente existe após a limpeza
if "Nome" not in df.columns:
    st.error("Erro: A coluna 'Nome' ainda não foi encontrada após a limpeza. Verifique o cabeçalho na planilha!")
    st.stop()

# Centralizar o logo
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("images/logo.png", width=200)

# Adicionar título e descrição
st.title("Consulta de Consumo e Pagamento")
st.markdown("**Selecione seu nome e o mês para visualizar o consumo, valor a pagar e o valor em atraso.**")

# Listar os meses para seleção
meses = [
    'Janeiro 2025', 'Fevereiro 2025', 'Março 2025',
    'Abril 2025', 'Maio 2025', 'Junho 2025', 'Julho 2025', 'Agosto 2025',
    'Setembro 2025', 'Outubro 2025', 'Novembro 2025', 'Dezembro 2025'
]

# Determinar o mês anterior ao atual
mes_atual = datetime.now().month
mes_anterior = mes_atual - 1 if mes_atual > 1 else 12  # Se for janeiro, retorna dezembro
mes_selecionado_padrao = meses[mes_anterior - 1]  # Índice começa em 0

# Listar os nomes dos usuários
nomes = df['Nome'].unique()
usuario_selecionado = st.selectbox("Selecione seu nome", nomes)

# Seleção do mês, com o mês anterior ao atual como padrão
mes_selecionado = st.selectbox("Selecione o mês", meses, index=mes_anterior - 1)

# Função para filtrar os dados com base no nome e no mês
def filtrar_dados(nome, mes):
    coluna_consumo = f"Consumo {mes} (m³)"
    coluna_valor = f"Valor {mes} (R$)"

    # Filtrar os dados para o usuário selecionado
    dados_usuario = df[df['Nome'] == nome][['Nome', coluna_consumo, coluna_valor, 'Valor em Atraso (R$)']]

    return dados_usuario, coluna_consumo, coluna_valor

# Filtrar os dados com base no nome e mês
dados_usuario, coluna_consumo, coluna_valor = filtrar_dados(usuario_selecionado, mes_selecionado)

# Verificar se há dados para exibição
if not dados_usuario.empty:
    consumo = dados_usuario[coluna_consumo].iloc[0]
    valor = dados_usuario[coluna_valor].iloc[0]
    valor_atraso = dados_usuario['Valor em Atraso (R$)'].iloc[0]

    # Converter valores para números (removendo "R$" e formatando corretamente)
    def converter_valor(valor):
        if isinstance(valor, (int, float)):
            return float(valor)
        elif isinstance(valor, str):
            valor_str = valor.replace('R$', '').replace('.', '').replace(',', '.')
            return float(valor_str) if valor_str.strip() else 0.0
        return 0.0

    # Tenta converter o consumo para float com segurança
    try:
        consumo_float = float(consumo)
    except (ValueError, TypeError):
        consumo_float = -1  # valor inválido ou ausente será tratado como indisponível

    # Condições de exibição
    if consumo_float < 0:
        st.write("**Consumo:** Indisponível")
    elif consumo_float == 0:
        st.write("**Consumo:** Inferior a 1 m³")
    else:
        st.write(f"**Consumo:** {consumo} m³")

    # Sempre exibir o valor a pagar e o valor em atraso
    st.write(f"**Valor a pagar:** {valor}")
    st.write(f"**Valor em Atraso:** {valor_atraso}")

    # Gerar dados para gráficos de todos os meses do ano para o usuário
    valores = []
    for mes in meses:
        dados_usuario, coluna_consumo, coluna_valor = filtrar_dados(usuario_selecionado, mes)
        valores.append(converter_valor(dados_usuario[coluna_valor].iloc[0]))

    # Adicionar gráfico de barras para consumo
    fig, ax = plt.subplots()
    ax.bar(range(len(meses)), valores)  # Adicionando os valores corretamente

    # Garantir que os rótulos correspondam corretamente aos ticks
    ax.set_xticks(range(len(meses)))  # Define os ticks corretamente
    ax.set_xticklabels(meses, rotation=45, ha='right')

    ax.set_xlabel('Meses')
    ax.set_ylabel('Valor (R$)')
    ax.set_title('Valor a Pagar por Mês')
    st.pyplot(fig)

else:
    st.warning("Nenhum dado encontrado para este usuário e mês selecionados.")
