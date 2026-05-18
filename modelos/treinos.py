from database.connection import conectar


def cadastrar_treino(
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
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        status
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def listar_treinos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * FROM treinos
        ORDER BY data_treino DESC
    """

    cursor.execute(sql)
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


def buscar_resumo():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            COUNT(*) AS total_treinos,
            COALESCE(SUM(distancia_metros), 0) AS distancia_total,
            COALESCE(SUM(duracao_minutos), 0) AS tempo_total
        FROM treinos
        WHERE status = 'realizado'
    """

    cursor.execute(sql)
    resumo = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resumo


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


def cadastrar_treino_modelo(
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
            equipamentos
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        equipamentos
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def listar_treinos_modelo():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT * FROM treinos_modelo
        ORDER BY criado_em DESC
    """

    cursor.execute(sql)
    treinos_modelo = cursor.fetchall()

    cursor.close()
    conexao.close()

    return treinos_modelo

def buscar_treino_modelo_por_id(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM treinos_modelo
        WHERE id = %s
    """

    cursor.execute(sql, (id,))
    treino = cursor.fetchone()

    cursor.close()
    conexao.close()

    return treino

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
    
    
def concluir_treino(id):

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
  
def concluir_treino_por_id(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE treinos
        SET status = 'concluido'
        WHERE id = %s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()    
    
def marcar_treino_realizado(id):
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