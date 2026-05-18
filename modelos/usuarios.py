from database.connection import conectar


def cadastrar_usuario(nome, email, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO usuarios (nome, email, senha)
        VALUES (%s, %s, %s)
    """

    valores = (nome, email, senha)

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_usuario_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE email = %s"

    cursor.execute(sql, (email,))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario