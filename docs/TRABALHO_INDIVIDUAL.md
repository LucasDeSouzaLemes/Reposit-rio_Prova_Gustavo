# Trabalho Individual - Responsabilidades

## Visão Geral

Este documento descreve as responsabilidades individuais de cada membro da equipe no desenvolvimento do sistema de análise de restaurante.

## Estrutura da Equipe

### Desenvolvedor Principal
**Responsabilidades:**
- Arquitetura geral do sistema
- Configuração do pipeline Kafka + Spark + PostgreSQL
- Implementação do producer de dados
- Configuração Docker e orquestração
- Documentação técnica principal

**Entregas:**
- ✅ `src/producer.py` - Gerador de dados simulados
- ✅ `infra/docker-compose.yml` - Orquestração dos serviços
- ✅ `infra/Dockerfile` - Container Python
- ✅ `docs/ARQUITETURA.md` - Documentação de arquitetura
- ✅ `docs/GUIA_EXECUCAO.md` - Guia de instalação e execução

### Especialista em Streaming
**Responsabilidades:**
- Implementação do consumer Kafka
- Configuração e otimização do Kafka
- Tratamento de mensagens e serialização
- Integração com banco de dados

**Entregas:**
- ✅ `src/consumer.py` - Processamento de mensagens Kafka
- ✅ `src/database.py` - Configuração e inicialização do banco
- ✅ `src/init.sql` - Scripts de criação de tabelas
- ✅ `docs/DICIONARIO_DADOS.md` - Estrutura de dados

### Especialista em Big Data
**Responsabilidades:**
- Implementação do processamento Spark
- Desenvolvimento de analytics em tempo real
- Otimização de queries e performance
- Geração de relatórios automatizados

**Entregas:**
- ✅ `src/spark_processor.py` - Engine de analytics
- ✅ `infra/Dockerfile.spark` - Container Spark customizado
- ✅ `notebooks/analise_exploratoria.ipynb` - Análises exploratórias
- ✅ `docs/LIMITACOES.md` - Pontos de falha e limitações

### Analista de Dados
**Responsabilidades:**
- Análise exploratória dos dados
- Definição de KPIs e métricas
- Validação da qualidade dos dados
- Documentação de insights

**Entregas:**
- ✅ `datasets/sample_data.json` - Dados de exemplo
- ✅ `notebooks/analise_exploratoria.ipynb` - Análises e visualizações
- ✅ `docs/DICIONARIO_DADOS.md` - Catalogação de dados
- ✅ Validação de métricas de negócio

### DevOps/Infraestrutura
**Responsabilidades:**
- Configuração de containers e dependências
- Documentação de deployment
- Troubleshooting e monitoramento
- Versionamento e organização do código

**Entregas:**
- ✅ `infra/requirements.txt` - Dependências Python
- ✅ `docs/DEPENDENCIAS.md` - Guia de dependências
- ✅ `docs/GUIA_EXECUCAO.md` - Procedimentos operacionais
- ✅ Estrutura organizacional do repositório

## Conhecimentos Técnicos por Membro

### Desenvolvedor Principal
- **Linguagens**: Python, SQL, YAML
- **Ferramentas**: Docker, Docker Compose, Git
- **Conceitos**: Arquitetura de microsserviços, Design patterns

### Especialista em Streaming
- **Tecnologias**: Apache Kafka, PostgreSQL
- **Conceitos**: Event streaming, Message queues, ACID transactions
- **Ferramentas**: Kafka CLI, psql, pgAdmin

### Especialista em Big Data
- **Tecnologias**: Apache Spark, PySpark, Hadoop ecosystem
- **Conceitos**: Distributed computing, ETL, Real-time analytics
- **Ferramentas**: Spark UI, Jupyter, SQL engines

### Analista de Dados
- **Linguagens**: Python, SQL, R (opcional)
- **Bibliotecas**: Pandas, Matplotlib, Seaborn, NumPy
- **Conceitos**: Statistical analysis, Data visualization, KPIs

### DevOps/Infraestrutura
- **Tecnologias**: Docker, Linux, Networking
- **Conceitos**: CI/CD, Infrastructure as Code, Monitoring
- **Ferramentas**: Docker CLI, System monitoring tools

## Metodologia de Trabalho

### Divisão de Tarefas
1. **Planejamento**: Definição conjunta da arquitetura
2. **Desenvolvimento**: Trabalho paralelo em componentes
3. **Integração**: Testes de integração entre componentes
4. **Documentação**: Cada membro documenta sua parte
5. **Validação**: Revisão cruzada e testes finais

### Comunicação
- **Daily standups**: Alinhamento diário de progresso
- **Code reviews**: Revisão de código entre pares
- **Documentação**: Cada entrega documentada individualmente

### Controle de Qualidade
- **Testes unitários**: Cada componente testado isoladamente
- **Testes de integração**: Pipeline completo validado
- **Documentação**: Todos os componentes documentados

## Avaliação Individual

### Critérios de Avaliação
1. **Entendimento técnico**: Domínio da tecnologia utilizada
2. **Qualidade do código**: Boas práticas e organização
3. **Documentação**: Clareza e completude
4. **Integração**: Capacidade de trabalhar em equipe
5. **Apresentação**: Habilidade de explicar o trabalho

### Preparação para Apresentação
Cada membro deve estar preparado para:
- Explicar sua parte do sistema em detalhes
- Demonstrar o funcionamento dos componentes
- Responder perguntas técnicas específicas
- Justificar decisões de design e implementação
- Discutir melhorias e limitações

## Cronograma de Entregas

### Semana 1
- [x] Arquitetura definida
- [x] Ambiente Docker configurado
- [x] Producer implementado

### Semana 2
- [x] Consumer e banco configurados
- [x] Spark analytics implementado
- [x] Testes de integração

### Semana 3
- [x] Documentação completa
- [x] Análises exploratórias
- [x] Preparação para apresentação

### Semana 4
- [x] Revisão final
- [x] Apresentação do projeto
- [x] Avaliação individual