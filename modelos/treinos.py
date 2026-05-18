# ============================================================
# IMPORTAÇÕES
# ============================================================

from database.connection import conectar


# ============================================================
# CADASTRAR TREINO
# ============================================================

def cadastrar_treino(
    usuario_id,
    data_treino,
    titulo,
    estilo,
    tamanho_piscina,
    voltas,
    distancia_metros,
    duracao_minutos,
    pace,
    observacoes,
    equipamentos,
    status="realizado",
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO treinos 
        (
            data_treino,
            titulo,
            estilo,
            tamanho_piscina,
            voltas,
            distancia_metros,
            duracao_minutos,
            pace,
            observacoes,
            equipamentos,
            status,
            usuario_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        data_treino,
        titulo,
        estilo,
        tamanho_piscina,
        voltas,
        distancia_metros,
        duracao_minutos,
        pace,
        observacoes,
        equipamentos,
        status,
        usuario_id
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


# ============================================================
# LISTAR / BUSCAR TREINOS
# ============================================================

def listar_treinos(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * FROM treinos
        WHERE usuario_id = %s
        ORDER BY data_treino DESC
    """

    cursor.execute(sql, (usuario_id,))
    treinos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return treinos


def buscar_treino_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * FROM treinos
        WHERE id = %s
    """

    cursor.execute(sql, (id,))
    treino = cursor.fetchone()

    cursor.close()
    conexao.close()

    return treino


# ============================================================
# ATUALIZAR / EXCLUIR TREINOS
# ============================================================

def atualizar_treino(
    id,
    data_treino,
    titulo,
    estilo,
    tamanho_piscina,
    voltas,
    distancia_metros,
    duracao_minutos,
    pace,
    observacoes,
    equipamentos,
    status="realizado"
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE treinos
        SET
            data_treino = %s,
            titulo = %s,
            estilo = %s,
            tamanho_piscina = %s,
            voltas = %s,
            distancia_metros = %s,
            duracao_minutos = %s,
            pace = %s,
            observacoes = %s,
            equipamentos = %s,
            status = %s
        WHERE id = %s
    """

    valores = (
        data_treino,
        titulo,
        estilo,
        tamanho_piscina,
        voltas,
        distancia_metros,
        duracao_minutos,
        pace,
        observacoes,
        equipamentos,
        status,
        id
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def excluir_treino_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        DELETE FROM treinos
        WHERE id = %s
    """

    cursor.execute(sql, (id,))
    conexao.commit()

    cursor.close()
    conexao.close()


# ============================================================
# RESUMO DOS TREINOS
# ============================================================

def buscar_resumo(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            COUNT(*) AS total_treinos,
            COALESCE(SUM(distancia_metros), 0) AS distancia_total,
            COALESCE(SUM(duracao_minutos), 0) AS tempo_total
        FROM treinos
        WHERE status = 'realizado'
        AND usuario_id = %s
    """

    cursor.execute(sql, (usuario_id,))
    resumo = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resumo


# ============================================================
# STATUS DO TREINO
# ============================================================

def atualizar_status_treino(id, status):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE treinos
        SET status = %s
        WHERE id = %s
    """

    cursor.execute(sql, (status, id))
    conexao.commit()

    cursor.close()
    conexao.close()


def concluir_treino_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE treinos
        SET status = 'realizado'
        WHERE id = %s
    """

    cursor.execute(sql, (id,))
    conexao.commit()

    cursor.close()
    conexao.close()


def marcar_treino_realizado(id):
    concluir_treino_por_id(id)


# ============================================================
# MODELOS DE TREINO
# ============================================================

def cadastrar_treino_modelo(
    usuario_id,
    titulo,
    estilo,
    tamanho_piscina,
    voltas,
    distancia_metros,
    duracao_minutos,
    pace,
    observacoes,
    equipamentos
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO treinos_modelo
        (
            titulo,
            estilo,
            tamanho_piscina,
            voltas,
            distancia_metros,
            duracao_minutos,
            pace,
            observacoes,
            equipamentos,
            usuario_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        titulo,
        estilo,
        tamanho_piscina,
        voltas,
        distancia_metros,
        duracao_minutos,
        pace,
        observacoes,
        equipamentos,
        usuario_id
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def listar_treinos_modelo(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
       SELECT * FROM treinos_modelo
       WHERE usuario_id = %s
       ORDER BY criado_em DESC
    """

    cursor.execute(sql, (usuario_id,))
    treinos_modelo = cursor.fetchall()

    cursor.close()
    conexao.close()

    return treinos_modelo

def buscar_treino_modelo_por_id(id, usuario_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM treinos_modelo
        WHERE id = %s
        AND usuario_id = %s
    """

    cursor.execute(sql, (id, usuario_id))
    treino = cursor.fetchone()

    cursor.close()
    conexao.close()

    return treino


# ============================================================
# CALENDÁRIO / MOVER TREINO PROGRAMADO
# ============================================================

def mover_treino_programado(id, nova_data):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE treinos
        SET data_treino = %s
        WHERE id = %s
        AND status = 'programado'
    """

    cursor.execute(sql, (nova_data, id))
    conexao.commit()

    cursor.close()
    conexao.close()