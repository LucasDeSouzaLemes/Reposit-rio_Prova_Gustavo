# Documentação do Projeto

## Índice

### 📋 Documentação Geral
- [**REQUISITOS.md**](REQUISITOS.md) - Descrição do problema, objetivos e escopo
- [**ARQUITETURA.md**](ARQUITETURA.md) - Diagrama e componentes da arquitetura
- [**TRABALHO_INDIVIDUAL.md**](TRABALHO_INDIVIDUAL.md) - Responsabilidades da equipe

### 🛠️ Guias Técnicos
- [**GUIA_EXECUCAO.md**](GUIA_EXECUCAO.md) - Como executar o projeto do zero
- [**DEPENDENCIAS.md**](DEPENDENCIAS.md) - Versões e configurações necessárias
- [**DICIONARIO_DADOS.md**](DICIONARIO_DADOS.md) - Estrutura e esquema dos dados

### ⚠️ Limitações e Considerações
- [**LIMITACOES.md**](LIMITACOES.md) - Pontos de falha e limitações conhecidas

## Visão Geral

Este projeto implementa um **pipeline de dados em tempo real** para análise de vendas de restaurante, utilizando:

- **Apache Kafka** para streaming de dados
- **Apache Spark** para processamento distribuído
- **PostgreSQL** para armazenamento
- **Docker** para containerização

## Fluxo de Leitura Recomendado

1. **Iniciantes**: Comece com [REQUISITOS.md](REQUISITOS.md) para entender o problema
2. **Técnicos**: Vá para [ARQUITETURA.md](ARQUITETURA.md) para ver a solução
3. **Implementadores**: Use [GUIA_EXECUCAO.md](GUIA_EXECUCAO.md) para rodar o projeto
4. **Desenvolvedores**: Consulte [DEPENDENCIAS.md](DEPENDENCIAS.md) para detalhes técnicos
5. **Analistas**: Veja [DICIONARIO_DADOS.md](DICIONARIO_DADOS.md) para estrutura de dados

## Estrutura do Projeto

```
Teste_projeto/
├── docs/                    # Documentação completa
│   ├── ARQUITETURA.md
│   ├── REQUISITOS.md
│   ├── GUIA_EXECUCAO.md
│   ├── DEPENDENCIAS.md
│   ├── DICIONARIO_DADOS.md
│   ├── LIMITACOES.md
│   └── TRABALHO_INDIVIDUAL.md
├── src/                     # Código-fonte
│   ├── producer.py
│   ├── consumer.py
│   ├── spark_processor.py
│   ├── database.py
│   └── init.sql
├── infra/                   # Infraestrutura
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── Dockerfile.spark
│   └── requirements.txt
├── notebooks/               # Análises exploratórias
│   └── analise_exploratoria.ipynb
├── datasets/                # Dados de exemplo
│   └── sample_data.json
└── README.md               # Visão geral do projeto
```

## Quick Start

```bash
# 1. Clonar repositório
git clone <url-do-repositorio>
cd Teste_projeto

# 2. Executar sistema
cd infra
docker-compose up --build -d

# 3. Verificar funcionamento
docker-compose logs -f

# 4. Consultar dados
docker-compose exec postgres psql -U admin -d datastore
```

## Contato e Suporte

Para dúvidas sobre a documentação ou implementação, consulte:
- [Issues do repositório](link-para-issues)
- [Wiki do projeto](link-para-wiki)
- Contato da equipe: [emails]