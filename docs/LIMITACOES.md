# Pontos de Falha e Limitações

## Pontos de Falha Identificados

### 1. Dependências de Inicialização
**Problema**: Ordem de inicialização dos containers
- Kafka precisa estar pronto antes do Producer/Spark
- PostgreSQL precisa estar pronto antes do db-init

**Impacto**: Falhas de conexão durante startup
**Mitigação**: 
- Retry logic implementado nos conectores
- Health checks e depends_on configurados

### 2. Falha do Kafka
**Problema**: Kafka é ponto único de falha
**Impacto**: Perda de mensagens em trânsito
**Mitigação**: 
- Restart automático configurado
- Dados persistidos em volume Docker

### 3. Falha do PostgreSQL
**Problema**: Perda de conectividade com banco
**Impacto**: Impossibilidade de persistir dados
**Mitigação**:
- Volume persistente configurado
- Retry logic nos conectores

### 4. Falha do Spark
**Problema**: Processamento analytics pode falhar
**Impacto**: Relatórios não são gerados
**Mitigação**:
- Restart automático
- Dados fonte mantidos para reprocessamento

## Limitações Técnicas

### 1. Escalabilidade
**Limitação**: Configuração single-node
- Kafka: 1 broker, 1 partição
- Spark: Modo local
- PostgreSQL: Instância única

**Impacto**: Throughput limitado
**Solução Futura**: Cluster multi-node

### 2. Durabilidade
**Limitação**: Sem replicação
- Dados em volume Docker local
- Sem backup automático

**Impacto**: Risco de perda de dados
**Solução Futura**: Backup automatizado

### 3. Monitoramento
**Limitação**: Sem observabilidade
- Sem métricas de performance
- Sem alertas automáticos
- Logs básicos apenas

**Impacto**: Dificuldade de troubleshooting
**Solução Futura**: Prometheus + Grafana

### 4. Segurança
**Limitação**: Sem autenticação
- Kafka sem SASL
- PostgreSQL com credenciais fixas
- Sem criptografia em trânsito

**Impacto**: Inadequado para produção
**Solução Futura**: TLS + autenticação

## Limitações de Dados

### 1. Dados Simulados
**Limitação**: Não reflete comportamento real
- Distribuição uniforme
- Sem sazonalidade
- Padrões artificiais

**Impacto**: Insights podem não ser realistas
**Solução**: Integração com dados reais

### 2. Volume de Dados
**Limitação**: Baixo volume para Big Data
- ~8.640 pedidos/dia
- Dados em memória

**Impacto**: Não testa escalabilidade real
**Solução**: Aumentar frequência de geração

### 3. Variedade de Dados
**Limitação**: Schema simples
- Apenas dados transacionais
- Sem dados de contexto (clima, eventos)

**Impacto**: Analytics limitado
**Solução**: Enriquecer com dados externos

## Limitações de Infraestrutura

### 1. Ambiente de Desenvolvimento
**Limitação**: Docker Compose local
- Não adequado para produção
- Recursos limitados

**Impacto**: Performance não representa produção
**Solução**: Deploy em Kubernetes

### 2. Persistência
**Limitação**: Volumes Docker locais
- Não distribuído
- Sem redundância

**Impacto**: Ponto único de falha
**Solução**: Storage distribuído

### 3. Rede
**Limitação**: Bridge network simples
- Sem isolamento de segurança
- Sem QoS

**Impacto**: Possível interferência entre serviços
**Solução**: Redes isoladas por função

## Limitações de Negócio

### 1. Tempo Real
**Limitação**: Micro-batches de 60 segundos no Spark Streaming
**Impacto**: Latência mínima de 1 minuto para relatórios
**Solução**: Reduzir janela de processamento para 10-30 segundos

### 2. Análises Básicas
**Limitação**: KPIs simples apenas
- Sem análise preditiva
- Sem detecção de anomalias
- Sem segmentação de clientes

**Impacto**: Insights limitados
**Solução**: ML pipeline adicional

### 3. Interface
**Limitação**: Sem dashboard visual
**Impacto**: Dados apenas via SQL
**Solução**: Integração com BI tools

## Plano de Melhorias

### Curto Prazo (1-2 semanas)
- [ ] Adicionar dashboard com Grafana
- [ ] Implementar health checks
- [ ] Melhorar logs estruturados

### Médio Prazo (1-2 meses)
- [ ] Cluster Kafka multi-broker
- [ ] Backup automatizado
- [ ] Monitoramento com Prometheus

### Longo Prazo (3-6 meses)
- [ ] Deploy em Kubernetes
- [ ] Pipeline de ML
- [ ] Integração com dados reais
- [ ] Implementar segurança completa