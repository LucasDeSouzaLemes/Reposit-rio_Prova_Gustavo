# Guia de Execução

## Pré-requisitos

### Software Necessário
- **Docker**: Versão 20.10+
- **Docker Compose**: Versão 2.0+
- **Git**: Para clonar o repositório
- **Cliente PostgreSQL** (opcional): Para consultas diretas

### Recursos de Sistema
- **RAM**: Mínimo 4GB disponível
- **CPU**: 2 cores recomendado
- **Disco**: 2GB espaço livre
- **Rede**: Portas 5432, 9092 disponíveis

## Instalação

### 1. Clonar Repositório
```bash
git clone <url-do-repositorio>
cd Teste_projeto
```

### 2. Verificar Estrutura
```bash
tree
# Deve mostrar:
# ├── docs/
# ├── src/
# ├── infra/
# ├── notebooks/
# ├── datasets/
# └── README.md
```

## Execução

### 1. Iniciar Sistema Completo
```bash
cd infra
docker-compose up --build -d
```

### 2. Verificar Status dos Serviços
```bash
docker-compose ps
```

**Saída esperada:**
```
NAME                    STATUS
infra-kafka-1          Up
infra-postgres-1       Up
infra-producer-1       Up
infra-consumer-1       Up
infra-spark-analytics-1 Up
infra-db-init-1        Exited (0)
```

### 3. Monitorar Logs
```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f producer
docker-compose logs -f consumer
docker-compose logs -f spark-analytics
```

## Validação

### 1. Verificar Geração de Dados
```bash
docker-compose logs producer | tail -10
```
**Deve mostrar**: Pedidos sendo enviados a cada 10 segundos

### 2. Verificar Processamento
```bash
docker-compose logs consumer | tail -10
```
**Deve mostrar**: Pedidos sendo salvos no banco

### 3. Verificar Analytics
```bash
docker-compose logs spark-analytics | tail -10
```
**Deve mostrar**: Relatórios sendo gerados a cada 1 minuto

### 4. Consultar Dados
```bash
# Conectar ao PostgreSQL
docker-compose exec postgres psql -U admin -d datastore

# Verificar pedidos
SELECT COUNT(*) FROM pedidos;

# Verificar relatórios
SELECT COUNT(*) FROM relatorio_vendas;

# Sair do psql
\q
```

## Troubleshooting

### Problema: Containers não iniciam
**Solução:**
```bash
docker-compose down
docker system prune -f
docker-compose up --build -d
```

### Problema: Porta já em uso
**Erro**: `Port 5432 already in use`
**Solução**: Parar serviços locais do PostgreSQL
```bash
# Windows
net stop postgresql-x64-13

# Linux/Mac
sudo systemctl stop postgresql
```

### Problema: Kafka não conecta
**Sintoma**: Logs mostram "NoBrokersAvailable"
**Solução**: Aguardar 2-3 minutos para inicialização completa

### Problema: Spark falha
**Sintoma**: Container spark-analytics reinicia constantemente
**Solução**: Verificar logs e aumentar memória Docker
```bash
docker-compose logs spark-analytics
```

## Parar Sistema

### Parar Todos os Serviços
```bash
docker-compose down
```

### Limpar Dados (Opcional)
```bash
docker-compose down -v
docker system prune -f
```

## Acesso aos Dados

### PostgreSQL
- **Host**: localhost
- **Porta**: 5432
- **Database**: datastore
- **Usuário**: admin
- **Senha**: password

### Kafka
- **Bootstrap Servers**: localhost:9092
- **Tópico**: pedidos

## Comandos Úteis

### Reiniciar Serviço Específico
```bash
docker-compose restart producer
```

### Ver Recursos Utilizados
```bash
docker stats
```

### Backup de Dados
```bash
docker-compose exec postgres pg_dump -U admin datastore > backup.sql
```

### Restaurar Dados
```bash
docker-compose exec -T postgres psql -U admin datastore < backup.sql
```