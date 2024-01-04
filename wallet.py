import streamlit as st
from db import conectar_banco, consultar_ativos_detalhes, adicionar_ativo, excluir_ativo
from datetime import datetime
import pandas as pd
import numpy as np

# Função para obter a lista local de criptoativos
def get_crypto_list_local():
    return ["BTC", "ETH", "LTC", "XRP", "ADA", "DOT", "BCH", "LINK", "BNB", "XLM"]

def format_decimal(decimal_value):
    return float(decimal_value)

def format_datetime(datetime_value):
    return datetime_value.strftime("%Y-%m-%d %H:%M:%S") if datetime_value else None

def main():
    # Configurar a largura da página
    st.set_page_config(layout="wide")

    st.sidebar.title("Painel de Controle")
    st.title("Carteira do investidor")

    # Colunas ocupam 90% da tela
    col1, col2 = st.columns([7, 3])
    # Conectar ao banco de dados
    conn = conectar_banco()

    # Adicionando elementos à primeira coluna
    criptoativos_disponiveis = get_crypto_list_local()

    # Consultar ativos no banco de dados
    ativos = consultar_ativos_detalhes(conn)

    opcao = st.sidebar.selectbox("Selecione o ativo que deseja adicionar", criptoativos_disponiveis, index=None, placeholder="Seleção...")
    opcao_excluir = st.sidebar.selectbox("Selecione o ativo que deseja excluir", [ativo[0] for ativo in ativos], index=None, placeholder="Seleção...")

    quantidade = st.sidebar.number_input("Quantidade comprada", min_value=0.01, step=0.01, format="%.2f")
    valor_pago = st.sidebar.number_input("Valor pago", min_value=0.01, step=0.01, format="%.2f")
    st.sidebar.write('Você selecionou:', opcao)

    # Botão para adicionar ativo ao banco de dados
    if st.sidebar.button("Adicionar Ativo", key="adicionar_ativo_button"):
        adicionar_ativo(conn, opcao, quantidade, valor_pago)
        st.success(f"Ativo {opcao} adicionado com sucesso!")
   
    # Botão para excluir ativo
    excluir_button = st.sidebar.button("Excluir Ativo", key="excluir_ativo_button")

 

    if excluir_button and opcao_excluir:
        if excluir_ativo(conn, opcao_excluir):
            st.success(f"Ativo {opcao_excluir} excluído com sucesso!")
        else:
            st.warning(f"Ativo {opcao_excluir} não encontrado para exclusão.")
    elif excluir_button:
        st.warning("Nenhum ativo selecionado para exclusão.")



    # Criar uma lista para armazenar os dados formatados
    formatted_data = []

    # Iterar sobre as transações e adicionar dados formatados à lista
    for ativo in ativos:
        formatted_data.append({
            "Ativo": ativo[0],
            "Usuário ID": ativo[1],
            "Quantidade": format_decimal(ativo[2]),
            "Valor Pago": format_decimal(ativo[3]),
            "Data Transação": format_datetime(ativo[4]),
        })

    # Criar um DataFrame Pandas com os dados formatados
    df = pd.DataFrame(formatted_data)

    
    # Exibir a tabela no Streamlit
    col1.subheader("Lista de ativos na carteira")
    col1.table(df)

    col2.subheader("Evolução da carteira por operação")
    col2.area_chart(df["Valor Pago"])


    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    col2.chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    # Adicione um título à aplicação
    st.subheader('Gráfico de atividades')

    st.scatter_chart(chart_data)

    # Fechar conexão
    conn.close()

if __name__ == "__main__":
    main()