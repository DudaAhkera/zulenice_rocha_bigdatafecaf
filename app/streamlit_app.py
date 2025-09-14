import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.load_data import main as load_data_main
from app.views import create_views
from app import dashboard

# =========================
# 1. Configuração da página
# =========================
st.set_page_config(
    page_title="Dashboard IoT",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 2. Carregamento inicial
# =========================
with st.spinner("Carregando dados e criando views..."):
    load_data_main()
    create_views()

# =========================
# 3. Cabeçalho e introdução
# =========================
st.title("📊 Dashboard IoT")
st.markdown("""
Bem-vindo ao **Painel de Monitoramento IoT**!  
Aqui você pode explorar dados de temperatura coletados por dispositivos IoT, com diferentes formas de visualização.

Use o menu lateral para escolher a análise desejada.
""")

# =========================
# 4. Menu lateral
# =========================
st.sidebar.header("⚙️ Configurações")
st.sidebar.markdown("Selecione abaixo a visualização que deseja explorar:")

view_options = {
    "📈 Média de temperatura por dispositivo": dashboard.grafico_media_por_dispositivo,
    "⏰ Leituras por hora": dashboard.grafico_leituras_por_hora,
    "🌡️ Temperaturas máxima e mínima por dia": dashboard.grafico_temp_max_min,
    "🏠 vs 🌳 Diferença In vs Out por dia": dashboard.grafico_temp_in_out
}

selected_view = st.sidebar.selectbox("Escolha a visualização", list(view_options.keys()))

# =========================
# 5. Renderização da view
# =========================
st.markdown(f"### {selected_view}")
view_options[selected_view]()  # Executa a função correspondente

# =========================
# 6. Rodapé
# =========================
st.markdown("---")
st.caption("Projeto desenvolvido por Zulenice • Dados simulados para fins acadêmicos")




