from db import engine

# Conectar e criar views
with engine.connect() as conn:
    # Média de temperatura por dispositivo
    conn.execute("""
    CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
    SELECT device_id, AVG(temperature) AS avg_temp
    FROM iot_temp
    GROUP BY device_id;
    """)

    # Média de vibração por dispositivo
    conn.execute("""
    CREATE OR REPLACE VIEW avg_vibration_por_dispositivo AS
    SELECT device_id, AVG(vibration) AS avg_vibration
    FROM iot_temp
    GROUP BY device_id;
    """)

    # Últimas 5 leituras por dispositivo
    conn.execute("""
    CREATE OR REPLACE VIEW ultimas_leituras AS
    SELECT *
    FROM iot_temp
    WHERE id IN (
        SELECT id
        FROM iot_temp t2
        WHERE t2.device_id = iot_temp.device_id
        ORDER BY timestamp DESC
        LIMIT 5
    );
    """)

    print("Views criadas com sucesso!")
