import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="natacao_app"
    )

    return conexao