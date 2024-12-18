import streamlit as st
import pandas as pd
from tinydb import TinyDB
from datetime import datetime

def carregar_dados():
    try:
        # Conecta ao banco TinyDB
        db = TinyDB('bitcoin.json')
        
        # Verifica se existem dados
        dados = pd.DataFrame(db.all())
        if dados.empty:
            st.warning("Nenhum dado encontrado no banco.")
            return pd.DataFrame()
        
        # Converte timestamp para datetime
        dados['timestamp'] = dados['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
        dados['valor'] = dados['valor'].astype(float)  # Garante que valor seja numérico
        
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def main():
    st.title('Dashboard Bitcoin')
    
    # Carrega os dados
    df = carregar_dados()
    
    # Exibe os últimos preços
    st.subheader('Últimos Preços do Bitcoin')
    st.dataframe(df.tail())
    
    # Gráfico de linha do preço
    st.subheader('Variação do Preço')
    st.line_chart(df.set_index('timestamp')['valor'])
    
    # Estatísticas básicas
    st.subheader('Estatísticas')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Preço Atual", f"${df['valor'].iloc[-1]:.2f}")
    with col2:
        st.metric("Preço Médio", f"${df['valor'].mean():.2f}")
    with col3:
        st.metric("Preço Máximo", f"${df['valor'].max():.2f}")

if __name__ == "__main__":
    main()
