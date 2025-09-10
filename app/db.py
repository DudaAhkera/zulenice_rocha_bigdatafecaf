from sqlalchemy import create_engine

# Configurações de conexão
DATABASE_URL = "postgresql+psycopg2://postgres:secret123@localhost:5432/iot_data"

# Criar engine
engine = create_engine(DATABASE_URL)
