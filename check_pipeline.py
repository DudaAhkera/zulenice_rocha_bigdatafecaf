import pandas as pd
from sqlalchemy import create_engine, inspect, text

# Configuração da conexão
DB_USER = "postgres"
DB_PASS = "secret123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "iot_data"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def check_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexão com o banco estabelecida com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar no banco: {e}")
        return False

def check_table():
    insp = inspect(engine)
    tables = insp.get_table_names()
    if "iot_temp" in tables:
        with engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM iot_temp")).scalar()
        print(f"✅ Tabela 'iot_temp' encontrada com {count} registros.")
    else:
        print("❌ Tabela 'iot_temp' não encontrada!")

def check_views():
    views = [
        "avg_temp_por_dispositivo",
        "leituras_por_hora",
        "temp_max_min_por_dia",
        "temp_in_out_por_dia"
    ]
    with engine.connect() as conn:
        for v in views:
            try:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {v}")).scalar()
                print(f"✅ View '{v}' encontrada com {count} registros.")
            except Exception as e:
                print(f"❌ View '{v}' não encontrada ou erro ao consultar: {e}")

if __name__ == "__main__":
    if check_connection():
        check_table()
        check_views()
