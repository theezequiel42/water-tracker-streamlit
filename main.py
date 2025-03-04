import streamlit as st
import pandas as pd
import os
import gdown
import matplotlib.pyplot as plt
from urllib.parse import quote_plus
import io
from datetime import datetime

# Definir o idioma como pt-BR usando o atributo lang
st.markdown("""
    <html lang="pt-br">
    <meta http-equiv="Content-Language" content="pt-br">
    <style>
        html {
            font-family: 'Arial', sans-serif;
        }
        body {
            background-color: #f5f5f5;
            color: #333;
            font-size: 16px;
            margin: 0;
            padding: 0;
        }
        .logo {
            width: 200px;  /* Ajuste do tamanho do logo */
            margin-left: auto;
            margin-right: auto;
            display: block; /* Garante centralização */
        }
        .stButton>button {
            background-color: #4CAF50; 
            color: white; 
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTitle {
            font-size: 36px;
            font-weight: bold;
            color: #2e7d32;
        }
        .stMarkdown {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Exibir o logo centralizado usando st.columns
col1, col2, col3 = st.columns([1, 4, 1])  # Dividindo a página em 3 partes
with col2:
    st.image("images/logo.png", width=200)  # Exibindo o logo com a largura ajustada

# Baixar a planilha do Google Drive
url = 'https://docs.google.com/spreadsheets/d/1UdM-Mew0af_fmyNXQpYvC3z4rZTYrWHph8SrcI60plU/export?format=xlsx'
output = 'dados.xlsx'
gdown.download(url, output, quiet=False)

# Carregar a planilha
df = pd.read_excel('dados.xlsx')


# Adicionar título e descrição
st.title("Consulta de Consumo e Pagamento")
st.markdown("**Selecione seu nome e o mês para visualizar o consumo, valor a pagar e o valor em atraso.**")

# Listar os nomes dos usuários
nomes = df['Nome'].unique()
usuario_selecionado = st.selectbox("Selecione seu nome", nomes)

# Listar os meses para seleção
meses = [
    'Janeiro 2025', 'Fevereiro 2025', 'Março 2025',
    'Abril 2025', 'Maio 2025', 'Junho 2025', 'Julho 2025', 'Agosto 2025',
    'Setembro 2025', 'Outubro 2025', 'Novembro 2025', 'Dezembro 2025'
]
mes_selecionado = st.selectbox("Selecione o mês", meses)

# Função para filtrar os dados com base no nome e no mês
def filtrar_dados(nome, mes):
    if mes == 'Janeiro 2025':
        coluna_consumo = 'Consumo Janeiro 2025 (m³)'
        coluna_valor = 'Valor Janeiro 2025 (R$)'
    elif mes == 'Fevereiro 2025':
        coluna_consumo = 'Consumo Fevereiro 2025 (m³)'
        coluna_valor = 'Valor Fevereiro 2025 (R$)'
    elif mes == 'Março 2025':
        coluna_consumo = 'Consumo Março 2025 (m³)'
        coluna_valor = 'Valor Março 2025 (R$)'
    elif mes == 'Abril 2025':
        coluna_consumo = 'Consumo Abril 2025 (m³)'
        coluna_valor = 'Valor Abril 2025 (R$)'
    elif mes == 'Maio 2025':
        coluna_consumo = 'Consumo Maio 2025 (m³)'
        coluna_valor = 'Valor Maio 2025 (R$)'
    elif mes == 'Junho 2025':
        coluna_consumo = 'Consumo Junho 2025 (m³)'
        coluna_valor = 'Valor Junho 2025 (R$)'
    elif mes == 'Julho 2025':
        coluna_consumo = 'Consumo Julho 2025 (m³)'
        coluna_valor = 'Valor Julho 2025 (R$)'
    elif mes == 'Agosto 2025':
        coluna_consumo = 'Consumo Agosto 2025 (m³)'
        coluna_valor = 'Valor Agosto 2025 (R$)'
    elif mes == 'Setembro 2025':
        coluna_consumo = 'Consumo Setembro 2025 (m³)'
        coluna_valor = 'Valor Setembro 2025 (R$)'
    elif mes == 'Outubro 2025':
        coluna_consumo = 'Consumo Outubro 2025 (m³)'
        coluna_valor = 'Valor Outubro 2025 (R$)'
    elif mes == 'Novembro 2025':
        coluna_consumo = 'Consumo Novembro 2025 (m³)'
        coluna_valor = 'Valor Novembro 2025 (R$)'
    elif mes == 'Dezembro 2025':
        coluna_consumo = 'Consumo Dezembro 2025 (m³)'
        coluna_valor = 'Valor Dezembro 2025 (R$)'

    # Filtrar os dados
    dados_usuario = df[df['Nome'] == nome][['Nome', coluna_consumo, coluna_valor, 'Valor em Atraso (R$)']]
    
    # Retornar tanto as colunas como os dados
    return dados_usuario, coluna_consumo, coluna_valor

# Filtrar os dados com base no nome e mês
dados_usuario, coluna_consumo, coluna_valor = filtrar_dados(usuario_selecionado, mes_selecionado)

# Acessar os valores diretamente pelas colunas
consumo = dados_usuario[coluna_consumo].iloc[0]
valor = dados_usuario[coluna_valor].iloc[0]
valor_atraso = dados_usuario['Valor em Atraso (R$)'].iloc[0]

# Função para converter valores em string para float (verificando se o valor é string ou número)
def converter_valor(valor):
    # Se o valor já for numérico (int ou float), retornamos diretamente
    if isinstance(valor, (int, float)):
        return float(valor)
    # Se for string (ex: "R$ 10,00"), removemos os caracteres e convertemos para float
    elif isinstance(valor, str):
        valor_str = valor.replace('R$', '').replace('.', '').replace(',', '.')
        return float(valor_str)
    else:
        # Caso o valor não seja string nem número, apenas retorna 0
        return 0.0

# Exibir consumo e valor
if consumo <= 0:
    st.write("Consumo: Indisponível")
else:
    st.write(f"Consumo: {consumo} m³")
    st.write(f"Valor a pagar: {valor}")

# Exibir valor em atraso
st.write(f"Valor em Atraso: {valor_atraso}")

# Gerar dados para gráficos de todos os meses do ano para o usuário
valores = []
for mes in meses:
    dados_usuario, coluna_consumo, coluna_valor = filtrar_dados(usuario_selecionado, mes)
    valores.append(converter_valor(dados_usuario[coluna_valor].iloc[0]))

# Adicionar gráfico de barras para consumo
fig, ax = plt.subplots()
ax.bar(meses, valores)

# Quebrar o texto das legendas no eixo X
ax.set_xticklabels(meses, rotation=45, ha='right')  # Ajustar o ângulo para melhorar a leitura
ax.set_xlabel('Meses')
ax.set_ylabel('Valor (R$)')
ax.set_title('Valor a Pagar por Mês')
st.pyplot(fig)

# Remover a planilha
os.remove('dados.xlsx')
