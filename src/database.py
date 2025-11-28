import psycopg2
import os
import time

def get_db_connection():
    retries = 10
    for i in range(retries):
        try:
            return psycopg2.connect(
                host=os.getenv('POSTGRES_HOST', 'localhost'),
                database=os.getenv('POSTGRES_DB', 'datastore'),
                user=os.getenv('POSTGRES_USER', 'admin'),
                password=os.getenv('POSTGRES_PASSWORD', 'password')
            )
        except psycopg2.OperationalError:
            print(f"Tentativa {i+1}/{retries}: PostgreSQL não disponível, aguardando...")
            time.sleep(3)
    raise Exception("Não foi possível conectar ao PostgreSQL")

def create_tables():
    print("Aguardando PostgreSQL...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id SERIAL PRIMARY KEY,
            nome_prato VARCHAR(100),
            preco DECIMAL(10,2),
            quantidade INTEGER,
            cliente_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatorio_vendas (
            id SERIAL PRIMARY KEY,
            periodo TIMESTAMP,
            total_vendas DECIMAL(12,2),
            prato_mais_vendido VARCHAR(100),
            quantidade_total INTEGER,
            ticket_medio DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Tabelas 'pedidos' e 'relatorio_vendas' criadas com sucesso!")

if __name__ == "__main__":
    create_tables()