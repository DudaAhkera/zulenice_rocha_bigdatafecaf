from app.db import engine
from sqlalchemy import text


# Conectar e criar views
def create_views():
    with engine.begin() as conn:
        try:
            # Média de temperatura por dispositivo
            conn.execute(text("""
                CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
                SELECT device_id,
                    AVG(temperature) AS avg_temp
                FROM iot_temp
                GROUP BY device_id;
            """))
            print("View avg_temp_por_dispositivo criada!")
        except Exception as e:
            print(f"Erro ao criar avg_temp_por_dispositivo: {e}")

        try:
            # Leituras por hora do dia
            conn.execute(text("""
                CREATE OR REPLACE VIEW leituras_por_hora AS
                SELECT EXTRACT(HOUR FROM timestamp) AS hora,
                    COUNT(*) AS contagem
                FROM iot_temp
                GROUP BY EXTRACT(HOUR FROM timestamp)
                ORDER BY hora;
            """))
            print("View leituras_por_hora criada!")
        except Exception as e:
            print(f"Erro ao criar leituras_por_hora: {e}")

        try:
            # Temperaturas máximas e mínimas por dia
            conn.execute(text("""
                CREATE OR REPLACE VIEW temp_max_min_por_dia AS
                SELECT DATE(timestamp) AS data,
                    MAX(temperature) AS temp_max,
                    MIN(temperature) AS temp_min
                FROM iot_temp
                GROUP BY DATE(timestamp)
                ORDER BY data;
            """))
            print("View temp_max_min_por_dia criada!")
        except Exception as e:
            print(f"Erro ao criar temp_max_min_por_dia: {e}")
        
        try:
            # Diferença de temperatura In vs Out por dia
            conn.execute(text("""
                CREATE OR REPLACE VIEW temp_in_out_por_dia AS
                SELECT DATE(timestamp) AS data,
                    AVG(CASE WHEN location_type='In' THEN temperature END) AS temp_in,
                    AVG(CASE WHEN location_type='Out' THEN temperature END) AS temp_out,
                    AVG(CASE WHEN location_type='In' THEN temperature END) - 
                    AVG(CASE WHEN location_type='Out' THEN temperature END) AS diff_in_out
                FROM iot_temp
                GROUP BY DATE(timestamp)
                ORDER BY data;
            """))
            print("View temp_in_out_por_dia criada!")
        except Exception as e:
            print(f"Erro ao criar temp_in_out_por_dia: {e}")
            

