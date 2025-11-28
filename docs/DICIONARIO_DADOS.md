# Dicionário de Dados

## Visão Geral

Este documento descreve a estrutura de dados utilizada no sistema de análise de restaurante, incluindo esquemas de tabelas, formatos de mensagens e tipos de dados.

## Origem dos Dados

### Dados Simulados
- **Fonte**: Gerador Python com biblioteca Faker
- **Frequência**: A cada 10 segundos
- **Volume**: ~8.640 pedidos/dia
- **Formato**: JSON via Kafka

## Esquema de Dados

### 1. Mensagem Kafka - Tópico `pedidos`

```json
{
  "nome_prato": "string",
  "preco": "decimal(10,2)",
  "quantidade": "integer",
  "cliente_id": "integer"
}
```

**Exemplo:**
```json
{
  "nome_prato": "Pizza Margherita",
  "preco": 45.90,
  "quantidade": 2,
  "cliente_id": 73
}
```

### 2. Tabela `pedidos` - PostgreSQL

| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | SERIAL | Chave primária auto-incremento | PRIMARY KEY |
| nome_prato | VARCHAR(100) | Nome do prato pedido | NOT NULL |
| preco | DECIMAL(10,2) | Preço unitário do prato | NOT NULL, > 0 |
| quantidade | INTEGER | Quantidade pedida | NOT NULL, > 0 |
| cliente_id | INTEGER | Identificador do cliente | NOT NULL |
| created_at | TIMESTAMP | Data/hora do pedido | DEFAULT CURRENT_TIMESTAMP |

**Índices:**
- PRIMARY KEY (id)
- INDEX idx_created_at (created_at)
- INDEX idx_cliente_id (cliente_id)

### 3. Tabela `relatorio_vendas` - PostgreSQL

| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | SERIAL | Chave primária auto-incremento | PRIMARY KEY |
| periodo | TIMESTAMP | Período de referência do relatório | NOT NULL |
| total_vendas | DECIMAL(12,2) | Valor total vendido no período | NOT NULL |
| prato_mais_vendido | VARCHAR(100) | Prato com maior quantidade vendida | NOT NULL |
| quantidade_total | INTEGER | Total de itens vendidos | NOT NULL |
| ticket_medio | DECIMAL(10,2) | Valor médio por cliente | NOT NULL |
| created_at | TIMESTAMP | Data/hora de geração do relatório | DEFAULT CURRENT_TIMESTAMP |

**Índices:**
- PRIMARY KEY (id)
- INDEX idx_periodo (periodo)
- INDEX idx_created_at (created_at)

## Domínios de Dados

### Pratos Disponíveis
- Pizza Margherita
- Hambúrguer Artesanal
- Lasanha Bolonhesa
- Salmão Grelhado
- Risotto de Camarão
- Frango à Parmegiana
- Massa Carbonara
- Picanha na Chapa
- Salada Caesar
- Sushi Combo

### Faixas de Valores
- **Preço**: R$ 15,00 - R$ 85,00
- **Quantidade**: 1 - 5 itens
- **Cliente ID**: 1 - 100

## Qualidade de Dados

### Validações Implementadas
- Preços sempre positivos
- Quantidades sempre positivas
- Nomes de pratos não nulos
- Timestamps automáticos

### Limitações Conhecidas
- Dados simulados (não refletem comportamento real)
- Distribuição uniforme (não considera sazonalidade)
- Clientes fictícios (IDs sequenciais)

## Governança

### Versionamento
- Esquema versionado via migrations SQL
- Compatibilidade backward mantida

### Catalogação
- Documentação em Markdown
- Esquemas definidos em código

### Retenção
- Dados mantidos indefinidamente
- Sem política de purge implementada