# Guia de Dependências

## Versões de Software

### Containers Base
| Componente | Imagem | Versão | Justificativa |
|------------|--------|--------|---------------|
| Apache Kafka | apache/kafka | 3.7.0 | Versão estável com KRaft mode |
| PostgreSQL | postgres | 13 | Versão LTS com boa performance |
| Python | python | 3.9-slim | Compatibilidade com PySpark |
| Java | eclipse-temurin | 11-jre | Requerido pelo Spark |

### Bibliotecas Python
| Biblioteca | Versão | Uso | Instalação |
|------------|--------|-----|------------|
| kafka-python | 2.0.2 | Cliente Kafka (Producer) | pip install |
| psycopg2-binary | 2.9.7 | Driver PostgreSQL | pip install |
| faker | 19.6.2 | Geração de dados | pip install |
| pyspark | 3.5.0 | Spark Streaming + Analytics | pip install |
| pandas | 2.0+ | Processamento de dados | pip install |

### Dependências de Sistema
| Componente | Versão Mínima | Uso |
|------------|---------------|-----|
| Docker | 20.10+ | Containerização |
| Docker Compose | 2.0+ | Orquestração |
| Git | 2.0+ | Versionamento |

## Configurações de Ambiente

### Variáveis de Ambiente - Kafka
```bash
KAFKA_NODE_ID=1
KAFKA_PROCESS_ROLES=broker,controller
KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka:29093
KAFKA_LISTENERS=PLAINTEXT://kafka:29092,CONTROLLER://kafka:29093,PLAINTEXT_HOST://0.0.0.0:9092
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER
KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1
KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0
KAFKA_LOG_DIRS=/tmp/kraft-combined-logs
CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk
```

### Variáveis de Ambiente - PostgreSQL
```bash
POSTGRES_DB=datastore
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
```

### Variáveis de Ambiente - Aplicações Python
```bash
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
POSTGRES_HOST=postgres
POSTGRES_DB=datastore
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
```

## Portas Utilizadas

| Serviço | Porta Host | Porta Container | Protocolo |
|---------|------------|-----------------|-----------|
| Kafka | 9092 | 9092 | TCP |
| PostgreSQL | 5432 | 5432 | TCP |
| Kafka Internal | - | 29092 | TCP |
| Kafka Controller | - | 29093 | TCP |

## Volumes Docker

| Volume | Tipo | Uso |
|--------|------|-----|
| postgres_data | Named Volume | Persistência PostgreSQL |
| ./src/init.sql | Bind Mount | Inicialização do banco |

## Dependências de Rede

### Comunicação Interna
- **Producer → Kafka**: kafka:29092
- **Spark → Kafka**: kafka:29092
- **Spark → PostgreSQL**: postgres:5432

### Comunicação Externa
- **Host → Kafka**: localhost:9092
- **Host → PostgreSQL**: localhost:5432

## Ordem de Inicialização

1. **PostgreSQL** - Banco de dados base
2. **Kafka** - Sistema de streaming
3. **db-init** - Inicialização das tabelas
4. **Producer** - Geração de dados
5. **Spark Streaming** - Consumo do Kafka + processamento analítico

## Recursos de Sistema

### Requisitos Mínimos
- **CPU**: 2 cores
- **RAM**: 4GB
- **Disco**: 2GB livre
- **Rede**: 100Mbps

### Recursos Recomendados
- **CPU**: 4 cores
- **RAM**: 8GB
- **Disco**: 10GB livre (SSD)
- **Rede**: 1Gbps

### Configuração Docker
```yaml
# Limites recomendados para produção
services:
  kafka:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
  
  spark-analytics:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
  
  postgres:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

## Compatibilidade

### Sistemas Operacionais Testados
- ✅ Windows 10/11 + Docker Desktop
- ✅ Ubuntu 20.04+ + Docker CE
- ✅ macOS 12+ + Docker Desktop

### Arquiteturas Suportadas
- ✅ x86_64 (Intel/AMD)
- ⚠️ ARM64 (Apple Silicon) - Pode requerer imagens específicas

## Troubleshooting de Dependências

### Problema: Versão Docker Incompatível
```bash
# Verificar versão
docker --version
docker-compose --version

# Atualizar se necessário
# Windows: Docker Desktop
# Ubuntu: apt update && apt upgrade docker-ce
```

### Problema: Porta em Uso
```bash
# Verificar portas ocupadas
netstat -tulpn | grep :5432
netstat -tulpn | grep :9092

# Parar serviços conflitantes
sudo systemctl stop postgresql
```

### Problema: Memória Insuficiente
```bash
# Verificar uso de memória
docker stats

# Aumentar limite Docker Desktop
# Settings → Resources → Memory → 6GB+
```

### Problema: Permissões Volume
```bash
# Linux: Ajustar permissões
sudo chown -R $USER:$USER ./data
chmod 755 ./data
```

## Atualizações

### Política de Versionamento
- **Major**: Mudanças incompatíveis
- **Minor**: Novas funcionalidades compatíveis
- **Patch**: Correções de bugs

### Processo de Atualização
1. Backup dos dados
2. Parar containers
3. Atualizar imagens
4. Testar em ambiente isolado
5. Deploy em produção