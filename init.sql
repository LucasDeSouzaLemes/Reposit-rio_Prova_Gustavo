CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    nome_prato VARCHAR(100),
    preco DECIMAL(10,2),
    quantidade INTEGER,
    cliente_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS relatorio_vendas (
    id SERIAL PRIMARY KEY,
    periodo TIMESTAMP,
    total_vendas DECIMAL(12,2),
    prato_mais_vendido VARCHAR(100),
    quantidade_total INTEGER,
    ticket_medio DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);