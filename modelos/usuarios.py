from database.connection import conectar


def cadastrar_usuario(nome, email, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO usuarios (nome, email, senha)
        VALUES (?, ?, ?)
    """

    valores = (nome, email, senha)

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_usuario_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM usuarios WHERE email = ?"

    cursor.execute(sql, (email,))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario

def buscar_usuario_por_id(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM usuarios WHERE id = ?"

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
            nome_exibicao = ?,
            idade = ?,
            peso_kg = ?,
            altura_cm = ?
        WHERE id = ?
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