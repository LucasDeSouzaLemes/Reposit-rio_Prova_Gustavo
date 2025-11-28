# Documento de Requisitos

## 1. Descrição do Problema

### Contexto
Restaurantes geram grandes volumes de dados transacionais diariamente através de pedidos, mas frequentemente carecem de insights em tempo real sobre:
- Performance de vendas
- Pratos mais populares
- Padrões de consumo
- Métricas operacionais

### Problema Identificado
A falta de análise em tempo real dos dados de vendas impede:
- Tomada de decisões rápidas sobre estoque
- Identificação de tendências de consumo
- Otimização do cardápio
- Monitoramento de KPIs operacionais

## 2. Objetivos do Sistema

### Objetivo Principal
Desenvolver um pipeline de dados em tempo real para análise de vendas de restaurante, fornecendo insights automatizados sobre performance operacional.

### Objetivos Específicos
- Capturar dados de pedidos em tempo real
- Processar e transformar dados para análise
- Gerar relatórios automatizados a cada minuto
- Armazenar dados históricos para análise temporal
- Fornecer métricas de negócio (ticket médio, prato mais vendido, etc.)

### Justificativa Técnica
- **Streaming**: Necessário para análise em tempo real
- **Big Data**: Preparação para escala de milhares de pedidos/dia
- **Analytics**: Geração automática de insights de negócio

## 3. Escopo da Solução

### Incluído
- ✅ Geração simulada de dados de pedidos
- ✅ Pipeline de streaming com Kafka
- ✅ Processamento em tempo real com Spark
- ✅ Armazenamento em banco relacional
- ✅ Relatórios automatizados
- ✅ Containerização completa

### Não Incluído
- ❌ Interface web para visualização
- ❌ Integração com sistemas de POS reais
- ❌ Autenticação e autorização
- ❌ Backup e disaster recovery
- ❌ Monitoramento e alertas
- ❌ Deploy em produção/nuvem

## 4. Requisitos Funcionais

### RF01 - Geração de Dados
O sistema deve gerar dados simulados de pedidos contendo:
- Nome do prato
- Preço
- Quantidade
- ID do cliente
- Timestamp

### RF02 - Streaming de Dados
O sistema deve processar dados em streaming com latência < 1 segundo.

### RF03 - Persistência
O sistema deve armazenar todos os pedidos em banco relacional.

### RF04 - Analytics
O sistema deve gerar relatórios a cada 1 minuto contendo:
- Total de vendas no período
- Prato mais vendido
- Quantidade total de itens
- Ticket médio por cliente

### RF05 - Histórico
O sistema deve manter histórico completo de pedidos e relatórios.

## 5. Requisitos Não Funcionais

### RNF01 - Performance
- Throughput: Mínimo 100 pedidos/segundo
- Latência: Máximo 1 segundo para processamento

### RNF02 - Disponibilidade
- Uptime: 99% durante execução
- Restart automático em caso de falha

### RNF03 - Escalabilidade
- Suporte a múltiplos consumers Kafka
- Processamento distribuído com Spark

### RNF04 - Manutenibilidade
- Código versionado
- Documentação completa
- Logs estruturados