import json
import time
import os
from datetime import datetime
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

def is_lunch_time():
    """Verifica se está no horário de almoço (11h às 15h)"""
    current_hour = datetime.now().hour
    return 11 <= current_hour < 15

def main():
    print("Iniciando producer...")
    producer = create_producer()
    print("Producer conectado ao Kafka!")
    
    # Modo de teste - sempre gera pedidos para demonstração
    test_mode = True
    
    if test_mode:
        print("MODO DE TESTE: Gerando pedidos independente do horário")
    else:
        print("Gerando pedidos apenas no horário de almoço (11h às 15h)")
    
    while True:
        try:
            if test_mode or is_lunch_time():
                pedido_data = generate_pedido_data()
                producer.send('pedidos', pedido_data)
                print(f"Pedido enviado: {pedido_data}")
                time.sleep(10)
            else:
                current_hour = datetime.now().hour
                print(f"Fora do horário de almoço (atual: {current_hour}h). Aguardando...")
                time.sleep(60)  # Verifica a cada minuto
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()