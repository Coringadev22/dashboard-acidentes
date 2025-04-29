import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Carregar dados
df = pd.read_csv('C:\\Users\\Doit\\Downloads\\cat_acidentes.csv', sep = ";")
df_limpo = df.dropna(subset=['latitude', 'longitude'])

# Sidebar para filtro
quantidade_min = st.sidebar.slider('Quantidade mínima de acidentes', 1, 20, 5)

# Filtrar locais
acidentes_por_local = df_limpo.groupby(['latitude', 'longitude']).size().reset_index(name='quantidade')
acidentes_filtrados = acidentes_por_local[acidentes_por_local['quantidade'] >= quantidade_min]

# Criar o mapa
mapa = folium.Map(location=[-30.1, -51.15], zoom_start=11)
cluster = MarkerCluster().add_to(mapa)

for idx, row in acidentes_filtrados.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['quantidade'] * 0.5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=f"Acidentes: {row['quantidade']}"
    ).add_to(cluster)

# Mostrar no Streamlit
folium_static(mapa)

# Mostrar estatísticas
st.write('Resumo dos acidentes filtrados:')
st.dataframe(acidentes_filtrados)
