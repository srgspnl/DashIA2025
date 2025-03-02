import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# Carregando os dados
file_path = r"C:\Users\User\Documents\Streamlit\global_peace_index.csv"
df = pd.read_csv(file_path, sep=';')
for col in df.columns[2:]:
    df[col] = df[col].str.replace(',', '.').astype(float)

# Configuração do Streamlit
st.set_page_config(page_title="Global Peace Index Dashboard", layout="wide")

# Sidebar para navegação
page = st.sidebar.selectbox("Selecione a página:", ["Página 1: Índice por Ano", "Página 2: Mudança no Índice (2008-2022)"])

if page == "Página 1: Índice por Ano":
    st.title("Índice Global de Paz por Ano")
    year = st.selectbox("Selecione o ano:", list(range(2008, 2023)))

    # Dados para o ano selecionado
    year_data = df[['Country', 'iso3c', str(year)]].rename(columns={str(year): 'Index'})
    year_data = year_data[year_data['Index'] > 0]

    # Mapa coroplético
    fig_map = px.choropleth(year_data, locations="iso3c", color="Index", hover_name="Country",
                            color_continuous_scale="YlOrRd", title=f"Índice Global de Paz em {year}")
    st.plotly_chart(fig_map)

    # Gráficos de barras
    st.subheader("Top 5 Países Mais e Menos Pacíficos")
    top_5 = year_data.nsmallest(5, 'Index')
    bottom_5 = year_data.nlargest(5, 'Index')
    st.bar_chart(pd.concat([top_5, bottom_5]).set_index('Country')['Index'])

elif page == "Página 2: Mudança no Índice (2008-2022)":
    st.title("Mudança no Índice Global de Paz (2008-2022)")
    df['Change'] = df['2022'] - df['2008']
    change_data = df[['Country', 'iso3c', 'Change']]
    fig_change = px.choropleth(change_data, locations="iso3c", color="Change", hover_name="Country",
                               color_continuous_scale="RdYlGn", range_color=[-0.5, 0.5],
                               title="Mudança no Índice de Paz (2008-2022)")
    st.plotly_chart(fig_change)

    # Gráfico de linha
    st.subheader("Evolução do Índice Global de Paz")
    avg_peace_index = df.iloc[:, 2:].mean()
    st.line_chart(avg_peace_index)
