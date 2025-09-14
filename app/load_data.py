import pandas as pd
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from app.db import engine
from app.models import metadata, iot_table


CSV_FILE = "CSV/IOT-temp.csv"

def main():
    try:
        # Ler CSV
        try:
            df = pd.read_csv(CSV_FILE)
            print(df.shape)  # Mostra quantas linhas e colunas foram lidas
        except FileNotFoundError:
            print(f"Erro: arquivo {CSV_FILE} não encontrado!")
            return
        except pd.errors.ParserError as e:
            print(f"Erro ao ler CSV: {e}")
            return

        # Limpeza e renomeação
        expected_columns = ["room_id/id", "noted_date", "temp", "out/in"]
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            print(f"Colunas faltando no CSV: {missing_cols}")
            return

        df.rename(columns={
            "room_id/id": "device_id",
            "noted_date": "timestamp",
            "temp": "temperature",
            "out/in": "location_type"
        }, inplace=True)

        # Converter timestamp
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d-%m-%Y %H:%M")
        except Exception as e:
            print(f"Erro ao converter timestamp: {e}")
            return

        # Selecionar apenas colunas necessárias
        df = df[["device_id", "timestamp", "temperature", "location_type"]]

        # Criar tabela no banco (se não existir)
        metadata.create_all(engine)
        
        # Inserir dados no banco
        try:
            with engine.begin() as conn:
                conn.execute(iot_table.delete())  # limpa dados antigos
                conn.execute(insert(iot_table), df.to_dict(orient="records"))
        except SQLAlchemyError as e:
            print(f"Erro ao inserir dados no banco: {e}")
            return

        print("Dados carregados com sucesso no PostgreSQL!")

    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()

