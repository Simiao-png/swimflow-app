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

def buscar_usuario_por_id(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE id = %s"

    cursor.execute(sql, (usuario_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario


def atualizar_perfil(
    usuario_id,
    nome_exibicao,
    idade,
    peso_kg,
    altura_cm
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE usuarios
        SET
            nome_exibicao = %s,
            idade = %s,
            peso_kg = %s,
            altura_cm = %s
        WHERE id = %s
    """

    valores = (
        nome_exibicao,
        idade,
        peso_kg,
        altura_cm,
        usuario_id
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()