import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "swimflow.db")

def conectar():
    conexao = sqlite3.connect(DB_PATH)

    # Permite usar:
    # usuario["nome"]
    # treino["titulo"]
    conexao.row_factory = sqlite3.Row

    return conexao