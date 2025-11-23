import json
import time
import os
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from faker import Faker

fake = Faker()

def create_producer():
    retries = 10
    for i in range(retries):
        try:
            return KafkaProducer(
                bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except NoBrokersAvailable:
            print(f"Tentativa {i+1}/{retries}: Kafka não disponível, aguardando...")
            time.sleep(5)
    raise Exception("Não foi possível conectar ao Kafka")

def generate_pedido_data():
    pratos = [
        'Pizza Margherita', 'Hambúrguer Artesanal', 'Lasanha Bolonhesa', 
        'Salmão Grelhado', 'Risotto de Camarão', 'Frango à Parmegiana',
        'Massa Carbonara', 'Picanha na Chapa', 'Salada Caesar', 'Sushi Combo'
    ]
    
    return {
        'nome_prato': fake.random_element(pratos),
        'preco': round(fake.random.uniform(15.0, 85.0), 2),
        'quantidade': fake.random_int(min=1, max=5),
        'cliente_id': fake.random_int(min=1, max=100)
    }

def main():
    print("Iniciando producer...")
    producer = create_producer()
    print("Producer conectado ao Kafka!")
    
    while True:
        try:
            pedido_data = generate_pedido_data()
            producer.send('pedidos', pedido_data)
            print(f"Pedido enviado: {pedido_data}")
            time.sleep(10)
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()