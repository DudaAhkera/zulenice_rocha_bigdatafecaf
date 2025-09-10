from sqlalchemy import MetaData, Table, Column, Integer, String, Float, DateTime

metadata = MetaData()

# Tabela principal de dados do IoT
iot_table = Table(
    "iot_temp", metadata,
    Column("device_id", String(50)),
    Column("timestamp", DateTime),
    Column("temperature", Float),
    Column("location_type", String(10), nullable=False)  # out/in
)
