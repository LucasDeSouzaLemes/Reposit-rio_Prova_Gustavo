# Arquitetura do Sistema

## Visão Geral

O sistema implementa um pipeline de dados em tempo real para análise de vendas de restaurante, utilizando uma arquitetura moderna de streaming com Apache Kafka, processamento distribuído com Apache Spark e armazenamento em PostgreSQL.

## Diagrama de Arquitetura

```mermaid
graph TD
    A[Producer] -->|Pedidos JSON| B[Apache Kafka]
    B -->|Spark Streaming| C[Apache Spark]
    C -->|INSERT| D[PostgreSQL - Pedidos]
    C -->|INSERT| E[PostgreSQL - Relatórios]
    
    subgraph "Camada de Ingestão"
        A
        B
    end
    
    subgraph "Camada de Processamento"
        C
    end
    
    subgraph "Camada de Armazenamento"
        D
        E
    end
```

## Componentes da Arquitetura

### 1. Camada de Ingestão
- **Producer**: Gera dados simulados de pedidos de restaurante
- **Apache Kafka**: Sistema de streaming distribuído (modo KRaft)

### 2. Camada de Processamento
- **Apache Spark Streaming**: Consome diretamente do Kafka e processa dados em tempo real

### 3. Camada de Armazenamento
- **PostgreSQL**: Banco relacional para dados transacionais e analíticos

## Fluxo de Dados

1. **Ingestão**: Producer gera pedidos a cada 10 segundos (11h às 15h)
2. **Streaming**: Kafka armazena mensagens em tópicos
3. **Processamento**: Spark Streaming consome diretamente do Kafka
4. **Persistência**: Spark salva pedidos individuais no PostgreSQL
5. **Analytics**: Spark gera relatórios agregados em micro-batches de 60s

## Decisões Técnicas

### Kafka vs RabbitMQ
- **Escolhido**: Apache Kafka
- **Justificativa**: Melhor para streaming de alta throughput, durabilidade e replicação

### Spark vs Pandas
- **Escolhido**: Apache Spark
- **Justificativa**: Processamento distribuído, escalabilidade e integração nativa com big data

### PostgreSQL vs MongoDB
- **Escolhido**: PostgreSQL
- **Justificativa**: ACID compliance, queries complexas e maturidade para analytics

## Infraestrutura

- **Containerização**: Docker e Docker Compose
- **Orquestração**: Docker Compose para desenvolvimento
- **Rede**: Bridge network para comunicação entre containers
- **Volumes**: Persistência de dados PostgreSQL

## Vantagens da Nova Arquitetura

- **Menor Latência**: Processamento direto do stream sem intermediários
- **Menos Componentes**: Arquitetura simplificada (sem consumer separado)
- **Streaming Real**: Verdadeiro processamento em tempo real
- **Menos Pontos de Falha**: Redução de componentes críticos

## Escalabilidade

- **Kafka**: Suporte a múltiplas partições e brokers
- **Spark**: Processamento distribuído em cluster
- **PostgreSQL**: Read replicas e particionamento de tabelas