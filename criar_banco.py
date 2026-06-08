import sqlite3

conexao = sqlite3.connect("swimflow.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foto TEXT,
    nome_exibicao TEXT,
    idade INTEGER,
    peso_kg REAL,
    altura_cm REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_treino TEXT NOT NULL,
    titulo TEXT NOT NULL,
    estilo TEXT,
    tamanho_piscina REAL,
    voltas INTEGER,
    distancia_metros REAL,
    duracao_minutos INTEGER,
    pace TEXT,
    observacoes TEXT,
    equipamentos TEXT,
    status TEXT DEFAULT 'realizado',
    usuario_id INTEGER,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS treinos_modelo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    estilo TEXT,
    tamanho_piscina REAL,
    voltas INTEGER,
    distancia_metros REAL,
    duracao_minutos INTEGER,
    pace TEXT,
    observacoes TEXT,
    equipamentos TEXT,
    usuario_id INTEGER,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conexao.commit()
conexao.close()

print("Banco swimflow.db criado com sucesso!")