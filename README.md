# Projeto Kafka + Docker + PostgreSQL

Este projeto demonstra um pipeline de dados usando Kafka para streaming, Docker para containerização e PostgreSQL para armazenamento.

## Arquitetura

- **Producer**: Gera dados falsos de usuários e envia para o tópico Kafka
- **Consumer**: Consome mensagens do Kafka e armazena no PostgreSQL
- **Kafka**: Sistema de streaming de mensagens
- **PostgreSQL**: Banco de dados para armazenamento

## Como executar

1. Inicie todos os serviços:
```bash
docker-compose up -d
```

2. Verifique os logs:
```bash
docker-compose logs -f producer
docker-compose logs -f consumer
```

3. Conecte ao PostgreSQL para ver os dados:
```bash
docker exec -it teste_projeto_postgres_1 psql -U admin -d datastore
```

4. Consulte os dados:
```sql
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
```

## Parar o projeto

```bash
docker-compose down
```