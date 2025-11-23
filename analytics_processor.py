import os
import time
import psycopg2
from datetime import datetime, timedelta

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

def generate_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Dados dos últimos 1 minuto
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    
    try:
        # Total de vendas
        cursor.execute("""
            SELECT 
                COALESCE(SUM(preco * quantidade), 0) as total_vendas,
                COALESCE(SUM(quantidade), 0) as quantidade_total,
                COUNT(DISTINCT cliente_id) as clientes_unicos
            FROM pedidos 
            WHERE created_at >= %s
        """, (one_minute_ago,))
        
        result = cursor.fetchone()
        total_vendas, quantidade_total, clientes_unicos = result
        
        if quantidade_total == 0:
            print("Nenhum pedido nos últimos 1 minuto")
            cursor.close()
            conn.close()
            return
        
        # Prato mais vendido
        cursor.execute("""
            SELECT nome_prato, SUM(quantidade) as total_qty
            FROM pedidos 
            WHERE created_at >= %s
            GROUP BY nome_prato
            ORDER BY total_qty DESC
            LIMIT 1
        """, (one_minute_ago,))
        
        prato_result = cursor.fetchone()
        prato_mais_vendido = prato_result[0] if prato_result else "Nenhum"
        
        # Ticket médio
        ticket_medio = float(total_vendas) / clientes_unicos if clientes_unicos > 0 else 0
        
        # Salvar relatório
        cursor.execute("""
            INSERT INTO relatorio_vendas (periodo, total_vendas, prato_mais_vendido, quantidade_total, ticket_medio)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now(), float(total_vendas), prato_mais_vendido, int(quantidade_total), ticket_medio))
        
        conn.commit()
        
        print(f"Relatório gerado - Total: R${total_vendas:.2f}, Prato: {prato_mais_vendido}, Qtd: {quantidade_total}")
        
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
    
    cursor.close()
    conn.close()

def main():
    print("Analytics iniciado - Gerando relatórios a cada 1 minuto")
    time.sleep(30)  # Aguarda dados iniciais
    
    while True:
        try:
            generate_report()
            time.sleep(60)  # 1 minuto
        except Exception as e:
            print(f"Erro no processamento: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()