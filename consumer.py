import json
import os
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from database import get_db_connection, create_tables

def create_consumer():
    retries = 10
    for i in range(retries):
        try:
            return KafkaConsumer(
                'pedidos',
                bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'
            )
        except NoBrokersAvailable:
            print(f"Tentativa {i+1}/{retries}: Kafka não disponível, aguardando...")
            time.sleep(5)
    raise Exception("Não foi possível conectar ao Kafka")

def save_to_database(pedido_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO pedidos (nome_prato, preco, quantidade, cliente_id) VALUES (%s, %s, %s, %s)",
        (pedido_data['nome_prato'], pedido_data['preco'], pedido_data['quantidade'], pedido_data['cliente_id'])
    )
    
    conn.commit()
    cursor.close()
    conn.close()

def main():
    print("Aguardando serviços iniciarem...")
    time.sleep(15)
    
    try:
        create_tables()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        time.sleep(5)
        create_tables()
    
    consumer = create_consumer()
    print("Consumidor iniciado. Aguardando mensagens...")
    
    for message in consumer:
        try:
            pedido_data = message.value
            save_to_database(pedido_data)
            print(f"Pedido salvo no banco: {pedido_data}")
        except Exception as e:
            print(f"Erro ao salvar pedido: {e}")

if __name__ == "__main__":
    main()