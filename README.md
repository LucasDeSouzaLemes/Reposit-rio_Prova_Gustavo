# Sistema de Análise de Restaurante - Kafka + Spark + PostgreSQL

Pipeline completo de dados em tempo real para análise de vendas de restaurante usando Kafka, Apache Spark e PostgreSQL.

## 🏗️ Arquitetura

```
Producer → Kafka → Consumer → PostgreSQL
                      ↓
                 Spark Analytics → Relatórios
```

### Componentes:
- **Producer**: Gera pedidos de restaurante a cada 10 segundos
- **Kafka**: Streaming de mensagens (modo KRaft, sem Zookeeper)
- **Consumer**: Consome pedidos do Kafka e salva no PostgreSQL
- **Spark Analytics**: Processa dados e gera relatórios a cada 1 minuto
- **PostgreSQL**: Armazena pedidos e relatórios

## 🚀 Como executar

1. **Iniciar o sistema:**
```bash
docker-compose up --build -d
```

2. **Monitorar logs:**
```bash
# Ver pedidos sendo gerados
docker-compose logs -f producer

# Ver pedidos sendo salvos
docker-compose logs -f consumer

# Ver relatórios do Spark
docker-compose logs -f spark-analytics
```

3. **Acessar banco de dados:**
```bash
docker-compose exec postgres psql -U admin -d datastore
```

## 📊 Consultas SQL

### Pedidos recentes:
```sql
SELECT * FROM pedidos ORDER BY created_at DESC LIMIT 10;
```

### Relatórios do Spark:
```sql
SELECT 
    periodo,
    total_vendas,
    prato_mais_vendido,
    quantidade_total,
    ticket_medio
FROM relatorio_vendas 
ORDER BY created_at DESC 
LIMIT 5;
```

### Estatísticas:
```sql
-- Total de pedidos
SELECT COUNT(*) FROM pedidos;

-- Total de relatórios gerados
SELECT COUNT(*) FROM relatorio_vendas;
```

## 🔧 Credenciais do Banco

- **Host:** localhost
- **Porta:** 5432
- **Database:** datastore
- **Usuário:** admin
- **Senha:** password

## 📈 Dados Gerados

### Tabela `pedidos`:
- `nome_prato`: Nome do prato (Pizza, Hambúrguer, etc.)
- `preco`: Preço do prato (R$ 15,00 - R$ 85,00)
- `quantidade`: Quantidade pedida (1-5)
- `cliente_id`: ID do cliente (1-100)
- `created_at`: Timestamp do pedido

### Tabela `relatorio_vendas`:
- `periodo`: Timestamp do relatório
- `total_vendas`: Valor total vendido no período
- `prato_mais_vendido`: Prato com maior quantidade vendida
- `quantidade_total`: Total de itens vendidos
- `ticket_medio`: Valor médio por cliente

## ⏹️ Parar o projeto

```bash
docker-compose down
```

## 🛠️ Tecnologias

- **Apache Kafka 3.7.0** (KRaft mode)
- **Apache Spark 3.5.0** (PySpark)
- **PostgreSQL 13**
- **Python 3.9**
- **Docker & Docker Compose**