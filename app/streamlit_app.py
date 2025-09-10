import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import engine
from load_data import main as load_data_main
from views import create_views

# 1️⃣ Carrega os dados do CSV e cria as views
load_data_main()
create_views()

st.title("Dashboard IoT 🚀")

# 2️⃣ Menu lateral para escolher a view
view_options = {
    "Média de temperatura por dispositivo": "avg_temp_por_dispositivo",
    "Leituras por hora": "leituras_por_hora",
    "Temperaturas máxima e mínima por dia": "temp_max_min_por_dia",
    "Diferença In vs Out por dia": "temp_in_out_por_dia"
}

selected_view = st.sidebar.selectbox("Escolha a view", list(view_options.keys()))
query = f"SELECT * FROM {view_options[selected_view]}"

# 3️⃣ Puxar os dados do banco
with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

# 4️⃣ Mostrar tabela
st.subheader(selected_view)
st.dataframe(df)

# 5️⃣ Mostrar gráfico dependendo da view
if not df.empty:
    if selected_view == "Média de temperatura por dispositivo":
        st.bar_chart(df.set_index("device_id")["avg_temp"])
    elif selected_view == "Leituras por hora":
        st.line_chart(df.set_index("hora")["contagem"])
    elif selected_view == "Temperaturas máxima e mínima por dia":
        st.line_chart(df.set_index("data")[["temp_max", "temp_min"]])
    elif selected_view == "Diferença In vs Out por dia":
        st.line_chart(df.set_index("data")[["temp_in", "temp_out", "diff_in_out"]])

