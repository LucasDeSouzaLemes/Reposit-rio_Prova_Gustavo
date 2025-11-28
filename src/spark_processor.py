import os
import time
import psycopg2
from datetime import datetime, timedelta

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, count, desc, col

def get_db_connection():
    retries = 5
    for i in range(retries):
        try:
            return psycopg2.connect(
                host=os.getenv('POSTGRES_HOST', 'localhost'),
                database=os.getenv('POSTGRES_DB', 'datastore'),
                user=os.getenv('POSTGRES_USER', 'admin'),
                password=os.getenv('POSTGRES_PASSWORD', 'password')
            )
        except:
            time.sleep(3)
    raise Exception("Não foi possível conectar ao PostgreSQL")

def create_spark_session():
    return SparkSession.builder \
        .appName("RestauranteAnalytics") \
        .config("spark.driver.extraClassPath", "/opt/postgresql-42.7.0.jar") \
        .config("spark.executor.extraClassPath", "/opt/postgresql-42.7.0.jar") \
        .config("spark.sql.adaptive.enabled", "false") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

def generate_report():
    spark = create_spark_session()
    
    # Configuração do PostgreSQL
    jdbc_url = f"jdbc:postgresql://{os.getenv('POSTGRES_HOST', 'localhost')}:5432/{os.getenv('POSTGRES_DB', 'datastore')}"
    properties = {
        "user": os.getenv('POSTGRES_USER', 'admin'),
        "password": os.getenv('POSTGRES_PASSWORD', 'password'),
        "driver": "org.postgresql.Driver"
    }
    
    # Ler dados dos últimos 1 minuto
    one_minute_ago = (datetime.now() - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
    
    query = f"""
    (SELECT nome_prato, preco, quantidade, cliente_id, created_at 
     FROM pedidos 
     WHERE created_at >= '{one_minute_ago}') as pedidos_recentes
    """
    
    try:
        df = spark.read.jdbc(jdbc_url, query, properties=properties)
        
        if df.count() == 0:
            print("Nenhum pedido nos últimos 1 minuto")
            return
        
        # Calcular métricas
        total_vendas = df.select(spark_sum(col("preco") * col("quantidade")).alias("total")).collect()[0]["total"]
        quantidade_total = df.select(spark_sum("quantidade").alias("total_qty")).collect()[0]["total_qty"]
        ticket_medio = total_vendas / df.select("cliente_id").distinct().count() if df.select("cliente_id").distinct().count() > 0 else 0
        
        # Prato mais vendido
        prato_mais_vendido = df.groupBy("nome_prato") \
            .agg(spark_sum("quantidade").alias("total_qty")) \
            .orderBy(desc("total_qty")) \
            .first()["nome_prato"]
        
        # Salvar relatório
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO relatorio_vendas (periodo, total_vendas, prato_mais_vendido, quantidade_total, ticket_medio)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now(), float(total_vendas), prato_mais_vendido, int(quantidade_total), float(ticket_medio)))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Relatório gerado - Total: R${total_vendas:.2f}, Prato mais vendido: {prato_mais_vendido}")
        
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
    
    spark.stop()

def main():
    print("Spark Analytics iniciado - Gerando relatórios a cada 1 minuto")
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