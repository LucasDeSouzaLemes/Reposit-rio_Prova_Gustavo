import os
import time
import psycopg2
from datetime import datetime, timedelta

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, count, desc, col, from_json, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

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
    jars = "/opt/postgresql-42.7.0.jar,/opt/kafka-clients-3.5.0.jar,/opt/spark-sql-kafka-0-10_2.12-3.5.0.jar"
    return SparkSession.builder \
        .appName("RestauranteAnalytics") \
        .config("spark.jars", jars) \
        .config("spark.driver.extraClassPath", jars) \
        .config("spark.executor.extraClassPath", jars) \
        .config("spark.sql.adaptive.enabled", "false") \
        .config("spark.driver.memory", "1g") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
        .getOrCreate()

def save_to_postgres(df, epoch_id):
    """Salva dados processados no PostgreSQL"""
    try:
        # Converter para Pandas para facilitar inserção
        pandas_df = df.toPandas()
        
        if len(pandas_df) == 0:
            print(f"Batch {epoch_id}: Nenhum dado para processar")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for _, row in pandas_df.iterrows():
            # Inserir pedido individual
            cursor.execute("""
                INSERT INTO pedidos (nome_prato, preco, quantidade, cliente_id, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['nome_prato'], row['preco'], row['quantidade'], row['cliente_id'], datetime.now()))
        
        # Calcular e inserir relatório agregado
        total_vendas = (pandas_df['preco'] * pandas_df['quantidade']).sum()
        quantidade_total = pandas_df['quantidade'].sum()
        ticket_medio = total_vendas / pandas_df['cliente_id'].nunique() if pandas_df['cliente_id'].nunique() > 0 else 0
        prato_mais_vendido = pandas_df.groupby('nome_prato')['quantidade'].sum().idxmax()
        
        cursor.execute("""
            INSERT INTO relatorio_vendas (periodo, total_vendas, prato_mais_vendido, quantidade_total, ticket_medio)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now(), float(total_vendas), prato_mais_vendido, int(quantidade_total), float(ticket_medio)))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Batch {epoch_id}: {len(pandas_df)} pedidos processados - Total: R${total_vendas:.2f}")
        
    except Exception as e:
        print(f"Erro ao salvar batch {epoch_id}: {e}")

def is_lunch_time():
    """Verifica se está no horário de almoço (11h às 15h)"""
    current_hour = datetime.now().hour
    return 11 <= current_hour < 15

def main():
    print("Spark Streaming Analytics iniciado - Consumindo diretamente do Kafka")
    print("Processando apenas no horário de almoço (11h às 15h)")
    
    spark = create_spark_session()
    
    # Schema dos dados do Kafka
    schema = StructType([
        StructField("nome_prato", StringType(), True),
        StructField("preco", DoubleType(), True),
        StructField("quantidade", IntegerType(), True),
        StructField("cliente_id", IntegerType(), True)
    ])
    
    # Ler stream do Kafka
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')) \
        .option("subscribe", "pedidos") \
        .option("startingOffsets", "latest") \
        .load()
    
    # Processar dados JSON
    pedidos_df = kafka_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Configurar stream para processar em micro-batches
    query = pedidos_df.writeStream \
        .foreachBatch(save_to_postgres) \
        .trigger(processingTime='60 seconds') \
        .start()
    
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("Parando Spark Streaming...")
        query.stop()
        spark.stop()

if __name__ == "__main__":
    main()