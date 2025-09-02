import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
from db import engine
from models import metadata, iot_table

# Nome do arquivo CSV (na raiz do projeto)
csv_file = "IOT-temp.csv"

def main():
    try:
        # Ler o CSV
        df = pd.read_csv(csv_file)

        # Mostrar as 5 primeiras linhas
        print("Prévia dos dados:")
        print(df.head())

        # Mostrar informações básicas
        print("\nInformações da tabela:")
        print(df.info())
        
        # Criar tabela se não existir
        metadata.create_all(engine)

        # Enviar dados para o banco
        df.to_sql("iot_temp", engine, if_exists="replace", index=False)

        print("\n Dados carregados com sucesso no PostgreSQL!")

    except FileNotFoundError:
        print(f"Erro: o arquivo {csv_file} não foi encontrado!")
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")

if __name__ == "__main__":
    main()

