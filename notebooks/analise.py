#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise Exploratória - Sistema de Restaurante
Este script demonstra análises exploratórias dos dados gerados pelo sistema de streaming.
"""

import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Configuração de visualização
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def conectar_banco():
    """Conecta ao banco PostgreSQL"""
    conn_params = {
        'host': 'localhost',
        'database': 'datastore',
        'user': 'admin',
        'password': 'password',
        'port': 5432
    }
    
    try:
        conn = psycopg2.connect(**conn_params)
        print("✅ Conexão estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def carregar_pedidos(conn):
    """Carrega dados de pedidos do banco"""
    query_pedidos = """
    SELECT 
        nome_prato,
        preco,
        quantidade,
        cliente_id,
        created_at,
        (preco * quantidade) as valor_total
    FROM pedidos 
    ORDER BY created_at DESC
    LIMIT 10000
    """
    
    df_pedidos = pd.read_sql(query_pedidos, conn)
    df_pedidos['created_at'] = pd.to_datetime(df_pedidos['created_at'])
    
    print(f"📊 Total de pedidos carregados: {len(df_pedidos)}")
    return df_pedidos

def estatisticas_gerais(df_pedidos):
    """Exibe estatísticas gerais dos pedidos"""
    print("\n=== ESTATÍSTICAS GERAIS ===")
    print(f"Período: {df_pedidos['created_at'].min()} até {df_pedidos['created_at'].max()}")
    print(f"Total de pedidos: {len(df_pedidos):,}")
    print(f"Valor total: R$ {df_pedidos['valor_total'].sum():,.2f}")
    print(f"Ticket médio: R$ {df_pedidos['valor_total'].mean():.2f}")
    print(f"Clientes únicos: {df_pedidos['cliente_id'].nunique()}")
    print(f"Pratos únicos: {df_pedidos['nome_prato'].nunique()}")

def top_pratos(df_pedidos):
    """Analisa os pratos mais pedidos"""
    top_pratos = df_pedidos.groupby('nome_prato').agg({
        'quantidade': 'sum',
        'valor_total': 'sum'
    }).sort_values('quantidade', ascending=False)
    
    print("\n=== TOP 10 PRATOS MAIS PEDIDOS ===")
    print(top_pratos.head(10))
    return top_pratos

def gerar_graficos(df_pedidos, top_pratos):
    """Gera visualizações dos dados"""
    # Gráfico 1: Top pratos
    plt.figure(figsize=(12, 6))
    top_10_pratos = top_pratos.head(10)
    plt.bar(range(len(top_10_pratos)), top_10_pratos['quantidade'])
    plt.xticks(range(len(top_10_pratos)), top_10_pratos.index, rotation=45, ha='right')
    plt.title('Top 10 Pratos Mais Pedidos')
    plt.ylabel('Quantidade Total')
    plt.tight_layout()
    plt.show()
    
    # Gráfico 2: Distribuição de preços
    plt.figure(figsize=(10, 6))
    plt.hist(df_pedidos['preco'], bins=20, alpha=0.7, edgecolor='black')
    plt.title('Distribuição de Preços dos Pratos')
    plt.xlabel('Preço (R$)')
    plt.ylabel('Frequência')
    plt.axvline(df_pedidos['preco'].mean(), color='red', linestyle='--', 
                label=f'Média: R$ {df_pedidos["preco"].mean():.2f}')
    plt.legend()
    plt.show()
    
    # Gráfico 3: Vendas por hora
    df_pedidos['hora'] = df_pedidos['created_at'].dt.hour
    vendas_por_hora = df_pedidos.groupby('hora')['valor_total'].sum()
    
    plt.figure(figsize=(12, 6))
    plt.plot(vendas_por_hora.index, vendas_por_hora.values, marker='o')
    plt.title('Vendas por Hora do Dia')
    plt.xlabel('Hora')
    plt.ylabel('Valor Total (R$)')
    plt.grid(True, alpha=0.3)
    plt.show()

def carregar_relatorios(conn):
    """Carrega relatórios do Spark"""
    query_relatorios = """
    SELECT 
        periodo,
        total_vendas,
        prato_mais_vendido,
        quantidade_total,
        ticket_medio,
        created_at
    FROM relatorio_vendas 
    ORDER BY created_at DESC
    LIMIT 1000
    """
    
    df_relatorios = pd.read_sql(query_relatorios, conn)
    df_relatorios['created_at'] = pd.to_datetime(df_relatorios['created_at'])
    df_relatorios['periodo'] = pd.to_datetime(df_relatorios['periodo'])
    
    print(f"\n📈 Total de relatórios: {len(df_relatorios)}")
    return df_relatorios

def dashboard_spark(df_relatorios):
    """Cria dashboard dos relatórios Spark"""
    if len(df_relatorios) == 0:
        print("⚠️ Nenhum relatório encontrado")
        return
    
    plt.figure(figsize=(15, 8))
    
    # Subplot 1: Total de vendas
    plt.subplot(2, 2, 1)
    plt.plot(df_relatorios['created_at'], df_relatorios['total_vendas'])
    plt.title('Evolução do Total de Vendas')
    plt.ylabel('Valor (R$)')
    plt.xticks(rotation=45)
    
    # Subplot 2: Quantidade total
    plt.subplot(2, 2, 2)
    plt.plot(df_relatorios['created_at'], df_relatorios['quantidade_total'], color='orange')
    plt.title('Evolução da Quantidade Total')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    
    # Subplot 3: Ticket médio
    plt.subplot(2, 2, 3)
    plt.plot(df_relatorios['created_at'], df_relatorios['ticket_medio'], color='green')
    plt.title('Evolução do Ticket Médio')
    plt.ylabel('Valor (R$)')
    plt.xticks(rotation=45)
    
    # Subplot 4: Pratos mais vendidos
    plt.subplot(2, 2, 4)
    prato_counts = df_relatorios['prato_mais_vendido'].value_counts().head(5)
    plt.pie(prato_counts.values, labels=prato_counts.index, autopct='%1.1f%%')
    plt.title('Pratos Mais Vendidos (Frequência nos Relatórios)')
    
    plt.tight_layout()
    plt.show()

def insights_principais(df_pedidos, df_relatorios, top_pratos):
    """Gera insights principais"""
    print("\n=== INSIGHTS PRINCIPAIS ===")
    print(f"1. Prato mais popular: {top_pratos.index[0]} ({top_pratos.iloc[0]['quantidade']} unidades)")
    print(f"2. Maior faturamento: {top_pratos.sort_values('valor_total', ascending=False).index[0]}")
    print(f"3. Preço médio dos pratos: R$ {df_pedidos['preco'].mean():.2f}")
    print(f"4. Quantidade média por pedido: {df_pedidos['quantidade'].mean():.1f}")
    print(f"5. Cliente mais ativo: {df_pedidos['cliente_id'].value_counts().index[0]} ({df_pedidos['cliente_id'].value_counts().iloc[0]} pedidos)")
    
    if len(df_relatorios) > 0:
        print(f"6. Média de vendas por minuto: R$ {df_relatorios['total_vendas'].mean():.2f}")
        print(f"7. Prato mais frequente nos relatórios: {df_relatorios['prato_mais_vendido'].mode()[0]}")

def main():
    """Função principal"""
    print("🚀 Iniciando Análise Exploratória - Sistema de Restaurante")
    
    # Conectar ao banco
    conn = conectar_banco()
    if not conn:
        return
    
    try:
        # Análise dos pedidos
        df_pedidos = carregar_pedidos(conn)
        if len(df_pedidos) == 0:
            print("⚠️ Nenhum pedido encontrado")
            return
        
        estatisticas_gerais(df_pedidos)
        top_pratos_df = top_pratos(df_pedidos)
        
        # Gerar gráficos
        print("\n📊 Gerando visualizações...")
        gerar_graficos(df_pedidos, top_pratos_df)
        
        # Análise dos relatórios Spark
        df_relatorios = carregar_relatorios(conn)
        dashboard_spark(df_relatorios)
        
        # Insights finais
        insights_principais(df_pedidos, df_relatorios, top_pratos_df)
        
        print("\n✅ Análise concluída!")
        
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
    
    finally:
        conn.close()
        print("🔌 Conexão fechada")

if __name__ == "__main__":
    main()