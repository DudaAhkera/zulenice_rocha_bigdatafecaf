import pandas as pd
import plotly.express as px
import streamlit as st
from app.db import engine

def load_data(view_name: str) -> pd.DataFrame:

    try:
        return pd.read_sql(f"SELECT * FROM {view_name}", engine)
    except Exception as e:
        st.error(f"Erro ao carregar dados da view '{view_name}': {e}")
        return pd.DataFrame()  # Retorna DF vazio em caso de erro

# Dashboard de Temperaturas IoT

# Gráfico 1: Média de Temperatura por Dispositivo
def grafico_media_por_dispositivo():
    st.header("Média de Temperatura por Dispositivo")
    df_avg = load_data("avg_temp_por_dispositivo")
    if not df_avg.empty:
        fig1 = px.bar(df_avg, x="device_id", y="avg_temp", labels={"avg_temp": "Temperatura Média"})
        st.plotly_chart(fig1)

# Gráfico 2: Leituras por Hora do Dia
def grafico_leituras_por_hora():
    st.header("Leituras por Hora do Dia")
    df_hora = load_data("leituras_por_hora")
    if not df_hora.empty:
        fig2 = px.line(df_hora, x="hora", y="contagem", labels={"contagem": "Número de Leituras"})
        st.plotly_chart(fig2)

# Gráfico 3: Temperaturas Máximas e Mínimas por Dia
def grafico_temp_max_min():
    st.header("Temperaturas Máximas e Mínimas por Dia")
    df_minmax = load_data("temp_max_min_por_dia")
    if not df_minmax.empty:
        fig3 = px.line(df_minmax, x="data", y=["temp_max", "temp_min"],
                    labels={"value": "Temperatura", "variable": "Tipo"})
        st.plotly_chart(fig3)

# Gráfico 4: Diferença de Temperatura In vs Out por Dia
def grafico_temp_in_out():
    st.header("Diferença de Temperatura In vs Out por Dia")
    df_in_out = load_data("temp_in_out_por_dia")
    if not df_in_out.empty:
        fig4 = px.line(df_in_out, x="data",
                    y=["temp_in", "temp_out", "diff_in_out"],
                    labels={
                        "temp_in": "Temperatura Interna",
                        "temp_out": "Temperatura Externa",
                        "diff_in_out": "Diferença (In - Out)"
                    })
        st.plotly_chart(fig4)
